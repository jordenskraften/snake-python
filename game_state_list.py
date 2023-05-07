from main_menu_state import MainMenuState
from single_game_state import SingleGameState
from player_versus_ai_state import PlayerVersusAiState 

 
class GameStateList:
    def __init__(self, context):
        self.main_menu = MainMenuState(context)
        self.single_player = SingleGameState(context)
        self.player_versus_ai = PlayerVersusAiState(context)