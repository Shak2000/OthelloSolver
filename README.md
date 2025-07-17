# Othello Game with AI

A full-featured Othello (Reversi) game implementation with both web interface and command-line interface, featuring an AI opponent powered by minimax algorithm with alpha-beta pruning.

## Features

- **Dual Interface**: Play via web browser or command line
- **AI Opponent**: Intelligent computer player using minimax with alpha-beta pruning
- **Game Management**: Start new games, undo moves, and track scores
- **Real-time Updates**: Dynamic board rendering and game state updates
- **Responsive Design**: Mobile-friendly web interface
- **Move Validation**: Automatic validation of legal moves according to Othello rules

## Technologies Used

- **Backend**: Python with FastAPI
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Styling**: Tailwind CSS
- **AI Algorithm**: Minimax with Alpha-Beta Pruning
- **Font**: Inter (Google Fonts)

## Installation

### Prerequisites

- Python 3.7+
- pip (Python package manager)

### Setup

1. **Clone or download the project files**
   ```bash
   # Ensure you have these files in your project directory:
   # - main.py
   # - app.py
   # - index.html
   # - styles.css
   # - script.js
   ```

2. **Install dependencies**
   ```bash
   pip install fastapi uvicorn pydantic
   ```

3. **Run the application**
   ```bash
   # For web interface
   uvicorn app:app --reload --host 0.0.0.0 --port 8000
   
   # For command-line interface
   python main.py
   ```

## Usage

### Web Interface

1. **Start the server**:
   ```bash
   uvicorn app:app --reload --host 0.0.0.0 --port 8000
   ```

2. **Open your browser** and navigate to `http://localhost:8000`

3. **Game Controls**:
   - Click "Start New Game" to begin
   - Click on board squares to make moves
   - Use "Computer Move" to let the AI play
   - "Undo Move" to take back the last move
   - "Start New Game" to reset the board
   - "Quit Game" to return to main menu

### Command Line Interface

1. **Run the game**:
   ```bash
   python main.py
   ```

2. **Main Menu Options**:
   - `1` - Start a New Game
   - `2` - Quit

3. **In-Game Options**:
   - `1` - Make a Move (Player)
   - `2` - Let Computer Make a Move
   - `3` - Undo Last Move
   - `4` - Start a New Game
   - `5` - Quit

## Game Rules

Othello is played on an 8×8 board with black and white discs.

### Objective
Have the majority of your colored discs on the board when the game ends.

### Rules
1. **Starting Position**: The game begins with 4 discs in the center (2 black, 2 white)
2. **Turn Order**: Black always moves first
3. **Valid Moves**: A move must be placed on an empty square that "flanks" one or more opponent discs
4. **Flanking**: A disc flanks opponent discs when it's placed such that one or more opponent discs are trapped between the new disc and an existing disc of the same color
5. **Flipping**: All flanked opponent discs are flipped to your color
6. **Passing**: If no valid moves are available, the turn passes to the opponent
7. **Game End**: The game ends when the board is full or neither player can make a valid move

## AI Algorithm

The computer opponent uses a **Minimax algorithm with Alpha-Beta Pruning**:

- **Depth**: Configurable search depth (default: 8 levels)
- **Evaluation**: Board position scoring based on disc count differential
- **Optimization**: Alpha-beta pruning for improved performance
- **Strategy**: Maximizes computer's advantage while minimizing player's advantage

### AI Difficulty
You can adjust the AI difficulty by modifying the `depth_limit` parameter in the computer move function. Higher values make the AI stronger but slower.

## Project Structure

```
othello-game/
├── main.py          # Core game logic and command-line interface
├── app.py           # FastAPI web server and API endpoints
├── index.html       # Web interface HTML
├── styles.css       # Custom CSS styles
├── script.js        # Frontend JavaScript logic
└── README.md        # This file
```

## API Endpoints

The web interface communicates with the backend through these REST API endpoints:

### Game Management
- `POST /start` - Start a new game
- `GET /get_current_state` - Get current game state
- `GET /is_game_over` - Check if game is finished
- `GET /get_winner` - Get game winner

### Move Operations
- `POST /add` - Make a player move
- `POST /computer_move` - Trigger AI move
- `GET /undo` - Undo last move
- `GET /get_valid_moves` - Get valid moves for current player

### Validation
- `GET /is_valid_move` - Check if a move is valid
- `GET /score_board` - Get current board evaluation

## Customization

### Styling
- Modify `styles.css` for custom board and piece appearance
- Update Tailwind classes in `index.html` for UI changes
- Adjust colors, fonts, and animations as desired

### AI Behavior
- Change `depth_limit` in `computer_move` function to adjust AI strength
- Modify `score_board` method in `Game` class for different evaluation strategies
- Implement additional heuristics for more sophisticated AI play

### Game Rules
- Adjust board size by modifying the grid dimensions in `Game.start()`
- Implement different starting positions
- Add time limits or move counters

## Troubleshooting

### Common Issues

1. **Server won't start**:
   - Check if port 8000 is already in use
   - Ensure FastAPI and uvicorn are installed
   - Try a different port: `uvicorn app:app --port 8080`

2. **Web interface not loading**:
   - Verify the server is running
   - Check browser console for JavaScript errors
   - Ensure all files are in the same directory

3. **AI moves slowly**:
   - Reduce the `depth_limit` parameter
   - The default depth of 8 provides good gameplay balance

4. **Invalid moves not being caught**:
   - Ensure the move validation logic is working
   - Check that the board state is being updated correctly

## Contributing

Feel free to enhance this Othello implementation:

- Add more sophisticated AI evaluation functions
- Implement different AI difficulty levels
- Add sound effects and animations
- Create multiplayer support
- Add game statistics and move history

## License

This project is open source and available under the MIT License.

---

Enjoy playing Othello! 🎮
