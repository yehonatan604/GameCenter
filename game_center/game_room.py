import main_system
from game_files import math_game, card_wars, hanging_man, tic_tac_toe
from art import *
from colorama import Fore
import json


def menu_list(num):
    full_list = {
        1: f'play Math Game',
        2: f'play Card Wars',
        3: f'play Hanging Man',
        4: f'play Tick Tack Toe',
        5: f'play Crack the Safe',
        6: f'play scrambled words',
        7: f'who is online',
        8: f'back to main menu',
        9: f'exit',
        10: f'change user'
    }
    return f'{Fore.LIGHTWHITE_EX}{int(num)} - {Fore.LIGHTYELLOW_EX}{full_list[num]}{Fore.LIGHTWHITE_EX}'


def game_room():
    with open("json_files/persona_high_scores.json") as file:
        score_list = json.load(file)
    for player in range(len(score_list) - 1):
        x = score_list[player]
        if x['player'] == main_system.user1_name:
            name = main_system.user1_name
            last_game = x['last_game']
            date_scored = x['date_scored']
            play_duration = x['play_duration']
            difficulty_color = Fore.LIGHTCYAN_EX
            try:
                difficulty = x['difficulty']
            except KeyError:
                difficulty = "normal"
                pass
            if difficulty == 'easy':
                difficulty_color = Fore.LIGHTGREEN_EX
            elif difficulty == ('intermediate' or 'normal'):
                difficulty_color = Fore.LIGHTYELLOW_EX
            if difficulty == 'hard':
                difficulty_color = Fore.LIGHTRED_EX

            print('\n\n\n')
            print(f"{Fore.LIGHTYELLOW_EX}{main_system.today_date('day')}" + f"{Fore.LIGHTWHITE_EX}user name - "
                                                                            f"{Fore.LIGHTYELLOW_EX}{name}".center(190))
            print(f"{Fore.LIGHTBLUE_EX}{main_system.today_date('time')}" + f"{Fore.LIGHTWHITE_EX}last game played: "
                                                                           f"{Fore.LIGHTCYAN_EX}{last_game}"
                                                                           f"".center(205))
            print(f"{Fore.LIGHTWHITE_EX}last time logged in: {Fore.LIGHTBLUE_EX}{str(date_scored)}".center(230))
            print(f"{Fore.LIGHTWHITE_EX}last play-time duration: {Fore.LIGHTBLUE_EX}{play_duration}".center(230))
            print(f"{Fore.LIGHTWHITE_EX}difficulty: {difficulty_color}{difficulty}{Fore.LIGHTGREEN_EX}\n\n\n".center(230))
            tprint(f'Game - Room'.center(85), font="small")
            print("\n")
            print(menu_list(1).center(70) + menu_list(4).center(42) + menu_list(7).center(64))
            print(menu_list(2).center(70) + menu_list(5).center(42) + menu_list(8).center(68))
            print(menu_list(3).center(72) + menu_list(6) + menu_list(9).center(58))
            print("\n" + menu_list(10).center(146) + Fore.LIGHTWHITE_EX)
            print("\n")

            option = input('\n\nplease enter choice: ')
            if option == '1':
                math_game.game_menu()
            elif option == '2':
                card_wars.game_menu()
            elif option == '3':
                hanging_man.game_menu()
            elif option == '4':
                tic_tac_toe.game_menu()
            elif option == '5':
                game_room()
            elif option == '6':
                game_room()
            elif option == '7':
                main_system.who_is_online()
            elif option == '8':
                main_system.menu()
            elif option == '9':
                main_system.exit_fn()
            elif option == '10':
                main_system.switch_user()
            else:
                print('wrong output')
            game_room()


for i in main_system.connect_to_database():
    if i['logged_in']:
        main_system. logged_list.append(i)
main_system.menu()
