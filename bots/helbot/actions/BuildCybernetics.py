from sc2.constants import *
from .Action import Action


class BuildCybernetics(Action):

    async def handle(self):
        if not self.ai.units(PYLON).ready.exists:
            return

        pylon = self.ai.units(PYLON).ready.random

        if not self.ai.units(GATEWAY).ready.exists:
            return
        if self.ai.units(CYBERNETICSCORE):
            return
        if not self.ai.can_afford(CYBERNETICSCORE):
            return
        if self.ai.already_pending(CYBERNETICSCORE):
            return
        await self.ai.build(CYBERNETICSCORE, near=pylon)
