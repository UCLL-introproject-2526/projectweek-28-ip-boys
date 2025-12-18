import os
from data.map_loader import load_map_from_file

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
MAP_DIR = os.path.join(BASE_DIR, "maps")

ALL_MAPS = {
    "ground": load_map_from_file(os.path.join(MAP_DIR, "ground.txt")),
    "first": load_map_from_file(os.path.join(MAP_DIR, "first.txt")),
    "classroom": load_map_from_file(os.path.join(MAP_DIR, "classroom.txt")),
    "director_room": load_map_from_file(os.path.join(MAP_DIR, "director_room.txt")),
}
