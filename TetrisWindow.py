from tkinter import *
from tkinter import messagebox
from TetrisGame import TetrisGame
from TetrisBrick import TetrisBrick
from TetrisDisplay import TetrisDisplay
import pygame
import os

class TetrisWindow(Tk):
    def __init__(self):
        
        super().__init__()

        self.win_width = 550
        self.win_height = 500
        self.sound_state = 1
       

        self.game = TetrisGame()
        self.display = TetrisDisplay(self, self.game)

        self.title("Tetris Game \t\t@Upendra Adhikari")
        self.geometry(f"{self.win_width}x{self.win_height}")

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.game_menu_bar()

        self.game.new_game()

        self.display.pack()
        self.mainloop()

    def game_menu_bar(self):
        menu_bar = Menu(self)
        self.config(menu=menu_bar)

        game_menu = Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Game", menu=game_menu)

        new_game = Menu(game_menu, tearoff=0)
        game_menu.add_cascade(label="New Game", menu=new_game)
        new_game.add_command(label="Start New Game", command=self.game.new_game)
        
        high_score = Menu(game_menu, tearoff=0)
        game_menu.add_cascade(label="High Score", menu=high_score)
        high_score.add_command(label="Display High Score", command=self.game.high_score_from_file)

        clear_high_score = Menu(game_menu, tearoff=0)
        game_menu.add_cascade(label="Clear High Score", menu=clear_high_score)
        clear_high_score.add_command(label="Clear All High Scores", command=self.game.clear_high_score)

        save_game = Menu(game_menu, tearoff=0)
        game_menu.add_cascade(label="Save Game", menu=save_game)
        save_game.add_command(label="Save Current Game", command=self.game.save_game_to_file)

        load_game = Menu(game_menu, tearoff=0)
        game_menu.add_cascade(label="Load Game", menu=load_game)
        load_game.add_command(label="Load Saved Game", command=self.game.load_game_from_file)

        music_menu = Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Music", menu=music_menu)
        music_menu.add_command(label="Toggle Music On/Off", command=self.toggle_music)

        color_menu = Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Color", menu=color_menu)

        default_color = Menu(color_menu, tearoff=0)
        color_menu.add_cascade(label="Default Color", menu=default_color)
        default_color.add_command(label="Set Default Colors", command=self.set_default_colors)

        color_combo_1 = Menu(color_menu, tearoff=0)
        color_menu.add_cascade(label="Color Combo 1", menu=color_combo_1)
        color_combo_1.add_command(label="Set Color Combo 1", command=self.set_color_combo_1)

        color_combo_2 = Menu(color_menu, tearoff=0)
        color_menu.add_cascade(label="Color Combo 2", menu=color_combo_2)
        color_combo_2.add_command(label="Set Color Combo 2", command=self.set_color_combo_2)

    def toggle_music(self):
        if self.sound_state == 1:
            pygame.mixer.music.stop()
            self.sound_state += 1
        elif self.sound_state == 2:
            pygame.mixer.music.play(-1)
            self.sound_state -= 1

    def set_default_colors(self):
        self.game.el_brick_color = "#56E39F"
        self.game.stack_brick_color = "#FADF63"
        self.game.jay_brick_color = "#53B3CB"
        self.game.square_brick_color = "#CE5374"
        self.game.ess_brick_color = "#BC96E6"
        self.game.long_brick_color = "#E9724C"
        self.game.zee_brick_color = "#EA3788"

        self.display.border_color = "#00AF54"

        self.display.colors = [
            "black", "#CE5374", "#53B3CB", "#BC96E6", "#FADF63", "#EA3788", "#56E39F", "#E9724C"
        ]

    def set_color_combo_1(self):
        self.game.el_brick_color = "#EB5E55"
        self.game.stack_brick_color = "#07BEB8"
        self.game.jay_brick_color = "#45462A"
        self.game.square_brick_color = "#386C0B"
        self.game.ess_brick_color = "#446DF6"
        self.game.long_brick_color = "#D81E5B"
        self.game.zee_brick_color = "#EFD9CE"

        self.display.border_color = "#FC2F00"

        self.display.colors = [
            "black", "#386C0B", "#45462A", "#446DF6", "#07BEB8", "#EFD9CE", "#EB5E55", "#D81E5B"
        ]

    def set_color_combo_2(self):
        self.game.el_brick_color = "#2F2963"
        self.game.stack_brick_color = "#FF9F1C"
        self.game.jay_brick_color = "#A22C29"
        self.game.square_brick_color = "#553555"
        self.game.ess_brick_color = "#CCFF66"
        self.game.long_brick_color = "#CC4BC2"
        self.game.zee_brick_color = "#333745"

        self.display.border_color = "#FF70A6"

        self.display.colors = [
            "black", "#553555", "#A22C29", "#CCFF66", "#FF9F1C", "#333745", "#2F2963", "#CC4BC2"
        ]

    def on_closing(self):
        self.game.high_score_to_file(self.game.game_score)
        self.destroy()

if __name__ == "__main__":
    TetrisWindow()
