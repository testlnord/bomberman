def get_keyboard_input():
    return input()


game_state = "in_progress"
player_inputs = {'w': "up", 'a': "left",
                 's': 'down', 'd': 'right',
                 ' ': 'bomb'
                 }

game_objects = {}
new_objects = []
movements = []
interactions = []
old_objects = []


def idle_logic(_):
    pass


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

object_logics = {
    'bomb': bomb_logic,
    'heatwave': heatwave_logic
}


def process_objects_logic():
    for game_object in game_objects:
        object_logics.get(game_object[0], idle_logic)(game_object)


def process_player_input(player_input):
    x, y = game_objects[('player',)]['position']
    if player_input == 'up':
        x = x - 1
    elif player_input == 'down':
        x = x + 1
    elif player_input == 'right':
        y = y + 1
    elif player_input == 'left':
        y = y - 1
    elif player_input == 'bomb':
        new_objects.append(create_object('bomb', (x, y)))
    movements.append((("player",), (x, y)))


objects_ids_counter = 0


def get_object_by_coords(position):
    for obj, desc in game_objects.items():
        if desc['position'] == position:
            return obj


def add_new_objects():
    global objects_ids_counter
    for object_type, desc, position in new_objects:
        if object_type == 'player':
            game_objects[('player',)] = desc
        else:
            obj_in_position = get_object_by_coords(position)
            if obj_in_position is None:
                new_obj_id = objects_ids_counter
                objects_ids_counter += 1
                game_objects[(object_type, new_obj_id)] = desc
            else:
                if game_objects[obj_in_position]['interactable']:
                    new_obj_id = objects_ids_counter
                    objects_ids_counter += 1
                    game_objects[(object_type, new_obj_id)] = desc
                    interactions.append(((object_type, new_obj_id), obj_in_position))
                else:
                    print("Can't add object. Place is busy")
                pass
    new_objects.clear()


def move_objects():
    for obj, new_position in movements:
        obj_in_new_position = get_object_by_coords(new_position)
        if obj_in_new_position is None:
            game_objects[obj]['position'] = new_position
        else:
            if game_objects[obj_in_new_position]['passable']:
                game_objects[obj]['position'] = new_position
                interactions.append((obj, obj_in_new_position))
    movements.clear()


def remove_objects():
    for old_object in old_objects:
        del game_objects[old_object]
    old_objects.clear()


def idle_interaction(_, __):
    pass


def player_interaction(_, object):
    if object[0] == 'coin':
        old_objects.append(object)
        game_objects[("player",)]['coins'] += 1


def wave_interaction(_, object):
    if object[0] == 'player' or object[0] == 'soft_wall':
        old_objects.append(object)


interaction_funs = {
    'player': player_interaction,
    'heatwave': wave_interaction,
}


def process_interactions():
    for obj1, obj2 in interactions:
        interaction_funs.get(obj1[0], idle_interaction)(obj1, obj2)
        interaction_funs.get(obj2[0], idle_interaction)(obj2, obj1)
    interactions.clear()


def check_game_state():
    if ('player',) not in game_objects:
        return "lose"

    for obj in game_objects:
        if obj[0] == 'coin':
            return 'in_progress'
    return 'win'


def draw_screen(screen):
    for line in screen:
        print(''.join(line))


def render_screen():
    screen = [["." for _ in range(10)] for __ in range(10)]
    for obj, desc in game_objects.items():
        x, y = desc['position']
        screen[x][y] = desc['char']
    return screen


# initialise game
level_example = """
##########
#@  %    #
#   %    #
#  %%%   #
# %%$%%  #
#  %%%   #
#   %    #
#   %    #
#   %    #
##########
"""

obj_char_to_types = {
    "#": "wall",
    "@": "player",
    "%": "soft_wall",
    "$": "coin"
}

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
        power = 3
        if 'power' in kwargs:
            power = kwargs['power']
        desc['power'] = power
        desc['life_time'] = 3
    return type, desc, position


for x, line in enumerate(level_example.strip().splitlines()):
    for y, char in enumerate(line):
        type = obj_char_to_types.get(char)
        if type is not None:
            new_objects.append(create_object(type, (x, y)))
add_new_objects()

while game_state == 'in_progress':
    screen = render_screen()
    draw_screen(screen)

    kb_inp = get_keyboard_input()
    if kb_inp == "ESC":
        game_state = "finished"
        break

    if kb_inp in player_inputs:
        process_player_input(player_inputs[kb_inp])

    process_objects_logic()
    add_new_objects()
    move_objects()
    process_interactions()
    remove_objects()
    game_state = check_game_state()

if game_state == 'win':
    print("You win")
elif game_state == 'lose':
    print("You lost")
else:
    print("Bye Bye!")