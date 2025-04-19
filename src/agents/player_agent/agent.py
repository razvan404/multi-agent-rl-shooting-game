from abc import ABC
from collections import deque

from src.map import PlayerMapData
from src.actions import PlayerAction, WaitAction
from src.constants import PLAYER_LAST_ACTIONS_LEN
from src.interfaces import Action, Agent

from .percept import PlayerPercept


class PlayerAgent(Agent, ABC):
    map_data: PlayerMapData
    shooting_delay: int = 0  # ticks
    is_alive: bool = True
    last_actions: deque[Action] = deque(maxlen=PLAYER_LAST_ACTIONS_LEN)
    current_percept: PlayerPercept | None = None

    def init(self, **kwargs):
        super().__init__(**kwargs)
        for _ in range(PLAYER_LAST_ACTIONS_LEN):
            self.last_actions.append(WaitAction())

    def see(self, percept: PlayerPercept):
        self.current_percept = percept

    def _choose_action(self, action: PlayerAction) -> PlayerAction:
        self.current_percept = None
        self.last_actions.append(action)
        return action

    def select_action(self) -> PlayerAction:
        return self._choose_action(WaitAction())
