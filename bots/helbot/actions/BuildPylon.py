from sc2.constants import *


class BuildPylon:

    def __init__(self, ai):
        self.ai = ai

    async def handle(self):
        if self.ai.supply_left < 5 and not self.ai.already_pending(PYLON):
            nexuses = self.ai.units(NEXUS).ready
            if nexuses.exists:
                if self.ai.can_afford(PYLON):
                    await self.ai.build(PYLON, near=nexuses.first)
