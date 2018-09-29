import os
from sc2 import run_game, maps, Race, Difficulty
from sc2.player import Bot, Computer

from bots.helbot.bot import HelBot

os.environ["SC2PATH"] = "G:\\BattleNet\\StarCraft II"

run_game(maps.get("Abyssal Reef LE"), [
    Bot(Race.Protoss, HelBot()),
    Computer(Race.Protoss, Difficulty.Easy)
], realtime=False)
