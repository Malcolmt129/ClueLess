from abc import ABC, abstractmethod
from dataclasses import dataclass
from defaults import Characters, Weapons, Rooms
from enum import Enum
from typing import Union, List
import json


class MessageTypes(str, Enum):
    MOVE = 'move'
    ACCUSATION = 'accusation'
    SUGGESTION = 'suggestion'
    DISPROVE = 'disprove'
    ERROR = 'error'
    END_TURN = 'end_turn'
    UPDATE = 'update'
    WELCOME = 'welcome'
    JOIN = 'join'


@dataclass
class AbstractMessage(ABC):
    user_id: int

    def to_json_str(self) -> str:
        return json.dumps(self.__dict__)

    def __post_init__(self):
        if not isinstance(self.user_id, int) or self.user_id < 0:
            raise ValueError("user_id must be a non-negative integer.")


@dataclass
class MoveMessage(AbstractMessage):
    coordinates: tuple[int, int]
    type: MessageTypes = MessageTypes.MOVE

    def __post_init__(self):
        super().__post_init__()
        # Convert lists to tuples for JSON reasons
        if isinstance(self.coordinates, list) and len(self.coordinates) == 2:
            self.coordinates = tuple(self.coordinates)
        if not (isinstance(self.coordinates, tuple) and len(self.coordinates) == 2 and all(isinstance(coord, int) for coord in self.coordinates)):
            raise ValueError("coordinates must be a tuple of two integers.")


@dataclass
class AccusationMessage(AbstractMessage):
    character: Characters
    weapon: Weapons
    room: Rooms
    type: MessageTypes = MessageTypes.ACCUSATION

    def __post_init__(self):
        super().__post_init__()
        if not isinstance(self.character, Characters):
            raise ValueError("character must be an instance of Characters enum.")
        if not isinstance(self.weapon, Weapons):
            raise ValueError("weapon must be an instance of Weapons enum.")
        if not isinstance(self.room, Rooms):
            raise ValueError("room must be an instance of Rooms enum.")


@dataclass
class SuggestionMessage(AbstractMessage):
    character: Characters
    weapon: Weapons
    room: Rooms
    type: MessageTypes = MessageTypes.SUGGESTION

    def __post_init__(self):
        super().__post_init__()
        if not isinstance(self.character, Characters):
            raise ValueError("character must be an instance of Characters enum.")
        if not isinstance(self.weapon, Weapons):
            raise ValueError("weapon must be an instance of Weapons enum.")
        if not isinstance(self.room, Rooms):
            raise ValueError("room must be an instance of Rooms enum.")


@dataclass
class DisproveMessage(AbstractMessage):
    card: Union[Characters, Weapons, Rooms]
    type: MessageTypes = MessageTypes.DISPROVE

    def __post_init__(self):
        super().__post_init__()
        if not isinstance(self.card, (Characters, Weapons, Rooms)):
            raise ValueError("card must be an instance of Characters, Weapons, or Rooms enum.")


@dataclass
class ErrorMessage(AbstractMessage):
    reason: str
    type: MessageTypes = MessageTypes.ERROR

    def __post_init__(self):
        super().__post_init__()
        if not isinstance(self.reason, str) or not self.reason.strip():
            raise ValueError("reason must be a non-empty string.")


@dataclass
class EndTurnMessage(AbstractMessage):
    type: MessageTypes = MessageTypes.END_TURN

    def __post_init__(self):
        super().__post_init__()


@dataclass
class UpdateMessage(AbstractMessage):
    type: MessageTypes = MessageTypes.UPDATE

    def __post_init__(self):
        super().__post_init__()


@dataclass
class WelcomeMessage(AbstractMessage):
    available_characters: List[Characters]
    type: MessageTypes = MessageTypes.WELCOME

    def __post_init__(self):
        super().__post_init__()
        if not (isinstance(self.available_characters, list) and all(isinstance(char, Characters) for char in self.available_characters)):
            raise ValueError("available_characters must be a list of Characters enum instances.")


@dataclass
class JoinMessage(AbstractMessage):
    character: Characters
    type: MessageTypes = MessageTypes.JOIN

    def __post_init__(self):
        super().__post_init__()
        if not isinstance(self.character, Characters):
            raise ValueError("character must be an instance of Characters enum.")


def message_from_json(msg: dict) -> AbstractMessage:
    for msg_obj in [
        MoveMessage,
        AccusationMessage,
        SuggestionMessage,
        DisproveMessage,
        EndTurnMessage,
        ErrorMessage,
        UpdateMessage,
        WelcomeMessage,
        JoinMessage,
    ]:
        if msg['type'] == msg_obj.type:
            msg['type'] = msg_obj.type  # Make sure it's the enum type
            return msg_obj(**msg)
    raise ValueError(f"Unknown message type: {msg['type']}")


# Tests to demonstrate functionality
if __name__ == '__main__':
    # Example WelcomeMessage
    welcome_message = WelcomeMessage(user_id=0, available_characters=list(Characters))
    print(welcome_message.to_json_str())

    # Example JoinMessage
    join_message = JoinMessage(user_id=1, character=Characters.SCARLET)
    print(join_message.to_json_str())

    # Example deserialization
    raw_data = {"user_id": 2, "type": "join", "character": "Miss Scarlet"}
    print(message_from_json(raw_data))
