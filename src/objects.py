from enum import IntEnum


class GameObject(IntEnum):
    NONE = 0
    WALL = 1
    TEAMMATE = 2
    ENEMY = 3


def game_object_size(obj: GameObject):
    return {
        GameObject.NONE: 0,
        GameObject.WALL: 1,
        GameObject.TEAMMATE: 1,
        GameObject.ENEMY: 1,
    }.get(obj, 1)
