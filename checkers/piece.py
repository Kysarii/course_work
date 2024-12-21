from .constants import SQUARE_SIZE, GREY
from PIL import Image, ImageTk
import tkinter as tk

class Piece:
    PADDING = 15
    OUTLINE = 2

    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color
        self.king = False
        self.x = 0
        self.y = 0
        self.calc_pos()

        crown_image = Image.open('crown.png')
        crown_image = crown_image.resize((40, 25), Image.Resampling.LANCZOS)
        self.crown_image = ImageTk.PhotoImage(crown_image)

    def calc_pos(self):
        self.x = SQUARE_SIZE * self.col + SQUARE_SIZE // 2
        self.y = SQUARE_SIZE * self.row + SQUARE_SIZE // 2

    def make_king(self):
        self.king = True

    def draw(self, canvas):
        radius = SQUARE_SIZE // 2 - self.PADDING

        canvas.create_oval(
            self.x - radius - self.OUTLINE,
            self.y - radius - self.OUTLINE,
            self.x + radius + self.OUTLINE,
            self.y + radius + self.OUTLINE,
            fill=GREY,
            outline=""
        )

        canvas.create_oval(
            self.x - radius,
            self.y - radius,
            self.x + radius,
            self.y + radius,
            fill=self.color,
            outline=""
        )

        if self.king:
            canvas.create_image(self.x, self.y, image=self.crown_image, anchor=tk.CENTER)

    def move(self, row, col):
        self.row = row
        self.col = col
        self.calc_pos()

