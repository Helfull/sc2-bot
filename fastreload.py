from importlib import reload
import os
import sc2
from sc2 import Race, Difficulty
from sc2.player import Bot, Computer
from bots.helbot import bot
from options import Options
import time

options = Options()


def main():
    player_config = [
        Bot(Race.Protoss, bot.HelBot(headless=options.headless, model=options.model)),
        Computer(Race.Protoss, Difficulty.Easy)
    ]

    gen = sc2.main._host_game_iter(
        sc2.maps.get("Abyssal Reef LE"),
        player_config,
        realtime=options.realtime, game_time_limit=1800
    )

    for i in range(0, options.times, 1):
        r = next(gen)

        time.sleep(5)

        reload(bot)
        player_config[0].ai = bot.HelBot(
            headless=options.headless, model=options.model)

        print(
            "\n\n### Starting next game (iteration {}/{}) ###\n\n".format(i, options.times))
        gen.send(player_config)

if __name__ == "__main__":
    main()
