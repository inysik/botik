import telebot
# import random

bot = telebot.TeleBot('5994897500:AAGIxzrN_x3Rs0NIyaLnJ1JJCFDMblYTPf0')
import telebot

# Создаем экземпляр класса TeleBot с токеном нашего бота
# bot = telebot.TeleBot("YOUR_TOKEN_HERE")

# Игровое поле для крестиков-ноликов, заполненное пробелами
# board = [[' ', ' ', ' '],
#          [' ', ' ', ' '],
#          [' ', ' ', ' ']]


# Символы для игроков
player_symbols = {'X': '❌', 'O': '⭕️'}

# Текущий символ игрока (X или O)
current_player = 'X'

# Функция для отрисовки игрового поля в виде строки
def draw_board():
    board_str = ''
    for row in board:
        for cell in row:
            board_str += f'{cell}|'
        board_str = board_str[:-1] + '\n'
    return board_str

# Функция для проверки, является ли данное состояние игры победным
def is_winner(board, player):
    # Проверяем горизонтали и вертикали
    for i in range(3):
        if board[i] == [player] * 3 or [row[i] for row in board] == [player] * 3:
            return True
    # Проверяем диагонали
    if [board[i][i] for i in range(3)] == [player] * 3 or [board[i][2-i] for i in range(3)] == [player] * 3:
        return True
    return False

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Добро пожаловать в игру крестики-нолики! Чтобы сделать ход, отправьте сообщение с координатами клетки, куда вы хотите поставить свой символ, например, '1,2'.")

# Обработчик любых текстовых сообщений, которые не являются командами
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    global current_player
    # Пытаемся получить координаты от пользователя
    try:
        x, y = map(int, message.text.split(','))
        # Проверяем, что клетка пуста
        if board[x-1][y-1] == ' ':
            board[x-1][y-1] = current_player
            bot.reply_to(message, f'{player_symbols[current_player]}\n{draw_board()}')
            # Проверяем, есть ли победитель или ничья
            if is_winner(board, current_player):
                bot.reply_to(message, f'Игрок {player_symbols[current_player]} победил!')
                # Сбрасываем игру
                reset_game()
            elif ' ' not in [cell for row in board for cell in row]:
                bot.reply_to(message, 'Ничья!')
                # Сб
            else:
                # Передаем ход следующему игроку
                current_player = 'O' if current_player == 'X' else 'X'
                bot.reply_to(message, f'Ход игрока {player_symbols[current_player]}')
        else:
            bot.reply_to(message, 'Эта клетка уже занята!')
    # Если не удалось получить координаты от пользователя, сообщаем об ошибке
    except:
        bot.reply_to(message, 'Некорректный формат ввода. Отправьте сообщение с координатами клетки, куда вы хотите поставить свой символ, например, "1,2".')

# Функция для сброса игры
def reset_game():
    global board, current_player
    board = [[' ', ' ', ' '],
             [' ', ' ', ' '],
             [' ', ' ', ' ']]
    current_player = 'X'

# Функция для отображения игрового поля в чате
def show_board():
    global board
    # Символы для границ и разделителей
    top = '╔═══╦═══╦═══╗'
    mid = '╠═══╬═══╬═══╣'
    bot = '╚═══╩═══╩═══╝'
    div = '║'

    # Собираем отображение игрового поля
    row1 = f'{div} {board[0][0]} {div} {board[0][1]} {div} {board[0][2]} {div}'
    row2 = f'{div} {board[1][0]} {div} {board[1][1]} {div} {board[1][2]} {div}'
    row3 = f'{div} {board[2][0]} {div} {board[2][1]} {div} {board[2][2]} {div}'

    # Отправляем игровое поле в чат
    # bot.send_message(chat_id, f'{top}\n{row1}\n{mid}\n{row2}\n{mid}\n{row3}\n{bot}')
    # bot.send_message(chat_id, game_board, parse_mode='Markdown')
    game_board = f'{top}\n{row1}\n{mid}\n{row2}\n{mid}\n{row3}\n{bot}'
    # Отправляем игровое поле в чат
    bot.send_message(chat_id, game_board, parse_mode='Markdown')

# Запускаем бота
bot.polling()

