from defaults import valid_moves, hallways, starting_locations, Characters, Weapons, Rooms
import random
from player import Player
from messages import MoveMessage, AccusationMessage, SuggestionMessage, DisproveMessage, ErrorMessage, EndTurnMessage, UpdateMessage
from typing import Dict, Union


class GameState():

    def __init__(self):
        self._game_started = False
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
    def move_player(self, character: Characters) -> Player:
        assert (self._game_started)
        pass

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
            for k, v in self._positions:
                if p_desired_coord == v:
                    return False
        return True

    def check_solution(self, guess: tuple[Characters, Weapons, Rooms]):
        """Setter for the position attribute"""
        if not isinstance(guess, tuple[Characters, Weapons, Rooms]):
            raise ValueError(
                "Name must be a tuple[Characters, Weapons, Rooms]")
        return self._solution == guess

    def process_message(
        self, msg: Union[MoveMessage, AccusationMessage, SuggestionMessage,
                         DisproveMessage, EndTurnMessage]
    ) -> list[tuple[Union[ErrorMessage, UpdateMessage], int]]:
        # Return a list of tuples with message and id for sending
        ret: list[tuple[Union[ErrorMessage, UpdateMessage], int]] = []
        id = msg.user_id
        if id is self._disprover and isinstance(msg, DisproveMessage):
            # TODO: Implement disprove logic
            ret.append((ErrorMessage(0, 'Disprove not implemented!'), id))
        if id is not self._current_player:
            ret.append((ErrorMessage(0, 'Not your turn!'), id))
        if isinstance(msg, DisproveMessage):
            ret.append((ErrorMessage(0, 'Unable to disprove your own suggestion!'), id))
        # TODO: Add message processing
        if isinstance(msg, MoveMessage):
            coords = msg.coordinates
            # if self.is_valid_move()
        return ret


if __name__ == '__main__':
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
        print()
        print(g._players[id])
