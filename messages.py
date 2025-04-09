from abc import ABC, abstractmethod
from dataclasses import dataclass
from defaults import Characters, Weapons, Rooms
from enum import StrEnum
from typing import Union, List
import json


class MessageTypes(StrEnum):
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
    STATE_UPDATE = 'state_update'


@dataclass
class AbstractMessage(ABC):
    user_id: int

    def to_json_str(self) -> str:
        return json.dumps(self.__dict__)


@dataclass
class MoveMessage(AbstractMessage):
    coordinates: tuple[int, int]
    type: MessageTypes = MessageTypes.MOVE

    def __post_init__(self):
        self.coordinates = tuple(self.coordinates)

@dataclass
class AccusationMessage(AbstractMessage):
    character: Characters
    weapon: Weapons
    room: Rooms
    type: MessageTypes = MessageTypes.ACCUSATION

    def __post_init__(self):
        self.character = Characters(self.character)
        self.weapon = Weapons(self.weapon)
        self.room = Rooms(self.room)


@dataclass
class SuggestionMessage(AbstractMessage):
    character: Characters
    weapon: Weapons
    room: Rooms
    type: MessageTypes = MessageTypes.SUGGESTION

    def __post_init__(self):
        self.character = Characters(self.character)
        self.weapon = Weapons(self.weapon)
        self.room = Rooms(self.room)


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
    msg: str
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

    def __post_init__(self):
        self.character = Characters(self.character)


@dataclass
class StateUpdateMessage(AbstractMessage):
    updates: dict
    type: MessageTypes = MessageTypes.STATE_UPDATE

    def __post_init__(self):
        # Validate that updates is a dictionary
        if not isinstance(self.updates, dict):
            raise ValueError("Updates must be a dictionary.")


def message_from_json(msg: dict) -> AbstractMessage:
    for msg_obj in [
        MoveMessage,
        AccusationMessage,
        SuggestionMessage,
        DisproveMessage,
        EndTurnMessage,
        StartTurnMessage,   
        ErrorMessage,
        UpdateMessage,
        WelcomeMessage,
        JoinMessage,
        StateUpdateMessage,  
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
