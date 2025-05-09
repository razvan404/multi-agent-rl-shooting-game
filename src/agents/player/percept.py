from pydantic import BaseModel

from src.geometry import Vector2D
from src.objects import GameObject
from src.interfaces.percept import Percept


class Ray(BaseModel):
    distance: float  # [0, 1]
    obj: GameObject
    angle: float


class PlayerPercept(Percept):
    rays: list[Ray]
    direction: Vector2D
