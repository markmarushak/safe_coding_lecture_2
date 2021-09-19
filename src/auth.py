import hashlib
import random
import time
import sqlite3

from randomuser import RandomUser
import pyjokes


class User:
    email = ""
    password = ""
    last_hash = ""
    reset_code = ""

    def __init__(self, email: str, password: str, last_hash: str):
        self.email = email
        self.password = password,
        self.last_hash = last_hash

    def gen_reset_code(self):
        code = random.randint(111111, 999999)
        self.reset_code = str(code)
        print("Your reset code: " + self.reset_code)

    def reset(self, email: str, reset_code):
        if email != self.email:
            print("Email is invalid")
            return False

        if reset_code != self.reset_code:
            print("Reset code is invalid")
            return False

        return str(input("Enter new password"))


class Authorization:

    @staticmethod
    def crypto(email: str, password: str) -> str:
        text = email + password
        h = hashlib.new('ripemd160')
        h.update(bytes(text, "utf-8"))
        return h.hexdigest()

    @staticmethod
    def validate(self, email, password, last_hash):
        if self.crypto(email, password) == last_hash:
            return True

        return False


class StatusBuilder:
    def __init__(self, name, only_one):
        self.name = name
        self.only_one = only_one
        self.count = 0
        self.active = False

    def validate(self):
        if self.count <= 0:
            return True

        if self.only_one:
            return False

        return True

    def get_name(self):
        return self.name

    def is_active(self):
        return self.active

    def start_active(self, statuses):
        for status in statuses:
            status.end_active()

        self.active = True

    def end_active(self):
        self.active = False


class Controller:
    LOGIN = 1
    REGISTER = 2
    RESET = 3
    VALIDATE = 4
    middleware = []
    status = 0
    goal = "Mark made this code!"

    def __init__(self):
        statuses = [
            ("start", True),
            ("login", False),
            ("register", True),
            ("reset", False),
            ("validate", False)
        ]

        

        for status in statuses:
            self.middleware.append(StatusBuilder(status[0], status[1]))


    def next(self, **arguments):
        time.sleep(2)
        getattr(self, self.middleware[self.status].get_name())(**arguments)

    def start(self):
        print("Hi there, Welcome to a board of Kharkiv Air Force University named after Ivan Kozhedub!!!")
        print("For Test this tool you should be registered before had to login")
        self.status = self.REGISTER
        self.next()

    def register(self):
        print("All right then. It will be really easy")

        _r_user = RandomUser()

        email = input("First one enter your email, you can enter simple email cause is dev version (test@email.com): ")
        if not email:
            print("Maaan, What are you doing? Are you kidding me? It was easy!!!")
            email = _r_user.get_email()
            print("Your Email will be " + email)

        password = input("Next one enter your password, don't make strong password\nit's just test.\nOf course If you "
                         "left your password you will restore it by reset code")
        if not password:
            print("It was bad idea to come and FLOOD ME. I will never forgive you!!!")
            password = _r_user.get_password()

        new_hash = Authorization.crypto(email, password)

        new_user = User(email, password, new_hash)
        new_user.gen_reset_code()

        print("Okay, You are already registered!",
              "\nYour email is: " + email,
              "\nYour password is: " + password,
              "\nYour reset_code is: " + new_user.reset_code)

        print("Registration is ended",
              "\rLet's go to Login page:)")

        self.status = self.LOGIN
        self.next(last_hash=new_hash)

    def login(self, last_hash: str):
        if not last_hash:
            print("Login doesn't work")
            exit(1)
        else:
            print(last_hash)

        login = input("Enter your email: ")
        password = input("Enter your password: ")
        if not login or not password:
            print("Login or Password is wrong")
            return self.login(last_hash)

        if Authorization.validate(login, password, last_hash):
            print("You are Logged to the dashboard!!!")
            return 0

        self.status = self.RESET
        self.next()

    def reset(self):
        is_reset = input("Do you forget password?")
        if is_reset:
            self.status = self.RESET
            



c = Controller()
c.next()