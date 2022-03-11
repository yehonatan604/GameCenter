'''import random
import hashlib
import string
import json
import main_system


class AddUser:
    file = ""
    first_password = ''
    'user_name': user_name,
    'email': email,
    'password': encoded_password,
    'coins': 0,
    'credit': 50,
    'is_login': False,
    'keep_login': False,
    'is_blocked': False

    def __init__(self, user_name, email):
        for i in range(8):
            self.first_password += random.choice(string.ascii_letters)
        encoded_password = hashlib.md5(self.first_password.encode()).hexdigest()
        to_id = main_system.users_list[len(main_system.users_list) - 1]
        self.add_new_user(user_name, email, encoded_password, to_id)
        self.add_to_jsons(user_name, email)

    def add_new_user(self, user_name, email, encoded_password, to_id):
        self.file = 'json_files/users.json'
        with open(self.file, "r") as f:
            x = json.load(f)
        x.append({'id': to_id['id'] + 1,
                  'user_name': user_name,
                  'email': email,
                  'password': encoded_password,
                  'coins': 0,
                  'credit': 50,
                  'is_login': False,
                  'keep_login': False,
                  'is_blocked': False
                  })
        with open(self.file, "w") as f:
            json_db = json.dumps(x, indent=4, separators=(", ", " : "))
            f.write(json_db)

    def add_to_jsons(self, user_name, email):
        self.file = 'json_files/persona_high_scores.json'
        with open(self.file, "r") as f:
            x = json.load(f)
        x.append({
            "player": user_name,
            "biggest_high_score": 0,
            "last_game": "you haven't played any games yet...",
            "date_scored": "you haven't played any games yet...",
            "play_duration": "you haven't played any games yet...",
            "difficulty": "you haven't played any games yet..."
        })
        self.write_it(x, self.file)

        self.file = 'json_files/card_wars_hs.json'
        with open(self.file, "r") as f:
            x = json.load(f)
        x.append({
            "rank": 0,
            "name": user_name,
            "high_score": 0,
            "date_scored": "01\\December\\1992",
            "play_duration": "00:00:00"
        })
        self.write_it(x, self.file)

        self.file = 'json_files/hanging_man_hs.json'
        with open(self.file, "r") as file:
            x = json.load(file)
        x.append({
            "rank": 0,
            "name": user_name,
            "high_score": 0,
            "date_scored": "01\\December\\1992",
            "play_duration": "00:00:00",
            "difficulty": "easy"
        })
        self.write_it(x, self.file)

        self.file = 'json_files/tic_tac_toe_hs.json'
        with open(self.file, "r") as file:
            x = json.load(file)
        x.append({
            "rank": 0,
            "name": user_name,
            "high_score": 0,
            "date_scored": "01\\December\\1992",
            "play_duration": "00:00:00",
            "difficulty": "easy"
        })
        self.write_it(x, self.file)

        self.file = 'json_files/math_game_hs.json'
        with open(self.file, "r") as file:
            x = json.load(file)
        x.append({
            "rank": 0,
            "name": user_name,
            "high_score": 0,
            "questions": 0,
            "date_scored": "01\\December\\1992",
            "play_duration": "00:00:00",
            "difficulty": "easy"
        })
        self.write_it(x, self.file)

        self.mail_it(user_name, email)

    def write_it(self, x, file):
        with open(file, "w") as f:
            json_db = json.dumps(x, indent=4, separators=(", ", " : "))
            f.write(json_db)
        return

    def mail_it(self, user_name, email):
                import mail
                mail_content = f''' '''dear {user_name},\nthank you for registering game_room_604\n
                                   your password for 1st login is: {self.first_password}\n 
                                   it is advised that you will make a new password after 1st login\n\n
                                   see you in game_room_604''' '''
                mail.send_it(email, "activate your account", mail_content)
                print("registration complete, please check your mail to activate your account")
                input("press enter to continue...")
                main_system.menu()'''
