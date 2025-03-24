from abc import ABC, abstractmethod
from dataclasses import dataclass
from defaults import Characters, Weapons, Rooms
from enum import Enum
from typing import Union
import json


class MessageTypes(str, Enum):
    MOVE = 'move'
    ACCUSATION = 'accusation'
    SUGGESTION = 'suggestion'
    DISPROVE = 'disprove'
    ERROR = 'error'
    END_TURN = 'end_turn'
    UPDATE = 'update'


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
class UpdateMessage(AbstractMessage):
    type: MessageTypes = MessageTypes.UPDATE

def message_from_json(msg: dict) -> AbstractMessage:
    for msg_obj in [MoveMessage, AccusationMessage, SuggestionMessage, DisproveMessage, EndTurnMessage, ErrorMessage, UpdateMessage]:
        if msg['type'] == msg_obj.type:
            return msg_obj(**msg)
    return None

# def message_from_json()
if __name__ == '__main__':
    print(EndTurnMessage({'user_id': 1}).to_json_str())
    print(json.loads(EndTurnMessage({'user_id': 1}).to_json_str()))
    print(message_from_json({'user_id': 1, 'type': 'move', 'coordinates': (0,0)}))
    
