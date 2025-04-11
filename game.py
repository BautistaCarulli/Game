import tkinter as tk
from tkinter import messagebox
import random
import math

# Initialize the board and scores
def initialize_board():
    return [" " for _ in range(9)]  # A 3x3 board represented as a list

player_score = 0
ai_score = 0
draws = 0
player_name = "Player"
difficulty = "Easy"

# Check for a winner
def check_winner(board):
    winning_combinations = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
        [0, 4, 8], [2, 4, 6]              # Diagonals
    ]
    for combo in winning_combinations:
        if board[combo[0]] == board[combo[1]] == board[combo[2]] and board[combo[0]] != " ":
            return board[combo[0]]
    return None

# Check if the board is full
def is_full(board):
    return " " not in board

# Minimax algorithm for AI (Hard difficulty)
def minimax(board, depth, is_maximizing):
    winner = check_winner(board)
    if winner == "O":  # AI wins
        return 1
    elif winner == "X":  # Player wins
        return -1
    elif is_full(board):  # Draw
        return 0

    if is_maximizing:
        best_score = -math.inf
        for i in range(9):
            if board[i] == " ":
                board[i] = "O"
                score = minimax(board, depth + 1, False)
                board[i] = " "
                best_score = max(best_score, score)
        return best_score
    else:
        best_score = math.inf
        for i in range(9):
            if board[i] == " ":
                board[i] = "X"
                score = minimax(board, depth + 1, True)
                board[i] = " "
                best_score = min(best_score, score)
        return best_score

# AI move
def ai_move(board):
    if difficulty == "Easy":
        # Random move for Easy difficulty
        available_moves = [i for i in range(9) if board[i] == " "]
        return random.choice(available_moves)
    else:
        # Minimax move for Hard difficulty
        best_score = -math.inf
        best_move = None
        for i in range(9):
            if board[i] == " ":
                board[i] = "O"
                score = minimax(board, 0, False)
                board[i] = " "
                if score > best_score:
                    best_score = score
                    best_move = i
        return best_move

# Handle button click
def handle_click(index):
    global board, buttons, player_score, ai_score, draws

    if board[index] == " ":
        # Player move
        board[index] = "😎"
        buttons[index].config(text="😎", state="disabled", disabledforeground="white", bg="black")

        # Check for a winner or draw
        winner = check_winner(board)
        if winner:
            player_score += 1
            update_scoreboard()
            messagebox.showinfo("Game Over", f"{player_name} wins!")
            reset_game()
            return
        if is_full(board):
            draws += 1
            update_scoreboard()
            messagebox.showinfo("Game Over", "It's a draw!")
            reset_game()
            return

        # AI move
        ai_index = ai_move(board)
        board[ai_index] = "🤖"
        buttons[ai_index].config(text="🤖", state="disabled", disabledforeground="black", bg="gray")

        # Check for a winner or draw
        winner = check_winner(board)
        if winner:
            ai_score += 1
            update_scoreboard()
            messagebox.showinfo("Game Over", "AI wins!")
            reset_game()
            return
        if is_full(board):
            draws += 1
            update_scoreboard()
            messagebox.showinfo("Game Over", "It's a draw!")
            reset_game()
            return

# Reset the game
def reset_game():
    global board, buttons
    board = initialize_board()
    for button in buttons:
        button.config(text=" ", state="normal", bg="white")

# Update the scoreboard
def update_scoreboard():
    global scoreboard_label
    scoreboard_label.config(text=f"{player_name}: {player_score}  |  AI: {ai_score}  |  Draws: {draws}")

# Restart the game and return to the main screen
def restart_game():
    global game_window
    game_window.destroy()
    main_screen()

# Start the game
def start_game():
    global player_name, difficulty
    player_name = player_name_entry.get() or "Player"
    difficulty = difficulty_var.get()
    root.destroy()
    tic_tac_toe_gui()

# Main GUI setup
def tic_tac_toe_gui():
    global board, buttons, scoreboard_label, game_window
    board = initialize_board()

    # Create the main window
    game_window = tk.Tk()
    game_window.title("Tic-Tac-Toe")
    game_window.configure(bg="black")

    # Create the scoreboard
    scoreboard_label = tk.Label(game_window, text=f"{player_name}: 0  |  AI: 0  |  Draws: 0", font=("Arial", 16), bg="black", fg="white")
    scoreboard_label.pack(pady=10)

    # Create buttons for the board
    buttons_frame = tk.Frame(game_window, bg="black")
    buttons_frame.pack()
    buttons = []
    for i in range(9):
        button = tk.Button(buttons_frame, text=" ", font=("Arial", 36), height=2, width=5,
                           bg="white", fg="black", relief="solid", borderwidth=2,
                           command=lambda i=i: handle_click(i))
        button.grid(row=i // 3, column=i % 3, padx=5, pady=5)
        buttons.append(button)

    # Add Restart Button
    restart_button = tk.Button(game_window, text="Restart", font=("Arial", 14), bg="white", fg="black", command=restart_game)
    restart_button.pack(pady=20)

    # Start the GUI event loop
    game_window.mainloop()

# Welcome screen
def main_screen():
    global root, player_name_entry, difficulty_var
    root = tk.Tk()
    root.title("BautistaGame")
    root.configure(bg="black")

    welcome_label = tk.Label(root, text="Welcome to BautistaGame!", font=("Arial", 20), bg="black", fg="white")
    welcome_label.pack(pady=10)

    player_name_label = tk.Label(root, text="Enter your name:", font=("Arial", 14), bg="black", fg="white")
    player_name_label.pack(pady=5)

    player_name_entry = tk.Entry(root, font=("Arial", 14))
    player_name_entry.pack(pady=5)

    difficulty_label = tk.Label(root, text="Select difficulty:", font=("Arial", 14), bg="black", fg="white")
    difficulty_label.pack(pady=5)

    difficulty_var = tk.StringVar(value="Easy")
    easy_button = tk.Radiobutton(root, text="Easy", variable=difficulty_var, value="Easy", font=("Arial", 12), bg="black", fg="white", selectcolor="black")
    easy_button.pack()

    hard_button = tk.Radiobutton(root, text="Hard", variable=difficulty_var, value="Hard", font=("Arial", 12), bg="black", fg="white", selectcolor="black")
    hard_button.pack()

    start_button = tk.Button(root, text="Start Game", font=("Arial", 14), bg="white", fg="black", command=start_game)
    start_button.pack(pady=20)

    root.mainloop()

# Start the main screen
main_screen()