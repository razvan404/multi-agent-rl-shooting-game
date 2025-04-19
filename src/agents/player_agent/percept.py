from pydantic import BaseModel

from src.objects import GameObject
from src.interfaces.percept import Percept


class Ray(BaseModel):
    distance: float  # [0, 1]
    obj: GameObject


class PlayerPercept(Percept):
    rays: list[Ray]
