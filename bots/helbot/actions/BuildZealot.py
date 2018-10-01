from sc2.constants import *
from .BuildUnit import BuildUnit


class BuildZealot(BuildUnit):

    async def handle(self):
        for sg in self.ai.units(GATEWAY).ready.noqueue:
            if self.can_train(ZEALOT):
                await self.ai.do(sg.train(ZEALOT))
