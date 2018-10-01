from sc2.constants import *
from .Action import Action


class BuildPylon(Action):

    async def handle(self):
        if self.ai.supply_left < 5 and not self.ai.already_pending(PYLON):
            nexuses = self.ai.units(NEXUS).ready
            if nexuses.exists:
                if self.ai.can_afford(PYLON):
                    await self.ai.build(PYLON, near=nexuses.first)
