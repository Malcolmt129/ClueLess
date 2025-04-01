from game_state import GameState
import random
from defaults import valid_moves, hallways, Characters, Weapons, Rooms, RoomPositions, RoomPositionsToRooms, RoomsToRoomPositions
from player import Player
from messages import (
    MoveMessage, JoinMessage, WelcomeMessage, AccusationMessage, SuggestionMessage,
    DisproveMessage, ErrorMessage, StartTurnMessage, EndTurnMessage, UpdateMessage, StateUpdateMessage
)
from typing import Union
import logging

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)
logger = logging.getLogger(__name__)


class GameLogic:
    """
    Manages game logic and interfaces with the game state stored in the GameState class.
    """
    def __init__(self):
        self.state = GameState()

    @property
    def is_over(self) -> bool:
        return self.state.is_over
    
    @property
    def players(self) -> dict[int, Player]:
        return self.state.players

    @property
    def available_characters(self):
        return self.state.available_characters

    def add_player(self, user_id: int, character: Characters) -> Union[Player, None]:
        if self.state.game_started:
            return None
        if user_id == 0 or user_id in self.state.players:
            return None
        if character not in self.state.available_characters:
            return None
        # Ensure that either the first added player or SCARLET becomes the first player
        if self.state.current_player == 0 or character == Characters.SCARLET:
            self.state.current_player = user_id
        self.state.available_characters = self.state.available_characters - {character}
        player = Player(user_id, character)
        self.state.players[user_id] = player
        return player

    def _move_player(self, p_player: Player, p_desired_coord: tuple[int, int], p_force: bool = False):
        assert self.state.game_started
        if not p_force:
            assert self.is_valid_move(p_player.position, p_desired_coord)
        p_player.position = p_desired_coord
        p_player.can_suggest = p_desired_coord not in hallways

    def start_game(self):
        assert not self.state.game_started
        ids = list(self.state.players.keys())
        i = 0
        while self.state.cards:
            card = random.choice(self.state.cards)
            self.state.cards.remove(card)
            self.state.players[ids[i]].add_card(card)
            i = (i + 1) % len(ids)
        self.state.game_started = True
        ret = []
        ret.append((StartTurnMessage(0), self.state.current_player))
        self.state.players[self.state.current_player].can_move = True

        for p_id in [p for p in self.state.players if p != self.state.current_player]:
            self.state.players[p_id].can_move = False
            ret.append((EndTurnMessage(0), p_id))
        return ret

    def is_valid_move(self, p_curr_coord: tuple[int, int], p_desired_coord: tuple[int, int]) -> bool:
        x, y = p_desired_coord
        if x < 0 or x > 4 or y < 0 or y > 4:
            return False
        if p_desired_coord not in valid_moves[p_curr_coord]:
            logger.info(f"{p_desired_coord} not in {valid_moves[p_curr_coord]}")
            return False
        if p_desired_coord in hallways:
            for k in self.state.positions:
                if p_desired_coord == self.state.positions[k]:
                    return False
        return True

    def check_solution(self, guess: tuple[Characters, Weapons, Rooms]):
        if not isinstance(guess, tuple):
            raise ValueError("Guess must be a tuple[Characters, Weapons, Rooms]")
        return self.state.solution == guess

    def get_welcome_message(self, id: int) -> WelcomeMessage:
        return WelcomeMessage(0, list(self.available_characters), id)

    def process_message(
        self,
        msg: Union[MoveMessage, AccusationMessage, SuggestionMessage,
                   DisproveMessage, EndTurnMessage, JoinMessage]
    ) -> list[tuple[
            Union[ErrorMessage, UpdateMessage, WelcomeMessage, StartTurnMessage, EndTurnMessage],
            int]]:
        handlers = {
            MoveMessage: self._handle_move_message,
            JoinMessage: self._handle_join_message,
            AccusationMessage: self._handle_accusation_message,
            SuggestionMessage: self._handle_suggestion_message,
            DisproveMessage: self._handle_disprove_message,
            EndTurnMessage: self._handle_end_turn_message,
        }
        ret = []
        
        handler = handlers.get(type(msg))
        if handler:
            logger.debug(f"Processing message: {type(msg).__name__}")
            valid, error_msg = self._validate_message(msg)
            if not valid:
                return [(error_msg, msg.user_id)]
            return handler(msg)
        else:
            ret.append((ErrorMessage(0, f"Message type <{msg.type}> not handled!"), msg.user_id))
            return ret

    def _validate_message(self, msg) -> tuple[bool, Union[None, ErrorMessage]]:
        player = self.state.players.get(msg.user_id, None)
        # Always allow join messages
        if isinstance(msg, JoinMessage):
            return True, None
        # Check if the player exists
        if not player:
            return False, ErrorMessage(0, f"Player with ID {msg.user_id} does not exist.")
        # Validate that the message is coming from the current player
        if msg.user_id != self.state.current_player:
            # DisproveMessage may come from non-current players
            if isinstance(msg, DisproveMessage):
                return True, None
            return False, ErrorMessage(0, "It is not your turn!")
        # Validate the player's eligibility
        if not player.eligable:
            return False, ErrorMessage(0, "You are not eligible to take a turn!")
        return True, None

    def _handle_move_message(self, msg: MoveMessage) -> list[tuple[Union[ErrorMessage, UpdateMessage], int]]:
        ret = []
        player = self.state.players.get(msg.user_id)
        coord = msg.coordinates
        curr_coord = player.position
        logger.info(f"Attempting to move from {curr_coord} to {coord}")
        if not player.can_move:
            ret.append((ErrorMessage(0, "Already moved this turn!"), msg.user_id))
        elif not self.is_valid_move(curr_coord, coord):
            ret.append((ErrorMessage(0, f"Move is not valid {curr_coord} -> {coord}!"), msg.user_id))
        else:
            self._move_player(player, coord)
            player.can_move = False
            ret.extend(self.build_broadcast_update())
        return ret

    def _handle_join_message(self, msg: JoinMessage) -> list[tuple[Union[ErrorMessage, WelcomeMessage], int]]:
        ret = []
        if msg.user_id in self.state.players:
            ret.append((ErrorMessage(0, "You already joined!"), msg.user_id))
        elif msg.character not in self.available_characters:
            ret.append((ErrorMessage(0, "Character unavailable!"), msg.user_id))
            ret.append((self.get_welcome_message(msg.user_id), msg.user_id))
        else:
            self.add_player(msg.user_id, msg.character)
            for p in self.state.players:
                ret.append((self.get_welcome_message(p), p))
        return ret

    def _handle_accusation_message(self, msg: AccusationMessage) -> list[tuple[
            Union[ErrorMessage, UpdateMessage, StartTurnMessage, EndTurnMessage], int]]:
        ret = []
        player = self.state.players[msg.user_id]
        correct = self.check_solution((msg.character, msg.weapon, msg.room))
        logger.info(f"Accusation result: {correct}")
        player.eligable = correct

        if correct or all(not p.eligable for p in self.state.players.values()):
            self.state.is_over = True
            ret.extend(self.build_broadcast_update())
        else:
            if player.position in hallways:
                self._move_player(player, (2, 2), True)
            ret.extend(self.build_broadcast_update())
            ret.append((EndTurnMessage(0), self.state.current_player))
            self.increment_player()
            ret.append((StartTurnMessage(0), self.state.current_player))
        return ret

    def _handle_suggestion_message(self, msg: SuggestionMessage) -> list[tuple[Union[ErrorMessage, UpdateMessage], int]]:
        ret = []
        player = self.state.players.get(msg.user_id)

        # Validate the player can make a suggestion
        if not player.can_suggest:
            logger.info(f"Player {msg.user_id} attempted to make a suggestion but is not allowed.")
            ret.append((ErrorMessage(0, "You are not allowed to make a suggestion right now!"), msg.user_id))
            return ret

        # Log the suggestion
        logger.info(f"Player {msg.user_id} suggested {msg.character}, {msg.weapon}, {msg.room}")

        # Move the player with the suggested character to the suggested room
        suggested_room_position = RoomsToRoomPositions(msg.room)  # Get room position using the mapping function
        for other_player in self.state.players.values():
            if other_player.character == msg.character:
                logger.info(f"Moving player with character {msg.character} to room {msg.room}")
                self._move_player(other_player, suggested_room_position, True)
                ret.append((UpdateMessage(0, f"You were moved to the room {msg.room} due to a suggestion."), other_player.id))
                break

        # Broadcast the suggestion to all players
        for p_id in self.state.players:
            ret.append((UpdateMessage(0, f"Player {msg.user_id} suggested {msg.character}, {msg.weapon}, {msg.room}"), p_id))

        # Identify a player who can disprove the suggestion
        for disprover_id, disprover in self.state.players.items():
            if disprover_id != msg.user_id:  # Skip the suggesting player
                matching_cards = [card for card in [msg.character, msg.weapon, msg.room] if card in disprover.cards]
                if matching_cards:
                    # Found a disprover
                    self.state.disprover = disprover_id
                    logger.info(f"Player {disprover_id} can disprove the suggestion.")
                    ret.append((UpdateMessage(0, f"You can disprove the suggestion with one of your cards: {matching_cards}"), disprover_id))
                    return ret

        # No one could disprove the suggestion
        logger.info(f"No players could disprove Player {msg.user_id}'s suggestion.")
        ret.append((UpdateMessage(0, "No one could disprove your suggestion."), msg.user_id))
        return ret


    def _handle_disprove_message(self, msg: DisproveMessage) -> list[tuple[Union[ErrorMessage], int]]:
        ret = []
        if msg.user_id != self.state.disprover:
            ret.append((ErrorMessage(0, "You are not the disprover!"), msg.user_id))
        else:
            ret.append((ErrorMessage(0, "Disprove not implemented!"), msg.user_id))
        return ret

    def _handle_end_turn_message(self, msg: EndTurnMessage) -> list[tuple[
            Union[ErrorMessage, UpdateMessage, StartTurnMessage, EndTurnMessage], int]]:
        ret = []
        ret.append((EndTurnMessage(0), self.state.current_player))
        self.increment_player()
        ret.extend(self.build_broadcast_update())
        ret.append((StartTurnMessage(0), self.state.current_player))
        return ret

    def build_broadcast_update(self):
        state_dict = self.state.to_dict()
        return [(StateUpdateMessage(0,state_dict), p) for p in self.state.players]

    def increment_player(self):
        # End the current player's turn:
        player = self.state.players[self.state.current_player]
        player.can_move = False
        ids = list(self.state.players.keys())
        next_index = ids.index(self.state.current_player)
        next_index = (next_index + 1) % len(ids)
        # Cycle until an eligible player is found:
        while not self.state.players[ids[next_index]].eligable:
            next_index = (next_index + 1) % len(ids)
        self.state.current_player = ids[next_index]
        self.state.players[self.state.current_player].can_move = True
