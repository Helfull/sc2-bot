from sc2.constants import *


class BuildAssimilators:

    def __init__(self, ai):
        self.ai = ai

    async def handle(self):
        for nexus in self.ai.units(NEXUS).ready:
            vaspenes = self.ai.state.vespene_geyser.closer_than(15.0, nexus)
            for vaspene in vaspenes:
                if not self.ai.can_afford(ASSIMILATOR):
                    break
                worker = self.ai.select_build_worker(vaspene.position)
                if worker is None:
                    break
                if not self.ai.units(ASSIMILATOR).closer_than(1.0, vaspene).exists:
                    await self.ai.do(worker.build(ASSIMILATOR, vaspene))
