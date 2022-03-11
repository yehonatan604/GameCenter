import main_system
import random
import json
import datetime
import hashlib
from art import *
from colorama import Fore

cards = ['2', '3', '4', '5', '6', '7', '8', '9', '0', 'J', 'Q', 'K', 'A']
sign = [f'♥', '♦', '♣', '♠']
player_deck = []
computer_deck = []
war_deck = []
name = ""
coins = 5
play_time = 0
with open("json_files/persona_high_scores.json") as f:
    all_score_list = json.load(f)


def time_fn(time_to_check):
    end_time = datetime.datetime.now()
    time_difference = end_time - time_to_check
    return time_difference


def cards_worth(card):
    cards_worth_dict = {
        '2': 2,
        '3': 3,
        '4': 4,
        '5': 5,
        '6': 6,
        '7': 7,
        '8': 8,
        '9': 9,
        '10': 10,
        'J': 11,
        'Q': 12,
        'K': 13,
        'A': 14,
    }
    worth = cards_worth_dict[card]
    return worth


def massages(massage):
    massages_dict = {
        0: '',
        1: f'{Fore.LIGHTRED_EX}wrong input!!!{Fore.LIGHTWHITE_EX}',
        2: f'{Fore.LIGHTRED_EX}use digits only!!!{Fore.LIGHTWHITE_EX}',
        3: f'{Fore.LIGHTRED_EX}no player is logged in!!!{Fore.LIGHTWHITE_EX}',
        4: f"{name} {Fore.LIGHTWHITE_EX}takes cards",
        5: f"computer {Fore.LIGHTWHITE_EX}takes cards",
        6: f"{Fore.LIGHTRED_EX}game over! {Fore.LIGHTYELLOW_EX}player {Fore.LIGHTWHITE_EX}wins {coins} coins",
        7: f"{Fore.LIGHTRED_EX}game over! {Fore.LIGHTYELLOW_EX}computer {Fore.LIGHTWHITE_EX}wins and {name} lose "
           f"{Fore.LIGHTBLUE_EX}{coins} {Fore.LIGHTWHITE_EX}coins",
        8: f"{Fore.LIGHTWHITE_EX}you can bet on {Fore.LIGHTBLUE_EX}"
           f"{str(main_system.login_user['coins'] + main_system.login_user['credit'])} {Fore.LIGHTWHITE_EX}"
           f"coins maximum",
        9: f"{Fore.LIGHTYELLOW_EX}{name} {Fore.LIGHTRED_EX}you don't have enough coins"
    }
    if massage in massages_dict.keys():
        print(massages_dict[massage])
        return ''
    else:
        return input('press enter to continue...')


def game_menu():
    global name
    with open("json_files/card_wars_hs.json") as file:
        score_list = json.load(file)
    for player in range(len(score_list) - 1):
        x = score_list[player]
        if x['name'] == main_system.user1_name and x['rank'] == 0:
            name = main_system.user1_name
    last_score = x['high_score']
    date_scored = x['date_scored']
    play_duration = x['play_duration']
    print('\n\n\n')
    print(f"{Fore.LIGHTWHITE_EX}{main_system.today_date('day')}" + f"{Fore.LIGHTWHITE_EX}user name -"
                                                                   f"{Fore.LIGHTYELLOW_EX}{name}".center(184))
    print(f"{Fore.LIGHTBLUE_EX}{main_system.today_date('time')}" + f"{Fore.LIGHTWHITE_EX}last high-score: "
                                                                   f"{Fore.LIGHTBLUE_EX}{str(last_score)}".center(205))
    print(f"{Fore.LIGHTWHITE_EX}last time played: {Fore.LIGHTBLUE_EX}{str(date_scored)}".center(230))
    print(f"{Fore.LIGHTWHITE_EX}last play-time duration: {Fore.LIGHTBLUE_EX}{play_duration}\n\n{Fore.LIGHTGREEN_EX}".center(230))
    tprint(f'Card Wars'.center(85), font="small")
    print("\n")
    print(f"{Fore.LIGHTYELLOW_EX}1-play".center(127))
    print(f'{Fore.MAGENTA}2-high scores'.center(126))
    print(f'{Fore.MAGENTA}3-who is online'.center(126))
    print(f'{Fore.RED}4-main menu'.center(126))
    print(f'{Fore.RED}0-exit'.center(126))
    try:
        answer = int(input(f'{Fore.LIGHTWHITE_EX}\nplease enter option:'))
    except ValueError:
        print(massages(2))
        game_menu()
    else:
        if answer == 0:
            main_system.exit_fn()
        elif answer == 1:
            if len(main_system.logged_list) == 0:
                print(massages(3))
                game_menu()
            start_game()
        elif answer == 2:
            high_scores()
            print(massages(0))
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


def high_scores():
    print(f"{Fore.LIGHTWHITE_EX}---------------------------".center(124))
    with open("json_files/card_wars_hs.json") as file:
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
            print(f"{Fore.LIGHTWHITE_EX}rank: {Fore.LIGHTBLUE_EX}{user['rank']}".center(130))
            print(f"{Fore.LIGHTWHITE_EX}player: {Fore.LIGHTYELLOW_EX}{user['name']}".center(130))
            print(f"{Fore.LIGHTWHITE_EX}high-score: {Fore.LIGHTBLUE_EX}{str(user['high_score'])}".center(130))
            print(f"{Fore.LIGHTWHITE_EX}date: {Fore.LIGHTBLUE_EX}{user['date_scored']}".center(130))
            print(f"{Fore.LIGHTWHITE_EX}play duration: {Fore.LIGHTBLUE_EX}{user['play_duration']}".center(130))
            print(f"{Fore.LIGHTWHITE_EX}---------------------------".center(124))
    return


def add_to_personal_json(a_name, what):

    if what == 'last_game':
        var = 'Card Wars'
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
    with open("json_files/card_wars_hs.json", "w") as file:
        file.write(json_db)
    return


def check_high_score():
    with open("json_files/card_wars_hs.json")as file:
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


def shuffle():
    global player_deck, computer_deck
    while len(player_deck) < 26:
        random_card = random.choice(cards)
        if player_deck.count(random_card) != 4:
            player_deck.append(random_card)
        else:
            continue
    while len(computer_deck) < 26:
        random_card = random.choice(cards)
        if computer_deck.count(random_card) != 4:
            computer_deck.append(random_card)
        else:
            continue

    for i in range(len(player_deck)):
        random_sign = random.choice(sign)
        if random_sign in player_deck[i]:
            continue
        else:
            player_deck[i] = (player_deck[i] + ' ' + random_sign)
    for i in range(len(computer_deck)):
        random_sign = random.choice(sign)
        if random_sign in computer_deck[i]:
            continue
        computer_deck[i] = (computer_deck[i] + ' ' + random_sign)
    return


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
    global name, coins
    print("in every turn computer pick a card & player pick a card, if player card is higher, player take cards,\n"
          "if computer card is higher, computer take cards, if theres tie, each player draws another card,\n until"
          "someone takes all cards\n"
          "the loser is the one that stays without any cards.\n")

    main_system.who_is_online()
    while True:
        try:
            user_id = int(input(f"\n\n{Fore.LIGHTWHITE_EX}please choose a user by temp id: ")) - 1
            password = input("please enter your password: ")
        except ValueError:
            print("wrong input!!!")
            input("press enter to continue")
            start_game()
        else:
            main_system.login_user = main_system.logged_list[user_id]
            name = main_system.login_user['user_name']
            break
    if password == 'c':
        game_menu()
    elif check_user(password, user_id):
        main_system.login_user = main_system.logged_list[user_id]
    print(massages(8))
    coins = int(input(f"on how much coins would you like to bet {name}?"))
    if coins > (main_system.login_user['coins']) + main_system.login_user['credit']:
        print(massages(9))
        start_game()

    game()
    
    
def game():
    global play_time, coins
    shuffle()
    start_time = datetime.datetime.now()
    while True:
        random_computer_card = random.choice(computer_deck)
        for i in range(len(player_deck)):
            card = player_deck[i]
            if card[0] == '0':
                player_deck[i] = '10 ' + card[2]
            print(f"{Fore.LIGHTWHITE_EX}{str(i + 1)} - {Fore.LIGHTRED_EX}{player_deck[i]}")

        player_select = input(f'{Fore.LIGHTWHITE_EX}\nplease select a card, enter '
                              f'{Fore.LIGHTBLUE_EX}100{Fore.LIGHTWHITE_EX} for random card: ')
        if player_select == '100':
            player_card = random.choice(player_deck)
        else:
            player_card = player_deck[int(player_select)-1]

        try:
            player_card_worth = cards_worth(player_card[0])
        except KeyError:
            player_card_worth = 10

        computer_card = random_computer_card
        try:
            computer_card_worth = cards_worth(computer_card[0])
        except KeyError:
            computer_card_worth = 10

        player_shape = player_card[len(player_card) - 1]
        computer_shape = computer_card[len(computer_card) - 1]
        print(f"\n    {Fore.LIGHTWHITE_EX}player card        computer card")
        print(f"      {Fore.LIGHTRED_EX}{player_shape} {player_shape}  {player_shape} {player_shape}      "
              f"      {computer_shape} {computer_shape}  {computer_shape} {computer_shape}  {Fore.LIGHTYELLOW_EX}")

        a_card = ''
        if player_card[1] == '0':
            a_card = '0'
        else:
            a_card = player_card
        tprint(f"\n{a_card} {computer_card}", font="block", chr_ignore=True)

        print(f"      {Fore.LIGHTRED_EX}{player_shape} {player_shape}  {player_shape} {player_shape}      "
              f"      {computer_shape} {computer_shape}  {computer_shape} {computer_shape}{Fore.LIGHTWHITE_EX}")

        if player_card_worth > computer_card_worth:
            print(massages(4,))
            print(massages(70,))
            player_deck.append(computer_card)
            computer_deck.remove(computer_card)
            player_deck.extend(war_deck)
            war_deck.clear()
        elif computer_card_worth > player_card_worth:
            print(massages(5,))
            print(massages(70,))
            computer_deck.append(player_card)
            player_deck.remove(player_card)
            computer_deck.extend(war_deck)
            war_deck.clear()
        else:
            print("WAR!!!")
            print(massages(70,))
            war_deck.append(computer_card)
            war_deck.append(player_card)
            player_deck.remove(player_card)
            computer_deck.remove(computer_card)

        if len(computer_deck) == 0:
            m, s = divmod(time_fn(start_time).total_seconds(), 60)
            play_time = f'{int(m // 60)}:{int(m % 60)}:{int(s)}'
            check_high_score()
            print(massages(6))
            add_player_coins(coins)
            add_to_personal_json(name, 'high_score')
            add_to_personal_json(name, 'last_game')
            add_to_personal_json(name, 'date_scored')
            add_to_personal_json(name, 'play_duration')
            game_menu()
        elif len(player_deck) == 0:
            print(massages(7))
            remove_player_coins(coins)
            coins = -coins
            add_to_personal_json(name, 'high_score')
            add_to_personal_json(name, 'last_game')
            add_to_personal_json(name, 'date_scored')
            add_to_personal_json(name, 'play_duration')
            game_menu()
