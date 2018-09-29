import sc2
from sc2 import position, Result
from sc2.constants import *
import random
from .intel import Intel
from .actions.StarGateAction import StarGateAction
from .actions.BuildForceAction import BuildForceAction
from .actions.BuildPylon import BuildPylon
from .actions.BuildWorker import BuildWorker
from .actions.BuildAssimilators import BuildAssimilators
from .actions.ExpandAction import ExpandAction

HEADLESS = False


class HelBot(sc2.BotAI):

    def __init__(self):
        self.intel_manager = Intel(self)
        self.MAX_WORKERS = 50
        self.do_something_after = 0
        self.train_data = []
        self.actions = [
            BuildPylon(self),
            BuildAssimilators(self),
            BuildWorker(self),
            StarGateAction(self),
            BuildForceAction(self),
            ExpandAction(self)
        ]

    def on_end(self, game_result):
        self.intel_manager.store(game_result)

    async def on_step(self, iteration):
        await self.scout()
        await self.distribute_workers()

        for action in self.actions:
            await action.handle()

        await self.intel()
        await self.attack()

    def random_location_variance(self, enemy_start_location):
        x = enemy_start_location[0]
        y = enemy_start_location[1]

        x += ((random.randrange(-20, 20)) / 100) * enemy_start_location[0]
        y += ((random.randrange(-20, 20)) / 100) * enemy_start_location[1]

        if x < 0:
            x = 0
        if y < 0:
            y = 0
        if x > self.game_info.map_size[0]:
            x = self.game_info.map_size[0]
        if y > self.game_info.map_size[1]:
            y = self.game_info.map_size[1]

        go_to = position.Point2(position.Pointlike((x, y)))
        return go_to

    async def scout(self):
        if len(self.units(OBSERVER)) > 0:
            scout = self.units(OBSERVER)[0]
            if scout.is_idle:
                enemy_location = self.enemy_start_locations[0]
                move_to = self.random_location_variance(enemy_location)
                await self.do(scout.move(move_to))

        else:
            for rf in self.units(ROBOTICSFACILITY).ready.noqueue:
                if self.can_afford(OBSERVER) and self.supply_left > 0:
                    await self.do(rf.train(OBSERVER))

    async def intel(self):
        self.intel_manager.new_cycle(self.game_info)

        for mineral_field in self.state.mineral_field:
            self.intel_manager.draw_mineral(mineral_field)

        for vespene_geyser in self.state.vespene_geyser:
            self.intel_manager.draw_geyser(vespene_geyser)

        draw_dict = {
            NEXUS: [15, (0, 255, 0)],
            PYLON: [3, (20, 235, 0)],
            PROBE: [1, (55, 200, 0)],
            ASSIMILATOR: [2, (55, 200, 0)],
            GATEWAY: [3, (200, 100, 0)],
            CYBERNETICSCORE: [3, (150, 150, 0)],
            STARGATE: [5, (255, 0, 0)],
            ROBOTICSFACILITY: [5, (215, 155, 0)],

            VOIDRAY: [3, (255, 100, 0)],
        }

        for unit_type in draw_dict:
            for unit in self.units(unit_type).ready:
                self.intel_manager.draw_unit(unit, draw_dict[unit_type][1])

        base_typeids = [NEXUS, HATCHERY, COMMANDCENTER]

        for enemy_building in self.known_enemy_structures:
            if enemy_building.type_id in base_typeids:
                self.intel_manager.draw_unit(enemy_building, (0, 0, 255))

        for enemy_building in self.known_enemy_structures:
            if enemy_building.type_id not in base_typeids:
                self.intel_manager.draw_unit(enemy_building, (200, 50, 212))

        for enemy_unit in self.known_enemy_units:

            if not enemy_unit.is_structure:
                worker_names = [PROBE, SCV, DRONE]
                if enemy_unit.type_id in worker_names:
                    self.intel_manager.draw_unit(enemy_unit, (55, 0, 155))
                else:
                    self.intel_manager.draw_unit(enemy_unit, (50, 0, 215))

        for obs in self.units(OBSERVER).ready:
            self.intel_manager.draw_unit(obs, (255, 255, 255))

        mineral_ratio = self.minerals / 1500
        if mineral_ratio > 1.0:
            mineral_ratio = 1.0

        vespene_ratio = self.vespene / 1500
        if vespene_ratio > 1.0:
            vespene_ratio = 1.0

        population_ratio = self.supply_left / self.supply_cap
        if population_ratio > 1.0:
            population_ratio = 1.0

        plausible_supply = self.supply_cap / 200.0

        military_weight = len(self.units(VOIDRAY)) / \
            (self.supply_cap - self.supply_left)
        if military_weight > 1.0:
            military_weight = 1.0

        self.intel_manager.draw_bar(
            military_weight, (250, 250, 200), (0, 19), 3)
        self.intel_manager.draw_bar(
            plausible_supply, (220, 200, 200), (0, 15), 3)
        self.intel_manager.draw_bar(
            population_ratio, (150, 150, 150), (0, 11), 3)
        self.intel_manager.draw_bar(vespene_ratio, (210, 200, 0), (0, 7), 3)
        self.intel_manager.draw_bar(mineral_ratio, (0, 255, 25), (0, 3), 3)

        self.intel_manager.show(HEADLESS)

    async def attack(self):
        if len(self.units(VOIDRAY).idle) > 0:
            choice = random.randrange(0, 4)
            target = False
            if self.time > self.do_something_after:
                if choice == 0:
                    # no attack
                    wait = random.randrange(7, 100) / 100
                    self.do_something_after = self.time + wait

                elif choice == 1:
                    # attack_unit_closest_nexus
                    if len(self.known_enemy_units) > 0:
                        target = self.known_enemy_units\
                            .closest_to(random.choice(self.units(NEXUS)))

                elif choice == 2:
                    # attack enemy structures
                    if len(self.known_enemy_structures) > 0:
                        target = random.choice(self.known_enemy_structures)

                elif choice == 3:
                    # attack_enemy_start
                    target = self.enemy_start_locations[0]

                if target:
                    for vr in self.units(VOIDRAY).idle:
                        await self.do(vr.attack(target))

                self.intel_manager.choose(choice)
