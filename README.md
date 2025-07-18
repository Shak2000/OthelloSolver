# Othello Game

A web-based implementation of the classic Othello (Reversi) board game with AI opponent using minimax algorithm with alpha-beta pruning.

## Features

- **Interactive Web Interface**: Clean, modern UI built with HTML, CSS, and JavaScript
- **Smart AI Opponent**: Minimax algorithm with alpha-beta pruning for challenging gameplay
- **Adjustable AI Difficulty**: Configure AI search depth from 1 to any desired level
- **Game Management**: Start new games, undo moves, and track scores
- **Real-time Updates**: Live board state updates and move validation
- **Responsive Design**: Works on desktop and mobile devices

## Game Rules

Othello is played on an 8×8 board with black and white pieces. Players take turns placing pieces on the board:

1. **Objective**: Have the most pieces of your color when the board is full or no moves are possible
2. **Valid Moves**: You can only place a piece where it will flip at least one opponent's piece
3. **Flipping**: When you place a piece, all opponent pieces in straight lines (horizontal, vertical, diagonal) between your new piece and another of your pieces are flipped to your color
4. **Turn Skipping**: If you have no valid moves, your turn is skipped
5. **Game End**: The game ends when the board is full or neither player can make a move

## Installation & Setup

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Clone or download the project files**
   ```bash
   git clone <repository-url>
   cd othello-game
   ```

2. **Install required dependencies**
   ```bash
   pip install fastapi uvicorn
   ```

3. **Start the web server**
   ```bash
   uvicorn app:app --reload
   ```

4. **Open your browser** and navigate to:
   ```
   http://localhost:8000
   ```

## File Structure

```
othello-game/
├── app.py          # FastAPI web server and API endpoints
├── main.py         # Core game logic and AI implementation
├── index.html      # Main web interface
├── styles.css      # Custom styling for the game board
├── script.js       # Frontend JavaScript for game interaction
└── README.md       # This file
```

## How to Play

### Web Interface

1. **Starting a Game**: Click "Start New Game" from the main menu
2. **Making Moves**: Click on any valid square on the board to place your piece
3. **Computer Moves**: Click "Computer Move" to let the AI make its move
4. **Adjusting AI Difficulty**: Use the "AI Depth" input to set the search depth (higher = stronger but slower)
5. **Undo Moves**: Click "Undo Move" to revert the last move
6. **Game Controls**: Use the control buttons to start new games or quit

### Console Interface

You can also run the game directly in the console:

```bash
python main.py
```

This provides a text-based interface with the same game features.

## AI Implementation

The AI uses the **minimax algorithm with alpha-beta pruning** to determine the best moves:

- **Evaluation Function**: Difference in piece count between maximizing and minimizing players
- **Search Depth**: Configurable depth limit (default: 4-8 moves ahead)
- **Optimization**: Alpha-beta pruning reduces the search space for faster computation
- **Strategy**: The AI considers all possible moves and their consequences to the specified depth

### AI Difficulty Levels

- **Depth 1-2**: Beginner (very fast, basic strategy)
- **Depth 3-4**: Intermediate (good balance of speed and strategy)
- **Depth 5-6**: Advanced (strong play, moderate computation time)
- **Depth 7+**: Expert (very strong play, longer computation time)

## API Endpoints

The FastAPI backend provides the following endpoints:

- `GET /` - Serve the main web interface
- `POST /start` - Start a new game
- `GET /get_current_state` - Get the current game state
- `POST /add` - Make a player move
- `POST /computer_move` - Execute AI move
- `GET /undo` - Undo the last move
- `GET /is_game_over` - Check if the game is finished
- `GET /get_winner` - Get the game winner
- `GET /get_valid_moves` - Get all valid moves for current player

## Technical Details

### Game Class

The `Game` class manages:
- Board state (8×8 grid)
- Player turns and scoring
- Move validation and execution
- Game history for undo functionality
- Win condition checking

### AI Class

The `AI` class implements:
- Minimax algorithm with alpha-beta pruning
- Position evaluation
- Move selection and execution
- Configurable search depth

### Frontend

The web interface uses:
- **HTML5** for structure
- **Tailwind CSS** for styling
- **Vanilla JavaScript** for interactivity
- **Fetch API** for server communication

## Development

### Running in Development Mode

```bash
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

### Customizing the AI

You can modify the AI behavior by:

1. **Changing the evaluation function** in `Game.score_board()`
2. **Adjusting the search depth** in the web interface or console
3. **Implementing additional pruning techniques** in the minimax algorithm

### Adding Features

The modular design makes it easy to add features like:
- Different AI difficulty presets
- Game statistics tracking
- Tournament mode
- Custom board sizes
- Advanced evaluation functions

## Performance

- **Typical response times**: 
  - Depth 4: < 1 second
  - Depth 6: 1-5 seconds
  - Depth 8: 5-30 seconds
- **Memory usage**: Minimal (< 50MB)
- **Browser compatibility**: Modern browsers with JavaScript enabled

## Troubleshooting

### Common Issues

1. **Server won't start**: Ensure FastAPI and uvicorn are installed
2. **Slow AI moves**: Reduce the AI depth setting
3. **Interface not loading**: Check that you're accessing `http://localhost:8000`
4. **Move validation errors**: Ensure you're clicking on valid squares (green highlights)

### Debug Mode

Run with debug logging:
```bash
uvicorn app:app --reload --log-level debug
```

## License

This project is open source and available under the MIT License.

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

## Credits

- Classic Othello game rules
- Minimax algorithm implementation
- Web interface design with Tailwind CSS
