from defaults import starting_locations, Characters, Weapons, Rooms
import random
from player import Player
import json

class GameState:
    def __init__(self):
        self._game_started: bool = False
        self._current_player: int = 0
        self._disprover: int = -1
        self._is_over: bool = False
        self._available_characters = {c for c in Characters}

        # Positions of characters on the game board
        # Initialize _positions with starting locations from defaults
        self._positions: dict[Characters, tuple[int, int]] = {
            character: starting_locations[character] for character in Characters
        }

        # Build solution:
        characters = list(Characters)
        weapons = list(Weapons)
        rooms = list(Rooms)
        solution_character = random.choice(characters)
        characters.remove(solution_character)
        solution_weapon = random.choice(weapons)
        weapons.remove(solution_weapon)
        solution_room = random.choice(rooms)
        rooms.remove(solution_room)
        self._solution = (solution_character, solution_weapon, solution_room)

        # The remainder becomes the deck of cards:
        self._cards = characters + weapons + rooms

        # Dictionary to map user_id to Player instances:
        self._players: dict[int, Player] = dict()

        # Initialize suggestion
        self._suggestion: tuple[Characters, Weapons, Rooms] = None  

    # Getters and setters for game_started
    @property
    def game_started(self) -> bool:
        return self._game_started

    @game_started.setter
    def game_started(self, value: bool):
        self._game_started = value

    # Getters and setters for current_player
    @property
    def current_player(self) -> int:
        return self._current_player

    @current_player.setter
    def current_player(self, value: int):
        self._current_player = value

    # Getters and setters for disprover
    @property
    def disprover(self) -> int:
        return self._disprover

    @disprover.setter
    def disprover(self, value: int):
        self._disprover = value

    # Getters and setters for is_over
    @property
    def is_over(self) -> bool:
        return self._is_over

    @is_over.setter
    def is_over(self, value: bool):
        self._is_over = value

    # Getters and setters for available_characters
    @property
    def available_characters(self):
        return self._available_characters

    @available_characters.setter
    def available_characters(self, value):
        self._available_characters = value

    # Getters and setters for solution
    @property
    def solution(self):
        return self._solution

    @solution.setter
    def solution(self, value: tuple):
        self._solution = value

    # Getters and setters for cards
    @property
    def cards(self):
        return self._cards

    @cards.setter
    def cards(self, value: list):
        self._cards = value

    # Getters and setters for players
    @property
    def players(self) -> dict[int, Player]:
        return self._players

    @players.setter
    def players(self, value: dict[int, Player]):
        self._players = value

    # Getters and setters for suggestion
    @property
    def suggestion(self) -> tuple[Characters, Weapons, Rooms]:
        return self._suggestion

    @suggestion.setter
    def suggestion(self, value: tuple[Characters, Weapons, Rooms] | None):
        if value is not None:
            if not isinstance(value, tuple) or len(value) != 3:
                raise ValueError("Suggestion must be a tuple of (Characters, Weapons, Rooms) or None.")
            if not isinstance(value[0], Characters) or not isinstance(value[1], Weapons) or not isinstance(value[2], Rooms):
                raise ValueError("Suggestion must contain valid Characters, Weapons, and Rooms.")
        self._suggestion = value

    # Getters and setters for positions
    @property
    def positions(self) -> dict[Characters, tuple[int, int]]:
        """Returns the current positions of all characters."""
        return self._positions
    
    @positions.setter
    def positions(self, new_positions: dict[Characters, tuple[int, int]]):
        if not isinstance(new_positions, dict):
            raise ValueError("Positions must be a dictionary with Characters as keys and tuples of (int, int) as values.")
        for character, position in new_positions.items():
            if not isinstance(character, Characters):
                raise ValueError(f"Invalid key in positions dictionary: {character}. Must be a valid Character.")
            if not isinstance(position, tuple) or len(position) != 2 or not all(isinstance(x, int) for x in position):
                raise ValueError(f"Invalid position for {character}: {position}. Must be a tuple of two integers.")
        self._positions = new_positions

    def update_position(self, character: Characters, position: tuple[int, int]):
        if character not in self._positions:
            raise ValueError(f"Character {character} is not valid.")
        if not isinstance(position, tuple) or len(position) != 2 or not all(isinstance(x, int) for x in position):
            raise ValueError(f"Position must be a tuple of two integers, got {position}.")
        self._positions[character] = position
        print(f"[DEBUG] Updated position of {character} to {position}")

    def to_dict(self) -> dict:
        return {
            "game_started": self.game_started,
            "current_player": self.current_player,
            "disprover": self.disprover,
            "is_over": self.is_over,
            "available_characters": list(self.available_characters),
            "solution": {
                "character": self.solution[0],
                "weapon": self.solution[1],
                "room": self.solution[2],
            } if self.solution else None,
            "cards": [card for card in self.cards],
            "players": {
                player_id: {
                    "character": player.character,
                    "cards": [card for card in player.cards],
                    "position": player.position,
                }
                for player_id, player in self.players.items()
            },
            "positions": {character.value: pos for character, pos in self.positions.items()},
            "suggestion": {
                "character": self.suggestion[0],
                "weapon": self.suggestion[1],
                "room": self.suggestion[2],
            } if self.suggestion else None,
        }

    @classmethod
    def from_dict(cls, data: dict):
        game_state = cls()
        game_state.game_started = data["game_started"]
        game_state.current_player = data["current_player"]
        game_state.disprover = data["disprover"]
        game_state.is_over = data["is_over"]
        game_state.available_characters = {Characters(char) for char in data["available_characters"]}
        game_state.solution = (
            Characters(data["solution"]["character"]),
            Weapons(data["solution"]["weapon"]),
            Rooms(data["solution"]["room"]),
        )
        game_state.cards = [Characters(c) if c in Characters._member_map_.values() else
                            Weapons(c) if c in Weapons._member_map_.values() else
                            Rooms(c) for c in data["cards"]]
        game_state.players = {
            int(player_id): Player(
                int(player_id),
                Characters(player_data["character"]),
                position=tuple(player_data["position"]),
                cards={Characters(c) if c in Characters._member_map_.values() else
                    Weapons(c) if c in Weapons._member_map_.values() else
                    Rooms(c) for c in player_data["cards"]}
            )
            for player_id, player_data in data["players"].items()
        }
        game_state.positions = {
            Characters(char): tuple(pos) for char, pos in data["positions"].items()
        }
        game_state.suggestion = (
            Characters(data["suggestion"]["character"]),
            Weapons(data["suggestion"]["weapon"]),
            Rooms(data["suggestion"]["room"]),
        ) if data.get("suggestion") else None
        return game_state
    
    def to_file(self, file_path: str):
        try:
            with open(file_path, 'w') as file:
                json.dump(self.to_dict(), file, indent=1)
            print(f"Game state successfully saved to {file_path}.")
        except Exception as e:
            print(f"An error occurred while saving the game state to {file_path}: {e}")

    @classmethod
    def from_file(cls, file_path: str):
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
            print(f"Game state successfully loaded from {file_path}.")
            return cls.from_dict(data)
        except Exception as e:
            print(f"An error occurred while loading the game state from {file_path}: {e}")
            return None
