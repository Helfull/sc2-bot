from sc2.constants import *
from .Action import Action


class BuildStargate(Action):

    async def handle(self):
        if not self.ai.units(PYLON).ready.exists:
            return

        pylon = self.ai.units(PYLON).ready.random

        if not self.ai.units(CYBERNETICSCORE).ready.exists:
            return
        if not self.should_build_stargate():
            return
        if not self.ai.can_afford(STARGATE):
            return
        if self.ai.already_pending(STARGATE):
            return
        await self.ai.build(STARGATE, near=pylon)

    def should_build_stargate(self):
        total_gates = len(self.ai.units(STARGATE))
        for_iterartion = total_gates < self.ai.time
        no_idle = len(self.ai.units(STARGATE).ready.noqueue) == 0
        return for_iterartion and no_idle
