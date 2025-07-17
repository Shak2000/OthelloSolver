document.addEventListener('DOMContentLoaded', () => {
    const initialMenu = document.getElementById('initial-menu');
    const gameContent = document.getElementById('game-content');
    const startGameInitialBtn = document.getElementById('start-game-initial-btn');
    const quitProgramInitialBtn = document.getElementById('quit-program-initial-btn');

    const boardContainer = document.getElementById('board-container');
    const startGameInGameBtn = document.getElementById('start-game-in-game-btn');
    // const makeMoveBtn = document.getElementById('make-move-btn'); // Removed this button
    const computerMoveBtn = document.getElementById('computer-move-btn');
    const undoMoveBtn = document.getElementById('undo-move-btn');
    const quitGameBtn = document.getElementById('quit-game-btn');
    const blackScoreDisplay = document.getElementById('black-score');
    const whiteScoreDisplay = document.getElementById('white-score');
    const currentPlayerDisplay = document.getElementById('current-player');
    const messageBox = document.getElementById('message-box');

    // let selectedCell = null; // No longer needed as clicks directly trigger moves

    // Function to display messages to the user
    function showMessage(message, type = 'info') {
        messageBox.textContent = message;
        messageBox.className = `mt-6 p-4 rounded-md text-center`;
        messageBox.classList.remove('hidden'); // Ensure it's visible

        if (type === 'error') {
            messageBox.classList.add('bg-red-100', 'border', 'border-red-300', 'text-red-800');
        } else if (type === 'success') {
            messageBox.classList.add('bg-green-100', 'border', 'border-green-300', 'text-green-800');
        } else { // info
            messageBox.classList.add('bg-blue-100', 'border', 'border-blue-300', 'text-blue-800');
        }
    }

    // Function to hide messages
    function hideMessage() {
        messageBox.classList.add('hidden');
    }

    // Function to render the board based on the game state
    async function renderBoard() {
        try {
            const response = await fetch('/get_current_state');
            const gameState = await response.json();

            boardContainer.innerHTML = ''; // Clear existing board
            gameState.board.forEach((row, y) => {
                row.forEach((cell, x) => {
                    const boardCell = document.createElement('div');
                    boardCell.classList.add('board-cell');
                    boardCell.dataset.x = x;
                    boardCell.dataset.y = y;

                    if (cell === 'B') {
                        const chip = document.createElement('div');
                        chip.classList.add('chip', 'black');
                        boardCell.appendChild(chip);
                    } else if (cell === 'W') {
                        const chip = document.createElement('div');
                        chip.classList.add('chip', 'white');
                        boardCell.appendChild(chip);
                    }

                    // Attach click listener directly to attempt a move
                    boardCell.addEventListener('click', () => handleCellClick(x, y));
                    boardContainer.appendChild(boardCell);
                });
            });

            // Update scores and current player display
            blackScoreDisplay.textContent = `Black: ${gameState.black}`;
            whiteScoreDisplay.textContent = `White: ${gameState.white}`;
            currentPlayerDisplay.textContent = `Current Player: ${gameState.player === 'B' ? 'Black' : 'White'}`;

            // Check if game is over
            const isGameOverResponse = await fetch('/is_game_over');
            const isGameOver = await isGameOverResponse.json();

            if (isGameOver) {
                const winnerResponse = await fetch('/get_winner');
                const winner = await winnerResponse.json();
                if (winner === 'T') {
                    showMessage("Game Over! It's a Tie!", 'info');
                } else {
                    showMessage(`Game Over! Winner: ${winner === 'B' ? 'Black' : 'White'}!`, 'success');
                }
                disableGameControls(true); // Disable controls when game is over
            } else {
                hideMessage();
                disableGameControls(false); // Enable controls if game is not over
            }

        } catch (error) {
            console.error('Error rendering board:', error);
            showMessage('Failed to load game state. Please try starting a new game.', 'error');
        }
    }

    // Function to handle cell clicks for player moves - now attempts the move directly
    async function handleCellClick(x, y) {
        try {
            const response = await fetch('/add', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ x: x, y: y }) // Send x, y directly
            });
            const result = await response.json();
            if (result) {
                showMessage(`Move made at (${x}, ${y}).`, 'success');
                renderBoard(); // Re-render board after successful move
            } else {
                showMessage('Invalid move. Please choose an empty square that flips at least one opponent\'s piece.', 'error');
            }
        } catch (error) {
            console.error('Error making move:', error);
            showMessage('Failed to make move. Please ensure coordinates are valid and server is running.', 'error');
        }
    }

    // Function to disable/enable game controls
    function disableGameControls(disable) {
        // makeMoveBtn.disabled = disable; // Removed
        computerMoveBtn.disabled = disable;
        undoMoveBtn.disabled = disable;
    }

    // Function to show/hide sections
    function showInitialMenu() {
        initialMenu.classList.remove('hidden');
        gameContent.classList.add('hidden');
    }

    function showGameContent() {
        initialMenu.classList.add('hidden');
        gameContent.classList.remove('hidden');
    }

    // Event Listeners for buttons
    startGameInitialBtn.addEventListener('click', async () => {
        try {
            await fetch('/start', { method: 'POST' });
            showMessage('New game started!', 'success');
            showGameContent(); // Show game content
            renderBoard();
        } catch (error) {
            console.error('Error starting game:', error);
            showMessage('Failed to start a new game.', 'error');
        }
    });

    quitProgramInitialBtn.addEventListener('click', () => {
        showMessage('Exiting Othello. Goodbye!', 'info');
        // In a real application, you might redirect or close the tab
        // For this example, we'll just show the message and keep the initial menu visible.
    });

    startGameInGameBtn.addEventListener('click', async () => {
        try {
            await fetch('/start', { method: 'POST' });
            showMessage('New game started!', 'success');
            renderBoard();
        } catch (error) {
            console.error('Error starting game:', error);
            showMessage('Failed to start a new game.', 'error');
        }
    });

    // makeMoveBtn.addEventListener('click', async () => { /* This listener is now removed */ });

    computerMoveBtn.addEventListener('click', async () => {
        showMessage('Computer is thinking...', 'info');
        try {
            // Fetch current game state to pass to computer_move
            const currentStateResponse = await fetch('/get_current_state');
            const currentState = await currentStateResponse.json();

            await fetch('/computer_move', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ temp_game: currentState, depth_limit: 4 }) // Pass current state and depth
            });
            showMessage('Computer made a move!', 'success');
            renderBoard();
        } catch (error) {
            console.error('Error with computer move:', error);
            showMessage('Computer failed to make a move.', 'error');
        }
    });

    undoMoveBtn.addEventListener('click', async () => {
        try {
            const response = await fetch('/undo');
            const result = await response.json();
            if (result) {
                showMessage('Move undone.', 'info');
                renderBoard();
            } else {
                showMessage('Cannot undo further (at initial state).', 'info');
            }
        } catch (error) {
            console.error('Error undoing move:', error);
            showMessage('Failed to undo move.', 'error');
        }
    });

    quitGameBtn.addEventListener('click', () => {
        showMessage('Game ended. Returning to main menu.', 'info');
        showInitialMenu(); // Show initial menu
        // Clear board and scores when quitting from in-game
        boardContainer.innerHTML = '';
        blackScoreDisplay.textContent = 'Black: 0';
        whiteScoreDisplay.textContent = 'White: 0';
        currentPlayerDisplay.textContent = 'Current Player: None';
        disableGameControls(true);
    });

    // Initial state: show only the initial menu
    showInitialMenu();
});
