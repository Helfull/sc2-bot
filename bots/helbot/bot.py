import random
import numpy as np
import keras
import uuid

import sc2
from sc2 import position, Result
from sc2.constants import *
from sc2.unit import Unit


from .intel import Intel
from .actions.ExpandAction import *
from .actions.BuildPylon import *
from .actions.BuildWorker import *
from .actions.BuildGateway import *
from .actions.BuildZealot import *
from .actions.BuildStalker import *
from .actions.BuildAssimilators import *
from .actions.BuildCybernetics import *
from .actions.BuildStargate import *
from .actions.BuildVoidray import *
from .actions.DefendBase import *
from .actions.GroupUnits import *
from .actions.AttackEnemyStart import *
from .actions.DoNothing import *
from .actions.BuildScout import *
from .actions.SendScout import *
from .actions.BuildRobotics import *


class HelBot(sc2.BotAI):

    def __init__(self, headless=False, model=False):
        print("Bot Config:")
        print("Headless: {}".format(headless))
        print("Model: {}".format(model))
        self.headless = headless
        self.model = model

        self.intel_manager = Intel(self)

        self.MAX_WORKERS = 50
        self.do_something_after = 0
        self.last_choice = 0
        self.train_data = []
        self.actions = {
            0: BuildPylon(self),
            1: BuildWorker(self),
            2: BuildGateway(self),
            3: BuildZealot(self),
            4: BuildStalker(self),
            5: BuildAssimilators(self),
            6: BuildCybernetics(self),
            7: BuildStargate(self),
            8: BuildVoidray(self),
            9: ExpandAction(self),
            10: DoNothing(self),
            11: GroupUnits(self),
            12: DefendBase(self),
            13: AttackEnemyStart(self),
            14: BuildScout(self),
            15: SendScout(self),
            16: BuildRobotics(self)
        }

        if self.model:
            print("USING MODEL!")
            print(self.model)
            self.loaded_model = keras.models.load_model(self.model)

    def on_start(self):
        print("---- PREPARE START ----")
        self.own_units = []
        self.intel_manager.on_start()

    async def on_step(self, iteration):
        await self.scout()
        await self.handle()
        await self.distribute_workers()
        await self.intel()

    def on_end(self, game_result):
        with open("log.txt", "a") as f:
            if self.model:
                f.write("{} {}\n".format(self.model, game_result))
            else:
                f.write("{} {}\n".format("Random", game_result))

        if game_result == Result.Victory:
            self.intel_manager.store()

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

        self.intel_manager.draw_units_enemy(self.state.units.enemy.structure)
        self.intel_manager.draw_units_enemy(
            self.state.units.enemy.not_structure)
        self.intel_manager.draw_units_own(self.state.units.owned.structure)
        self.intel_manager.draw_units_own(self.state.units.owned.not_structure)

        mineral_ratio = self.minerals / 1500
        if mineral_ratio > 1.0:
            mineral_ratio = 1.0

        vespene_ratio = self.vespene / 1500
        if vespene_ratio > 1.0:
            vespene_ratio = 1.0

        if self.state.common.food_cap > 0:
            worker_ratio = self.state.common.food_workers /\
                self.state.common.food_cap

            army_ratio = self.state.common.food_army /\
                self.state.common.food_cap

            if worker_ratio > 1.0:
                worker_ratio = 1.0

            if army_ratio > 1.0:
                army_ratio = 1.0

            self.intel_manager.draw_bar(
                army_ratio, (250, 250, 200), (0, 15), 3)
            self.intel_manager.draw_bar(
                worker_ratio, (220, 200, 200), (0, 11), 3)

        self.intel_manager.draw_bar(vespene_ratio, (210, 200, 0), (0, 7), 3)
        self.intel_manager.draw_bar(mineral_ratio, (0, 255, 25), (0, 3), 3)

        self.intel_manager.show(self.headless)

    def select_choice(self):
        choice = 0
        if self.model:
            prediction = self.loaded_model.predict(
                [self.flipped.reshape([-1, 176, 200, 3])])
            choice = np.argmax(prediction[0])
        else:
            choice = random.randrange(0, len(self.actions))

        self.last_choice = choice
        print("Choice #{}:{}".format(
            choice, self.actions[choice].__class__.__name__))
        self.intel_manager.choose(choice, len(self.actions))
        return self.actions[choice]

    async def handle(self):
        if self.do_something_after < self.time:
            choice = self.select_choice()
            await choice.handle()

    def can_feed(self, unit_type: UnitTypeId) -> bool:
        """ Checks if you have enough free supply to build the unit """
        return self.supply_left >= self._game_data.units[unit_type.value]._proto.food_required
