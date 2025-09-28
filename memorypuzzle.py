import random
import time
import os

# Constants
GRID_SIZE = 4  # 4x4 grid = 16 cards = 8 pairs
TIME_LIMIT = 60  # seconds

# Symbols to match (can be emojis or letters)
SYMBOLS = ['😀', '🐶', '🍎', '🚗', '🌟', '🎵', '🏀', '💡']

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def create_board():
    cards = SYMBOLS * 2  # 8 pairs
    random.shuffle(cards)
    board = [cards[i:i+GRID_SIZE] for i in range(0, len(cards), GRID_SIZE)]
    return board

def create_mask():
    return [['*' for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

def display_board(masked_board):
    print("\n    " + "  ".join(str(i) for i in range(GRID_SIZE)))
    print("   " + "---" * GRID_SIZE)
    for idx, row in enumerate(masked_board):
        print(f"{idx} | " + "  ".join(row))
    print()

def get_coordinates(prompt):
    while True:
        try:
            coords = input(prompt).split(',')
            if len(coords) != 2:
                raise ValueError
            row, col = int(coords[0]), int(coords[1])
            if 0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE:
                return row, col
            else:
                raise ValueError
        except ValueError:
            print("Invalid input. Use format 'row,col' (e.g., 1,2) within grid limits.")

def memory_game():
    board = create_board()
    masked = create_mask()
    matched = [[False]*GRID_SIZE for _ in range(GRID_SIZE)]
    start_time = time.time()
    pairs_found = 0
    total_pairs = len(SYMBOLS)

    while pairs_found < total_pairs:
        clear_console()
        elapsed = int(time.time() - start_time)
        remaining = TIME_LIMIT - elapsed

        if remaining <= 0:
            print("⏰ Time's up! Game Over.")
            print("Final board:")
            display_board(board)
            return

        print(f"🧠 Memory Puzzle - Match the pairs! Time left: {remaining}s")
        display_board(masked)

        # First card
        r1, c1 = get_coordinates("Enter coordinates for first card (row,col): ")
        if matched[r1][c1]:
            print("Card already matched. Choose a different one.")
            time.sleep(1)
            continue

        masked[r1][c1] = board[r1][c1]
        clear_console()
        display_board(masked)

        # Second card
        r2, c2 = get_coordinates("Enter coordinates for second card (row,col): ")
        if (r1 == r2 and c1 == c2) or matched[r2][c2]:
            print("Invalid selection. Choose a different second card.")
            masked[r1][c1] = '*'
            time.sleep(1)
            continue

        masked[r2][c2] = board[r2][c2]
        clear_console()
        display_board(masked)

        # Check match
        if board[r1][c1] == board[r2][c2]:
            print("✅ It's a match!")
            matched[r1][c1] = matched[r2][c2] = True
            pairs_found += 1
        else:
            print("❌ Not a match.")
            time.sleep(1.5)
            masked[r1][c1] = masked[r2][c2] = '*'

        time.sleep(0.5)

    print("🎉 Congratulations! You matched all pairs in time!")

if __name__ == "__main__":
    memory_game()
