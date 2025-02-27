import unittest
import game



class GameTests(unittest.TestCase):
    
    # This will be called for every test case automatically! Just a feature of unittest
    def setUp(self):
        self.game = game.Game()



    def test_deckSize(self):

        # Should be 21 cards...  
        self.assertEqual(len(self.game.deck), 21)

    def test_CardTypes(self):

        categories =[] 

        for card in self.game.deck:
            if card.category not in categories:
                categories.append(card.category)
        self.assertEqual(len(categories), 3)
    

    def test_SolutionDraw(self):

        self.game.solutionCreate()

        self.assertEqual(len(self.game.solution), 3)
        self.assertEqual(len(self.game.deck), 18)




if __name__ == "__main__":
    unittest.main()
