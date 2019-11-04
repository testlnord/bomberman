# process player input
def get_keyboard_input():
    return input()


player_inputs = {'w': "up", 'a': "left",
                 's': 'down', 'd': 'right',
                 ' ': 'bomb'
                 }


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


# GLOBALS
game_state = "in_progress"
game_objects = {}
new_objects = []
movements = []
interactions = []
old_objects = []


# GAME OBJECTS LOGIC
def idle_logic(_):
    pass


def bomb_logic(bomb_object):
    raise NotImplementedError


def heatwave_logic(heatwave):
    raise NotImplementedError


object_logics = {
    'bomb': bomb_logic,
    'heatwave': heatwave_logic
}


def process_objects_logic():
    for game_object in game_objects:
        object_logics.get(game_object[0], idle_logic)(game_object)


# UTILITIES
def get_objects_by_coords(position):
    raise NotImplementedError


objects_ids_counter = 0


def get_next_counter_value():
    global objects_ids_counter
    result = objects_ids_counter
    objects_ids_counter += 1
    return result


# OBJECT CREATION
def add_new_objects():
    raise NotImplementedError


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


# OBJECT MOVEMENT
def move_objects():
    raise NotImplementedError


# OBJECT REMOVAL
def remove_objects():
    raise NotImplementedError


# OBJECT INTERACTIONS
def idle_interaction(o1, o2):
    pass


def player_interaction(player, object):
    raise NotImplementedError


def wave_interaction(wave, object):
    raise NotImplementedError


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
    raise NotImplementedError


# GRAPHIC
def draw_screen(screen):
    for line in screen:
        print(''.join(line))


def render_screen():
    screen = [["." for _ in range(10)] for __ in range(10)]
    for obj, desc in game_objects.items():
        x, y = desc['position']
        screen[x][y] = desc['char']
    return screen


# GAME LOAD

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


def load_level(level):
    raise NotImplementedError


# GAME

load_level(level_example)
screen = render_screen()
draw_screen(screen)

while game_state == 'in_progress':

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

    screen = render_screen()
    draw_screen(screen)

    game_state = check_game_state()

if game_state == 'win':
    print("You win")
elif game_state == 'lose':
    print("You lost")
else:
    print("Bye Bye!")
