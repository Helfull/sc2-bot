from sc2.constants import *


class StarGateAction:

    def __init__(self, ai):
        self.ai = ai

    async def handle(self):
        if self.ai.units(PYLON).ready.exists:
            pylon = self.ai.units(PYLON).ready.random
            await self.cyber_or_gateway(pylon)
            await self.build_stargate(pylon)

    def should_build_stargate(self):
        total_gates = len(self.ai.units(STARGATE))
        for_iterartion = total_gates < self.ai.time
        no_idle = len(self.ai.units(STARGATE).ready.noqueue) == 0
        return for_iterartion and no_idle

    async def build_stargate(self, pylon):
        if not self.ai.units(CYBERNETICSCORE).ready.exists:
            return
        if not self.should_build_stargate():
            return
        if not self.ai.can_afford(STARGATE):
            return
        if self.ai.already_pending(STARGATE):
            return
        await self.ai.build(STARGATE, near=pylon)

    async def cyber_or_gateway(self, pylon):
        if self.ai.units(GATEWAY).ready.exists:
            await self.build_cybernetics(pylon)
        else:
            await self.build_gateway(pylon)

    async def build_cybernetics(self, pylon):
        if self.ai.units(CYBERNETICSCORE):
            return
        if not self.ai.can_afford(CYBERNETICSCORE):
            return
        if self.ai.already_pending(CYBERNETICSCORE):
            return
        await self.ai.build(CYBERNETICSCORE, near=pylon)

    async def build_gateway(self, pylon):
        if len(self.ai.units(GATEWAY)) >= 1:
            return
        if self.ai.can_afford(GATEWAY) and not self.ai.already_pending(GATEWAY):
            await self.ai.build(GATEWAY, near=pylon)
