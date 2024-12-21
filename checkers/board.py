from .constants import BROWN, ROWS, BROWN2, SQUARE_SIZE, COLS, WHITE, BLACK
from .piece import Piece


class Board:
    def __init__(self, canvas):
        self.canvas = canvas
        self.board = []
        self.white_left = self.black_left = 16
        self.white_kings = self.black_kings = 0
        self.create_board()

    def draw_squares(self):
        self.canvas.delete("all")
        for row in range(ROWS):
            for col in range(COLS):
                color = BROWN2 if (row + col) % 2 == 1 else BROWN
                x0 = col * SQUARE_SIZE
                y0 = row * SQUARE_SIZE
                x1 = x0 + SQUARE_SIZE
                y1 = y0 + SQUARE_SIZE
                self.canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline=color)

    def move(self, piece, row, col):
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        piece.move(row, col)

        if row == ROWS - 1 or row == 0:
            piece.make_king()
            if piece.color == BLACK:
                self.black_kings += 1
            else:
                self.white_kings += 1

    def get_piece(self, row, col):
        return self.board[row][col]

    def create_board(self):
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                if 1<=row<=2:
                    self.board[row].append(Piece(row, col, BLACK))
                elif 5<=row<=6:
                    self.board[row].append(Piece(row, col, WHITE))
                else:
                    self.board[row].append(0)

    def draw(self):
        self.draw_squares()
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(self.canvas)

    def remove(self, pieces):
        for piece in pieces:
            self.board[piece.row][piece.col] = 0
            if piece != 0:
                if piece.color == WHITE:
                    self.white_left -= 1
                else:
                    self.black_left -= 1

    def winner(self):
        if self.white_left <= 1:
            return "Побеждают Черные"
        elif self.black_left <= 1:
            return "Побеждают Белые"
        elif self.white_left == 1 and self.black_left == 1:
            return "Ничья"
        return None

    def get_valid_moves(self, piece):
        moves = {}
        row = piece.row
        col = piece.col

        if piece.color == WHITE and not piece.king:
            start = row - 1
            stop = max(row - 3, -1)
            moves.update(self._traverse_vertical(start, stop, -1, piece.color, col))
            moves.update(self._traverse_horizontal(col - 1, -1, -1, piece.color, row))
            moves.update(self._traverse_horizontal(col + 1, COLS, 1, piece.color, row))
        if piece.color == BLACK and not piece.king:
            moves.update(self._traverse_vertical(row + 1, min(row + 3, ROWS), 1, piece.color, col))
            moves.update(self._traverse_horizontal(col - 1, -1, -1, piece.color, row))
            moves.update(self._traverse_horizontal(col + 1, COLS, 1, piece.color, row))

        if piece.king:
            moves.update(self._traverse_vertical_king(row + 1, ROWS, 1, piece.color, col))
            moves.update(self._traverse_vertical_king(row - 1, -1, -1, piece.color, col))
            moves.update(self._traverse_horizontal_king(col - 1, -1, -1, piece.color, row))
            moves.update(self._traverse_horizontal_king(col + 1, COLS, 1, piece.color, row))

        capture_moves = {pos: skipped for pos, skipped in moves.items() if skipped}
        if capture_moves:
            max_captures = max(len(skipped) for skipped in capture_moves.values())
            capture_moves = {pos: skipped for pos, skipped in capture_moves.items() if len(skipped) == max_captures}
            return capture_moves

        return moves

    def _traverse_vertical(self, start, stop, step, color, col, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            current = self.board[r][col]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, col)] = skipped + last
                else:
                    moves[(r, col)] = last
                if last:
                    row_limit = max(r - 3, -1) if step == -1 else min(r + 3, ROWS)
                    new_skipped = skipped + last
                    moves.update(self._traverse_vertical(r + step, row_limit, step, color, col, skipped=new_skipped))
                    moves.update(self._traverse_horizontal(col - 1, -1, -1, color, r, skipped=new_skipped))
                    moves.update(self._traverse_horizontal(col + 1, COLS, 1, color, r, skipped=new_skipped))
                break
            elif current.color == color:
                break
            else:
                if last:
                    break
                last = [current]

        return moves

    def _traverse_horizontal(self, start, stop, step, color, row, skipped=[]):
        moves = {}
        last = []
        for c in range(start, stop, step):
            current = self.board[row][c]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(row, c)] = skipped + last
                else:
                    moves[(row, c)] = last

                if last:
                    col_limit = max(c - 3, -1) if step == -1 else min(c + 3, COLS)
                    new_skipped = skipped + last
                    moves.update(self._traverse_horizontal(c + step, col_limit, step, color, row, skipped=new_skipped))
                    moves.update(self._traverse_vertical(row - 1, max(row - 3, -1), -1, color, c, skipped=new_skipped))
                    moves.update(self._traverse_vertical(row + 1, min(row + 3, ROWS), 1, color, c, skipped=new_skipped))
                break
            elif current.color == color:
                break
            else:
                if last:
                    break
                last = [current]  

        return moves

    def _traverse_vertical_king(self, start, stop, step, color, col, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            current = self.board[r][col]
            if current == 0:
                if skipped:
                    moves[(r, col)] = skipped + last
                else:
                    moves[(r, col)] = last
                if last:
                    row_limit = -1 if step == -1 else ROWS
                    new_skipped = skipped + last
                    moves.update(self._traverse_vertical(r + step, row_limit, step, color, col, skipped=new_skipped))
                    moves.update(self._traverse_horizontal(col - 1, -1, -1, color, r, skipped=new_skipped))
                    moves.update(self._traverse_horizontal(col + 1, COLS, 1, color, r, skipped=new_skipped))
            elif current.color == color:
                break
            else:
                if last:
                    break
                last = [current]
        return moves

    def _traverse_horizontal_king(self, start, stop, step, color, row, skipped=[]):
        moves = {}
        last = []
        for c in range(start, stop, step):
            current = self.board[row][c]
            if current == 0:
                if skipped:
                    moves[(row, c)] = skipped + last
                else:
                    moves[(row, c)] = last

                if last:
                    col_limit = -1 if step == -1 else COLS
                    new_skipped = skipped + last
                    moves.update(self._traverse_horizontal(c + step, col_limit, step, color, row, skipped=new_skipped))
                    moves.update(self._traverse_vertical(row - 1, -1, -1, color, c, skipped=new_skipped))
                    moves.update(self._traverse_vertical(row + 1, ROWS, 1, color, c, skipped=new_skipped))
            elif current.color == color:
                break
            else:
                if last:
                    break
                last = [current]

        return moves

