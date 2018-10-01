from sc2.constants import *
from .BuildUnit import BuildUnit


class BuildWorker(BuildUnit):

    async def handle(self):
        if (len(self.ai.units(NEXUS)) * 16) > len(self.ai.units(PROBE)) and len(self.ai.units(PROBE)) < self.ai.MAX_WORKERS:
            for nexus in self.ai.units(NEXUS).ready.noqueue:
                if self.can_train(PROBE):
                    await self.ai.do(nexus.train(PROBE))
