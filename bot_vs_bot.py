import sc2
from sc2 import Race
from sc2.player import Bot
from bots.helbot.bot import HelBot
from options import Options

options = Options()


def main():
    for i in range(options.times):
        sc2.run_game(sc2.maps.get("Abyssal Reef LE"), [
            Bot(Race.Protoss, HelBot(
                headless=options.headless, model=options.model)),
            Bot(Race.Protoss, HelBot(
                headless=options.headless, model=options.model))
        ], realtime=options.realtime)


if __name__ == '__main__':
    main()
