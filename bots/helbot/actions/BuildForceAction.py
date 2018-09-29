from sc2.constants import *


class BuildForceAction:

    def __init__(self, ai):
        self.ai = ai

    async def handle(self):
        for sg in self.ai.units(STARGATE).ready.noqueue:
            if self.ai.can_afford(VOIDRAY) and self.ai.supply_left > 0:
                await self.ai.do(sg.train(VOIDRAY))
