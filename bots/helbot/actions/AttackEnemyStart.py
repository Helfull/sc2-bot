import random
from sc2.constants import *
from .Action import Action


class AttackEnemyStart(Action):

    async def handle(self):
        position = random.choice(self.ai.enemy_start_locations)

        army = self.ai.units.not_structure.exclude_type(
            [DRONE, SCV, PROBE])

        actions = []

        for unit in army:
            actions.append(unit.attack(position))

        await self.ai.do_actions(actions)
