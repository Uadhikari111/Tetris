from abc import ABC, abstractmethod
from enum import Enum
import tkinter as tk

class Color(Enum):
    RED = "red"
    GREEN = "green"
    BLUE = "blue"
    YELLOW = "yellow"
    CYAN = "cyan"

class TetrisBrick(ABC):
    def __init__(self, orientation, num_segments, col_num, color):
        self.position = self.init_position(col_num)
        self.orientation = orientation
        self.num_segments = num_segments
        self.color = color

    @abstractmethod
    def init_position(self, cols):
        pass

    @abstractmethod
    def rotate(self):
        pass

    @abstractmethod
    def unrotate(self):
        pass

    def move_left(self):
        for temp_row in range(self.num_segments):
            if self.position[temp_row][0] < 1:
                break
            else:
                self.position[temp_row][0] -= 1

    def move_right(self):
        counter = 0
        number_of_columns = 12
        validity_checker = number_of_columns - 3

        if self.position[counter][0] < validity_checker and counter < self.num_segments:
            for temp_row in range(self.num_segments):
                self.position[temp_row][0] += 1
                counter += 1

    def move_up(self):
        for temp_row in range(self.num_segments):
            self.position[temp_row][1] -= 1
        return True

    def move_down(self):
        for temp_row in range(self.num_segments):
            self.position[temp_row][1] += 1

    def get_bottom(self):
        bottom_row = 0

        for row in range(self.num_segments):
            if self.position[row][1] > bottom_row:
                bottom_row = self.position[row][1]

        return bottom_row

    def move_long_brick(self, random_brick):
        if random_brick == 5:
            counter = 0
            number_of_columns = 12
            validity_checker = number_of_columns - 4

            if self.position[counter][0] < validity_checker and counter < self.num_segments:
                for temp_row in range(self.num_segments):
                    self.position[temp_row][0] += 1
                    counter += 1

    def move_square_brick(self, random_brick):
        if random_brick == 3:
            counter = 0
            number_of_columns = 12
            validity_checker = number_of_columns - 2

            if self.position[counter][0] < validity_checker and counter < self.num_segments:
                for temp_row in range(self.num_segments):
                    self.position[temp_row][0] += 1
                    counter += 1

class tetris_brick(TetrisBrick):
    def init_position(self, cols):
        pass

    def rotate(self):
        pass
    


