from sc2.constants import *
from .Action import Action


class SendScout(Action):

    async def handle(self):

        scouts = self.ai.units(OBSERVER)

        if len(scouts) == 0:
            return

        actions = []
        for center in self.ai.expansion_locations:
            actions.append(scouts.closest_to(center).move(center))

        await self.ai.do_actions(actions)
