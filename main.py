class Game:
    def __init__(self):
        self.board = []
        self.history = []
        self.player = 'B'
        self.rem = 0

    def start(self):
        self.board = [['.' for j in range(8)] for i in range(8)]
        self.history = []
        self.player = 1
        self.rem = 64

    def add(self, x, y):
        if 0 <= x < 8 and 0 <= y < 8 and self.board[y][x] == '.':
            self.board[y][x] = self.player
            self.rem -= 1
            if self.player == 'B':
                self.player = 'W'
            else:
                self.player = 'B'

            self.flip(x, y, 0, 1)
            self.flip(x, y, 0, -1)
            self.flip(x, y, 1, 0)
            self.flip(x, y, -1, 0)
            self.flip(x, y, 1, 1)
            self.flip(x, y, 1, -1)
            self.flip(x, y, -1, 1)
            self.flip(x, y, -1, -1)

            self.history.append([[self.board[i][j] for j in range(8)] for i in range(8)])
            return True

        return False

    def flip(self, x, y, dx, dy):
        ex = x
        ey = y
        steps = 0
        while 0 <= ex < 8 and 0 <= ey < 8 and self.board[ey][ex] != '.' and self.board[ey][ex] != self.player:
            ex += dx
            ey += dy
            steps += 1

        if 0 <= ex < 8 and 0 <= ey < 8 and self.board[ey][ex] == self.player:
            for i in range(steps - 1):
                ex -= dx
                ey -= dy
                self.board[ey][ex] = self.player

    def get_winner(self):
        if self.rem > 0:
            b = 0
            w = 0

            for i in range(8):
                for j in range(8):
                    if self.board[i][j] == 'B':
                        b += 1
                    elif self.board[i][j] == 'W':
                        w += 1

            if b > w:
                return 'B'
            elif w > b:
                return 'W'
            return 'T'

        return None

    def undo(self):
        if len(self.history) > 0:
            self.board = self.history.pop()


def main():
    print("Welcome to the Othello Solver!")


if __name__ == "__main__":
    main()
