import os
import sc2
from sc2 import Race
from sc2.player import Bot
from bots.helbot.bot import HelBot

import optparse

parser = optparse.OptionParser()

parser.add_option('-r', '--realtime',
                  action="store_true", dest="realtime",
                  help="Run in realtime", default=False)

parser.add_option('-l', '--headless',
                  action="store_true", dest="headless",
                  help="Run in headless mode", default=False)

parser.add_option('-m', '--model',
                  action="store", dest="model",
                  help="Model to use", default=False)

parser.add_option('-t', '--times', type="int",
                  action="store", dest="times",
                  help="How often to run", default=1)

options, args = parser.parse_args()


def main():
    for i in range(options.times):
        sc2.run_game(sc2.maps.get("Abyssal Reef LE"), [
            Bot(Race.Protoss,  HelBot(
                headless=options.headless, model=options.model)),
            Bot(Race.Protoss,  HelBot(headless=options.headless, model=options.model))
        ], realtime=options.realtime)

if __name__ == '__main__':
    main()
