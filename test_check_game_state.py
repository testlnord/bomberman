def check_game_state():
    if ('player',) not in game_objects:
        return "lose"

    for obj in game_objects:
        if obj[0] == 'coin':
            return 'in_progress'
    return 'win'


##################
game_objects = {}
assert check_game_state() == 'lose'

game_objects = {('player', ): {}}
assert check_game_state() == 'win'

game_objects = {('coin', 1): {}}
assert check_game_state() == 'lose'

game_objects = {('player', ): {},
                ('coin', 0): {}}
assert check_game_state() == 'in_progress'


print(19)