import tkinter as tk
from tkinter import messagebox

class TetrisDisplay(tk.Canvas):
    def __init__(self, master, game):
        super().__init__(master, width=500, height=500, bg="white")
        self.game = game
        self.start_x = 115
        self.start_y = 40
        self.cell_size = 40
        self.colors = [
            "black", "#CE5374", "#53B3CB", "#BC96E6",
            "#FADF63", "#EA3788", "#56E39F", "#E9724C"
        ]
        self.boarder_color = "#00AF54"
        self.game_over_color = "#403F4B"
        self.score_color = "#ec4e20"
        self.timer = None
        self.timer_speed = 250

    def paint_component(self):
        self.delete("all")
        self.game.init_board(self.start_x, self.start_y, self.cell_size, self)

        for row in range(len(self.game.get_falling_brick().position)):
            brick_start_x = (self.game.get_falling_brick().position[row][0] * self.cell_size) + self.start_x
            brick_start_y = (self.game.get_falling_brick().position[row][1] * self.cell_size) + self.start_y

            self.create_rectangle(
                brick_start_x,
                brick_start_y,
                brick_start_x + self.cell_size,
                brick_start_y + self.cell_size,
                fill=self.game.get_falling_brick().get_color(),
                outline="black"
            )

        self.create_line(
            self.start_x,
            self.start_y,
            self.start_x + (self.game.fetch_cols() * self.cell_size),
            self.start_y,
            fill=self.boarder_color
        )

        self.create_rectangle(
            self.start_x - self.cell_size,
            self.start_y,
            self.start_x + self.game.fetch_cols() * self.cell_size,
            self.start_y + self.game.fetch_rows() * self.cell_size,
            fill=self.boarder_color
        )

        self.create_rectangle(
            self.start_x - self.cell_size,
            self.start_y + self.game.fetch_rows() * self.cell_size,
            self.start_x + (self.game.fetch_cols() + 2) * (self.cell_size),
            self.start_y + (self.game.fetch_rows() + 1) * self.cell_size,
            fill=self.boarder_color
        )

        for row in range(self.game.fetch_rows()):
            for col in range(self.game.fetch_cols()):
                individual_cell_color = self.game.brick_color(row, col)
                if individual_cell_color > 0:
                    self.create_rectangle(
                        self.start_x + col * self.cell_size,
                        self.start_y + row * self.cell_size,
                        self.start_x + (col + 1) * self.cell_size,
                        self.start_y + (row + 1) * self.cell_size,
                        fill=self.colors[individual_cell_color],
                        outline="black"
                    )

        self.game_score_board()

        if self.game.game_over_detection():
            self.game_over_display()

    def process_move(self):
        self.bind("<Left>", lambda event: self.move_left())
        self.bind("<Right>", lambda event: self.move_right())
        self.bind("<Down>", lambda event: self.move_down())
        self.bind("<Up>", lambda event: self.rotate())
        self.bind("<n>", lambda event: self.new_game())

    def move_left(self):
        self.game.get_falling_brick().move_left()
        self.paint_component()

    def move_right(self):
        self.game.get_falling_brick().move_right()
        self.paint_component()

    def move_down(self):
        self.game.get_falling_brick().move_down()
        self.paint_component()

    def rotate(self):
        self.game.rotate()
        self.paint_component()

    def new_game(self):
        self.game.new_game()
        self.paint_component()

    def translate_key(self, event):
        move = event.keysym
        if move == "Left":
            return 1
        elif move == "Right":
            return 2
        elif move == "Down":
            return 3
        elif move == "Up":
            return 4
        elif move == "n":
            return 5
        return 0

    def pause_the_game(self):
        self.timer.stop()

    def game_score_board(self):
        x_score = 1
        y_score = 1
        score_width = 140
        score_height = 30
        score_font_y = 22

        self.create_rectangle(
            x_score, y_score,
            x_score + score_width, y_score + score_height,
            outline=self.score_color, fill=self.score_color
        )

        final_score = "Score: " + str(self.game.game_score)
        self.create_text(x_score + 10, score_font_y, text=final_score, anchor=tk.W, font=("Arial", 20), fill="black")

    def game_over_display(self):
        game_over_x = 60
        game_over_y = 120
        game_over_width = 350
        game_over_height = 200
        game_over_font_x = 70
        game_over_font_y = 235
        new_game_font_x = 120
        new_game_font_y = 280

        self.create_rectangle(
            game_over_x, game_over_y,
            game_over_x + game_over_width, game_over_y + game_over_height,
            outline=self.game_over_color, fill=self.game_over_color
        )

        self.create_text(
            game_over_font_x, game_over_font_y,
            text="Game Over !!", anchor=tk.W, font=("Arial", 50), fill="#009b72"
        )

        self.create_text(
            new_game_font_x, new_game_font_y,
            text="Press N to start a new game", anchor=tk.W, font=("Arial", 20), fill="#009b72"
        )

    def start_timer(self):
        self.timer = self.after(self.timer_speed, self.timer_handler)

    def timer_handler(self):
        self.game.get_falling_brick().move_down()
        self.paint_component()

        if not self.game.validate_move():
            row_test = True
            self.game.get_falling_brick().move_up()
            self.game.transfer_color()
            self.paint_component()

            if self.game.game_over_detection():
                self.pause_the_game()
            else:
                while row_test:
                    row_test = self.game.full_row_detection()
                self.game.spawn_brick()

        self.paint_component()
        self.start_timer()


class TetrisGame:
    def __init__(self):
        self.start_x = 115
        self.start_y = 40
        self.rows = 10
        self.cols = 12
        self.falling_brick = None
        self.game_score = 0
        self.state = 0  # 0: running, 1: paused
        self.board = [[0] * self.cols for _ in range(self.rows)]

    def fetch_cols(self):
        return self.cols

    def fetch_rows(self):
        return self.rows

        def init_board(self, start_x, start_y, cell_size, canvas):
            canvas.create_line(
                start_x, start_y,
                start_x + (self.cols * cell_size),
                start_y,
                fill="#00AF54"
        )

        canvas.create_rectangle(
            start_x - cell_size, start_y,
            start_x + self.cols * cell_size,
            start_y + self.rows * cell_size,
            fill="#00AF54"
        )

        canvas.create_rectangle(
            start_x - cell_size, start_y + self.rows * cell_size,
            start_x + (self.cols + 2) * cell_size,
            start_y + (self.rows + 1) * cell_size,
            fill="#00AF54"
        )

        for row in range(self.rows):
            for col in range(self.cols):
                individual_cell_color = self.board[row][col]
                if individual_cell_color > 0:
                    canvas.create_rectangle(
                        start_x + col * cell_size,
                        start_y + row * cell_size,
                        start_x + (col + 1) * cell_size,
                        start_y + (row + 1) * cell_size,
                        fill="#00AF54",
                        outline="black"
                    )

    def get_falling_brick(self):
        return self.falling_brick

    def fetch_rows(self):
        return self.rows

    def fetch_cols(self):
        return self.cols

    def brick_color(self, row, col):
        return self.board[row][col]

    def game_over_detection(self):
        # Add your game over detection logic here
        return False

    def full_row_detection(self):
        # Add your full row detection logic here
        return False

    def transfer_color(self):
        # Add your logic to transfer the color of the falling brick to the board
        pass

    def spawn_brick(self):
        # Add your logic to spawn a new brick
        pass

    def validate_move(self):
        # Add your logic to validate the current move of the falling brick
        return False

    def make_move(self, move):
        # Add your logic to handle the player's move
        pass

    def rotate(self):
        # Add your logic to rotate the falling brick
        pass

    def new_game(self):
        # Add your logic to start a new game
        pass

    def high_score_from_file(self):
        # Add your logic to read and sort high scores from a file
        pass

    def clear_high_score(self):
        # Add your logic to clear all high scores from a file
        pass

    def save_game_to_file(self):
        # Add your logic to save the current game state to a file
        pass

    def load_game_from_file(self):
        # Add your logic to load a saved game state from a file
        pass

