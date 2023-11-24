import random
import tkinter as tk
from tkinter import messagebox
from ElBrick import ElBrick
from EssBrick import EssBrick
from JayBrick import JayBrick
from LongBrick import LongBrick
from StackBrick import StackBrick
from SquareBrick import SquareBrick
from ZeeBrick import ZeeBrick


class TetrisGame:
    def __init__(self):
        self.start_x = 115
        self.start_y = 40
        self.rows = 20
        self.cols = 12
        self.num_segments = 4
        self.state = 0
        self.game_score = 0
        self.background = [[0] * self.cols for _ in range(self.rows)]
        self.falling_brick = None

        self.el_brick_color = "#56E39F"
        self.stack_brick_color = "#FADF63"
        self.jay_brick_color = "#53B3CB"
        self.square_brick_color = "#CE5374"
        self.ess_brick_color = "#BC96E6"
        self.long_brick_color = "#E9724C"
        self.zee_brick_color = "#EA3788"

        self.colors = [
            "black", self.square_brick_color, self.jay_brick_color, self.ess_brick_color,
            self.stack_brick_color, self.zee_brick_color, self.el_brick_color,
            self.long_brick_color
        ]

    def fetch_position(self, row, col):
        return self.background[row][col]

    def fetch_rows(self):
        return len(self.background)

    def fetch_cols(self):
        return len(self.background[0])

    def init_board(self, start_x, start_y, cell_size, canvas):
        game_row = start_y
        for row in range(self.fetch_rows()):
            game_col = start_x
            for col in range(self.fetch_cols()):
                canvas.create_rectangle(
                    game_col, game_row, game_col + cell_size, game_row + cell_size, fill="white"
                )
                game_col += cell_size
            game_row += cell_size

    def new_game(self):
        self.high_score_to_file(self.game_score)
        self.background = [[0] * self.cols for _ in range(self.rows)]
        self.game_score = 0
        self.spawn_brick()

    def spawn_brick(self):
        total_no_of_bricks = 7
        random_brick = random.randint(0, total_no_of_bricks - 1)
        brick_orientation = 0
        num_segments = 4

        if random_brick == 0:
            self.falling_brick = ElBrick(brick_orientation, num_segments, self.cols, self.el_brick_color)
        elif random_brick == 1:
            self.falling_brick = StackBrick(brick_orientation, num_segments, self.cols, self.stack_brick_color)
        elif random_brick == 2:
            self.falling_brick = JayBrick(brick_orientation, num_segments, self.cols, self.jay_brick_color)
        elif random_brick == 3:
            self.falling_brick = SquareBrick(brick_orientation, num_segments, self.cols, self.square_brick_color)
        elif random_brick == 4:
            self.falling_brick = EssBrick(brick_orientation, num_segments, self.cols, self.ess_brick_color)
        elif random_brick == 5:
            self.falling_brick = LongBrick(brick_orientation, num_segments, self.cols, self.long_brick_color)
        elif random_brick == 6:
            self.falling_brick = ZeeBrick(brick_orientation, num_segments, self.cols, self.zee_brick_color)

    def make_move(self, get_key):
        if get_key == 1:
            if self.validate_move():
                self.falling_brick.move_left()
        elif get_key == 2:
            if self.validate_move():
                if self.falling_brick.get_type() == 5:
                    if self.validate_move():
                        self.falling_brick.move_long_brick()
                elif self.falling_brick.get_type() == 3:
                    if self.validate_move():
                        self.falling_brick.move_square_brick()
                else:
                    self.falling_brick.move_right()
            else:
                if self.validate_move():
                    self.falling_brick.move_right()
        elif get_key == 3:
            self.state = (self.state + 1) % 2

    def validate_move(self):
        if self.falling_brick.get_bottom() <= 0:
            return False
        if self.falling_brick.get_bottom() >= self.rows:
            return False

        for current_segment in range(self.num_segments):
            previous_brick_col = self.falling_brick.get_position()[current_segment][0]
            previous_brick_row = self.falling_brick.get_position()[current_segment][1]

            if self.background[previous_brick_row][previous_brick_col] > 0:
                return False

        return True

    def transfer_color(self):
        falling_brick_position = self.falling_brick.get_position()

        red_color = 1
        blue_color = 2
        teal_color = 3
        yellow_color = 4
        purple_color = 5
        green_color = 6
        orange_color = 7

        for current_segment in range(self.num_segments):
            col = falling_brick_position[current_segment][0]
            row = falling_brick_position[current_segment][1]

            brick_type = self.falling_brick.get_type()

            if brick_type == 0:
                self.background[row][col] = green_color
            elif brick_type == 1:
                self.background[row][col] = yellow_color
            elif brick_type == 2:
                self.background[row][col] = blue_color
            elif brick_type == 3:
                self.background[row][col] = red_color
            elif brick_type == 4:
                self.background[row][col] = teal_color
            elif brick_type == 5:
                self.background[row][col] = orange_color
            elif brick_type == 6:
                self.background[row][col] = purple_color

    def rotate(self):
        if self.falling_brick.get_type() == 5:
            if self.validate_move():
                self.falling_brick.rotate()
        else:
            self.falling_brick.rotate()

        def brick_color(self, row, col):
            return self.background[row][col]

    def get_falling_brick(self):
        return self.falling_brick

    def game_over_detection(self):
        top_row = 1

        for temp_col in range(self.cols):
            if self.background[top_row][temp_col] > 0:
                return True

        return False

    def full_row_detection(self):
        full_row = True
        final_row = self.rows - 1

        for temp_row in range(self.rows):
            for temp_col in range(self.cols):
                if self.background[final_row][temp_col] == 0:
                    full_row = False

        if full_row:
            self.row_deletion()
            self.drop_bricks()

        return full_row

    def row_deletion(self):
        score_increment = 100
        final_row = self.rows - 1

        for temp_col in range(self.cols):
            self.background[final_row][temp_col] = 0

        self.game_score += score_increment

    def drop_bricks(self):
        final_row = self.rows - 1
        final_col = self.cols - 1

        for temp_col in range(final_col, -1, -1):
            for temp_row in range(final_row, -1, -1):
                new_row = temp_row + 1

                if self.background[temp_row][temp_col] > 0:
                    self.background[new_row][temp_col] = self.background[temp_row][temp_col]
                    self.background[temp_row][temp_col] = 0

    def high_score_to_file(self, highest_score):
        file_name = "highScore.csv"
        try:
            with open(file_name, "a") as file:
                if highest_score > 0:
                    file.write(f"{highest_score}\n")
        except IOError as ioe:
            messagebox.showwarning("File IO Error", f"Warning: error in data from file: {file_name}")

    def high_score_from_file(self):
        file_name = "highScore.csv"
        total_high_score_tracker = 0
        ten_high_score = 10

        try:
            with open(file_name) as file:
                lines = file.readlines()
                total_high_score_tracker = len(lines)

                if total_high_score_tracker > 0:
                    high_score_array = [int(score.strip()) for score in lines]

                    if total_high_score_tracker > 2:
                        high_score_array.sort(reverse=True)

                    elif total_high_score_tracker == 2:
                        high_score_array.sort(reverse=True)

                    if total_high_score_tracker < 10:
                        messagebox.showinfo(
                            "Top 10 highScore",
                            "\n".join(f"<html><b>{score}</b></html>" for score in high_score_array)
                        )
                    else:
                        messagebox.showinfo(
                            "Top 10 highScore",
                            "\n".join(f"<html><b>{score}</b></html>" for score in high_score_array[:ten_high_score])
                        )
                elif total_high_score_tracker == 0:
                    messagebox.showinfo("Top 10 highScore", "Empty HighScore")

        except IOError as ioe:
            messagebox.showwarning("File IO Error", f"Warning: error in data from file: {file_name}")

    def clear_high_score(self):
        file_name = "highScore.csv"

        try:
            with open(file_name, "w") as file:
                file.write("")
            messagebox.showinfo("HighScore Cleared", "All High Scores Cleared")
        except IOError as ioe:
            messagebox.showwarning("File IO Error", f"Warning: error in data from file: {file_name}")

    def save_game_to_file(self):
        file_name = "saveGame.csv"
        try:
            with open(file_name, "w") as file:
                for temp_row in range(self.rows):
                    for temp_col in range(self.cols):
                        file.write(f"{self.background[temp_row][temp_col]},")
                    file.write("\n")
        except IOError as ioe:
            messagebox.showwarning("File IO Error", f"Warning: error in data from file: {file_name}")

    def load_game_from_file(self):
        file_name = "saveGame.csv"

        try:
            with open(file_name) as file:
                for temp_row in range(self.rows):
                    line = file.readline()
                    self.background[temp_row] = [int(cell) for cell in line.strip().split(",")]

        except IOError as ioe:
            messagebox.showwarning("File IO Error", f"Warning: error in data from file: {file_name}")

