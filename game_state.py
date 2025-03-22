from defaults import valid_moves, Characters, Weapons, Rooms
import random
from player import Player


class GameState():
    def __init__(self):
        self.game_started = False
        self.current_player = 0
        self.disprover = -1
        self.avaliable_characters = {c for c in Characters}

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
        self.solution = (solution_character, solution_weapon, solution_room)
        self.cards = characters + weapons + rooms
        self.players = list()

    def add_player(self, character: Characters) -> Player:
        if self.game_started:
            return None
        if character not in self.avaliable_characters:
            return None
        self.avaliable_characters.remove(character)
        player = Player(character)
        self.players.append(player)
        return player

        
    def start_game(self): 
        assert(len(self.players) > 2)      
        i = 0
        while self.cards:
            card = random.choice(self.cards)
            self.cards.remove(card)
            self.players[i].add_card(card)
            i = (i + 1) % len(self.players)
        self.game_started = True


    def is_valid_move(p_curr_coord: tuple[int, int], p_desired_coord: tuple[int, int]) -> bool:
        x = p_desired_coord[0]
        y = p_desired_coord[1]
        if x < 0 or x > 4 or y < 0 or y > 4:
            return False
        if p_desired_coord not in valid_moves[p_curr_coord]:
            return False
        # TODO: check for player in hallway
        return True
    
    def check_solution(self, guess: tuple[Characters, Weapons, Rooms]):
        """Setter for the position attribute"""
        if not isinstance(guess, tuple[Characters, Weapons, Rooms]):
            raise ValueError("Name must be a tuple[Characters, Weapons, Rooms]")
        return self.solution == guess

if __name__ == '__main__':
    g = GameState()
    assert(g.add_player(Characters.MUSTARD))
    assert(not g.add_player(Characters.MUSTARD))
    while g.avaliable_characters:
        assert(g.add_player(next(iter(g.avaliable_characters))))
    g.start_game()
    for p in g.players:
        print()
        print(p)
    
    