from defaults import starting_locations, Characters, Weapons, Rooms
import random
from player import Player
import json

class GameState:
    def __init__(self, custom_names=None):
        self._game_started: bool = False
        self._current_player: int = 0
        self._disprover: int = -1
        self._is_over: bool = False
        self._available_characters = {c for c in Characters}
        
        # Store custom names if provided
        self._custom_names = custom_names or {
            'characters': {c: c.value for c in Characters},
            'weapons': {w: w.value for w in Weapons},
            'rooms': {r: r.value for r in Rooms}
        }

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

    def get_custom_name(self, item):
        """Get the custom name for a character, weapon, or room"""
        if isinstance(item, Characters):
            return self._custom_names['characters'].get(item, item.value)
        elif isinstance(item, Weapons):
            return self._custom_names['weapons'].get(item, item.value)
        elif isinstance(item, Rooms):
            return self._custom_names['rooms'].get(item, item.value)
        return item.value

    def to_dict(self) -> dict:
        return {
            "game_started": self.game_started,
            "current_player": self.current_player,
            "disprover": self.disprover,
            "is_over": self.is_over,
            "available_characters": [self.get_custom_name(c) for c in self.available_characters],
            "solution": {
                "character": self.get_custom_name(self.solution[0]),
                "weapon": self.get_custom_name(self.solution[1]),
                "room": self.get_custom_name(self.solution[2]),
            } if self.solution else None,
            "cards": [self.get_custom_name(card) for card in self.cards],
            "players": {
                player_id: {
                    "character": self.get_custom_name(player.character),
                    "cards": [self.get_custom_name(card) for card in player.cards],
                    "position": player.position,
                }
                for player_id, player in self.players.items()
            },
            "positions": {self.get_custom_name(character): pos for character, pos in self.positions.items()},
            "suggestion": {
                "character": self.get_custom_name(self.suggestion[0]),
                "weapon": self.get_custom_name(self.suggestion[1]),
                "room": self.get_custom_name(self.suggestion[2]),
            } if self.suggestion else None,
        }

    @classmethod
    def from_dict(cls, data: dict, custom_names=None):
        game_state = cls(custom_names)
        game_state.game_started = data["game_started"]
        game_state.current_player = data["current_player"]
        game_state.disprover = data["disprover"]
        game_state.is_over = data["is_over"]
        
        # Convert custom names back to enums
        def get_enum_from_custom_name(custom_name, enum_class):
            if custom_names:
                for enum_value in enum_class:
                    if custom_names[enum_class.__name__.lower()].get(enum_value, enum_value.value) == custom_name:
                        return enum_value
            return enum_class(custom_name)
        
        game_state.available_characters = {
            get_enum_from_custom_name(char, Characters) for char in data["available_characters"]
        }
        
        if data["solution"]:
            game_state.solution = (
                get_enum_from_custom_name(data["solution"]["character"], Characters),
                get_enum_from_custom_name(data["solution"]["weapon"], Weapons),
                get_enum_from_custom_name(data["solution"]["room"], Rooms),
            )
        
        game_state.cards = [
            get_enum_from_custom_name(card, Characters) if card in [c.value for c in Characters] else
            get_enum_from_custom_name(card, Weapons) if card in [w.value for w in Weapons] else
            get_enum_from_custom_name(card, Rooms) for card in data["cards"]
        ]
        
        game_state.players = {
            int(player_id): Player(
                int(player_id),
                get_enum_from_custom_name(player_data["character"], Characters),
                position=tuple(player_data["position"]),
                cards={
                    get_enum_from_custom_name(card, Characters) if card in [c.value for c in Characters] else
                    get_enum_from_custom_name(card, Weapons) if card in [w.value for w in Weapons] else
                    get_enum_from_custom_name(card, Rooms) for card in player_data["cards"]
                }
            )
            for player_id, player_data in data["players"].items()
        }
        
        game_state.positions = {
            get_enum_from_custom_name(char, Characters): tuple(pos) for char, pos in data["positions"].items()
        }
        
        if data.get("suggestion"):
            game_state.suggestion = (
                get_enum_from_custom_name(data["suggestion"]["character"], Characters),
                get_enum_from_custom_name(data["suggestion"]["weapon"], Weapons),
                get_enum_from_custom_name(data["suggestion"]["room"], Rooms),
            )
        
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
