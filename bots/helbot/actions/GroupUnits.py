from sc2.constants import *
from .Action import Action


class GroupUnits(Action):

    async def handle(self):

        army = self.ai.units.not_structure.exclude_type(
            [DRONE, SCV, PROBE])

        if len(army) == 0:
            return
        center = army.center

        actions = []
        for unit in army:
            actions.append(unit.move(center))

        await self.ai.do_actions(actions)
