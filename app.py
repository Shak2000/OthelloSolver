from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel  # Import BaseModel for request body validation
from main import Game, AI

game = Game()
ai = AI()
app = FastAPI()


# Define a Pydantic model for the move coordinates
class Move(BaseModel):
    x: int
    y: int


# Define a Pydantic model for the game state dictionary
class GameState(BaseModel):
    board: list[list[str]]
    player: str
    rem: int
    black: int
    white: int


# Define a Pydantic model for the computer move request body
class ComputerMoveRequest(BaseModel):
    # We no longer need temp_game here since the AI will operate on the global 'game' object.
    # However, if the frontend still sends it, Pydantic will ignore it if not defined here.
    # For clarity, we'll keep it if the frontend sends it, but it won't be used to set game state.
    # If the frontend only sends depth_limit, this model should be adjusted.
    temp_game: GameState  # This will map to the 'temp_game' key in the incoming JSON
    depth_limit: int = 8  # This will map to the 'depth_limit' key


@app.get("/")
async def get_ui():
    return FileResponse("index.html")


@app.get("/styles.css")
async def get_styles():
    return FileResponse("styles.css")


@app.get("/script.js")
async def get_script():
    return FileResponse("script.js")


@app.post("/start")
async def start():
    game.start()


@app.get("/get_current_state")
async def get_current_state():
    return game.get_current_state()


@app.get("/set_state")
async def set_state(state):
    game.set_state(state)


@app.get("/is_valid_move")
async def is_valid_move(x: int, y: int, current_player: str):  # Added type hints for clarity
    return game.is_valid_move(x, y, current_player)


@app.post("/add")
async def add(move: Move):  # Now expects a JSON body matching the Move model
    # Access x and y from the move object
    return game.add(move.x, move.y)


@app.get("/get_valid_moves")
async def get_valid_moves():
    return game.get_valid_moves()


@app.get("/is_game_over")
async def is_game_over():
    return game.is_game_over()


@app.get("/get_winner")
async def get_winner():
    return game.get_winner()


@app.get("/undo")
async def undo():
    return game.undo()


@app.get("/score_board")
async def score_board(maximizing_player: str):  # Added type hint
    return game.score_board(maximizing_player)


@app.get("/minimax")
async def minimax(game_state: GameState, depth: int, maximizing_player: str, alpha: int, beta: int,
                  is_maximizing_turn: bool):  # Added type hints
    # Note: Passing complex objects like game_state via GET query params can be problematic due to URL length limits.
    # For a full game, consider POST with a body for minimax if game_state gets very large.
    # Also, the minimax function in main.py already creates a temp_game from the game_state dict,
    # so we don't need to reconstruct it here before passing.
    return ai.minimax(game_state.dict(), depth, maximizing_player, alpha, beta, is_maximizing_turn)


@app.post("/computer_move")
async def computer_move(request: ComputerMoveRequest):  # Now expects the new ComputerMoveRequest model
    # The 'ai.computer_move' function in main.py expects a Game object.
    # We should operate on the global 'game' object here, as the AI's move
    # needs to modify the actual game state, not a temporary copy.

    # The 'temp_game' from the request is the current state from the frontend,
    # but the 'ai.computer_move' function in main.py is designed to modify
    # the 'game' object passed to it. So, we pass the global 'game' object.
    ai.computer_move(game, request.depth_limit)
    # The computer_move function in main.py modifies the game object directly,
    # so we don't need to return anything here. The frontend will re-render.
