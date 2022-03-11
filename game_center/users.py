import random
import hashlib
import string
import json
import main_system


class Users:

    id = 0
    user_name = ''
    email = ''
    password = ''
    coins = 0
    credit = 50
    logged_in = False
    keep_login = False
    is_blocked = False

    def login(self, name, password):
        for i in main_system.logged_list:
            if i["user_name"] == name:
                return 'logged_in'

        for user in main_system.users_list:
            if user['user_name'] != name:
                continue
            elif (user['user_name'] or user['email']) == name and user['password'] == password:
                self.id = user['id']
                self.user_name = user['user_name']
                self.email = user['email']
                self.password = user['password']
                self.coins = user['coins']
                self.credit = user['credit']
                self.logged_in = True
                main_system.login_user = user
                main_system.logged_list.append(user)
                return True

        return False

    def logout(self, name):
        for user in main_system.users_list:
            if user['user_name'] != name:
                continue
            elif user['user_name'] == name:
                user['logged_in'] = False
                user['keep_login'] = False
                for j in main_system.logged_list:
                    if j['user_name'] == name:
                        main_system.logged_list.remove(j)
                        main_system.login_user = {}
            return

    def add_new_user(self, user_name, email):
        to_id = main_system.users_list[len(main_system.users_list) - 1]
        first_password = ''
        for i in range(8):
            first_password += random.choice(string.ascii_letters)
        encoded_password = hashlib.md5(first_password.encode()).hexdigest()

        self.id = to_id['id'] + 1
        self.user_name = user_name
        self.email = email
        self.password = encoded_password
        self.coins = 0
        self.credit = 50
        self.logged_in = False
        self.keep_login = False
        self.is_blocked = False

        file = 'json_files/users.json'
        with open(file, "r") as f:
            x = json.load(f)
        x.append({'id': to_id['id'] + 1,
                  'user_name': user_name,
                  'email': email,
                  'password': encoded_password,
                  'coins': 0,
                  'credit': 50,
                  'logged_in': False,
                  'keep_login': False,
                  'is_blocked': False
                  })
        with open(file, "w") as f:
            json_db = json.dumps(x, indent=4, separators=(", ", " : "))
            f.write(json_db)

        self.add_to_jsons(user_name, email, first_password)

    def add_to_jsons(self, user_name, email, first_password):
        file = 'json_files/persona_high_scores.json'
        with open(file, "r") as f:
            x = json.load(f)
        x.append({
            "user": user_name,
            "biggest_high_score": 0,
            "last_game": "you haven't played any games yet...",
            "date_scored": "you haven't played any games yet...",
            "play_duration": "you haven't played any games yet...",
            "difficulty": "you haven't played any games yet..."
        })
        self.write_it(x, file)

        file = 'json_files/card_wars_hs.json'
        with open(file, "r") as f:
            x = json.load(f)
        x.append({
            "rank": 0,
            "name": user_name,
            "high_score": 0,
            "date_scored": "01\\December\\1992",
            "play_duration": "00:00:00"
        })
        self.write_it(x, file)

        file = 'json_files/hanging_man_hs.json'
        with open(file, "r") as f:
            x = json.load(f)
        x.append({
            "rank": 0,
            "name": user_name,
            "high_score": 0,
            "date_scored": "01\\December\\1992",
            "play_duration": "00:00:00",
            "difficulty": "easy"
        })
        self.write_it(x, file)

        file = 'json_files/tic_tac_toe_hs.json'
        with open(file, "r") as f:
            x = json.load(f)
        x.append({
            "rank": 0,
            "name": user_name,
            "high_score": 0,
            "date_scored": "01\\December\\1992",
            "play_duration": "00:00:00",
            "difficulty": "easy"
        })
        self.write_it(x, file)

        file = 'json_files/math_game_hs.json'
        with open(file, "r") as f:
            x = json.load(f)
        x.append({
            "rank": 0,
            "name": user_name,
            "high_score": 0,
            "questions": 0,
            "date_scored": "01\\December\\1992",
            "play_duration": "00:00:00",
            "difficulty": "easy"
        })
        self.write_it(x, file)

        self.mail_it(user_name, email, first_password)

    def change_password(self, new_password):
        for user in main_system.users_list:
            if user['user_name'] != main_system.user1.user_name:
                continue
            if user['user_name'] == main_system.user1.user_name:
                user['password'] = new_password
                main_system.write_to_database(main_system.connect_to_database())

        main_system.menu()

    def change_user_name(self, new_name):
        for user in main_system.users_list:
            if user['user_name'] != main_system.user1.user_name:
                continue
            if user['user_name'] == main_system.user1.user_name:
                user['user_name'] = new_name
                main_system.write_to_database(main_system.connect_to_database())

        main_system.menu()

    '''def remove_user():
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
        menu()'''

    def write_it(self, x, file):
        with open(file, "w") as f:
            print(file)
            print(type(file))
            json_db = json.dumps(x, indent=4, separators=(", ", " : "))
            f.write(json_db)
        return

    def mail_it(self, user_name, email, first_password):
        import mail
        mail_content = f'''dear {user_name},\nthank you for registering game_room_604\n
                           your password for 1st login is: {first_password}\n 
                           it is advised that you will make a new password after 1st login\n\n
                           see you in game_room_604'''
        mail.send_it(email, "activate your account", mail_content)
        print("registration complete, please check your mail to activate your account")
        input("press enter to continue...")
        main_system.menu()
