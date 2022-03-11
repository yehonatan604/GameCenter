import random
import datetime
import json
import main_system
import hashlib
from colorama import Fore
from art import *

init_time = datetime.datetime.now()
final_time = 0
name1 = ''
name2 = ''
move = ''
win_name = ''
num_of_players = 1
points = 20
game_difficulty = 1
players_list = []
options = []
temp_options = []
full = 0
win = 0
turn = 0
shape = ''
shape_2 = ''
win_shape = ''

print('welcome to tic tac toe game')

board_dict = {'a1': ' ',
              'b1': ' ',
              'c1': ' ',
              'a2': ' ',
              'b2': ' ',
              'c2': ' ',
              'a3': ' ',
              'b3': ' ',
              'c3': ' '
              }

random_move_list = ['a1', 'a2', 'a3', 'b1', 'b2', 'b3', 'c1', 'c2', 'c3']

with open("json_files/persona_high_scores.json") as f:
    all_score_list = json.load(f)


def game_menu():
    with open("json_files/tic_tac_toe_hs.json") as file:
        score_list = json.load(file)
    for player in range(len(score_list) - 1):
        x = score_list[player]
        if x['name'] == main_system.user1_name and x['rank'] == 0:
            name = main_system.user1_name
            last_score = x['high_score']
            date_scored = x['date_scored']
            play_duration = x['play_duration']
            difficulty = x['difficulty']
            difficulty_color = Fore.LIGHTCYAN_EX
            if difficulty == 'easy':
                difficulty_color = Fore.LIGHTGREEN_EX
            elif difficulty == 'intermediate':
                difficulty_color = Fore.LIGHTYELLOW_EX
            print('\n\n\n')
            print(f"{Fore.LIGHTWHITE_EX}{main_system.today_date('day')}" + f"{Fore.LIGHTWHITE_EX}user name -"
                                                                          f"{Fore.LIGHTYELLOW_EX}{name}".center(184))
            print(f"{Fore.LIGHTBLUE_EX}{main_system.today_date('time')}" + f"{Fore.LIGHTWHITE_EX}last high-score: "
                                                                           f"{Fore.LIGHTBLUE_EX}{str(last_score)}"
                                                                           f"".center(205))
            print(f"{Fore.LIGHTWHITE_EX}last time played: {str(date_scored)}".center(230))
            print(f"{Fore.LIGHTWHITE_EX}last play-time duration: {play_duration}".center(230))
            print(f"{Fore.LIGHTWHITE_EX}difficulty: {difficulty_color}{difficulty}\n\n{Fore.LIGHTGREEN_EX}".center(230))
            tprint(f'Tic-Tac-Toe'.center(85), font="small")
            print("\n")
            print(f"{Fore.LIGHTYELLOW_EX}1-play".center(126))
            print(f'{Fore.MAGENTA}2-high scores'.center(126))
            print(f'{Fore.MAGENTA}3-who is online'.center(126))
            print(f'{Fore.RED}4-main menu'.center(126))
            print(f'{Fore.RED}0-exit'.center(126))
            answer = int(input(f'{Fore.LIGHTWHITE_EX}\nplease enter option:\n\n>'))
            if not str(answer).isdigit():
                print(massages(2))
                game_menu()
            elif answer == 0:
                main_system.exit_fn()
            elif answer == 1:
                start_game()
            elif answer == 2:
                high_scores()
                print(massages(0))
            elif answer == 3:
                main_system.who_is_online()
                print(massages(0))
            elif answer == 4:
                main_system.menu()
            else:
                print(massages(1))


def time_fn(time_to_check):
    end_time = datetime.datetime.now()
    time_difference = end_time - time_to_check
    return time_difference


def massages(massage):
    massages_dict = {
        0: '',
        1: 'wrong input!!!'.center(130),
        2: 'use digits only!!!'.center(130),
        3: 'not enough players are logged in!!!'.center(130),
        4: "you are the only one who's logged in at the moment, please try again later.".center(130),
        5: f"correct answer {main_system.login_user['user_name']}!!! you've earned {str(points)} points".center(130),
        10: f"{main_system.login_user['user_name']}, you scored {str(points)} in this session".center(130),
        11: f"{name1}, you win!!! you've scored {str(points)} in this session, "
            f"{name2}, you scored {str(points)} in this session, but lost them all. better luck next time".center(130),
        12: f"{name2}, you win!!! you've scored {str(points)} in this session, "
            f"{name1}, you scored {str(points)} in this session, but lost them all. better luck next time".center(130),
        13: f"tie!!! you've earned {str(points)} coins for each player in this session".center(130),
        15: f"turn of player: {main_system.login_user['user_name']}".center(130),
        16: f"new high-score, {main_system.login_user['user_name']}!!!".center(130),
        18: f"game over!!!".center(130),
        100: ''
    }
    if massage == 100:
        print(massages_dict[massage])
        return input('press enter to continue...')
    elif massage in massages_dict.keys():
        print(massages_dict[massage])
        return ''
    else:
        print("*error* no such massage!!!")


def high_scores():
    print(f"{Fore.LIGHTWHITE_EX}---------------------------".center(124))
    with open("json_files/tic_tac_toe_hs.json") as file:
        score_list = json.load(file)
    count = 0
    for user in score_list:
        count += 1
        if count == 2:
            input('press enter to continue...')
            count = 0
        if user['rank'] == 0:
            break
        else:
            if user['difficulty'] == 'easy':
                the_color = Fore.LIGHTGREEN_EX
            elif user['difficulty'] == 'intermediate':
                the_color = Fore.LIGHTYELLOW_EX
            elif user['difficulty'] == 'hard':
                the_color = Fore.LIGHTRED_EX
            print(f"{Fore.LIGHTWHITE_EX}rank: {Fore.LIGHTBLUE_EX}{user['rank']}".center(130))
            print(f"{Fore.LIGHTWHITE_EX}player: {Fore.LIGHTYELLOW_EX}{user['name']}".center(130))
            print(f"{Fore.LIGHTWHITE_EX}high-score: {Fore.LIGHTBLUE_EX}{str(user['high_score'])}".center(130))
            print(f"{Fore.LIGHTWHITE_EX}difficulty: {the_color}{user['difficulty']}".center(130))
            print(f"{Fore.LIGHTWHITE_EX}date: {Fore.LIGHTBLUE_EX}{user['date_scored']}".center(130))
            print(f"{Fore.LIGHTWHITE_EX}play duration: {Fore.LIGHTBLUE_EX}{user['play_duration']}".center(130))
            print(f"{Fore.LIGHTWHITE_EX}---------------------------".center(124))
    return


def add_high_score(a_list):
    scores_list = a_list
    json_db = json.dumps(scores_list, indent=4, separators=(", ", " : "))
    with open("json_files/tic_tac_toe_hs.json", "w") as file:
        file.write(json_db)
    return


def check_user(password, user_id):
    main_system.login_user = main_system.logged_list[user_id]
    password = hashlib.md5(password.encode()).hexdigest()
    if password == main_system.login_user['password']:
        return True
    else:
        print('wrong password!')
        main_system.login_user = {}
        return False


def check_high_score(score, difficulty):
    global game_difficulty
    if game_difficulty == 1:
        game_difficulty = 'easy'
    if game_difficulty == 2:
        game_difficulty = 'intermediate'
    if game_difficulty == 3:
        game_difficulty = 'hard'
    with open("json_files/tic_tac_toe_hs.json")as file:
        scores_list = json.load(file)
    for i in scores_list:
        if i['rank'] != 0 and i['difficulty'] == game_difficulty:
            if score > i['high_score']:
                i['high_score'] = score
                i['name'] = win_name
                i['date_scored'] = main_system.today_date('day')
                print(i)
                add_high_score(scores_list)
                break
    for i in scores_list:
        if i['rank'] == 0 and i['name'] == win_name:
            if score > i['high_score']:
                i['name'] = win_name
                i['difficulty'] = game_difficulty
                i['high_score'] = score
                i['date_scored'] = main_system.today_date('day')
                add_high_score(scores_list)
                break
    print(massages(16))
    return


def add_player_points(add_points):
    for i in main_system.users_list:
        if i['user_name'] == main_system.login_user['user_name']:
            i['coins'] += add_points
    main_system.write_to_database(main_system.users_list)
    return add_points


def remove_player_points(remove_points):
    for i in main_system.users_list:
        if i['user_name'] == main_system.login_user['user_name']:
            i['coins'] += remove_points
    main_system.write_to_database(main_system.users_list)
    return remove_points


def add_to_personal_json(name, what):

    if what == 'last_game':
        var = 'Tic-Tac-Toe'
    elif what == 'difficulty':
        var = game_difficulty
        if var == 1:
            var = 'easy'
        elif var == 2:
            var = 'medium'
        elif var == 3:
            var = 'hard'
    elif what == 'high_score':
        var = points
    elif what == 'date_scored':
        var = main_system.today_date('day')
    elif what == 'play_duration':
        var = final_time
    else:
        print('something got wrong with adding to personal json')
        input("press enter to continue...")
        return False
    for i in all_score_list:
        if i['player'] == name:
            i[what] = var
    json_db = json.dumps(all_score_list, indent=4, separators=(", ", " : "))
    with open("json_files/persona_high_scores.json", "w") as file:
        file.write(json_db)
    return


def the_board(move, shape):
    global board_dict
    board = [f"\n{Fore.LIGHTWHITE_EX}",
             f"                                      a       b       c  ",
             f"                                  ┌───────┐ ┌───────┐ ┌───────┐",
             f"                                  │       │ │       │ │       │",
             f"                                1 │   {board_dict['a1']}   │ │   {board_dict['b1']}   │ │   {board_dict['c1']}   │",
             f"                                  │       │ │       │ │       │",
             f"                                  └───────┘ └───────┘ └───────┘",
             f"                                  ┌───────┐ ┌───────┐ ┌───────┐",
             f"                                  │       │ │       │ │       │",
             f"                                2 │   {board_dict['a2']}   │ │   {board_dict['b2']}   │ │   {board_dict['c2']}   │",
             f"                                  │       │ │       │ │       │",
             f"                                  └───────┘ └───────┘ └───────┘",
             f"                                  ┌───────┐ ┌───────┐ ┌───────┐",
             f"                                  │       │ │       │ │       │",
             f"                                3 │   {board_dict['a3']}   │ │   {board_dict['b3']}   │ │   {board_dict['c3']}   │",
             f"                                  │       │ │       │ │       │",
             f"                                  └───────┘ └───────┘ └───────┘\n"]
    for i in board_dict.keys():
        if move == 'a' and shape == '':
            return board
        if i == move:
            board_dict[move] = shape

    return board


def check_if_win(shape_to_check):
    global win

    def show_final_board():
        for i in the_board('a', ''):
            print(i)

    for i in board_dict:
        if board_dict.get('a1') == shape_to_check and board_dict.get('a2') == shape_to_check and board_dict.get('a3') == shape_to_check:
            show_final_board()
            print(shape_to_check + 'wins!!!')
            win = 1
            return True
        elif board_dict.get('b1') == shape_to_check and board_dict.get('b2') == shape_to_check and board_dict.get('b3') == shape_to_check:
            show_final_board()
            print(shape_to_check + 'wins!!!')
            win = 1
            return True
        elif board_dict.get('c1') == shape_to_check and board_dict.get('c2') == shape_to_check and board_dict.get('c3') == shape_to_check:
            show_final_board()
            print(shape_to_check + 'wins!!!')
            win = 1
            return True
        elif board_dict.get('a1') == shape_to_check and board_dict.get('b1') == shape_to_check and board_dict.get('c1') == shape_to_check:
            show_final_board()
            print(shape_to_check + 'wins!!!')
            win = 1
            return True
        elif board_dict.get('a2') == shape_to_check and board_dict.get('b2') == shape_to_check and board_dict.get('c2') == shape_to_check:
            show_final_board()
            print(shape_to_check + 'wins!!!')
            win = 1
            return True
        elif board_dict.get('a3') == shape_to_check and board_dict.get('b3') == shape_to_check and board_dict.get('c3') == shape_to_check:
            show_final_board()
            print(shape_to_check + 'wins!!!')
            win = 1
            return True
        elif board_dict.get('a1') == shape_to_check and board_dict.get('b2') == shape_to_check and board_dict.get('c3') == shape_to_check:
            show_final_board()
            print(shape_to_check + 'wins!!!')
            win = 1
            return True
        elif board_dict.get('a3') == shape_to_check and board_dict.get('b2') == shape_to_check and board_dict.get('c1') == shape_to_check:
            show_final_board()
            print(shape_to_check + 'wins!!!')
            win = 1
            return True
        else:
            return False


def start_game():
    print(len(main_system.logged_list))
    global shape, shape_2, name1, name2, num_of_players
    num_of_players = int(input("please enter number of players (1/2): "))
    shape = input("please pick a shape x or o:\n>")
    if shape == 'o':
        shape = f'{Fore.LIGHTYELLOW_EX}O{Fore.LIGHTWHITE_EX}'
        shape_2 = f'{Fore.LIGHTRED_EX}X{Fore.LIGHTWHITE_EX}'
    elif shape == 'x':
        shape = f'{Fore.LIGHTYELLOW_EX}X{Fore.LIGHTWHITE_EX}'
        shape_2 = f'{Fore.LIGHTRED_EX}O{Fore.LIGHTWHITE_EX}'

    if num_of_players == 1:
        while True:
            main_system.who_is_online()
            try:
                user_id = int(input(f"\n\n{Fore.LIGHTWHITE_EX}please choose a user by temp id: ")) - 1
                password = input("please enter your password: ")
            except ValueError:
                print("wrong input!!!")
                input("press enter to continue")
            else:
                name2 = 'computer'
                break
        if password == 'c':
            game_menu()
        elif check_user(password, user_id):
            players_list.append(main_system.logged_list[user_id])
            main_system.login_user = players_list[0]
            name1 = main_system.login_user['user_name']
            add_to_personal_json(name1, 'last_game')
            add_to_personal_json(name1, 'difficulty')
            add_to_personal_json(name1, 'date_scored')

    elif num_of_players == 2:
        main_system.who_is_online()
        while True:
            try:
                user_id = int(input(f"\n\n{Fore.LIGHTWHITE_EX}please choose a user by temp id: ")) - 1
                password = input("please enter your password: ")
            except ValueError:
                print("wrong input!!!")
                input("press enter to continue")
            else:
                break
        if password == 'c':
            game_menu()
        elif check_user(password, user_id):
            players_list.append(main_system.logged_list[0])
            name1 = main_system.login_user['user_name']
            add_to_personal_json(name1, 'last_game')
            add_to_personal_json(name1, 'difficulty')
            add_to_personal_json(name1, 'date_scored')
        while True:
            try:
                user_id = int(input(f"\n\n{Fore.LIGHTWHITE_EX}please choose a user by temp id: ")) - 1
                password = input("please enter your password: ")
            except ValueError:
                print("wrong input!!!")
                input("press enter to continue")
            else:
                break
            if password == 'c':
                game_menu()
            elif check_user(password, user_id):
                players_list.append(main_system.logged_list[1])
                name2 = main_system.login_user['user_name']
                add_to_personal_json(name2, 'last_game')
                add_to_personal_json(name2, 'difficulty')
                add_to_personal_json(name2, 'date_scored')
    game()


def check(list_to_check):
    global options, temp_options, move
    list1 = list(list_to_check.keys())
    list2 = list(list_to_check.values())
    for i in range(2):
        if list2[i] == ' ':
            print(list_to_check)
            temp_options.append(list1[i])
            continue
    if len(temp_options)-1 == 1:
        options.extend(temp_options)
        return True


def computer_ai_intermediate():
    global move
    win_list_a_vertical = {'a1': board_dict.get('a1'), 'a2': board_dict.get('a2'), 'a3': board_dict.get('a3')}
    win_list_b_vertical = {'b1': board_dict.get('b1'), 'b2': board_dict.get('b2'), 'b3': board_dict.get('b3')}
    win_list_c_vertical = {'c1': board_dict.get('c1'), 'c2': board_dict.get('c2'), 'c3': board_dict.get('c3')}

    win_list_1_horizontal = {'a1': board_dict.get('a1'), 'b1': board_dict.get('b1'), 'c1': board_dict.get('c1')}
    win_list_2_horizontal = {'a2': board_dict.get('a2'), 'b2': board_dict.get('b2'), 'c2': board_dict.get('c2')}
    win_list_3_horizontal = {'a3': board_dict.get('a3'), 'b3': board_dict.get('b3'), 'c3': board_dict.get('c3')}

    win_list_a_diagonal = {'a1': board_dict.get('a1'), 'b2': board_dict.get('b2'), 'c3': board_dict.get('c3')}
    win_list_c_diagonal = {'c1': board_dict.get('c1'), 'b2': board_dict.get('b2'), 'a3': board_dict.get('a3')}

    if check(win_list_a_vertical):
        pass
    elif check(win_list_b_vertical):
        pass
    elif check(win_list_c_vertical):
        pass
    elif check(win_list_1_horizontal):
        pass
    elif check(win_list_2_horizontal):
        pass
    elif check(win_list_3_horizontal):
        pass
    elif check(win_list_a_diagonal):
        pass
    elif check(win_list_c_diagonal):
        pass
    print(options)
    try:
        a_list = list(board_dict.values())
        b_list = list(board_dict.keys())
        new_list = []
        for i in range(len(a_list)-1):
            if a_list[i] != ' ':
                continue
            else:
                new_list.append(b_list[i])
                move = random.randrange(new_list(options)-1)
        return move
    except Exception:
        new_list = []
        print('exception')
        a_list = list(board_dict.values())
        b_list = list(board_dict.keys())
        for i in range(len(a_list)-1):
            if a_list[i] == (shape or shape_2):
                print(a_list[i])
                continue
            else:
                new_list.append(b_list[i])
                continue
        print(new_list)
        move = random.choice(new_list)
        print(move)
        return move


def game():
    global win, turn, full, shape, shape_2, win_name, win_shape
    while True:
        for i in the_board('a', shape):
            print(i)
        if full == 1 or win == 1:
            print("game over!!!")
            win = 0
            game_over()
        else:
            if turn == 0:
                main_system.login_user = players_list[0]
                move = input("please select an empty location on the board, marked by its row and column(a1,b2,c3): \n>")
                the_board(move, shape)
                if check_if_win(shape):
                    win_shape = shape
                    print("game over!!!")
                    win_name = name1
                    win = 0
                    game_over()
                else:
                    pass
            for i in the_board(move, shape):
                print(i)
            turn = 1
            if turn == 1:
                if num_of_players == 1:
                    input('computer turn, press enter to continue')
                    move = computer_ai_intermediate()
                    the_board(move, shape_2)
                elif num_of_players == 2:
                    main_system.login_user = players_list[1]
                    input('player 2 turn, press enter to continue')
                    while True:
                        move = input(
                            "please select an empty location on the board, marked by its row and column(a1,b2,c3): \n>")
                        if board_dict.get(move) == (shape or shape_2):
                            continue
                        else:
                            break
                    the_board(move, shape_2)

                if check_if_win(shape_2):
                    print("game over!!!")
                    win_name = name2
                    win = 0
                    game_over()
                else:
                    pass
                turn = 0
            for i in the_board(move, shape_2):
                print(i)

            check_list = []
            for i in board_dict.values():
                if len(check_list) == 9:
                    full = 1
                    continue
                else:
                    continue


def game_over():
    global turn, final_time, points, board_dict
    if num_of_players == 1:
        if shape == win_shape:
            check_high_score(points, game_difficulty)
            add_player_points(points)
            m, s = divmod(time_fn(init_time).total_seconds(), 60)
            final_time = f'{int(m // 60)}:{int(m % 60)}:{int(s)}'
            add_to_personal_json(win_name, 'play_duration')
            print(massages(10), massages(0))
        else:
            print('you lose, computer wins.')

    elif num_of_players == 2:
        if win_name == name1:
            main_system.login_user = players_list[0]
            check_high_score(points, game_difficulty)
            add_player_points(points*2)
            main_system.login_user = players_list[1]
            remove_player_points(points)
            m, s = divmod(time_fn(init_time).total_seconds(), 60)
            final_time = f'{int(m // 60)}:{int(m % 60)}:{int(s)}'
            add_to_personal_json(win_name, 'play_duration')
            print(massages(10), massages(0))

    for i in board_dict:
        board_dict[i] = ' '

    input('press enter to continue...')
    points = 0
    turn = 0
    game_menu()
