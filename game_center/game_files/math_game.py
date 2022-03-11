from decimal import Decimal
import random
import datetime
import operator
import json
import main_system
import hashlib
from colorama import Fore, Style
from art import *

init_time = datetime.datetime.now()
final_time = 0
questions = 0
name = ''
name1 = ''
name2 = ''
lives = 5
players = 1
time_limit = 15
points = 0
sum_points = 0
sum_points_player2 = 0
turn = 0
game_difficulty = 1
players_list = []

with open("json_files/persona_high_scores.json") as f:
    all_score_list = json.load(f)

operator_lookup = {
    '+': operator.add,
    '-': operator.sub,
    '*': operator.mul,
    '/': operator.truediv
}
# ================================================= game menu ==========================================================


def game_menu():
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
            difficulty_color = Fore.LIGHTYELLOW_EX
            if difficulty == 'easy':
                difficulty_color = Fore.LIGHTGREEN_EX
            elif difficulty == ('intermediate' or 'normal'):
                difficulty_color = Fore.LIGHTYELLOW_EX
            if difficulty == 'hard':
                difficulty_color = Fore.LIGHTRED_EX
            print('\n\n\n')
            print(f"{Fore.LIGHTWHITE_EX}{main_system.today_date('day')}" + f"{Fore.LIGHTWHITE_EX}user name -"
                                                                           f"{Fore.LIGHTYELLOW_EX}{name}".center(174))
            print(f"{Fore.LIGHTBLUE_EX}{main_system.today_date('time')}" + f"{Fore.LIGHTWHITE_EX}last high-score: "
                                                                           f"{Fore.LIGHTBLUE_EX}{str(last_score)}"
                                                                           f"".center(205))
            print(f"{Fore.LIGHTWHITE_EX}last time played: {Fore.LIGHTBLUE_EX}{str(date_scored)}".center(230))
            print(f"{Fore.LIGHTWHITE_EX}last play-time duration: {Fore.LIGHTBLUE_EX}{play_duration}".center(230))
            print(f"{Fore.LIGHTWHITE_EX}difficulty: {difficulty_color}{difficulty}\n\n{Fore.LIGHTGREEN_EX}".center(230))
            tprint(f'Math Game'.center(85), font="small")
            print("\n")
            print(f"{Fore.LIGHTYELLOW_EX}1-play".center(126))
            print(f'{Fore.MAGENTA}2-high scores'.center(126))
            print(f'{Fore.MAGENTA}3-who is online'.center(126))
            print(f'{Fore.RED}4-main menu'.center(126))
            print(f'{Fore.RED}0-exit'.center(126))
            for i in main_system.logged_list:
                players_list.append(i)
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
# ================================================= system functions ===================================================


def time_fn(time_to_check):
    end_time = datetime.datetime.now()
    time_difference = end_time - time_to_check
    return time_difference


def massages(massage):
    massages_dict = {
        0: '',
        1: f'{Fore.LIGHTYELLOW_EX}wrong input!!!{Fore.LIGHTWHITE_EX}'.center(130),
        2: f'{Fore.LIGHTRED_EX}use digits only!!!{Fore.LIGHTWHITE_EX}'.center(130),
        3: f'{Fore.LIGHTRED_EX}not enough players are logged in!!!{Fore.LIGHTWHITE_EX}'.center(130),
        4: f"{Fore.LIGHTRED_EX}you are the only one who's logged in at the moment, "
           f"{Fore.LIGHTWHITE_EX}please try again later".center(130),
        5: f"{Fore.LIGHTGREEN_EX}correct answer {Fore.LIGHTYELLOW_EX}{main_system.login_user['user_name']}!!! "
           f"{Fore.LIGHTWHITE_EX}you've earned {Fore.LIGHTBLUE_EX}{str(points)} points{Fore.LIGHTWHITE_EX}".center(130),
        6: f"{Fore.LIGHTRED_EX}wrong answer {Fore.LIGHTYELLOW_EX}{main_system.login_user['user_name']}!!! "
           f"{Fore.LIGHTBLUE_EX}{str(lives)}{Fore.LIGHTWHITE_EX} lives left".center(130),
        7: f"{Fore.LIGHTRED_EX}too much time {Fore.LIGHTYELLOW_EX}{main_system.login_user['user_name']}!!! "
           f"{Fore.LIGHTBLUE_EX}{str(lives)}{Fore.LIGHTWHITE_EX} lives left".center(130),
        8: f"{Fore.LIGHTYELLOW_EX} {main_system.login_user['user_name']},{Fore.LIGHTWHITE_EX} your score is : "
           f"{Fore.LIGHTBLUE_EX}{str(sum_points)}{Fore.LIGHTWHITE_EX} points out of{Fore.LIGHTBLUE_EX}{str(questions)}"
           f"{Fore.LIGHTWHITE_EX} questions so far".center(130),
        9: f"{Fore.LIGHTWHITE_EX}end of session {Fore.LIGHTYELLOW_EX}{main_system.login_user['user_name']}"
           f"{Fore.LIGHTWHITE_EX}".center(130),
        10: f"{main_system.login_user['user_name']}, you scored {str(sum_points)} in this session".center(130),
        11: f"{Fore.LIGHTYELLOW_EX}{name1}, {Fore.LIGHTWHITE_EX}you win!!! you've scored {Fore.LIGHTBLUE_EX}"
            f"{str(sum_points_player2)} {Fore.LIGHTWHITE_EX}in this session,{Fore.LIGHTYELLOW_EX}{name2}, "
            f"{Fore.LIGHTWHITE_EX}you scored {Fore.LIGHTBLUE_EX}{str(sum_points)} {Fore.LIGHTWHITE_EX} points "
            f"in this session, but lost them all. "
            f"{Fore.LIGHTWHITE_EX}better luck next time".center(130),
        12: f"{Fore.LIGHTYELLOW_EX}{name2}, {Fore.LIGHTWHITE_EX}you win!!! you've scored {Fore.LIGHTBLUE_EX}"
            f"{str(sum_points_player2)}{Fore.LIGHTWHITE_EX} in this session, {Fore.LIGHTYELLOW_EX}{name1}, "
            f"{Fore.LIGHTWHITE_EX}you scored {Fore.LIGHTBLUE_EX}{str(sum_points)}{Fore.LIGHTWHITE_EX} points "
            f"in this session, but lost them all. "
            f"better luck next time".center(130),
        13: f"{Fore.LIGHTWHITE_EX}tie!!! you've earned {Fore.LIGHTBLUE_EX}{str(sum_points)}{Fore.LIGHTWHITE_EX} "
            f"coins for each player in this session".center(130),
        14: f"\n{Fore.LIGHTWHITE_EX}enter the answers for the questions, '{Fore.LIGHTBLUE_EX}points{Fore.LIGHTWHITE_EX}' "
            f"to see how much points have you earned so far,\n"
            f"'{Fore.LIGHTBLUE_EX}stop{Fore.LIGHTWHITE_EX}' to end game and back to title\n".center(130),
        15: f"{Fore.LIGHTWHITE_EX}turn of player: {Fore.LIGHTYELLOW_EX}{main_system.login_user['user_name']}"
            f"{Fore.LIGHTWHITE_EX}".center(130),
        16: f"{Fore.LIGHTGREEN_EX}new high-score, {Fore.LIGHTYELLOW_EX}{main_system.login_user['user_name']}"
            f"{Fore.LIGHTWHITE_EX}!!!".center(130),
        17: f"\n{Fore.LIGHTRED_EX}2 players mode {Fore.LIGHTWHITE_EX}- each player gets 5 seconds and "
            f"one chance to answer each question, if the player answer\nis wrong, the turn ends, "
            f"and the 2nd player gets his chance, who answers more questions wins.\n"
            f"enter '{Fore.LIGHTBLUE_EX}points{Fore.LIGHTWHITE_EX}' to see how much points have you earned so far, or "
            f"'{Fore.LIGHTBLUE_EX}stop{Fore.LIGHTWHITE_EX}' to end game and back to title\n",
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
    with open("json_files/math_game_hs.json") as file:
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
            print(f"{Fore.LIGHTWHITE_EX}questions: {Fore.LIGHTBLUE_EX}{str(user['questions'])}".center(130))
            print(f"{Fore.LIGHTWHITE_EX}difficulty: {the_color}{user['difficulty']}".center(130))
            print(f"{Fore.LIGHTWHITE_EX}date: {Fore.LIGHTBLUE_EX}{user['date_scored']}".center(130))
            print(f"{Fore.LIGHTWHITE_EX}play duration: {Fore.LIGHTBLUE_EX}{user['play_duration']}".center(130))
            print(f"{Fore.LIGHTWHITE_EX}---------------------------".center(124))
    return


def add_high_score(a_list):
    scores_list = a_list
    json_db = json.dumps(scores_list, indent=4, separators=(", ", " : "))
    with open("json_files/math_game_hs.json", "w") as file:
        file.write(json_db)
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


def check_high_score(score, difficulty):
    global game_difficulty
    if difficulty == 1:
        game_difficulty = 'easy'
    elif difficulty == 2:
        game_difficulty = 'intermediate'
    elif difficulty == 3:
        game_difficulty = 'hard'
    with open("json_files/math_game_hs.json")as file:
        scores_list = json.load(file)
    for i in scores_list:
        if i['rank'] != 0 and i['difficulty'] == game_difficulty:
            if score > i['high_score']:
                i['high_score'] = score
                add_high_score(scores_list)
                break
    for i in scores_list:
        if i['rank'] == 0 and i['name'] == main_system.login_user['user_name']:
            if score > i['high_score']:
                i['name'] = main_system.login_user['user_name']
                i['difficulty'] = game_difficulty
                i['questions'] = questions
                i['high_score'] = score
                i['date_scored'] = main_system.today_date('day')
                add_high_score(scores_list)
                break
    print(massages(16))
    return

# ================================================= game functions =====================================================


def random_numbers(difficulty):
    if difficulty == 1:
        number = random.randrange(1, 11)
        return number
    if difficulty == 2:
        number = random.randrange(1, 21)
        return number
    if difficulty == 3:
        number = random.randrange(1, 101)
        return number


def math_again(difficulty):
    num1 = random_numbers(difficulty)
    num2 = random_numbers(difficulty)
    op = random.choice(list(operator_lookup.keys()))
    sign = operator_lookup.get(op)
    math(num1, sign, num2, difficulty)


def math(num1, sign, num2, difficulty):
    correct_answer = sign(Decimal(num1), Decimal(num2))
    if difficulty == 1:
        correct_answer = round(correct_answer, 1)
        if str(sign) == '<built-in function truediv>' or correct_answer == -correct_answer:
            math_again(difficulty)
    elif difficulty == 2:
        correct_answer = round(correct_answer, 1)
        if num2 > num1:
            math_again(difficulty)
    else:
        correct_answer = round(correct_answer, 2)
    return correct_answer


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
    global game_difficulty
    if game_difficulty == 1:
        game_difficulty = 'easy'
    elif game_difficulty == 2:
        game_difficulty = 'intermediate'
    elif game_difficulty == 3:
        game_difficulty = 'hard'
    else:
        pass
    if what == 'last_game':
        var = 'Math Game'
    elif what == 'difficulty':
        var = game_difficulty
        if var == 1:
            var = 'easy'
        elif var == 2:
            var = 'medium'
        elif var == 3:
            var = 'hard'
    elif what == 'high_score':
        if players == 1:
            var = sum_points
        elif players == 2:
            var = sum_points_player2
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


# ============================================= game ===================================================================


def start_game():
    global points, game_difficulty, time_limit, name, name1, name2, turn, lives, init_time, players
    init_time = datetime.datetime.now()
    game_difficulty = int(input(f'{Fore.LIGHTWHITE_EX}please choose difficulty:\n\n1-{Fore.LIGHTGREEN_EX}easy '
                                f'{Fore.LIGHTWHITE_EX}2-{Fore.LIGHTYELLOW_EX}intermediate {Fore.LIGHTWHITE_EX}'
                                f'3-{Fore.LIGHTRED_EX}hard\n{Fore.LIGHTWHITE_EX}>'))

    if not str(game_difficulty).isdigit():
        print(massages(2), massages(0))
    else:
        if game_difficulty == 1:
            time_limit = 15
            points = 3
            lives = 7
        elif game_difficulty == 2:
            time_limit = 10
            points = 5
            lives = 5
        elif game_difficulty == 3:
            time_limit = 5
            points = 10
            lives = 3
        else:
            print(massages(1), massages(0))

    num_of_players = int(input('how many players?\n>'))
    players = num_of_players
    if not str(num_of_players).isdigit():
        print(massages(2), massages(0))
    else:
        if num_of_players == 1:
            main_system.who_is_online()
            if players == 1:
                x = 0
            elif players == 2:
                x = 1
            num = x
            while num != 3:
                if num == 0:
                    num = 4
                    name = name1
                elif num == 1:
                    name = name1
                elif num == 2:
                    name = name2
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
                    main_system.login_user = main_system.logged_list[user_id]
                    if num == 1:
                        id1 = main_system.logged_list[user_id]
                    if num == 2:
                        id2 = main_system.logged_list[user_id]
                    name = main_system.login_user['user_name']
                    add_to_personal_json(name, 'last_game')
                    add_to_personal_json(name, 'difficulty')
                    add_to_personal_json(name, 'date_scored')
                    if num != 4:
                        num += 1
                    elif num == 4:
                        num -= 1
                    continue
                elif not check_user(password, user_id):
                    continue
                 
            turn = 0
            if players == 1:
                game_1player(num_of_players, game_difficulty)
            elif players == 2:
                game_2players(num_of_players, game_difficulty, id1, id2)
            
        else:
            print(massages(1), massages(0))

    game_menu()


def game_over(players, difficulty, id1, id2):
    global turn, sum_points, sum_points_player2, final_time
    if players == 1:

        check_high_score(sum_points, difficulty)
        add_player_points(sum_points)
        m, s = divmod(time_fn(init_time).total_seconds(), 60)
        final_time = f'{int(m // 60)}:{int(m % 60)}:{int(s)}'
        add_to_personal_json(name1, 'play_duration')
        print(massages(10), massages(0))

    elif players == 2:

        if sum_points > sum_points_player2:
            check_high_score(sum_points, difficulty)
            main_system.login_user = players_list[id2]
            print(massages(11), massages(0))
            add_to_personal_json(name1, 'high_score')
            sum_points += sum_points_player2
            remove_player_points(sum_points_player2)
            main_system.login_user = players_list[id1]
            add_player_points(sum_points)
            m, s = divmod(time_fn(init_time).total_seconds(), 60)
            final_time = f'{int(m // 60)}:{int(m % 60)}:{int(s)}'
            add_to_personal_json(name1, 'play_duration')

        elif sum_points < sum_points_player2:
            check_high_score(sum_points_player2, difficulty)
            main_system.login_user = players_list[id1]
            print(massages(12), massages(0))
            add_to_personal_json(name2, 'high_score')
            sum_points_player2 += sum_points
            remove_player_points(sum_points)
            main_system.login_user = players_list[id2]
            add_player_points(sum_points_player2)
            m, s = divmod(time_fn(init_time).total_seconds(), 60)
            final_time = f'{int(m // 60)}:{int(m % 60)}:{int(s)}'
            add_to_personal_json(name2, 'play_duration')

        else:
            print(massages(13), massages(0))

            main_system.login_user = players_list[id1]
            check_high_score(sum_points, difficulty)
            add_to_personal_json(name1, 'high_score')
            add_player_points(sum_points)
            m, s = divmod(time_fn(init_time).total_seconds(), 60)
            final_time = f'{int(m // 60)}:{int(m % 60)}:{int(s)}'
            add_to_personal_json(name1, 'play_duration')

            main_system.login_user = players_list[id2]
            check_high_score(sum_points, difficulty)
            add_to_personal_json(name2, 'high_score')
            add_player_points(sum_points)
            m, s = divmod(time_fn(init_time).total_seconds(), 60)
            final_time = f'{int(m // 60)}:{int(m % 60)}:{int(s)}'
            add_to_personal_json(name2, 'play_duration')

    turn = 0
    sum_points = 0
    sum_points_player2 = 0
    game_menu()


def game_2players(players, difficulty, id1, id2):
    if difficulty == 'easy':
        difficulty = 1
    if difficulty == 'intermediate':
        difficulty = 2
    if difficulty == 'hard':
        difficulty = 3
    global lives, turn, sum_points, sum_points_player2, questions, time_limit
    print(massages(17))
    if turn == 0:
        num = id1
    elif turn == 1:
        num = id2
    main_system.login_user = players_list[num]
    print(massages(15), massages(0))

    time_limit = 5
    lives = 1
    while lives != 0:
        questions += 1

        start_time = datetime.datetime.now()

        number1 = random_numbers(difficulty)
        number2 = random_numbers(difficulty)
        op = random.choice(list(operator_lookup.keys()))
        sign = operator_lookup.get(op)

        do_math = math(number1, sign, number2, difficulty)
        answer = input((f'{str(number1)} {op} {str(number2)} =\n'.center(132)))
        m, s = divmod(time_fn(start_time).total_seconds(), 60)
        if answer == '':
            lives -= 1
            print(massages(1), massages(0))
            continue
        if answer == 'points':
            print(massages(8), massages(0))
            continue
        elif answer == 'stop':
            print(massages(18))
            game_over(players, difficulty, id1, id2)
        elif float(answer) == float(do_math) and s < time_limit:
            print(massages(5), massages(0))
            if turn == 0:
                sum_points += points
            elif turn == 1:
                sum_points_player2 += points
        elif s >= time_limit:
            lives -= 1
            print(massages(7), massages(0))
        elif float(answer) != do_math:
            lives -= 1
            print(massages(6))
            print(f'correct answer is: {Fore.LIGHTBLUE_EX}{str(do_math)}\n{Fore.LIGHTWHITE_EX}'.center(130), massages(0))
        else:
            lives -= 1
            print(massages(1), massages(0))
            continue
    if turn == 0:
        print(massages(9), massages(0))
        turn = 1
        lives = 1
        game_2players(players, game_difficulty, id1, id2)
    elif turn == 1:
        print(massages(18))
        game_over(players, difficulty, id1, id2)


def game_1player(playerss, difficulty):
    global lives, turn, sum_points, sum_points_player2, questions
    if difficulty == 'easy':
        difficulty = 1
    if difficulty == 'intermediate':
        difficulty = 2
    if difficulty == 'hard':
        difficulty = 3
    print(massages(14), massages(0))

    while lives != 0:
        questions += 1

        start_time = datetime.datetime.now()

        number1 = random_numbers(difficulty)
        number2 = random_numbers(difficulty)
        op = random.choice(list(operator_lookup.keys()))
        sign = operator_lookup.get(op)

        do_math = math(number1, sign, number2, difficulty)
        answer = input((f'{Fore.LIGHTYELLOW_EX}{str(number1)} {Fore.LIGHTBLUE_EX}{op} {Fore.LIGHTYELLOW_EX}'
                        f'{str(number2)} {Fore.LIGHTBLUE_EX}={Fore.LIGHTWHITE_EX}\n'.center(132)))
        m, s = divmod(time_fn(start_time).total_seconds(), 60)
        if answer == 'points':
            print(massages(8), massages(0))
            continue
        elif answer == 'stop':
            print(massages(18))
            game_over(playerss, difficulty, 0, 0)
        elif float(answer) == float(do_math) and s < time_limit:
            print(massages(5), massages(0))
            sum_points += points
        elif s >= time_limit:
            lives -= 1
            print(massages(7), massages(0))
        elif float(answer) != do_math:
            lives -= 1
            print(massages(6))
            print(f'correct answer is: {Fore.LIGHTBLUE_EX}{str(do_math)}\n{Fore.LIGHTWHITE_EX}'.center(130), massages(0))
        else:
            print(massages(1), massages(0))
            lives -= 1
            continue

    print(massages(18))
    game_over(playerss, difficulty, 0, 0)
