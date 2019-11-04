

def player_interaction(player, object):
    if object[0] == 'coin':
        old_objects.append(object)
        game_objects[player]['coins'] += 1


def wave_interaction(wave, object):
    if object[0] == 'player' or object[0] == 'soft_wall':
        old_objects.append(object)




################3
old_objects = []
game_objects = {
    ('wall', 0): {'position': (0, 0), 'passable': False, 'interactable': False, 'char': '#'},
    ('wall', 1): {'position': (0, 1), 'passable': False, 'interactable': False, 'char': '#'},
    ('coin', 2): {'position': (2, 1), 'passable': True, 'interactable': True, 'char': '$'},
    ('player',): {'position': (1, 1), 'passable': True, 'interactable': True, 'char': '@', 'coins': 0},
    ('heatwave', 3): {'position': (2, 3), 'passable': True, 'interactable': True, 'char': '+'},
    ('soft_wall', 11): {'position': (1, 4), 'passable': False, 'interactable': True, 'char': '%'}
}

interactions = []

interaction_funs = {
    'player': player_interaction,
    'heatwave': wave_interaction,
}


def idle_interaction(o1, o2):
    pass


def process_interactions():
    for obj1, obj2 in interactions:
        interaction_funs.get(obj1[0], idle_interaction)(obj1, obj2)
        interaction_funs.get(obj2[0], idle_interaction)(obj2, obj1)
    interactions.clear()



interactions = [(('player', ), ('heatwave', 3))]
process_interactions()
assert old_objects == [('player', )]
assert not interactions

old_objects.clear()
interactions = [(('player', ), ('coin', 2))]
process_interactions()
assert old_objects == [('coin', 2)]
assert not interactions

old_objects.clear()
interactions = [(('player', ), ('wall', 0))]
process_interactions()
assert old_objects == []
assert not interactions

old_objects.clear()
interactions = [(('heatwave', 3), ('wall', 0))]
process_interactions()
assert old_objects == []
assert not interactions

old_objects.clear()
interactions = [(('wall', 1), ('heatwave', 3))]
process_interactions()
assert old_objects == []
assert not interactions

old_objects.clear()
interactions = [(('heatwave', 3), ('soft_wall', 11))]
process_interactions()
assert old_objects == [('soft_wall', 11)]
assert not interactions

