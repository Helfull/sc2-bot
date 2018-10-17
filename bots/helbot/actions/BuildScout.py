import random
from sc2.constants import *
from .BuildUnit import BuildUnit


class BuildScout(BuildUnit):

    async def handle(self):
        if not self.ai.units(ROBOTICSFACILITY).exists:
            return

        rf = self.ai.units(ROBOTICSFACILITY).ready.noqueue

        if len(rf) == 0:
            return

        if not self.can_train(OBSERVER):
            return

        rf = random.choice(rf)

        await self.ai.do(rf.train(OBSERVER))
