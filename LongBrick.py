import tkinter as tk
from tkinter import Canvas
from enum import Enum


class Color(Enum):
    RED = "red"
    GREEN = "green"
    BLUE = "blue"
    YELLOW = "yellow"
    CYAN = "cyan"


class TetrisBrick:
    def __init__(self, orientation, num_segments, col_num, color):
        self.position = self.init_position(10)  # Assuming 10 columns in Tetris grid
        self.orientation = orientation
        self.num_segments = num_segments
        self.col_num = col_num
        self.color = color

    def init_position(self, cols):
        return [[0, 0] for _ in range(4)]

    def rotate(self):
        pass

    def unrotate(self):
        pass


class LongBrick(TetrisBrick):
    def __init__(self, orientation, num_segments, col_num, color):
        super().__init__(orientation, num_segments, col_num, color)

    def init_position(self, cols):
        return [[0, 0], [1, 0], [2, 0], [3, 0]]

    def rotate(self):
        if self.orientation == 1:
            self.position[0][0] += 2
            self.position[0][1] -= 2
            self.position[1][0] += 1
            self.position[1][1] -= 1
            self.position[3][0] -= 1
            self.position[3][1] += 1
            self.orientation = 2
        else:
            self.unrotate()

    def unrotate(self):
        self.position[0][0] -= 2
        self.position[0][1] += 2
        self.position[1][0] -= 1
        self.position[1][1] += 1
        self.position[3][0] += 1
        self.position[3][1] -= 1
        self.orientation = 1


# Example usage:
long_brick = LongBrick(1, 4, 0, Color.RED)
long_brick.rotate()
print(long_brick.position)
long_brick.unrotate()
print(long_brick.position)
