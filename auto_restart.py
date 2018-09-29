from importlib import reload
import os
import time
import sc2
from sc2 import Race, Difficulty
from sc2.player import Bot, Computer

from bots.helbot import bot

os.environ["SC2PATH"] = "G:\\BattleNet\\StarCraft II"


def main():
    player_config = [
        Bot(Race.Protoss, bot.HelBot()),
        Computer(Race.Terran, Difficulty.Hard)
    ]

    gen = sc2.main._host_game_iter(
        sc2.maps.get("Abyssal Reef LE"),
        player_config,
        realtime=False
    )

    for i in range(100):
        r = next(gen)

        time.sleep(5)

        reload(bot)
        player_config[0].ai = bot.HelBot()
        gen.send(player_config)

if __name__ == "__main__":
    main()
