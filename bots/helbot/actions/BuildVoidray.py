from sc2.constants import *
from .BuildUnit import BuildUnit


class BuildVoidray(BuildUnit):

    async def handle(self):
        for sg in self.ai.units(STARGATE).ready.noqueue:
            if self.can_train(VOIDRAY):
                await self.ai.do(sg.train(VOIDRAY))
