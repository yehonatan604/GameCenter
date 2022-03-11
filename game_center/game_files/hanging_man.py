import main_system
import random
import datetime
import json
import hashlib
from colorama import Fore, Style
from art import *

name = ""
coins = 10
score = 0
guesses = 5
subject = ''
start_time = 0
game_difficulty = 0
game_vocabulary = []
used_vocabulary = []
play_time = 0
a_number = 4

with open("json_files/persona_high_scores.json") as f:
    all_score_list = json.load(f)

vocabulary = [
    ['paris', 'london', 'jerusalem', 'washington', 'madrid', 'rome', 'mexico city', 'oslo', 'belgrade', 'cairo', 'riga',
     'luxembourg ', 'guatemala city', 'islamabad', 'copenhagen', 'rabat', 'baku', 'male', 'berlin', 'amsterdam'],
    ['afghanistan', 'united states of america', 'israel', 'japan', 'germany', 'china', 'morocco', 'chad', 'mali',
     'nepal', 'bulgaria', 'bolivia', 'thailand', 'new zealand', 'cambodia', 'san marino', 'solomon islands', 'jamaica'],
    ['lemon', 'orange', 'watermelon', 'melon', 'strawberry', 'pineapple', 'passion fruit', 'mango', 'kiwi', 'banana',
     'apple', 'blueberry', 'carambola', 'clementine', 'durian', 'grapefruit', 'pomegranate', 'raspberry', 'cranberry'],
    ['artichoke', 'asparagus', 'green beans', 'celery', 'tomato', 'onion', 'cucumber', 'garlic', 'carrot', 'potato',
     'spinach', 'zucchini', 'corn', 'leak', 'parsley', 'rosemary', 'basil', 'cabbage', 'mushroom', 'chili pepper']
]


def massages(massage):
    massages_dict = {
        0: '',
        1: f'{Fore.LIGHTRED_EX}wrong input!!!{Fore.LIGHTWHITE_EX}',
        2: f'{Fore.LIGHTRED_EX}use digits only!!!{Fore.LIGHTWHITE_EX}',
        3: f'{Fore.LIGHTRED_EX}no player is logged in!!!{Fore.LIGHTWHITE_EX}',
        4: f"{Fore.LIGHTRED_EX}game over!!!{Fore.LIGHTWHITE_EX}",
        5: f"{Fore.LIGHTYELLOW_EX}{name},{Fore.LIGHTWHITE_EX} you win "
           f"{Fore.LIGHTBLUE_EX}{score}{Fore.LIGHTWHITE_EX} coins!",
        6: f"{Fore.LIGHTYELLOW_EX}{name},{Fore.LIGHTWHITE_EX} you lose "
           f"{Fore.LIGHTBLUE_EX}{coins}{Fore.LIGHTWHITE_EX} coins!",
        7: f"{Fore.LIGHTYELLOW_EX}{name}, {Fore.LIGHTRED_EX}you don't have enough coins{Fore.LIGHTWHITE_EX}"
    }
    if massage in massages_dict.keys():
        print(massages_dict[massage])

    return input('press enter to continue...')


def game_menu():
    global name
    with open("json_files/hanging_man_hs.json") as file:
        score_list = json.load(file)
    for player in range(len(score_list) - 1):
        x = score_list[player]
        if x['name'] == main_system.user1_name and x['rank'] == 0:
            name = main_system.login_user['user_name']
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
                                                                           f"{Fore.LIGHTYELLOW_EX}{name}".center(190))
            print(f"{Fore.LIGHTBLUE_EX}{main_system.today_date('time')}" + f"{Fore.LIGHTWHITE_EX}last high-score: "
                                                                           f"{Fore.LIGHTBLUE_EX}{str(last_score)}"
                                                                           f"".center(205))
            print(f"{Fore.LIGHTWHITE_EX}last time played: {Fore.LIGHTBLUE_EX}{str(date_scored)}".center(230))
            print(f"{Fore.LIGHTWHITE_EX}last play-time duration: {Fore.LIGHTBLUE_EX}{play_duration}".center(230))
            print(f"{Fore.LIGHTWHITE_EX}difficulty: {difficulty_color}{difficulty}\n\n{Fore.LIGHTGREEN_EX}".center(230))
            tprint(f'Hanging Man'.center(85), font="small")
            print("\n")
            print(f"{Fore.LIGHTYELLOW_EX}1-play".center(130))
            print(f'{Fore.MAGENTA}2-high scores'.center(130))
            print(f'{Fore.MAGENTA}3-who is online'.center(130))
            print(f'{Fore.RED}4-main menu'.center(130))
            print(f'{Fore.RED}0-exit'.center(130))
            answer = int(input(f'{Fore.LIGHTWHITE_EX}\nplease enter option:\n\n>'))
            if not str(answer).isdigit():
                print(massages(2))
                game_menu()
            elif answer == 0:
                main_system.exit_fn()
            elif answer == 1:
                if len(main_system.logged_list) == 0:
                    print(massages(3))
                    game_menu()
                start_game()
            elif answer == 2:
                high_scores()
            elif answer == 3:
                if len(main_system.logged_list) == 0:
                    print(massages(3))
                    game_menu()
                main_system.who_is_online()
                print(massages(0))
            elif answer == 4:
                main_system.menu()
            else:
                print(massages(1))
            game_menu()


def add_to_personal_json(a_name, what):

    if what == 'last_game':
        var = 'Hanging Man'
    elif what == 'high_score':
        var = coins
    elif what == 'difficulty':
        var = game_difficulty
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
    with open("json_files/hanging_man_hs.json", "w") as file:
        file.write(json_db)
    return


def check_high_score():
    global game_difficulty
    if game_difficulty == 1:
        game_difficulty = 'normal'
    elif game_difficulty == 2:
        game_difficulty = 'intermediate'
    with open("json_files/hanging_man_hs.json") as file:
        scores_list = json.load(file)
    for i in scores_list:
        if i['rank'] != 0 and i['difficulty'] == game_difficulty:
            if coins > i['high_score']:
                i['name'] = name
                i['difficulty'] = game_difficulty
                i['high_score'] = coins
                i['date_scored'] = main_system.today_date('day')
                i['play_duration'] = play_time
                add_high_score(scores_list)
                break
    for i in scores_list:
        if i['rank'] == 0 and i['name'] == name:
            if coins > i['high_score']:
                i['name'] = name
                i['difficulty'] = game_difficulty
                i['high_score'] = coins
                i['date_scored'] = main_system.today_date('day')
                i['play_duration'] = play_time
                add_high_score(scores_list)
                break
    return


def high_scores():
    print(f"{Fore.LIGHTWHITE_EX}---------------------------".center(124))
    with open("json_files/hanging_man_hs.json") as file:
        score_list = json.load(file)
    count = 0
    for user in score_list:
        count += 1
        if count == 2:
            count = 0
            print(massages(0))
        if user['rank'] == 0:
            break
        else:
            if user['difficulty'] == 'normal':
                the_color = Fore.LIGHTGREEN_EX
            elif user['difficulty'] == 'intermediate':
                the_color = Fore.LIGHTRED_EX
            print(f"{Fore.LIGHTWHITE_EX}rank: {Fore.LIGHTBLUE_EX}{user['rank']}".center(130))
            print(f"{Fore.LIGHTWHITE_EX}player: {Fore.LIGHTYELLOW_EX}{user['name']}".center(130))
            print(f"{Fore.LIGHTWHITE_EX}high-score: {Fore.LIGHTBLUE_EX}{str(user['high_score'])}".center(130))
            print(f"{Fore.LIGHTWHITE_EX}difficulty: {the_color}{user['difficulty']}".center(130))
            print(f"{Fore.LIGHTWHITE_EX}date: {Fore.LIGHTBLUE_EX}{user['date_scored']}".center(130))
            print(f"{Fore.LIGHTWHITE_EX}play duration: {Fore.LIGHTBLUE_EX}{user['play_duration']}".center(130))
            print(f"{Fore.LIGHTWHITE_EX}---------------------------".center(124))
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
            i['coins'] -= remove_points
    main_system.write_to_database(main_system.users_list)
    return remove_points


def time_fn(time_to_check):
    end_time = datetime.datetime.now()
    time_difference = end_time - time_to_check
    return time_difference


def random_word(vocabulary_type):
    global game_vocabulary, subject
    game_vocabulary = []
    while True:
        if vocabulary_type == 0:
            subject = 'cities around the world'
            game_vocabulary.extend(vocabulary[0])
            break
        elif vocabulary_type == 1:
            subject = 'countries around the world'
            game_vocabulary.extend(vocabulary[1])
            break
        elif vocabulary_type == 2:
            subject = 'fruits'
            game_vocabulary.extend(vocabulary[2])
            break
        elif vocabulary_type == 3:
            subject = 'vegetables'
            game_vocabulary.extend(vocabulary[3])
            break
        else:
            continue

    num = random.randrange(len(game_vocabulary)-1)
    word = game_vocabulary[num]
    return word


def check_user(password, user_id):
    login_user = main_system.logged_list[user_id]
    password = hashlib.md5(password.encode()).hexdigest()
    if password == login_user['password']:
        return True
    else:
        print('wrong password!')
        main_system.login_user = {}
        return False


def start_game():
    global game_difficulty, coins, guesses, name, start_time
    main_system.who_is_online()
    while True:
        try:
            user_id = int(input(f'{Fore.LIGHTWHITE_EX}please enter user id:\n')) - 1
            password = input("please enter your password, c to cancel: ")
        except  ValueError:
            print("wrong input!!!")
            input("press enter to continue")
        else:
            break
    if password == 'c':
        game_menu()
    elif check_user(password, user_id):
        main_system.login_user = main_system.logged_list[user_id]
        name = main_system.login_user['user_name']
    else:
        print(massages(1), massages(0))
        game_menu()
    guesses = 5
    vocabulary_type = random.randrange(len(vocabulary)-1)
    game_difficulty = int(input(f"\n{Fore.LIGHTWHITE_EX}1- {Fore.LIGHTGREEN_EX}normal\n{Fore.LIGHTWHITE_EX}"
                                f"2- {Fore.LIGHTYELLOW_EX}intermediate\n{Fore.LIGHTWHITE_EX}"
                                f"3- {Fore.LIGHTRED_EX}challenge mode\n\n{Fore.LIGHTWHITE_EX}"
                                f"please choose difficulty: "))
    start_time = datetime.datetime.now()
    if game_difficulty == 1:
        coins = 10
        time_limit = 60
        while True:
            word = random_word(vocabulary_type)
            if len(word) > 7:
                continue
            else:
                game(time_limit, word)
    elif game_difficulty == 2:
        coins = 20
        time_limit = 30
        while True:
            word = random_word(vocabulary_type)
            if len(word) <= 7:
                continue
            else:
                game(time_limit, word)
    elif game_difficulty == 3:
        coins = 40
        time_limit = 20
        challenge_mode(time_limit)
    else:
        print(massages(1))
        start_game()


def game_over():
    global guesses, play_time, coins
    guesses = 5
    print(massages(4))
    m, s = divmod(time_fn(start_time).total_seconds(), 60)
    play_time = f'{int(m // 60)}:{int(m % 60)}:{int(s)}'
    if score == 0:
        print(massages(6))
        remove_player_coins(coins)
        coins = 0
        add_to_personal_json(name, 'high_score')
        add_to_personal_json(name, 'last_game')
        add_to_personal_json(name, 'difficulty')
        add_to_personal_json(name, 'date_scored')
        add_to_personal_json(name, 'play_duration')
    else:
        add_to_personal_json(name, 'high_score')
        add_to_personal_json(name, 'last_game')
        add_to_personal_json(name, 'difficulty')
        add_to_personal_json(name, 'date_scored')
        add_to_personal_json(name, 'play_duration')
        check_high_score()
        print(massages(5))
        add_player_coins(score)

    game_menu()


def board(word, guess):
    guess_array = []
    word_array = []
    if len(guess) != len(word):
        return 'wrong number of characters!!!'
    else:
        for i in word:
            word_array.append(i)
        for i in range(len(guess)):
            if guess[i] == word_array[i]:
                guess_array.append(guess[i])
            else:
                guess_array.append('*')
        show_word = ''.join(guess_array)

    return show_word


def challenge_mode(time_limit):
    global game_vocabulary, subject, score, guesses, used_vocabulary
    vocabulary_type = random.randrange(3)
    game_vocabulary = []
    while True:
        if vocabulary_type == 0:
            subject = 'cities around the world'
            game_vocabulary.extend(vocabulary[0])
            break
        elif vocabulary_type == 1:
            subject = 'countries around the world'
            game_vocabulary.extend(vocabulary[1])
            break
        elif vocabulary_type == 2:
            subject = 'fruits'
            game_vocabulary.extend(vocabulary[2])
            break
        elif vocabulary_type == 3:
            subject = 'vegetables'
            game_vocabulary.extend(vocabulary[3])
            break
        else:
            continue
    num = random.randrange(len(game_vocabulary) - 1)

    def the_word():
        global a_number
        wordd = game_vocabulary[num]
        while True:
            if len(wordd)-1 == a_number:
                a_number += 1
                return wordd
            else:
                challenge_mode(time_limit)

    word = the_word()
    drawing = [
        f'{Fore.LIGHTRED_EX}               |     ',
        f'{Fore.LIGHTRED_EX}               O     ',
        f'{Fore.LIGHTRED_EX}              \\|/   ',
        f'{Fore.LIGHTRED_EX}               |     ',
        f'{Fore.LIGHTRED_EX}              / \\   ',
    ]
    game_drawing = []
    drawing_count = 0
    guesses = 5
    while guesses != 0:
        print(word)
        m, s = divmod(time_fn(start_time).total_seconds(), 60)
        if s > time_limit:
            game_over()
        else:
            print(f'{Fore.LIGHTYELLOW_EX}             _____   ')
            for i in game_drawing:
                print(i)
            guess_word = input(
                f"\n\n{Fore.LIGHTWHITE_EX}please guess the word, subject is  - {Fore.LIGHTBLUE_EX}{subject}"
                f"{Fore.LIGHTWHITE_EX}, you have {Fore.LIGHTBLUE_EX}{str(guesses)}{Fore.LIGHTWHITE_EX} guesses left\n"
                f"the word has {Fore.LIGHTBLUE_EX}{len(word)}{Fore.LIGHTWHITE_EX} characters:\n>")
            print(f"{Fore.LIGHTYELLOW_EX}word - {board(word, guess_word)}{Fore.LIGHTWHITE_EX}".center(80))
            if guess_word == 'stop':
                game_over()
            elif guess_word != word:
                guesses -= 1
                drawing_count += 1
                game_drawing.append(drawing[drawing_count - 1])
                continue
            elif guess_word == word:
                used_vocabulary.append(word)
                score += coins
                if len(used_vocabulary)-1 == 73:
                    print(f'{Fore.LIGHTWHITE_EX}congratulations {Fore.LIGHTYELLOW_EX}{name}{Fore.LIGHTWHITE_EX}'
                          f'! you win the game! you get extra {Fore.LIGHTBLUE_EX}200{Fore.LIGHTWHITE_EX} coins!!!')
                    score += 200
                    game_over()
                if len(word) == 24:
                    a_number = 4
                else:
                    guesses = 0
                    drawing_count = 0
                    challenge_mode(time_limit)

    print('             _____   ')
    for i in game_drawing:
        print(i)
    print(massages(4))
    game_over()


def game(time_limit, word):
    global score, guesses, used_vocabulary
    drawing = [
               f'{Fore.LIGHTRED_EX}               |     ',
               f'{Fore.LIGHTRED_EX}               O     ',
               f'{Fore.LIGHTRED_EX}              \\|/   ',
               f'{Fore.LIGHTRED_EX}               |     ',
               f'{Fore.LIGHTRED_EX}              / \\   ',
            ]
    game_drawing = []
    drawing_count = 0
    while guesses != 0:
        m, s = divmod(time_fn(start_time).total_seconds(), 60)
        if s > time_limit:
            game_over()
        else:
            print('             _____   ')
            for i in game_drawing:
                print(i)
            guess_word = input(f"\n\n{Fore.LIGHTWHITE_EX}please guess the word, subject is  - "
                               f"{Fore.LIGHTBLUE_EX}{subject}{Fore.LIGHTWHITE_EX}, you have {Fore.LIGHTBLUE_EX}"
                               f"{str(guesses)}{Fore.LIGHTWHITE_EX} guesses left\n"
                               f"the word has {Fore.LIGHTBLUE_EX}{len(word)}{Fore.LIGHTWHITE_EX} characters:\n>")
            print(f"word - {board(word, guess_word)}".center(80))
            print(word)
            if guess_word == 'stop':
                game_over()
            elif guess_word != word:
                guesses -= 1
                drawing_count += 1
                game_drawing.append(drawing[drawing_count-1])
                continue
            elif guess_word == word:
                used_vocabulary.append(word)
                score += coins
                vocabulary_type = random.randrange(len(vocabulary)-1)
                while True:
                    word = random_word(vocabulary_type)
                    if word in used_vocabulary:
                        continue
                    else:
                        guesses = 0
                        drawing_count = 0
                        game(time_limit, word)
                
    print('             _____   ')
    for i in game_drawing:
        print(i)
    game_over()
