from main_menu_state import MainMenuState
from single_game_state import SingleGameState
from player_versus_ai_state import PlayerVersusAiState 
from ai_versus_ai_state import AiVersusAiState
from boss_mode_state import BossModeState
 
class GameStateList:
    def __init__(self, context):
        self.main_menu = MainMenuState(context)
        self.single_player = SingleGameState(context)
        self.player_versus_ai = PlayerVersusAiState(context)
        self.ai_versus_ai = AiVersusAiState(context)
        self.boss_mode = BossModeState(context)