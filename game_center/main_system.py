import json
import game_room
import datetime
import random
import string
import hashlib
from users import Users
from art import *
from colorama import Fore, Style
tries = 0
logged_list = []
user1 = Users()
login_user = {'user_name': ''}
users_list = {}


def write_to_database(list_of_dicts):
    json_db = json.dumps(list_of_dicts, indent=4, separators=(", ", " : "))
    file = open("json_files/users.json", "w")
    file.write(json_db)
    file.close()
    return 'success'


def connect_to_database():
    global users_list
    file = open("json_files/users.json")
    users_list = json.load(file)
    return users_list


def today_date(day_or_time):
    time = datetime.datetime.now()
    now = datetime.datetime(time.year, time.month, time.day, time.hour, time.minute, time.second)
    if day_or_time == 'day':
        return now.strftime(f"{'%d'}\\{'%B'}\\{'%Y'}")
    elif day_or_time == 'time':
        return now.strftime(f"{'%H'}:{'%M'}:{'%S'}")


def menu_list(num):
    full_list = {
        1: 'login',
        2: 'logout',
        3: 'register new user',
        4: 'switch user',
        5: 'user settings',
        6: 'user info',
        7: 'to game center',
        8: 'massages',
        9: 'exit'
    }
    return f'{Fore.LIGHTWHITE_EX}{int(num)} - {Fore.LIGHTYELLOW_EX}{full_list[num]}{Fore.LIGHTWHITE_EX}'


def admin_menu():
    '''global user1.user_name, user1_password, login_user
    try:
        if login_user['user_name'] == 'admin' and login_user['logged_in']:
            print('\n')
            print('*****************************'.center(124))
            print('*        admin menu         *'.center(124))
            print('*****************************'.center(124))
            print("\n")
            print(menu_list(10).center(40) + menu_list(13).center(40))
            print(menu_list(11).center(38))
            print(menu_list(12).center(47))

            option = input('\n\nplease enter choice admin: ')

            if option == '10':
                remove_user()
            elif option == '11':
                admin_menu()
            elif option == '12':
                admin_menu()
            elif option == '13':
                menu()
        else:
            print('admin is not logged in')
    except KeyError:
        print('admin is not logged in')'''


def menu():
    global login_user, user1
    print('\n\n\n')
    print(f"{Fore.LIGHTYELLOW_EX}{today_date('day')}" + f"{Fore.LIGHTWHITE_EX}@ who is online:"
                                                        f"".center(94) + f"\n{Fore.LIGHTBLUE_EX}"
                                                                         f"{today_date('time')}")
    who_is_online().center(167)
    print(f"{Fore.LIGHTGREEN_EX}\n\n")
    tprint('Main System'.center(82), font="small")
    print(f"{Fore.LIGHTRED_EX}{Style.BRIGHT}hi {login_user['user_name']}!\n\n\n{Fore.LIGHTCYAN_EX}".center(140))
    print(menu_list(1).center(60) + menu_list(4).center(54) + menu_list(7).center(62))
    print(menu_list(2).center(62) + menu_list(5).center(52) + menu_list(8).center(56))
    print(menu_list(3).center(72) + menu_list(6) + f"{menu_list(9)}{Fore.LIGHTWHITE_EX}".center(84))
    option = input('\n\n\n\nplease enter choice: ')
    if option == 'admin':
        admin_menu()
    if option == '1':
        login()
    elif option == '2':
        logout(user1.user_name)
    elif option == '3':
        name = input("please enter user name: ")
        email = input("please enter email: ")
        user1 = Users()
        user1.add_new_user(name, email)
        x = connect_to_database()
    elif option == '4':
        switch_user()
    elif option == '5':
        change_password()
    elif option == '6':
        info()
    elif option == '7':
        if user1.user_name == '':
            print("please login or select a logged user")
            menu()
        game_room.game_room()
    elif option == '8':
        print()
    elif option == '9':
        exit_fn()
    else:
        print('wrong input')
    menu()


def info():
    try:
        password = input('please enter password: ')
        password = hashlib.md5(password.encode()).hexdigest()
        if password == login_user['password']:
            for i in login_user:
                print(login_user[i])
    except KeyError:
        print('you are not logged in!!!')
    menu()


def who_is_online():
    num = 0
    for i in logged_list:
        print(f'{Fore.LIGHTWHITE_EX}{str(num + 1)} - {Fore.LIGHTCYAN_EX}{str(i["user_name"])}'.center(130))
        num += 1
    return ''


def switch_user():
    global user1
    global login_user
    who_is_online()
    name = input(f"\n\n{Fore.LIGHTWHITE_EX}please enter user name: ")
    password = input("please enter your password: ")
    password = hashlib.md5(password.encode()).hexdigest()
    if user1.login(name, password):
        for i in logged_list:
            if i['user_name'] != name:
                continue
            elif i['user_name'] == name:
                login_user = i
        return
    elif not user1.login(name, password):
        print('wrong user name or password!')
        input("press enter to continue...")
        login_user = {}
        return


def reset_password(user_name, email):
    import mail
    new_password = ''
    for i in range(8):
        new_password += random.choice(string.ascii_letters)
    x = connect_to_database()
    print(x)
    for i in x:
        if i['user_name'] == user_name:
            i['password'] = hashlib.md5(new_password.encode()).hexdigest()
            write_to_database(x)
    mail_content = f'''dear {user_name},\nyour password was reset\n
                       your new password for next login is: {new_password}\n 
                       it is advised that you will make a new password after that login\n\n
                       see you in game_room_604'''
    mail.send_it(email, "activate your account", mail_content)
    print("password reset, please check your mail to activate your account")
    input("press enter to continue...")
    return


def login():
    global login_user, tries, users_list, user1
    user1 = Users()
    while tries != 3:
        name = input("please enter user name, c to cancel: ")
        this_password = input("please enter password: ")
        new_password = hashlib.md5(this_password.encode()).hexdigest()
        if user1.login(name, new_password) == 'logged_in':
            print('user already logged in!!!')
            menu()
        elif name == 'c':
            menu()
        elif not user1.login(name, new_password):
            print("wrong user name or password! please try again")
            tries += 1
            continue
        elif user1.login(name, new_password):
            print(f'\nhi {name}'.center(124))
            return
        elif tries == 3:
            print("too much tries, password was reset\nnew password was sent to your mail")
            reset_password(name, login_user['email'])
            login_user = {}
            menu()


def logout(user_name):
    global login_user, user1
    choice = input(f"are you sure you want to log out {user_name} (y/n)?\n")
    if user1.user_name == '':
        print('you are not logged in already!!!')
    elif choice == "y".lower():
        user1.logout(user_name)
        print(f"ok, you are logged out {user_name}")
        del user1
        user1 = Users()
        menu()
    elif choice == "n".lower():
        pass
    else:
        print('wrong output!')
    menu()


def change_password():
    if user1.password != '':
        password = input('please enter password: ')
        password = hashlib.md5(password.encode()).hexdigest()
        if password == login_user['password']:
            new_password = input('please enter new password: ')
            new_password = hashlib.md5(new_password.encode()).hexdigest()
            user1.change_password(new_password)
            print('new password entered - ' + login_user['password'] + '\n\n')
            info()
        elif password != login_user['password']:
            print('wrong password!!!')
    else:
        print('please login first')
    menu()


def change_user_name():
    if user1.password != '':
        password = input('please enter password: ')
        if password == login_user['password']:
            new_user_name = input('please enter new user name: ')
            user1.change_user_name(new_user_name)
            print('new user name entered - ' + login_user['user_name'] + '\n\n')
            info()
        elif password != login_user['password']:
            print('wrong password!!!')
            login_user['logged_in'] = False
    else:
        print('please login first')
    menu()


def remove_user():
    try:
        if login_user['user_name'] == 'admin' and login_user['logged_in']:
            print('this is the user list:')
            for i in connect_to_database():
                print(i)
            id_to_remove = int(input("please enter id of the desired user: "))
            temp_list = connect_to_database()
            temp_list.remove(temp_list[id_to_remove])
            write_to_database(temp_list)
            print(f'user id {id_to_remove} was removed from the system')
        else:
            print('please contact admin to remove a user')
    except KeyError:
        print('please login and contact admin to remove a user')
    menu()


def exit_fn():
    print("are you sure you want to quit ?")
    choice = input(">")
    if choice == ("n" or "N"):
        pass
    elif choice == ("y" or "Y"):
        for i in logged_list:
            if not i['keep_login']:
                i['logged_in'] = False
            else:
                continue
        write_to_database(connect_to_database())
        print("thank you for using my game room")
        exit()
    else:
        print("wrong input!")
        exit_fn()


for user in users_list:
    if user['logged_in']:
        logged_list.append(user)
