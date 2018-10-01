import random
from sc2.constants import *
from .Action import Action


class DefendBase(Action):

    async def handle(self):

        if len(self.ai.known_enemy_units) > 0:
            target = self.ai.known_enemy_units\
                .closest_to(random.choice(self.ai.units.structure))

            army = self.ai.units.not_structure.exclude_type(
                [DRONE, SCV, PROBE])

            actions = []
            for unit in army:
                actions.append(unit.attack(target))

            await self.ai.do_actions(actions)
