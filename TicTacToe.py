board_map = [['_', '_', '_'], ['_', '_', '_'], ['_', '_', '_']]

def print_board(board):
    print('---------')
    for row in board:
        print(f'| {" ".join(row)} |')
    print('---------')


def validate_input():
    transform_input_axis = {
        '1 3': '0 0',
        '2 3': '0 1',
        '3 3': '0 2',
        '1 2': '1 0',
        '2 2': '1 1',
        '3 2': '1 2',
        '1 1': '2 0',
        '2 1': '2 1',
        '3 1': '2 2'
    }

    while True:
        user_input = input('Enter the coordinates:')
        coordinates = user_input.split()

        if len(coordinates) <= 1:
            print('You should enter numbers!')
        elif not (coordinates[0].isnumeric() and coordinates[1].isnumeric()):
            print('You should enter numbers!')
        elif not(1 <= int(coordinates[0]) <= 3 and 1 <= int(coordinates[1]) <= 3):
            print('Coordinates should be from 1 to 3!')
        else:
            x, y = transform_input_axis[user_input].split()
            x = int(x)
            y = int(y)
            current_movement = board_map[x][y]

            if current_movement == "X" or current_movement == "O":
                print('This cell is occupied! Choose another one!')
            else:
                return (x, y)


def get_wins(data):
    posibles_win = []
    matrix_win = [
        [(0, 0), (0, 1), (0, 2)],
        [(1, 0), (1, 1), (1, 2)],
        [(2, 0), (2, 1), (2, 2)],
        [(0, 0), (1, 0), (2, 0)],
        [(0, 1), (1, 1), (2, 1)],
        [(0, 2), (1, 2), (2, 2)],
        [(0, 0), (1, 1), (2, 2)],
        [(0, 2), (1, 1), (2, 0)]
    ]

    for win in matrix_win:
        posibles_win.append(all([board_map[x][y] == data for x, y in win]))

    return posibles_win


def verify_draw():
    for row in board_map:
        underscore = '_' not in row

    return all(['_' not in row for row in board_map])


def start_game():
    turn = 1

    while True:
        x, y = validate_input()
        move = "X" if turn % 2 == 0 else "O"
        board_map[x][y] = move
        print_board(board_map)
        x_wins = get_wins('X')
        o_wins = get_wins('O')
        if any(x_wins) or any(o_wins):
            print(f'{move} wins')
            break
        elif verify_draw():
            print('Draw')
            break
        turn += 1

print_board(board_map)
start_game()
