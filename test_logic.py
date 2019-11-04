def bomb_logic(bomb_object):
    if game_objects[bomb_object]['life_time'] == 0:
        x, y = game_objects[bomb_object]['position']
        new_objects.append(create_object('heatwave', (x, y)))
        new_objects.append(create_object('heatwave', (x + 1, y)))
        new_objects.append(create_object('heatwave', (x - 1, y)))
        new_objects.append(create_object('heatwave', (x, y + 1)))
        new_objects.append(create_object('heatwave', (x, y - 1)))
        old_objects.append(bomb_object)
    else:
        game_objects[bomb_object]['life_time'] -= 1


def heatwave_logic(heatwave):
    old_objects.append(heatwave)


#################################
def idle_logic(_):
    pass


object_logics = {
    'bomb': bomb_logic,
    'heatwave': heatwave_logic
}

old_objects = []


def process_objects_logic():
    for game_object in game_objects:
        object_logics.get(game_object[0], idle_logic)(game_object)


new_objects = []

obj_types_to_char = {
    "player": "@", "wall": '#', 'soft_wall': '%', 'heatwave': '+', "bomb": '*', "coin": '$'
}

def create_object(type, position, **kwargs):
    desc = {'position': position,
            'passable': type not in ['wall', 'soft_wall'],
            'interactable': type not in ['wall'],
            'char': obj_types_to_char[type]
            }
    if type == 'player':
        desc['coins'] = 0
    if type == 'bomb':
        desc['power'] = 3
        desc['life_time'] = 3
    desc.update(kwargs)
    return type, desc, position

###################

game_objects = {('bomb', 0): {'position': (1, 1), 'interactable': True, 'passable': True, 'life_time': 1}}
process_objects_logic()
assert game_objects[('bomb', 0)]['life_time'] == 0

process_objects_logic()
assert old_objects == [('bomb', 0)]
assert len(new_objects) == 5
assert all(t == 'heatwave' for t, desc, pos in new_objects)
assert set(pos for t, desc, pos in new_objects) == set([(1,1), (0,1), (1,0),(2,1),(1,2)])

old_objects.clear()
game_objects = {('heatwave', 0): {'position': (1, 1), 'interactable': True, 'passable': True, 'life_time': 1}}
process_objects_logic()
assert  old_objects == [('heatwave', 0)]

