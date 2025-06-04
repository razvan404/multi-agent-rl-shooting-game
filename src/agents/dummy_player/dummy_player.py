import random
from src.actions import (
    PlayerAction,
    WaitAction,
    ForwardAction,
    TurnLeftAction,
    ShootAction,
)
from src.constants import PLAYER_NUM_RAYS
from src.objects import GameObject

from ..player import PlayerAgent


class DummyPlayerAgent(PlayerAgent):
    def _select_raw_action(self) -> PlayerAction:
        wall_hits = []
        enemy_hits = []
        for ray in range(PLAYER_NUM_RAYS):
            if self.current_percept.rays[ray].obj == GameObject.WALL:
                wall_hits.append(self.current_percept.rays[ray])
            elif self.current_percept.rays[ray].obj == GameObject.ENEMY:
                enemy_hits.append(self.current_percept.rays[ray])
        if any(
            [
                self.current_percept.rays[ray].obj == GameObject.WALL
                and self.current_percept.rays[ray].distance < 0.3
                for ray in range(PLAYER_NUM_RAYS)
            ]
        ):
            return TurnLeftAction()

        if any(
            [
                self.current_percept.rays[ray].obj == GameObject.ENEMY
                for ray in range(PLAYER_NUM_RAYS // 2 - 4, PLAYER_NUM_RAYS // 2 + 5)
            ]
        ):
            return ShootAction()

        p = random.random()
        if p < 0.85:
            return ForwardAction()
        elif p < 0.95:
            return TurnLeftAction()
        else:
            return WaitAction()
