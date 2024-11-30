import pickle

class GameState:
    def __init__(self, party=None, matrix=None, area="", spawn=None, scroll=None):
        self.area = area  # Current game area
        self.party = party if party else []
        self.matrix = matrix
        self.area = area
        self.spawn = spawn
        self.scroll = scroll

# Save function
def save_game(state, filename="savegame.pkl"):
    try:
        with open(filename, "wb") as file:
            pickle.dump(state, file)
        print("Game saved successfully!")
    except Exception as e:
        print(f"Failed to save game: {e}")

# Load function
def load_game(filename="savegame.pkl"):
    try:
        with open(filename, "rb") as file:
            state = pickle.load(file)
        print("Game loaded successfully!")
        return state
    except FileNotFoundError:
        print("Save file not found!")
    except Exception as e:
        print(f"Failed to load game: {e}")
    return None