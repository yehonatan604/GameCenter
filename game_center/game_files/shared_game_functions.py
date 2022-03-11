import main_system
import json
import datetime
from art import *
from colorama import Fore

with open("json_files/persona_high_scores.json") as f:
    all_score_list = json.load(f)


def time_fn(time_to_check):
    end_time = datetime.datetime.now()
    time_difference = end_time - time_to_check
    return time_difference


def game_menu(game):
    with open("json_files/math_game_hs.json") as file:
        score_list = json.load(file)
    for player in range(len(score_list) - 1):
        x = score_list[player]
        if x['name'] == main_system.user1_name and x['rank'] == 0:
            name = main_system.user1_name
            last_score = x['high_score']
            date_scored = x['date_scored']
            play_duration = x['play_duration']
            difficulty = x['difficulty']
            print('\n\n\n')
            print(f"{Fore.LIGHTCYAN_EX}{main_system.today_date('day')}" + f"user name -{name}".center(184))
            print(f"{Fore.LIGHTCYAN_EX}{main_system.today_date('time')}" + f"last high-score: {str(last_score)}".center(205))
            print(f"{Fore.LIGHTCYAN_EX}last time played: {str(date_scored)}")
            print(f"{Fore.LIGHTCYAN_EX}last play-time duration: {play_duration}")
            print(f"{Fore.LIGHTCYAN_EX}difficulty: {difficulty}\n\n{Fore.LIGHTGREEN_EX}")
            tprint(f'{game}'.center(85), font="small")
            print("\n")
            print(f"{Fore.LIGHTYELLOW_EX}1-play".center(127))
            print(f'{Fore.MAGENTA}2-high scores'.center(126))
            print(f'{Fore.MAGENTA}3-who is online'.center(126))
            print(f'{Fore.RED}4-main menu'.center(126))
            print(f'{Fore.RED}0-exit'.center(126))
            answer = int(input(f'{Fore.LIGHTWHITE_EX}\nplease enter option:\n\n>'))
            if not str(answer).isdigit():
                print(game.massages(2))
                game_menu(game)
            elif answer == 0:
                main_system.exit_fn()
            elif answer == 1:
                game.start_game()
            elif answer == 2:
                high_scores()
                print(game.massages(0))
            elif answer == 3:
                main_system.who_is_online()
                print(game.massages(0))
            elif answer == 4:
                main_system.menu()
            else:
                print(game.massages(1))


def high_scores():
    print("----------------------")
    with open("json_files/card_wars_hs.json") as file:
        score_list = json.load(file)
    for user in score_list:
        if user['rank'] == 0:
            break
        else:
            print(f"rank: {user['rank']}\n"
                  f"player: {user['name']}\n"
                  f"high-score: {str(user['high_score'])}\n"
                  f"date: {user['date_scored']}\n"
                  f"play duration: {user['play_duration']}")
            print("----------------------")

    return


def add_to_personal_json(a_name, what):

    if what == 'last_game':
        var = 'Math Game'
    elif what == 'high_score':
        var = coins
    elif what == 'date_scored':
        var = main_system.today_date('day')
    elif what == 'play_duration':
        var = play_time
    else:
        print('something got wrong with adding to personal json')
        input("press enter to continue...")
        return False
    for i in all_score_list:
        if i['player'] == a_name:
            i[what] = var
    json_db = json.dumps(all_score_list, indent=4, separators=(", ", " : "))
    with open("json_files/persona_high_scores.json", "w") as file:
        file.write(json_db)
    return


def add_high_score(a_list):
    scores_list = a_list
    json_db = json.dumps(scores_list, indent=4, separators=(", ", " : "))
    with open("json_files/math_game_hs.json", "w") as file:
        file.write(json_db)
    return


def check_high_score():
    with open("json_files/hanging_man_hs.json")as file:
        scores_list = json.load(file)
    for i in scores_list:
        if i['rank'] != 0:
            if coins > i['high_score']:
                i['high_score'] = coins
                add_high_score(scores_list)
                break
    for i in scores_list:
        if i['rank'] == 0 and i['name'] == main_system.login_user['user_name']:
            if coins > i['high_score']:
                i['name'] = main_system.login_user['user_name']
                i['high_score'] = coins
                i['date_scored'] = main_system.today_date('day')
                i['play_duration'] = play_time
                add_high_score(scores_list)
                break
    print(massages(16))
    return


def add_player_coins(add_points):
    for i in main_system.users_list:
        if i['user_name'] == main_system.login_user['user_name']:
            i['coins'] += add_points
    main_system.write_to_database(main_system.users_list)
    return add_points


def remove_player_coins(remove_points):
    for i in main_system.users_list:
        if i['user_name'] == main_system.login_user['user_name']:
            i['coins'] += remove_points
    main_system.write_to_database(main_system.users_list)
    return remove_points
