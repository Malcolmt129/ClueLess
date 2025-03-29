from defaults import valid_moves, hallways, starting_locations, Characters, Weapons, Rooms
import random
from player import Player
from messages import MoveMessage, AccusationMessage, SuggestionMessage, DisproveMessage, ErrorMessage, EndTurnMessage, UpdateMessage
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
        # TODO: Scarlet should be first 
        self._current_player = 0
        self._disprover = -1
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
        assert (len(self._players) > 2)
        ids = list(self._players.keys())
        i = 0
        while self._cards:
            card = random.choice(self._cards)
            self._cards.remove(card)
            self._players[ids[i]].add_card(card)
            i = (i + 1) % len(self._players)
        self._game_started = True

    def is_valid_move(self, p_curr_coord: tuple[int, int],
                      p_desired_coord: tuple[int, int]) -> bool:
        x = p_desired_coord[0]
        y = p_desired_coord[1]
        if x < 0 or x > 4 or y < 0 or y > 4:
            return False
        if p_desired_coord not in valid_moves[p_curr_coord]:
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

    def process_message(
        self, msg: Union[MoveMessage, AccusationMessage, SuggestionMessage,
                         DisproveMessage, EndTurnMessage]
    ) -> list[tuple[Union[ErrorMessage, UpdateMessage], int]]:
        # Return a list of tuples with message and id for sending
        ret: list[tuple[Union[ErrorMessage, UpdateMessage], int]] = []
        # Processing 
        user_id = msg.user_id
        player = self._players[user_id]
        if isinstance(msg, (ErrorMessage, UpdateMessage)) or not isinstance(msg, (MoveMessage, AccusationMessage, SuggestionMessage, DisproveMessage, EndTurnMessage)):
            ret.append((ErrorMessage(0, 'Message type <%s> not handled!'.format(msg.type)), user_id))
        # Only Disprove is allowed to be from non-current playerr
        elif user_id is self._disprover and isinstance(msg, DisproveMessage):
            # TODO: Implement disprove logic
            ret.append((ErrorMessage(0, 'Disprove not implemented!'), user_id))
        # Ensure only current player sent a message
        elif user_id is not self._current_player + 1:
            ret.append((ErrorMessage(0, 'Not your turn!'), user_id))
        # Start processing the different message types for current user
        elif isinstance(msg, DisproveMessage):
            ret.append((ErrorMessage(0, 'Unable to disprove your own suggestion!'), user_id))
        elif isinstance(msg, MoveMessage):
            coord = msg.coordinates
            curr_coord = player.position
            logger.debug('Attempting to move from {} to {}'.format(curr_coord, coord))
            if not self.is_valid_move(curr_coord, coord):
                ret.append((ErrorMessage(0, 'Move is not valid {} -> {}!'.format(curr_coord, coord)), user_id))
            else:
                self._move_player(player, coord)
        elif isinstance(msg, AccusationMessage):
            correct = self.check_solution((msg.character, msg.weapon, msg.room))
            logger.info('Accusation result: {}'.format(correct))
            if correct:
                # TODO: End game
                pass
            else:
                # Move to the Billard room to get them out of the hallway
                if player.position in hallways:
                    self._move_player(player, (2,2), True)
                player.eligable = False
        elif isinstance(msg, SuggestionMessage):
            pass
        
        return ret


if __name__ == '__main__':
    characters = [c for c in Characters]
    weapons = [w for w in Weapons]
    rooms = [r for r in Rooms]
    i = 0
    g = GameState()
    assert (not g.add_player(i, Characters.MUSTARD))
    i += 1
    assert (g.add_player(i, Characters.MUSTARD))
    assert (not g.add_player(i, Characters.MUSTARD))
    assert (not g.add_player(i + 1, Characters.MUSTARD))
    while g.avaliable_characters:
        i += 1
        assert (g.add_player(i, next(iter(g.avaliable_characters))))
    g.start_game()
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
    

