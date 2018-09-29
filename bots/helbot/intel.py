import cv2
import math
import numpy as np
import time


class Intel:

    def __init__(self, game):
        self.game = game
        self.history = []
        self.storage = "train_data_intel"

        self.colors = {
            "mineral": (50, 0, 0),
            "geyser": (0, 50, 0)
        }

    def show(self, headless):
        self.flipped = cv2.flip(self.game_data, 0)

        if not headless:
            resized = cv2.resize(self.flipped, dsize=None, fx=2, fy=2)
            cv2.imshow('Intel', resized)
            cv2.waitKey(1)

    def new_cycle(self, game_info):
        self.game_data = np.zeros(
            (
                game_info.map_size[1],
                game_info.map_size[0],
                3
            ),
            np.uint8
        )

    def choose(self, choice):
        y = np.zeros(4)
        y[choice] = 1
        self.history.append([y, self.flipped])

    def draw_mineral(self, mineral):
        self.draw_unit(mineral, self.colors["mineral"])

    def draw_geyser(self, geyser):
        self.draw_unit(geyser, self.colors["geyser"])

    def draw_bar(self, amount, color, position, height, line_max=50):
        cv2.line(self.game_data, position,
                 (int(line_max * amount), position[1]), color, height)

    def draw_unit(self, unit, color):
        cv2.circle(
            self.game_data,
            self._int_pos(unit.position),
            math.ceil(unit.radius), color, -1
        )

    def store(self, game_result, enemy):
        np.save(
            "{}\\{}-{}.npy".format(
                self.storage,
                str(int(time.time())),
                suffix
            ),
            np.array(self.history)
        )

    def _int_pos(self, position):
        return (int(position[0]), int(position[1]))
