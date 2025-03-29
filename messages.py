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
    START_TURN = 'start_turn'  # New message type added
    UPDATE = 'update'
    WELCOME = 'welcome'
    JOIN = 'join'


@dataclass
class AbstractMessage(ABC):
    user_id: int

    def to_json_str(self) -> str:
        return json.dumps(self.__dict__)


@dataclass
class MoveMessage(AbstractMessage):
    coordinates: tuple[int, int]
    type: MessageTypes = MessageTypes.MOVE


@dataclass
class AccusationMessage(AbstractMessage):
    character: Characters
    weapon: Weapons
    room: Rooms
    type: MessageTypes = MessageTypes.ACCUSATION


@dataclass
class SuggestionMessage(AbstractMessage):
    character: Characters
    weapon: Weapons
    room: Rooms
    type: MessageTypes = MessageTypes.SUGGESTION


@dataclass
class DisproveMessage(AbstractMessage):
    card: Union[Characters, Weapons, Rooms]
    type: MessageTypes = MessageTypes.DISPROVE


@dataclass
class ErrorMessage(AbstractMessage):
    reason: str
    type: MessageTypes = MessageTypes.ERROR


@dataclass
class EndTurnMessage(AbstractMessage):
    type: MessageTypes = MessageTypes.END_TURN


@dataclass
class StartTurnMessage(AbstractMessage):
    type: MessageTypes = MessageTypes.START_TURN


@dataclass
class UpdateMessage(AbstractMessage):
    type: MessageTypes = MessageTypes.UPDATE


@dataclass
class WelcomeMessage(AbstractMessage):
    available_characters: List[Characters]
    assigned_id: int
    type: MessageTypes = MessageTypes.WELCOME


@dataclass
class JoinMessage(AbstractMessage):
    character: Characters
    type: MessageTypes = MessageTypes.JOIN


def message_from_json(msg: dict) -> AbstractMessage:
    for msg_obj in [
        MoveMessage,
        AccusationMessage,
        SuggestionMessage,
        DisproveMessage,
        EndTurnMessage,
        StartTurnMessage,   # Added new message type here
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
    welcome_message = WelcomeMessage(user_id=0, assigned_id=10, available_characters=list(Characters))
    print(welcome_message.to_json_str())

    # Example JoinMessage
    join_message = JoinMessage(user_id=10, character=Characters.SCARLET)
    print(join_message.to_json_str())
    
    # Example StartTurnMessage
    start_turn_message = StartTurnMessage(user_id=10)
    print(start_turn_message.to_json_str())

    # Example deserialization
    raw_data = {"user_id": 2, "type": "join", "character": "Miss Scarlet"}
    print(message_from_json(raw_data))
