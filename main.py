import sys


class Game:
    def __init__(self):
        self.board = []
        self.history = []
        self.player = 'B'  # 'B' for Black, 'W' for White
        self.rem = 0  # Remaining empty squares
        self.black = 0  # Number of black pieces
        self.white = 0  # Number of white pieces

    def start(self):
        """Initializes a new game of Othello."""
        self.board = [['.' for _ in range(8)] for _ in range(8)]
        # Set up initial four pieces
        self.board[3][3] = 'W'
        self.board[3][4] = 'B'
        self.board[4][3] = 'B'
        self.board[4][4] = 'W'

        self.player = 'B'  # Black always starts
        self.rem = 60  # 64 total squares - 4 initial pieces
        self.black = 2
        self.white = 2
        self.history = []
        # Store the initial state for undo functionality
        self.history.append(self.get_current_state())
        print("New game started!")
        self.display_board()

    def get_current_state(self):
        """Returns a deep copy of the current game state."""
        return {
            'board': [row[:] for row in self.board],  # Deep copy of the board
            'player': self.player,
            'rem': self.rem,
            'black': self.black,
            'white': self.white
        }

    def set_state(self, state):
        """Sets the game state from a given state dictionary."""
        self.board = [row[:] for row in state['board']]
        self.player = state['player']
        self.rem = state['rem']
        self.black = state['black']
        self.white = state['white']

    def display_board(self):
        """Prints the current state of the Othello board."""
        print("\n  0 1 2 3 4 5 6 7")
        print("  ---------------")
        for i, row in enumerate(self.board):
            print(f"{i}|{' '.join(row)}|")
        print("  ---------------")
        print(f"Black: {self.black} | White: {self.white} | Current Player: {self.player}")
        print(f"Remaining squares: {self.rem}\n")

    def is_valid_move(self, x, y, current_player):
        """
        Checks if placing a piece at (x, y) is a valid move for the current_player.
        A move is valid if it's an empty square and if it flips at least one opponent's piece.
        """
        if not (0 <= x < 8 and 0 <= y < 8) or self.board[y][x] != '.':
            return False

        opponent = 'W' if current_player == 'B' else 'B'

        # Check all 8 directions
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue  # Skip current position

                # Simulate a flip in this direction to see if any pieces would be flipped
                if self._simulate_flip(x, y, dx, dy, current_player, opponent) > 0:
                    return True
        return False

    def _simulate_flip(self, x, y, dx, dy, current_player, opponent):
        """
        Simulates flipping pieces in a given direction (dx, dy) from (x, y).
        Returns the number of pieces that would be flipped. Does not modify the board.
        """
        count = 0
        nx, ny = x + dx, y + dy

        # Traverse in the given direction
        while 0 <= nx < 8 and 0 <= ny < 8 and self.board[ny][nx] == opponent:
            count += 1
            nx += dx
            ny += dy

        # If we found at least one opponent's piece and then hit our own piece, it's a valid flip
        if count > 0 and 0 <= nx < 8 and 0 <= ny < 8 and self.board[ny][nx] == current_player:
            return count
        return 0

    def _execute_flip(self, x, y, dx, dy, current_player, opponent):
        """
        Executes flipping pieces in a given direction (dx, dy) from (x, y).
        Modifies the board and returns the number of pieces flipped.
        """
        flipped_count = 0
        nx, ny = x + dx, y + dy
        pieces_to_flip = []

        # Collect pieces to flip
        while 0 <= nx < 8 and 0 <= ny < 8 and self.board[ny][nx] == opponent:
            pieces_to_flip.append((nx, ny))
            nx += dx
            ny += dy

        # If we found at least one opponent's piece and then hit our own piece, flip them
        if len(pieces_to_flip) > 0 and 0 <= nx < 8 and 0 <= ny < 8 and self.board[ny][nx] == current_player:
            for fx, fy in pieces_to_flip:
                self.board[fy][fx] = current_player
                flipped_count += 1
            return flipped_count
        return 0

    def add(self, x, y):
        """
        Adds a piece at (x, y) for the current player, if the move is valid.
        Flips opponent's pieces and updates scores.
        """
        if not self.is_valid_move(x, y, self.player):
            return False  # Invalid move

        opponent = 'W' if self.player == 'B' else 'B'
        total_flipped = 0

        # Place the current player's piece
        self.board[y][x] = self.player
        self.rem -= 1

        # Execute flips in all 8 directions
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                total_flipped += self._execute_flip(x, y, dx, dy, self.player, opponent)

        # Update scores based on the placed piece and flipped pieces
        if self.player == 'B':
            self.black += (1 + total_flipped)  # 1 for the new piece, plus flipped
            self.white -= total_flipped  # Opponent loses flipped pieces
        else:  # self.player == 'W'
            self.white += (1 + total_flipped)
            self.black -= total_flipped

        # Save the state before switching player
        self.history.append(self.get_current_state())

        # Switch player
        self.player = opponent
        return True

    def get_valid_moves(self):
        """Returns a list of all valid (x, y) moves for the current player."""
        moves = []
        for y in range(8):
            for x in range(8):
                if self.is_valid_move(x, y, self.player):
                    moves.append((x, y))
        return moves

    def is_game_over(self):
        """Checks if the game is over."""
        # Game is over if no empty squares left
        if self.rem == 0:
            return True

        # Game is over if neither player can make a move
        current_player_has_moves = len(self.get_valid_moves()) > 0

        # Temporarily switch player to check if the *other* player has moves
        original_player = self.player
        self.player = 'W' if original_player == 'B' else 'B'
        other_player_has_moves = len(self.get_valid_moves()) > 0
        self.player = original_player  # Revert player back

        return not current_player_has_moves and not other_player_has_moves

    def get_winner(self):
        """Returns the winner ('B', 'W', or 'T' for Tie) or None if game not over."""
        if not self.is_game_over():
            return None  # Game not over yet

        if self.black > self.white:
            return 'B'
        elif self.white > self.black:
            return 'W'
        else:
            return 'T'  # Tie

    def undo(self):
        """Undoes the last move, restoring the previous game state."""
        if len(self.history) > 1:  # We need at least two states to undo (current + previous)
            self.history.pop()  # Remove current state
            previous_state = self.history[-1]  # Get the state before the last move
            self.set_state(previous_state)
            print("Move undone.")
            self.display_board()
            return True
        else:
            print("Cannot undo further (at initial state).")
            return False

    def score_board(self, maximizing_player):
        """
        Scores the current board state for the minimax algorithm.
        Returns (maximizing_player_score - minimizing_player_score).
        """
        if maximizing_player == 'B':
            return self.black - self.white
        else:  # maximizing_player == 'W'
            return self.white - self.black


class AI:
    def minimax(self, game_state, depth, maximizing_player, alpha, beta, is_maximizing_turn):
        """
        Minimax algorithm with Alpha-Beta Pruning to find the best move.

        Args:
            game_state: A dictionary representing the current state of the game.
            depth: The current depth in the search tree.
            maximizing_player: The player for whom we are maximizing the score ('B' or 'W').
            alpha: The alpha value for alpha-beta pruning.
            beta: The beta value for alpha-beta pruning.
            is_maximizing_turn: True if it's the maximizing player's turn, False otherwise.

        Returns:
            A tuple (score, best_move) where best_move is (x, y).
        """
        temp_game = Game()
        temp_game.set_state(game_state)

        # Base case: if depth is 0 or game is over
        if depth == 0 or temp_game.is_game_over():
            return temp_game.score_board(maximizing_player), None

        valid_moves = temp_game.get_valid_moves()

        # If no valid moves for the current player, skip turn
        if not valid_moves:
            # Switch player and recursively call minimax for the next turn
            temp_game.player = 'W' if temp_game.player == 'B' else 'B'
            return self.minimax(temp_game.get_current_state(), depth - 1, maximizing_player, alpha, beta,
                                not is_maximizing_turn)

        if is_maximizing_turn:
            max_eval = -sys.maxsize
            best_move = None
            for move in valid_moves:
                new_game = Game()
                new_game.set_state(game_state)  # Start from the current state
                new_game.add(move[0], move[1])  # Make the move (updates player, scores, etc.)

                eval_score, _ = self.minimax(new_game.get_current_state(), depth - 1, maximizing_player, alpha, beta,
                                             False)

                if eval_score > max_eval:
                    max_eval = eval_score
                    best_move = move
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break  # Beta cut-off
            return max_eval, best_move
        else:  # Minimizing turn
            min_eval = sys.maxsize
            for move in valid_moves:
                new_game = Game()
                new_game.set_state(game_state)  # Start from the current state
                new_game.add(move[0], move[1])  # Make the move

                eval_score, _ = self.minimax(new_game.get_current_state(), depth - 1, maximizing_player, alpha, beta,
                                             True)

                if eval_score < min_eval:
                    min_eval = eval_score
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break  # Alpha cut-off
            return min_eval, None  # We don't care about the minimizing player's best move here

    def computer_move(self, game, depth_limit):  # Removed default depth_limit
        """
        Determines and executes the computer's move using minimax with alpha-beta pruning.
        """
        print(f"Computer ({game.player}) is thinking with depth limit {depth_limit}...")
        current_state = game.get_current_state()

        # The computer is the maximizing player for its own turn
        score, best_move = self.minimax(current_state, depth_limit, game.player, -sys.maxsize, sys.maxsize, True)

        if best_move:
            print(f"Computer chooses move: ({best_move[0]}, {best_move[1]})")
            game.add(best_move[0], best_move[1])
        else:
            # This can happen if there are no valid moves for the computer
            print(f"Computer ({game.player}) has no valid moves. Skipping turn.")
            # Manually switch player if the computer can't move
            game.player = 'W' if game.player == 'B' else 'B'
            game.history.append(game.get_current_state())  # Save state after skipping turn


def main():
    game = Game()
    ai = AI()
    game_active = False  # Flag to indicate if a game is currently in progress

    while True:
        if not game_active:
            print("\n--- Othello Main Menu ---")
            print("1. Start a New Game")
            print("2. Quit")
            choice = input("Enter your choice: ").strip()

            if choice == '1':
                game.start()
                game_active = True
            elif choice == '2':
                print("Exiting Othello. Goodbye!")
                break
            else:
                print("Invalid choice. Please enter 1 or 2.")
        else:
            # Game is active
            if game.is_game_over():
                winner = game.get_winner()
                if winner == 'T':
                    print("\nGame Over! It's a Tie!")
                else:
                    print(f"\nGame Over! Winner: {winner}!")
                game_active = False  # End current game session
                continue  # Go back to main menu

            print("\n--- Game Menu ---")
            print("1. Make a Move (Player)")
            print("2. Let Computer Make a Move")
            print("3. Undo Last Move")
            print("4. Start a New Game")
            print("5. Quit")
            choice = input("Enter your choice: ").strip()

            if choice == '1':
                valid_moves = game.get_valid_moves()
                if not valid_moves:
                    print(f"No valid moves for {game.player}. Skipping turn.")
                    # If no valid moves, the player's turn is skipped
                    game.player = 'W' if game.player == 'B' else 'B'
                    game.history.append(game.get_current_state())  # Save state after skipping turn
                    game.display_board()
                    continue

                print(f"Valid moves for {game.player}: {valid_moves}")
                try:
                    x = int(input("Enter x-coordinate (0-7): "))
                    y = int(input("Enter y-coordinate (0-7): "))
                    if game.add(x, y):
                        print(f"Move made at ({x}, {y}).")
                        game.display_board()
                    else:
                        print("Invalid move. Please choose an empty square that flips at least one opponent's piece.")
                except ValueError:
                    print("Invalid input. Please enter numbers for coordinates.")
            elif choice == '2':
                # Prompt for depth limit for console
                while True:
                    try:
                        depth_input = input("Enter AI search depth (e.g., 4, 6, 8): ").strip()
                        depth_limit = int(depth_input)
                        if depth_limit > 0:
                            break
                        else:
                            print("Depth limit must be a positive integer.")
                    except ValueError:
                        print("Invalid input. Please enter a number for depth.")

                ai.computer_move(game, depth_limit)  # Pass the user-defined depth
                game.display_board()
            elif choice == '3':
                game.undo()
            elif choice == '4':
                game.start()
            elif choice == '5':
                print("Exiting Othello. Goodbye!")
                break
            else:
                print("Invalid choice. Please enter a number from 1 to 5.")


if __name__ == "__main__":
    main()
