from .constants import WHITE, GREEN, SQUARE_SIZE, BLACK
from checkers.board import Board
from tkinter import messagebox

class Game:
    def __init__(self, canvas, turn_label):
        self.canvas = canvas
        self.turn_label = turn_label
        self._init()

    def show_rules(self):
        messagebox.showinfo("Правила игры", "Правила игры:\n"
                            "1. Простая шашка ходит на одно поле вперёд, влево, вправо. \n"
                            "2. Простая шашка бьёт шашку противника, стоящую спереди, справа или слева (бить назад запрещено), перескакивая через неё на следующее поле по вертикали или горизонтали. \n"
                            "3. Бой возможен только тогда, когда поле за шашкой противника свободно. Если с новой позиции шашки, побившей шашку противника, можно бить дальше, бой продолжается (за один ход можно побить несколько шашек противника). \n"
                            "4. Если есть несколько вариантов боя, игрок обязан выбрать тот, при котором берётся наибольшее количество шашек противника. \n"
                            "5. Простая шашка, вступившая на восьмую горизонталь, становится дамкой. \n"
                            "6. Дамка ходит на любое количество пустых полей вперёд, назад, вправо, влево. \n"
                            "7. Дамка бьёт шашки противника, стоящие от неё через любое количество пустых клеток спереди, сзади, справа и слева, если следующее за шашкой поле свободно. \n"           
                            "8. Выигрывает тот, кто смог уничтожить все шашки противника, либо тот, кто остался с несколькими своими простыми шашками против одной простой шашки противника. \n"
                            "9. Если на доске осталось по одной шашке — объявляется ничья.")

    def update(self):
        self.board.draw()
        self.draw_valid_moves(self.valid_moves)

    def _init(self):
        self.selected = None
        self.board = Board(self.canvas)
        self.turn = WHITE
        self.valid_moves = {}

    def winner(self):
        return self.board.winner()

    def reset(self):
        self._init()
        self.turn_label.config(text="Сейчас ходят: Белые")
        self.update()

    def select(self, row, col):
        if self.selected:
            result = self._move(row, col)
            if not result:
                self.selected = None
                self.select(row, col)

        piece = self.board.get_piece(row, col)
        if piece != 0 and piece.color == self.turn:
            self.selected = piece
            self.valid_moves = self.board.get_valid_moves(piece)
            return True
        if self.selected != piece and self.turn == WHITE:
            self.turn_label.config(text="Выберите шашку БЕЛОГО цвета")
        if self.selected != piece and self.turn == BLACK:
            self.turn_label.config(text="Выберите шашку ЧЕРНОГО цвета")
        return False

    def _move(self, row, col):
        piece = self.board.get_piece(row, col)
        if self.selected and piece == 0 and (row, col) in self.valid_moves:
            self.board.move(self.selected, row, col)
            skipped = self.valid_moves[(row, col)]
            if skipped:
                self.board.remove(skipped)
            self.change_turn()
        else:
            return False

        return True

    def draw_valid_moves(self, moves):
        for move in moves:
            row, col = move
            x = col * SQUARE_SIZE + SQUARE_SIZE // 2
            y = row * SQUARE_SIZE + SQUARE_SIZE // 2
            self.canvas.create_oval(x - 15, y - 15, x + 15, y + 15, fill=GREEN, outline=GREEN)

    def change_turn(self):
        self.valid_moves = {}
        if self.turn == WHITE:
            self.turn = BLACK
            self.turn_label.config(text="Сейчас ходят: Черные")
        else:
            self.turn = WHITE
            self.turn_label.config(text="Сейчас ходят: Белые")