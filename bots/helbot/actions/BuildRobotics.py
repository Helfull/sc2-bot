from sc2.constants import *
from .Action import Action


class BuildRobotics(Action):

    async def handle(self):
        if not self.ai.units(PYLON).ready.exists:
            return

        pylon = self.ai.units(PYLON).ready.random

        if not self.ai.units(GATEWAY).ready.exists:
            return
        if self.ai.units(ROBOTICSFACILITY):
            return
        if not self.ai.can_afford(ROBOTICSFACILITY):
            return
        if self.ai.already_pending(ROBOTICSFACILITY):
            return
        await self.ai.build(ROBOTICSFACILITY, near=pylon)
