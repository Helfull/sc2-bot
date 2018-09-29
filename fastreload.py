from importlib import reload
import os
import sc2
from sc2 import Race, Difficulty
from sc2.player import Bot, Computer

from bots.HelBot import *
from bots.SentaBot import *

os.environ["SC2PATH"] = "G:\\BattleNet\\StarCraft II"

def main():
    player_config = [
        Bot(Race.Zerg, HelBot()),
        Computer(Race.Terran, Difficulty.Medium)
    ]

    gen = sc2.main._host_game_iter(
        sc2.maps.get("Abyssal Reef LE"),
        player_config,
        realtime=False
    )

    while True:
        r = next(gen)

        input("Press enter to reload ")

        reload(HelBot)
        player_config[0].ai = HelBot.Gen1()
        gen.send(player_config)

if __name__ == "__main__":
    main()
