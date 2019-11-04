def remove_objects():
    for old_object in old_objects:
        if old_object in game_objects:
            del game_objects[old_object]
    old_objects.clear()

old_objects = []
game_objects = {
    ('wall', 0): {'position': (0, 0), 'passable': False, 'interactable': False, 'char': '#'},
    ('wall', 1): {'position': (0, 1), 'passable': False, 'interactable': False, 'char': '#'},
    ('player',): {'position': (1, 1), 'passable': True, 'interactable': True, 'char': '@', 'coins': 0},
    ('soft_wall', 11): {'position': (1, 4), 'passable': False, 'interactable': True, 'char': '%'}
}

old_objects = [('player', )]
remove_objects()
assert not ('player', ) in game_objects
assert not old_objects

old_objects = [('player', )]
remove_objects()
assert not ('player', ) in game_objects
assert not old_objects

old_objects = [('coin', 1), ('coin', 2), ('wall', 1)]
remove_objects()
assert not ('player', ) in game_objects
assert not ('wall', 1) in game_objects
assert not old_objects

print(19)