import cv2
import math
import numpy as np
import time


class Intel:

    def __init__(self, ai):
        self.ai = ai
        self.history = []
        self.storage = "train_data_intel"

        self.colors = {
            "mineral": (50, 0, 0),
            "geyser": (0, 50, 0)
        }

    def on_start(self):
        print(self.ai.player_id)

    def show(self, headless):
        self.flipped = cv2.flip(self.game_data, 0)

        if not headless:
            resized = cv2.resize(self.flipped, dsize=None, fx=2, fy=2)
            cv2.imshow("Intel - {}".format(self.ai.player_id), resized)
            cv2.waitKey(1)

    def new_field(self, game_info):
        return np.zeros(
            (
                game_info.map_size[1],
                game_info.map_size[0],
                3
            ),
            np.uint8
        )

    def new_cycle(self, game_info):
        self.feature_units = self.new_field(game_info)
        self.feature_units_health = self.new_field(game_info)
        self.game_data = self.new_field(game_info)

    def choose(self, choice, choices):
        y = np.zeros(choices)
        y[choice] = 1
        self.history.append([y, self.flipped])

    def draw_mineral(self, mineral):
        self.draw_unit(mineral, self.colors["mineral"])

    def draw_geyser(self, geyser):
        self.draw_unit(geyser, self.colors["geyser"])

    def draw_bar(self, amount, color, position, height, line_max=50):
        cv2.line(self.game_data, position,
                 (int(line_max * amount), position[1]), color, height)

    def draw_units(self, units, color):
        for unit in units:
            self.draw_unit(unit, color)

    def draw_units_own(self, units):
        for unit in units:
            self.draw_unit_own(unit)

    def draw_units_enemy(self, units):
        for unit in units:
            self.draw_unit_enemy(unit)

    def draw_unit_own(self, unit):
        if unit.is_structure:
            self.draw_unit(unit, (0, 255, 0))
        else:
            self.draw_unit(unit, (255, 100, 0))

    def draw_unit_enemy(self, unit):
        if unit.is_structure:
            self.draw_unit(unit, (0, 0, 255))
        else:
            self.draw_unit(unit, (55, 0, 155))

    def draw_unit(self, unit, color):
        cv2.circle(
            self.game_data,
            self._int_pos(unit.position),
            math.ceil(unit.radius), color, -1
        )

    def store(self):
        storeTo = "{}/{}.npy".format(
            self.storage,
            str(int(time.time()))
        )
        print(storeTo)
        np.save(storeTo, np.array(self.history))

    def _int_pos(self, position):
        return (int(position[0]), int(position[1]))
