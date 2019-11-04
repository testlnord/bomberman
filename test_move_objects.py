

def move_objects():
    for obj, new_position in movements:
        objs_in_new_position = get_objects_by_coords(new_position)
        all_passable = True
        for obj_in_new_position in objs_in_new_position:
            if not game_objects[obj_in_new_position]['passable']:
                all_passable = False
                break

        if all_passable:
            game_objects[obj]['position'] = new_position
            for obj_in_new_position in objs_in_new_position:
                interactions.append((obj, obj_in_new_position))
    movements.clear()


movements = []
interactions = []



def get_objects_by_coords(position):
    result = []
    for obj, desc in game_objects.items():
        if desc['position'] == position:
            result.append(obj)
    return result


game_objects = {
    ('wall', 0): {'position': (0, 0), 'passable': False, 'interactable': False, 'char': '#'},
    ('wall', 1): {'position': (0, 1), 'passable': False, 'interactable': False, 'char': '#'},
    ('player',): {'position': (1, 1), 'passable': True, 'interactable': True, 'char': '@', 'coins': 0},
    ('coin', 2): {'position': (1, 3), 'passable': True, 'interactable': True, 'char': '$'},
    ('soft_wall', 11): {'position': (1, 4), 'passable': False, 'interactable': True, 'char': '%'}
}

movements = [(('player',), (0, 1))]
move_objects()
assert not movements
assert not interactions
assert game_objects[('player',)]['position'] == (1, 1)

movements = [(('player',), (1, 2))]
move_objects()
assert not movements
assert not interactions
assert game_objects[('player',)]['position'] == (1, 2)

movements = [(('player',), (1, 3))]
move_objects()
assert not movements
assert interactions == [(('player',), ('coin', 2))] or interactions == [(('coin', 2), ('player',))]
assert game_objects[('player',)]['position'] == (1, 3)

print(19)

