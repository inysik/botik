import telebot
import random

bot = telebot.TeleBot('5994897500:AAGIxzrN_x3Rs0NIyaLnJ1JJCFDMblYTPf0')

# создание пустого поля для игры в крестики-нолики
board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

# определение текущего игрока (1 - крестики, 2 - нолики)
current_player = 1

# функция, которая проверяет, есть ли победитель
def check_winner():
    # проверка по горизонтали
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != 0:
            return board[i][0]

    # проверка по вертикали
    for i in range(3):
        if board[0][i] == board[1][i] == board[2][i] != 0:
            return board[0][i]

    # проверка по диагонали
    if board[0][0] == board[1][1] == board[2][2] != 0:
        return board[0][0]

    if board[2][0] == board[1][1] == board[0][2] != 0:
        return board[2][0]

    # если победитель не найден, возвращает 0
    return 0

# функция, которая выводит текущее состояние поля
def print_board():
    for i in range(3):
        for j in range(3):
            if board[i][j] == 0:
                print("-", end="")
            elif board[i][j] == 1:
                print("X", end="")
            else:
                print("O", end="")
        print()

# функция, которая обрабатывает сообщение от пользователя
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    global current_player

    # получение координат, на которые пользователь хочет поставить свой символ
    coords = message.text.split(",")
    x = int(coords[0])
    y = int(coords[1])

    # проверка, что координаты находятся в пределах поля
    if x < 0 or x > 2 or y < 0 or y > 2:
        bot.reply_to(message, "Координаты должны быть от 0 до 2")
        return

    # проверка, что поле свободно
    if board[x][y] != 0:
        bot.reply_to(message, "Эта клетка уже занята")
        return

    # установка символа на поле
    board[x][y] = current_player

    # вывод текущего состояния поля
    print_board()

    # проверка наличия победителя
    winner = check_winner()
    if winner != 0:
        bot.reply_to(message, f"Победил игрок {winner}!")
        return

    # проверка, что на поле остались свободные
