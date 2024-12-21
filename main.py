import tkinter as tk
from checkers.constants import WIDTH, HEIGHT, SQUARE_SIZE
from checkers.game import Game
from tkinter import messagebox
import json
import os

def get_row_col_from_mouse(event):
    x, y = event.x, event.y
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col

class Resize:
    def __init__(self, root):
        self.root = root

    def resize_and_center(self, window_width, window_height):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x_coordinate = int((screen_width / 2) - (window_width / 2))
        y_coordinate = int((screen_height / 2) - (window_height / 2))
        self.root.geometry("{}x{}+{}+{}".format(window_width, window_height, x_coordinate, y_coordinate))

class LoginRegisterApp(Resize):
    def __init__(self, root):
        super().__init__(root)

        self.root.title("Login or Register")

        self.frame = tk.Frame(root)
        self.frame.pack(pady=20)

        self.title_label = tk.Label(self.frame, text="Добро пожаловать в Checkers!", font=("Arial", 18))
        self.title_label.pack(pady=10)

        self.login_button = tk.Button(self.frame, text="Вход", command=self.show_login)
        self.login_button.pack(pady=5)

        self.register_button = tk.Button(self.frame, text="Регистрация", command=self.show_register)
        self.register_button.pack(pady=5)
        self.resize_and_center(400, 200)

    def show_login(self):
        self.frame.destroy()
        LoginForm(self.root, self.start_game)

    def show_register(self):
        self.frame.destroy()
        RegisterForm(self.root, self.start_game)

    def start_game(self):
        self.root.destroy()
        start_checkers_game()


class LoginForm(Resize):
    def __init__(self, root, success_callback):
        super().__init__(root)
        self.success_callback = success_callback

        self.frame = tk.Frame(root)
        self.frame.pack(pady=20)

        self.title_label = tk.Label(self.frame, text="Вход", font=("Arial", 18))
        self.title_label.pack(pady=10)

        self.username_label = tk.Label(self.frame, text="Имя пользователя")
        self.username_label.pack()
        self.username_entry = tk.Entry(self.frame)
        self.username_entry.pack(pady=5)

        self.password_label = tk.Label(self.frame, text="Пароль")
        self.password_label.pack()
        self.password_entry = tk.Entry(self.frame, show="*")
        self.password_entry.pack(pady=5)

        self.login_button = tk.Button(self.frame, text="Войти", command=self.login)
        self.login_button.pack(pady=5)

        self.back_button = tk.Button(self.frame, text="Назад", command=self.go_back)
        self.back_button.pack(pady=5)
        self.resize_and_center(400, 300)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if username and password:
            if validate_user(username, password):
                self.success_callback()
            else:
                messagebox.showerror("Ошибка", "Неправильное имя пользователя или пароль")
        else:
            messagebox.showerror("Ошибка", "Заполните все поля")

    def go_back(self):
        self.frame.destroy()
        LoginRegisterApp(self.root)


class RegisterForm(Resize):
    def __init__(self, root, success_callback):
        super().__init__(root)
        self.success_callback = success_callback

        self.frame = tk.Frame(root)
        self.frame.pack(pady=20)

        self.title_label = tk.Label(self.frame, text="Регистрация", font=("Arial", 18))
        self.title_label.pack(pady=10)

        self.username_label = tk.Label(self.frame, text="Имя пользователя")
        self.username_label.pack()
        self.username_entry = tk.Entry(self.frame)
        self.username_entry.pack(pady=5)

        self.password_label = tk.Label(self.frame, text="Пароль")
        self.password_label.pack()
        self.password_entry = tk.Entry(self.frame, show="*")
        self.password_entry.pack(pady=5)

        self.register_button = tk.Button(self.frame, text="Регистрация", command=self.register)
        self.register_button.pack(pady=5)

        self.back_button = tk.Button(self.frame, text="Назад", command=self.go_back)
        self.back_button.pack(pady=5)
        self.resize_and_center(400, 300)

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username and password:
            if add_user(username, password):
                messagebox.showinfo("Успешно", "Регистрация выполнена!")
                self.success_callback()
            else:
                messagebox.showerror("Ошибка", "Имя пользователя уже занято")
        else:
            messagebox.showerror("Ошибка", "Заполните все поля для регистрации")

    def go_back(self):
        self.frame.destroy()
        LoginRegisterApp(self.root)

class CheckersApp(Resize):
    def __init__(self, root):
        super().__init__(root)
        self.root.title("Checkers")

        self.button_frame = tk.Frame(root)
        self.button_frame.pack(pady=10)

        self.turn_label = tk.Label(text="Сейчас ходят: Белые", font=("Arial", 14))
        self.turn_label.pack(pady=2)

        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT)
        self.canvas.pack()
        self.game = Game(self.canvas, self.turn_label)

        self.rules_button = tk.Button(self.button_frame, text="Правила", command=self.game.show_rules)
        self.rules_button.pack(side=tk.LEFT, padx=5)
        self.reset_button = tk.Button(self.button_frame, text="Начать сначала", command=self.game.reset)
        self.reset_button.pack(side=tk.LEFT, padx=5)
        self.reset_button = tk.Button(self.button_frame, text="Выход", command=self.quit)
        self.reset_button.pack(side=tk.LEFT, padx=5)

        self.resize_and_center(1250, 800)
        self.canvas.bind("<Button-1>", self.on_click)
        self.update_game()

    def on_click(self, event):
        row, col = get_row_col_from_mouse(event)
        self.game.select(row, col)

    def update_game(self):
        if self.game.winner() is not None:
            self.game.update()
            self.turn_label.config(text=f"{self.game.winner()} ")
        else:
            self.game.update()
            self.root.after(1000 // 60, self.update_game)

    def quit(self):
        self.root.quit()

def validate_user(username, password):
    if not os.path.exists("users.json"):
        return False

    with open("users.json", "r") as file:
        users = json.load(file)

    return users.get(username) == password


def add_user(username, password):
    if not os.path.exists("users.json"):
        users = {}
    else:
        with open("users.json", "r") as file:
            users = json.load(file)

    if username in users:
        return False

    users[username] = password
    with open("users.json", "w") as file:
        json.dump(users, file)

    return True



def start_checkers_game():
    root = tk.Tk()
    CheckersApp(root)
    root.mainloop()


def main():
    root = tk.Tk()
    LoginRegisterApp(root)
    root.mainloop()


main()
