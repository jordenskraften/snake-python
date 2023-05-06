from main_menu_state import MainMenuState
from single_game_state import SingleGameState

 
class GameStateList:
    def __init__(self, context):
        self.main_menu = MainMenuState(context)
        self.single_player = SingleGameState(context)