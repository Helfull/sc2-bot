from sc2.constants import *


class BuildWorker:

    def __init__(self, ai):
        self.ai = ai

    async def handle(self):
        if (len(self.ai.units(NEXUS)) * 16) > len(self.ai.units(PROBE)) and len(self.ai.units(PROBE)) < self.ai.MAX_WORKERS:
            for nexus in self.ai.units(NEXUS).ready.noqueue:
                if self.ai.can_afford(PROBE):
                    await self.ai.do(nexus.train(PROBE))
