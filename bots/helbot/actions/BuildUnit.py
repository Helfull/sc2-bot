from sc2.constants import *
from .Action import Action


class BuildUnit(Action):

    def can_train(self, unit: UnitTypeId) -> bool:
        return self.ai.can_feed(unit) and self.ai.can_afford(unit)
