
def add_new_objects():
    for object_type, desc, position in new_objects:
        desc['position']=position
        objs_in_position = get_objects_by_coords(position)
        all_interactable = True
        for obj_in_position in objs_in_position:
            if not game_objects[obj_in_position]['interactable']:
                all_interactable = False
        if all_interactable:
            if object_type == 'player':
                obj_id = ('player', )
            else:
                new_obj_id = get_next_counter_value()
                obj_id = (object_type, new_obj_id)
            game_objects[obj_id] = desc
            for obj_in_position in objs_in_position:
                interactions.append((obj_id, obj_in_position))
    new_objects.clear()

############################3
interactions = []
objects_ids_counter = 0
def get_next_counter_value():
    global objects_ids_counter
    result = objects_ids_counter
    objects_ids_counter += 1
    return result


def get_objects_by_coords(position):
    result = []
    for obj, desc in game_objects.items():
        if desc['position'] == position:
            result.append(obj)
    return result


new_objects = []
game_objects = {
    ('wall', 0): {'position': (0, 0), 'passable': False, 'interactable': False, 'char': '#'},
    ('wall', 1): {'position': (0, 1), 'passable': False, 'interactable': False, 'char': '#'},
    ('player',): {'position': (1, 1), 'passable': True, 'interactable': True, 'char': '@', 'coins': 0},
    ('soft_wall', 11): {'position': (1, 4), 'passable': False, 'interactable': True, 'char': '%'}
}

new_objects = [('bomb', {'passable': True, 'interactable': True, 'lifetime': 5}, (1, 1))]
add_new_objects()
assert get_objects_by_coords((1, 1)) == [('player', ), ('bomb', 0)]

new_objects = [('heatwave', {'passable': True, 'interactable': True}, (1, 1)),
('heatwave', {'passable': True, 'interactable': True}, (0, 1)),
('heatwave', {'passable': True, 'interactable': True}, (1, 0)),
('heatwave', {'passable': True, 'interactable': True}, (2, 1)),
('heatwave', {'passable': True, 'interactable': True}, (1, 2))]
add_new_objects()
assert len(get_objects_by_coords((1, 1))) == 3
assert get_objects_by_coords((0, 1)) == [('wall', 1)]
