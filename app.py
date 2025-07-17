from fastapi import FastAPI
from fastapi.responses import FileResponse
from main import Game, AI

game = Game()
ai = AI()
app = FastAPI()


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
async def is_valid_move(x, y, current_player):
    return game.is_valid_move(x, y, current_player)


@app.post("/add")
async def add(x, y):
    return game.add(x, y)


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
async def score_board(maximizing_player):
    return game.score_board(maximizing_player)


@app.get("/minimax")
async def minimax(game_state, depth, maximizing_player, alpha, beta, is_maximizing_turn):
    return ai.minimax(game_state, depth, maximizing_player, alpha, beta, is_maximizing_turn)


@app.post("/computer_move")
async def computer_move(temp_game, depth_limit=8):
    ai.computer_move(temp_game, depth_limit)
