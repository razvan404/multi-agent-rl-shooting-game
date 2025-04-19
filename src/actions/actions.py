from abc import ABC

from src.interfaces import Action


class PlayerAction(Action, ABC):
    pass


class ForwardAction(PlayerAction):
    pass


class TurnLeftAction(PlayerAction):
    pass


class TurnRightAction(PlayerAction):
    pass


class ShootAction(PlayerAction):
    angle: float


class WaitAction(PlayerAction):
    pass
