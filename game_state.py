from defaults import valid_moves, hallways, starting_locations, Characters, Weapons, Rooms
import random
from player import Player
from messages import MoveMessage, JoinMessage, WelcomeMessage, AccusationMessage, SuggestionMessage, DisproveMessage, ErrorMessage, StartTurnMessage, EndTurnMessage, UpdateMessage
from typing import Dict, Union
import logging

# Configure logging
logging.basicConfig(
    # filename='app.log',
    # filemode='w', # 'w' to overwrite, 'a' to append
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)

# Get a logger instance (using __name__ for module-specific logging)
logger = logging.getLogger(__name__)

class GameState():

    def __init__(self):
        self._game_started = False
        self._current_player = 0
        self._disprover = -1
        self._is_over = False
        self._avaliable_characters = {c for c in Characters}

        # Build solution
        characters = [c for c in Characters]
        weapons = [w for w in Weapons]
        rooms = [r for r in Rooms]
        solution_character = random.choice(characters)
        characters.remove(solution_character)
        solution_weapon = random.choice(weapons)
        weapons.remove(solution_weapon)
        solution_room = random.choice(rooms)
        rooms.remove(solution_room)
        self._solution = (solution_character, solution_weapon, solution_room)
        self._cards = characters + weapons + rooms
        self._players: Dict[int, Player] = dict()
        self._positions = starting_locations

    @property
    def is_over(self):
        """Getter for the is_over attribute"""
        return self._is_over

    @property
    def avaliable_characters(self):
        """Getter for the avaliable_characters attribute"""
        return self._avaliable_characters

    def add_player(self, user_id: int, character: Characters) -> Player:
        if self._game_started:
            return None
        if user_id == 0 or user_id in self._players.keys():
            return None
        if character not in self._avaliable_characters:
            return None
        # Make sure first player added is the first player or SCARLET if she is in the game
        if self._current_player == 0 or character == Characters.SCARLET:
            self._current_player = user_id
        self._avaliable_characters.remove(character)
        player = Player(user_id, character)
        self._players[user_id] = player
        return player

    # TODO: Move player and mark if not current player that
    # it was suggestion and they can make one during their turn
    def _move_player(self, p_player: Player, p_desired_coord: tuple[int, int], p_force: bool = False):
        assert (self._game_started)
        if not p_force:
            assert (self.is_valid_move(p_player.position, p_desired_coord))
        p_player.position = p_desired_coord
        p_player.can_suggest = not p_desired_coord in hallways

    def start_game(self):
        assert (not self._game_started)
        # assert (len(self._players) > 2)
        ids = list(self._players.keys())
        i = 0
        while self._cards:
            card = random.choice(self._cards)
            self._cards.remove(card)
            self._players[ids[i]].add_card(card)
            i = (i + 1) % len(self._players)
        self._game_started = True
        ret = list()
        ret.append((StartTurnMessage(0), self._current_player))
        self._players[self._current_player].can_move = True
        for p_id in [p for p in self._players if p != self._current_player]:
            self._players[p_id].can_move = False
            ret.append((EndTurnMessage(0), p_id))
        return ret

    def is_valid_move(self, p_curr_coord: tuple[int, int],
                      p_desired_coord: tuple[int, int]) -> bool:
        x = p_desired_coord[0]
        y = p_desired_coord[1]
        if x < 0 or x > 4 or y < 0 or y > 4:
            return False
        if p_desired_coord not in valid_moves[p_curr_coord]:
            logger.info("{} not in {}".format(p_desired_coord, valid_moves[p_curr_coord]))
            return False
        if p_desired_coord in hallways:
            for k in self._positions:
                if p_desired_coord == self._positions[k]:
                    return False
        return True

    def check_solution(self, guess: tuple[Characters, Weapons, Rooms]):
        if not isinstance(guess, tuple):
            raise ValueError(
                "Name must be a tuple[Characters, Weapons, Rooms]")
        return self._solution == guess
    
    def get_welcome_message(self, id: int) -> WelcomeMessage:
        return WelcomeMessage(0, list(self.avaliable_characters), id)
    
    def process_message(
        self, msg: Union[MoveMessage, AccusationMessage, SuggestionMessage,
                         DisproveMessage, EndTurnMessage, JoinMessage]
    ) -> list[tuple[Union[ErrorMessage, UpdateMessage, WelcomeMessage, StartTurnMessage, EndTurnMessage], int]]:
        """Main entry point for processing a message. Delegates to specific handlers."""
        handlers = {
            MoveMessage: self._handle_move_message,
            JoinMessage: self._handle_join_message,
            AccusationMessage: self._handle_accusation_message,
            SuggestionMessage: self._handle_suggestion_message,
            DisproveMessage: self._handle_disprove_message,
            EndTurnMessage: self._handle_end_turn_message,
        }

        # Return a list of tuples with message and id for sending
        ret: list[tuple[Union[ErrorMessage, UpdateMessage, WelcomeMessage, StartTurnMessage, EndTurnMessage], int]] = []

        valid, error_msg = self._validate_message(msg)
        if not valid:
            return [(error_msg, msg.user_id)]

        # Check if the message type has a specific handler
        handler = handlers.get(type(msg))
        if handler:
            logger.debug(f"Processing message: {type(msg).__name__}")
            return handler(msg)
        else:
            ret.append((ErrorMessage(0, f"Message type <{msg.type}> not handled!"), msg.user_id))
            return ret

    def _validate_message(self, msg) -> tuple[bool, Union[None, ErrorMessage]]:
        player = self._players.get(msg.user_id, None)
        # Always allow join messages
        if isinstance(msg, JoinMessage):
            return True, None
        # Check if the player exists
        if not player:
            return False, ErrorMessage(0, f"Player with ID {msg.user_id} does not exist.")
        # Validate that the message is coming from the current player
        if msg.user_id != self._current_player:
            # Special case: DisproveMessage can come from non-current players
            if isinstance(msg, DisproveMessage):
                return True, None
            return False, ErrorMessage(0, "It is not your turn!")
        # Validate the player's eligibility
        if not player.eligable:
            return False, ErrorMessage(0, "You are not eligible to take a turn!")
        # If all checks pass, the message is valid
        return True, None

    def _handle_move_message(self, msg: MoveMessage) -> list[tuple[Union[ErrorMessage, UpdateMessage], int]]:
        """Handle MoveMessage logic."""
        ret = []
        player = self._players.get(msg.user_id)
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
        """Handle JoinMessage logic."""
        ret = []
        if msg.user_id in self._players:
            ret.append((ErrorMessage(0, "You already joined!"), msg.user_id))
        elif msg.character not in self.avaliable_characters:
            ret.append((ErrorMessage(0, "Character unavailable!"), msg.user_id))
            ret.append((self.get_welcome_message(msg.user_id), msg.user_id))
        else:
            self.add_player(msg.user_id, msg.character)
            for p in self._players:
                ret.append((self.get_welcome_message(p), p))
        return ret

    def _handle_accusation_message(self, msg: AccusationMessage) -> list[tuple[Union[ErrorMessage, UpdateMessage, StartTurnMessage, EndTurnMessage], int]]:
        """Handle AccusationMessage logic."""
        ret = []
        player = self._players[msg.user_id]
        correct = self.check_solution((msg.character, msg.weapon, msg.room))
        logger.info(f"Accusation result: {correct}")
        player.eligable = correct

        if correct or all(not p.eligable for p in self._players.values()):
            self._is_over = True
            ret.extend(self.build_broadcast_update())
        else:
            if player.position in hallways:
                self._move_player(player, (2, 2), True)
            ret.extend(self.build_broadcast_update())
            ret.append((EndTurnMessage(0), self._current_player))
            self.increment_player()
            ret.append((StartTurnMessage(0), self._current_player))

        return ret

    def _handle_suggestion_message(self, msg: SuggestionMessage) -> list[tuple[Union[ErrorMessage, UpdateMessage], int]]:
        """Handle SuggestionMessage logic."""
        ret = []
        # TODO: Implement suggestion mechanics
        logger.info(f"Player {msg.user_id} made a suggestion: {msg.character}, {msg.weapon}, {msg.room}")
        ret.append((ErrorMessage(0, "Suggestion not implemented!"), msg.user_id))
        return ret

    def _handle_disprove_message(self, msg: DisproveMessage) -> list[tuple[Union[ErrorMessage], int]]:
        """Handle DisproveMessage logic."""
        ret = []
        if msg.user_id != self._disprover:
            ret.append((ErrorMessage(0, "You are not the disprover!"), msg.user_id))
        else:
            ret.append((ErrorMessage(0, "Disprove not implemented!"), msg.user_id))
        return ret

    def _handle_end_turn_message(self, msg: EndTurnMessage) -> list[tuple[Union[ErrorMessage, UpdateMessage, StartTurnMessage, EndTurnMessage], int]]:
        """Handle EndTurnMessage logic."""
        ret = []
        ret.append((EndTurnMessage(0), self._current_player))
        self.increment_player()
        ret.extend(self.build_broadcast_update())
        ret.append((StartTurnMessage(0), self._current_player))
        return ret
    
    def build_broadcast_update(self):
        return [(UpdateMessage(0), p) for p in self._players]
    
    def increment_player(self):
        # End the current player's turn
        player = self._players[self._current_player]
        player.can_move = False
        ids = list(self._players.keys())
        next_index = ids.index(player.id)
        next_index = (next_index + 1) % len(ids)
        while not self._players[next_index].eligable:
            next_index = (next_index + 1) % len(ids) # Use modulo for looping
        self._current_player = ids[next_index]
        # Start next turn
        self._players[self._current_player].can_move = True

    def _create_fake_data(self):
        i = 0
        assert (not self.add_player(i, Characters.MUSTARD))
        i += 1
        assert (self.add_player(i, Characters.MUSTARD))
        assert (not self.add_player(i, Characters.MUSTARD))
        assert (not self.add_player(i + 1, Characters.MUSTARD))
        while self.avaliable_characters:
            i += 1
            assert (self.add_player(i, next(iter(self.avaliable_characters))))
        self.start_game()

if __name__ == '__main__':
    characters = [c for c in Characters]
    weapons = [w for w in Weapons]
    rooms = [r for r in Rooms] 
    g = GameState()
    g._create_fake_data()
    for id in g._players:
        logger.debug(g._players[id])
    logger.debug('Processing message')
    logger.debug('Before message processing: {}'.format(g._players[1]))
    # Invalid move for Mustard
    ret = g.process_message(MoveMessage(1, (1,2)))
    logger.debug(f'Ret: {ret}')
    # Valid move for mustard
    logger.debug('Before move: {}'.format(g._players[1]))
    ret = g.process_message(MoveMessage(1, (0,4)))
    logger.debug(f'Ret: {ret}')
    logger.debug('After move: {}'.format(g._players[1]))
    # Try to accuse
    ret = g.process_message(AccusationMessage(1,random.choice(characters), random.choice(weapons), random.choice(rooms)))
    logger.debug(f'Ret: {ret}')
    logger.debug('After accuse: {}'.format(g._players[1]))
    

