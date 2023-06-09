import itertools
import random
from oscdraw.draw import Canvas
from oscdraw.objects import Point, Line, Polygon, Ellipse, ObjectCollection


class SquareData:
    BASE         = 0b00000000
    BOMB         = 0b10000000
    REVEALED     = 0b01000000
    MARKED       = 0b00100000
    SURROUNDED_1 = 0b00000001
    SURROUNDED_2 = 0b00000010
    SURROUNDED_3 = 0b00000011
    SURROUNDED_4 = 0b00000100
    SURROUNDED_5 = 0b00000101
    SURROUNDED_6 = 0b00000110
    SURROUNDED_7 = 0b00000111
    SURROUNDED_8 = 0b00001000

class Board:
    def __init__(self, width: int = 10, height: int = 10, bomb_amount: int = 30):
        assert 0 < width and isinstance(width, int), "width must be a positive whole number"
        assert 0 < height and isinstance(height, int), "height must be a positive whole number"
        assert 0 < bomb_amount and isinstance(bomb_amount, int), "bomb_amount must be a positive whole number"
        self.width, self.height = width, height
        # left, right, up, down, up: \, /, down: \, /
        directions = ((0, -1), (0, 1), (1, 0), (-1, 0), (1, -1), (1, 1), (-1, 1), (-1, -1))
        self.board = [[SquareData.BASE for x in range(width)] for y in range(height)]
        self.state = 0  # 0: game, 1: win, -1: lose
        # region bombs
        coords = []
        for y in range(height):
            for x in range(width):
                coords.append((y, x))
        print(coords)
        for i in range(bomb_amount):
            coord = random.choice(coords)
            coords.remove(coord)
            self.board[coord[0]][coord[1]] |= SquareData.BOMB
        # endregion
        # region count neighbour bombs
        for y in range(len(self.board)):
            for x in range(len(self.board[0])):
                for d in directions:
                    if 0 <= y + d[0] < height and 0 <= x + d[1] < width:
                        if self.board[y + d[0]][x + d[1]] & SquareData.BOMB:
                            self.board[y][x] += 1
        # endregion

    def _check_win(self):
        win = True
        for line in self.board:
            for square in line:
                if not square & SquareData.BOMB:
                    win = False
                    break
        if win:
            self.state = 1

    def _reveal_square(self, x: int, y: int):
        assert self.state == 0, "cannot reveal in a not ongoing game"
        assert 0 <= x < self.width, f"x must be between 0 and width - 1 {self.width - 1}"
        assert 0 <= y < self.height, f"y must be between 0 and height - 1 {self.height - 1}"
        self.board[y][x] |= SquareData.REVEALED
        if self.board[y][x] & SquareData.MARKED:
            self.board[y][x] ^= SquareData.MARKED
        if self.board[y][x] & SquareData.BOMB:
            self.state = -1
        """else:
            self._check_win()"""

    def reveal_squares(self, x: int, y: int):
        assert self.state == 0, "cannot reveal in a not ongoing game"
        assert 0 <= x < self.width, f"x must be between 0 and width - 1 {self.width - 1}"
        assert 0 <= y < self.height, f"y must be between 0 and height - 1 {self.height - 1}"
        self._reveal_square()

    def mark_square(self, x: int, y: int):
        assert self.state == 0, "cannot mark in a not ongoing game"
        assert 0 <= x < self.width, f"x must be between 0 and width - 1 {self.width - 1}"
        assert 0 <= y < self.height, f"y must be between 0 and height - 1 {self.height - 1}"
        assert not self.board[y][x] & SquareData.REVEALED, "cannot mark a revealed square"
        self.board[y][x] |= SquareData.MARKED

    def get_board(self):
        return self.board

    def get_state(self):
        """
        * 0: ongoing game
        * 1: win
        * -1: lose
        :return: state
        """
        return self.state

    def _print_board(self, *, cheat=False):
        """
        Text representation of the board.
        :return: str
        """
        print("|", end="")
        for line in self.board:
            for square in line:
                if square & SquareData.REVEALED or cheat:
                    for i in range(1, 9):
                        if square & i == i:
                            print(f"{i}|", end="")
                            break
                    else:
                        if square & SquareData.MARKED:
                            print("?|", end="")
                        elif square & SquareData.BOMB:
                            print("X|", end="")
                        else:
                            print(" |", end="")
                else:
                    print("-|", end="")
            print("\n|", end="")
        print()


def textgame():
    board = Board()
    while board.get_state() == 0:
        board._print_board(cheat=True)
        command = input("> ")
        command = command.split(" ")
        command, args = command[0], command[1:]
        if command == "r":
            if len(args) != 2:
                print("ERROR")
                continue
            args = (int(args[0]), int(args[1]))
            board.reveal_square(*args)
        elif command == "m":
            if len(args) != 2:
                print("ERROR")
                continue
            args = (int(args[0]), int(args[1]))
            board.mark_square(*args)
    board._print_board()
    if board.get_state() == 1:
        print("You win!")
    elif board.get_state() == -1:
        print("You lose...")
    print(board.get_state())
if __name__ == '__main__':
    textgame()