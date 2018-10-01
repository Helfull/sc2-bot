from sc2.constants import *
from .Action import Action


class ExpandAction(Action):

    async def handle(self):
        if self.ai.units(NEXUS).amount < self.ai.time / 2 and self.ai.can_afford(NEXUS):
            await self.ai.expand_now()
