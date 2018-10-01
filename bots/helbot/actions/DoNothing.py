import random
from .Action import Action


class DoNothing(Action):

    async def handle(self):
        self.ai.do_something_after = self.ai.time + \
            random.randrange(5, 20)
