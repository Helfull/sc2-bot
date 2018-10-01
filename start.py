from sc2 import run_game, maps, Race, Difficulty
from sc2.player import Bot, Computer
from bots.helbot.bot import HelBot
from options import Options

options = Options()

run_game(maps.get("Abyssal Reef LE"), [
    Bot(Race.Protoss, HelBot(headless=options.headless, model=options.model)),
    Computer(Race.Protoss, Difficulty.Easy)
], realtime=options.realtime)
