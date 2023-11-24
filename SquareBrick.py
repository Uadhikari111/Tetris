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


class SquareBrick(TetrisBrick):
    def __init__(self, orientation, num_segments, col_num, color):
        super().__init__(orientation, num_segments, col_num, color)

    def init_position(self, cols):
        return [[0, 0], [1, 0], [1, -1], [0, -1]]

    def rotate(self):
        # No need for rotation
        pass

    def unrotate(self):
        # No need for rotation
        pass


# Example usage:
square_brick = SquareBrick(1, 4, 0, Color.RED)
print(square_brick.position)
