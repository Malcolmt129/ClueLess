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


@dataclass
class AbstractMessage(ABC):
    def to_json(self) -> str:
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

def message_from_json(msg: dict) -> AbstractMessage:
    for msg_obj in [MoveMessage, AccusationMessage, SuggestionMessage, DisproveMessage, EndTurnMessage]:
        if msg['type'] == msg_obj.type:
            return msg_obj(**msg)
    return None

# def message_from_json()
if __name__ == '__main__':
    print(EndTurnMessage().to_json())
    print(json.loads(EndTurnMessage().to_json()))
    print(message_from_json({'type': 'move', 'coordinates': (0,0)}))
    
