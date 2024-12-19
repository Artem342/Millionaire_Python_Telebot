# Импорт необходимых модулей
import time
import telebot
from telebot import types
import sqlite3
import random

# Глобальные переменные
db_name = 'mil.db'

user_Name = None
time_answer = 60

# Создание экземпляра телебота и присваивание его переменной bot
TOKEN = "7976311138:AAGS8br0OaSv27Iq5eOtYArCxTjPLUfcYnQ"
bot = telebot.TeleBot(TOKEN)

# Обработчик команды 'start' или 's' для запуска игры
@bot.message_handler(commands=['start', 's'])
def start_game(message):
    if user_Name == None:
        msg = "Добро пожаловать на викторину Кто хочет стать миллионером?"
    else:
        msg = "Попробуем еще раз?"
    markup = types.ReplyKeyboardMarkup()
    btn_play = types.KeyboardButton('Играть')
    btn_rules = types.KeyboardButton('Правила')
    btn_stat = types.KeyboardButton('Статистика')
    btn_exit = types.KeyboardButton('Выход')
    markup.row(btn_play, btn_rules)
    markup.row(btn_stat, btn_exit)
    bot.send_message(message.chat.id, msg, reply_markup=markup)

# Обработчик нажатия на кнопку в меню start
@bot.message_handler(content_types=['text'])
def menu(message):
    if message.text == 'Играть':
        play_game(message)
    elif message.text == 'Правила':
        msg = f'{rules}'
        markup = types.ReplyKeyboardMarkup()
        btn_play = types.KeyboardButton('Играть')
        btn_stat = types.KeyboardButton('Статистика')
        btn_exit = types.KeyboardButton('Выход')
        markup.add(btn_play)
        markup.row(btn_stat, btn_exit)
        bot.send_message(message.chat.id,msg, reply_markup=markup)
    elif message.text == 'Статистика':
        cn = sqlite3.connect(db_name)
        sql_q = '''SELECT name, Result FROM Users'''
        cur = cn.cursor()
        cur.execute(sql_q)
        results = cur.fetchall()
        msg = ''
        for element in results:
            msg = msg + '\n' + str(element)
        cn.close()
        markup = types.ReplyKeyboardMarkup()
        btn_play = types.KeyboardButton('Играть')
        btn_rules = types.KeyboardButton('Правила')
        btn_exit = types.KeyboardButton('Выход')
        markup.add(btn_play)
        markup.row(btn_rules, btn_exit)
        bot.send_message(message.chat.id, msg, reply_markup=markup)
    elif message.text == 'Выход':
        game_exit(message)

# Обработчик логики игры
def play_game(message):
    global game_status
    global right_answer_text
    global user_Name
    global game_result
    global fireproof_price
    global win_price
    global help_hall_use
    global help_fifty_use
    global help_friend_use
    global help_mistake_use
    global help_change_use
    global help_count
    global current_price
    global game_level
    global current_question
    help_hall_use = False
    help_fifty_use = False
    help_friend_use = False
    help_mistake_use = False
    help_change_use = False
    help_count = 4
    fireproof_price = 0
    win_price = 0
    chat_id = message.chat.id
    import_data
    if user_Name == None:
        msg = bot.send_message(message.chat.id,"Как вас зовут?")
        bot.register_next_step_handler(msg, user_login)
        while user_Name == None:
            time.sleep(1)
        msg = (f'Очень приятно, <b><i>{user_Name}</i></b>!\nИтак, приступим!\n'
           f'Выберите несгораемую сумму:\n')
    else:
        msg = (f'Итак, <b><i>{user_Name}</i></b>, приступим!\n'
           f'Выберите несгораемую сумму:\n')

    markup = types.ReplyKeyboardMarkup()

    btn_1 = types.KeyboardButton(f'{get_price(1)}')
    btn_2 = types.KeyboardButton(f'{get_price(2)}')
    btn_3 = types.KeyboardButton(f'{get_price(3)}')
    btn_4 = types.KeyboardButton(f'{get_price(4)}')
    btn_5 = types.KeyboardButton(f'{get_price(5)}')
    btn_6 = types.KeyboardButton(f'{get_price(6)}')
    btn_7 = types.KeyboardButton(f'{get_price(7)}')
    btn_8 = types.KeyboardButton(f'{get_price(8)}')
    btn_9 = types.KeyboardButton(f'{get_price(9)}')
    btn_10 = types.KeyboardButton(f'{get_price(10)}')
    btn_11= types.KeyboardButton(f'{get_price(11)}')
    btn_12 = types.KeyboardButton(f'{get_price(12)}')
    btn_13 = types.KeyboardButton(f'{get_price(13)}')
    btn_14 = types.KeyboardButton(f'{get_price(14)}')
    markup.add(btn_1, btn_2, btn_3, btn_4, btn_5, btn_6, btn_7,
               btn_8, btn_9, btn_10, btn_11, btn_12, btn_13, btn_14)
    bot.register_next_step_handler(bot.send_message(chat_id, msg, parse_mode="html", reply_markup=markup), set_fireproof_price)

    while fireproof_price == 0:
        time.sleep(1)
    game_level = 1
    game_status = 'game_processed'

    # Цикл уровней
    while game_status == 'game_processed':
        current_question = get_question(game_level)
        current_price = get_price(game_level)
        right_answer_num = current_question[7]
        right_answer_text = current_question[right_answer_num+1]
        msg = (f'Внимание, <b>вопрос № <i>{game_level}</i></b>\n'
               f'Цена вопроса: <b><i>{current_price}</i> рублей.</b>\n'
               f'<b><i>\"{current_question[1]}\"</i></b>\n')
        markup = types.ReplyKeyboardMarkup()
        btn_A = types.KeyboardButton(f'{current_question[2]}')
        btn_B = types.KeyboardButton(f'{current_question[3]}')
        btn_C = types.KeyboardButton(f'{current_question[4]}')
        btn_D = types.KeyboardButton(f'{current_question[5]}')
        btn_help = types.KeyboardButton(f'Получить подсказку')
        markup.row(btn_A, btn_C)
        markup.row(btn_B, btn_D)
        if help_count > 0:
            markup.add(btn_help)
        bot.register_next_step_handler(bot.send_message(chat_id, msg, parse_mode="html", reply_markup=markup), get_game_status)
        game_status = 'answer_waiting'
        game_waiting(message)
        if game_status == 'answer_true':
            if game_level == 15:
                game_result = 'Win'
                win_price = current_price
            else:
                game_level += 1
                bot.send_message(chat_id, f'<b>Верно:</b>\n'
                                              f'- {right_answer_text} -\n', parse_mode="html")
                game_status = 'game_processed'
        elif game_status == 'answer_wrong':
            bot.send_message(chat_id, f'<b>Увы</b>, ответ неверный, правильный вариант:\n<b>{right_answer_text}</b>', parse_mode="html")
        elif game_status == 'time_out':
            bot.send_message(chat_id, f'<b>Время вышло!</b> К сожалению вы не выбрали ответ.\n'
                                      f'Правильный вариант:\n'
                                      f'<b>{right_answer_text}</b>', parse_mode="html")
        # game_result = current_price
        if (int(current_price) > int(fireproof_price)):
            win_price = fireproof_price
        else:
            win_price = 0

    bot.send_message(chat_id, f'<b>Игра окончена.</b>\n'
                              f'Ваш выигрыш составляет <b>{win_price} рублей</b>', parse_mode="html")
    set_result(user_Name, win_price)
    fireproof_price = 0
    win_price = 0
    start_game(message)

def game_waiting(message):
    global game_status
    i = 0
    while game_status == 'answer_waiting':
        time.sleep(1)
        i += 1
        if i == time_answer:
            game_status = 'time_out'
    return game_status

def user_login(message):
    global user_Name
    user_Name = message.text
    return

# Проверка правильности ответа
@bot.callback_query_handler(func=lambda callback: True)
def get_game_status(message):
    global game_status
    global right_answer_text
    if message.text == 'Получить подсказку':
        get_help(message)
    elif message.text == right_answer_text:
        game_status = 'answer_true'
    else:
        game_status = 'answer_wrong'
    return game_status

def set_fireproof_price(message):
    global fireproof_price
    fireproof_price = message.text

# Функция получения ответа из базы
def get_question(level):
    cn = sqlite3.connect(db_name)
    sql = 'select * from [Questions] WHERE Level = ? order by random() Limit 1'
    cur = cn.cursor()
    cur.execute(sql, [level])
    q =  cur.fetchone()
    cn.commit()
    cn.close()
    return q

def get_price(level):
    cn = sqlite3.connect(db_name)
    sql = 'select * from [Levels] WHERE Level = ? order by random() Limit 1'
    cur = cn.cursor()
    cur.execute(sql, [level])
    q =  cur.fetchone()[2]
    cn.commit()
    cn.close()
    return q

def set_result(user_Name, win_price):
    cn = sqlite3.connect(db_name)
    sql = "INSERT INTO [Users] (Name, Surname, Result) VALUES (?, ?, ?)"
    cur = cn.cursor()
    cur.execute(sql, (f'{user_Name}', '-', f'{win_price}'))
    cn.commit()
    cn.close()

# Функция загрузки базы
def import_data():
    cn = sqlite3.connect(db_name)
    sql_q = '''INSERT INTO "Questions" ("QuestionText", 
        "Answer1", 	"Answer2",
        "Answer3", 	"Answer4",
        "RightAnswer", "Level") VALUES (?,?,?,?,?,?,?)'''
    sql_l = '''INSERT INTO "Levels" ("Level", "Price") VALUES (?,?)'''
    cur = cn.cursor()
    with open('Вопросы.txt', 'r') as f:
        for line in f:
            r = line.strip().split('\t')
            cur.execute(sql_q, (r[0],r[1],r[2],r[3],r[4],int(r[5]),int(r[6])))
    with open('Уровни.txt', 'r') as f:
        for line in f:
            r = line.strip().split('\t')
            cur.execute(sql_l, (int(r[0]),int(r[1])))
    cn.commit()
    cn.close()

# Обработчик вывода кнопок "Подсказки"
def get_help(message):
    global help_hall_use
    global help_fifty_use
    global help_friend_use
    global help_mistake_use
    global help_change_use
    chat_id = message.chat.id
    markup = types.ReplyKeyboardMarkup()
    msg = f'Доступны подсказки ({help_count}): '
    btn_h1 = types.KeyboardButton(f'Помощь зала')
    btn_h2 = types.KeyboardButton(f'50 на 50')
    btn_h3 = types.KeyboardButton(f'Звонок другу')
    btn_h4 = types.KeyboardButton(f'Право на ошибку')
    btn_h5 = types.KeyboardButton(f'Замена вопроса')
    if not help_hall_use:
        markup.add(btn_h1)
    if not help_fifty_use:
        markup.add(btn_h2)
    if not help_friend_use:
        markup.add(btn_h3)
    if not help_mistake_use:
        markup.add(btn_h4)
    if not help_change_use:
        markup.add(btn_h5)
    bot.register_next_step_handler(bot.send_message(chat_id, msg, reply_markup=markup), choice_help)

# Обработчик выбора подсказок
def choice_help(message):
    global help_hall_use
    global help_fifty_use
    global help_friend_use
    global help_mistake_use
    global help_change_use
    global help_count
    if message.text == 'Помощь зала':
        help_hall_use = True
        help_count -= 1
        help_hall(message)
    elif message.text == '50 на 50':
        help_fifty_use = True
        help_count -= 1
        help_fifty(message)
    elif message.text == 'Звонок другу':
        help_friend_use = True
        help_count -= 1
        help_friend(message)
    elif message.text == 'Право на ошибку':
        help_mistake_use = True
        help_count -= 1
        help_mstake(message)
    elif message.text == 'Замена вопроса':
        help_change_use = True
        help_count -= 1
        help_change(message)

# Реализация подсказки "Помощь зала"
def help_hall(message):
    global right_answer_text
    global current_question
    chat_id = message.chat.id
    my_dict = {current_question[2] : 0, current_question[3] : 0,current_question[4] : 0, current_question[5]: 0}
    s = 0
    for key in my_dict:
        if key != right_answer_text:
            my_dict[key] = random.randint(5,19)
            s = s + my_dict[key]
    for key in my_dict:
        if key == right_answer_text:
            my_dict[key] = 100-s

    msg = (f'{current_question[2]} - {my_dict[current_question[2]]} %\n'
        f'{current_question[3]} - {my_dict[current_question[3]]} %\n'
        f'{current_question[4]} - {my_dict[current_question[4]]} %\n'
        f'{current_question[5]} - {my_dict[current_question[5]]} %\n\n'
        f' Выбор за вами')

    markup = types.ReplyKeyboardMarkup()
    btn_A = types.KeyboardButton(f'{current_question[2]}')
    btn_B = types.KeyboardButton(f'{current_question[3]}')
    btn_C = types.KeyboardButton(f'{current_question[4]}')
    btn_D = types.KeyboardButton(f'{current_question[5]}')
    markup.row(btn_A, btn_C)
    markup.row(btn_B, btn_D)
    bot.register_next_step_handler(bot.send_message(chat_id, msg, parse_mode="html", reply_markup=markup),
                                   get_game_status)

# Реализация подсказки "50 на 50"
def help_fifty(message):
    global right_answer_text
    global current_question
    chat_id = message.chat.id
    my_dict = {current_question[2]: 0, current_question[3]: 0, current_question[4]: 0, current_question[5]: 0}
    msg = (f'Выбор за вами')
    btn_A = types.KeyboardButton(f'{right_answer_text}')
    s = 0
    for key in my_dict:
        if key != right_answer_text:
            btn_B = types.KeyboardButton(f'{key}')
    markup = types.ReplyKeyboardMarkup()
    markup.add(btn_A)
    markup.add(btn_B)
    bot.register_next_step_handler(bot.send_message(chat_id, msg, parse_mode="html", reply_markup=markup),
                                   get_game_status)

# Реализация подсказки "Звонок другу"
def help_friend(message):
    global right_answer_text
    global current_question
    chat_id = message.chat.id
    msg = (f'<b>Друг:</b> Привет, я считаю что правильный ответ - <b>{right_answer_text}</b>\n'
           f'<b>Ведущий:</b> Выбор за вами')
    markup = types.ReplyKeyboardMarkup()
    btn_A = types.KeyboardButton(f'{current_question[2]}')
    btn_B = types.KeyboardButton(f'{current_question[3]}')
    btn_C = types.KeyboardButton(f'{current_question[4]}')
    btn_D = types.KeyboardButton(f'{current_question[5]}')
    markup.row(btn_A, btn_C)
    markup.row(btn_B, btn_D)
    bot.register_next_step_handler(bot.send_message(chat_id, msg, parse_mode="html", reply_markup=markup),
                                   get_game_status)

# Реализация подсказки "Право на ошибку"
def help_mstake(message):
    global current_question
    chat_id = message.chat.id
    msg = (f'Вы выбрали подсказку "Право на ошибку".\n'
           f'Итак, ваша первая попытка')
    markup = types.ReplyKeyboardMarkup()
    btn_A = types.KeyboardButton(f'{current_question[2]}')
    btn_B = types.KeyboardButton(f'{current_question[3]}')
    btn_C = types.KeyboardButton(f'{current_question[4]}')
    btn_D = types.KeyboardButton(f'{current_question[5]}')
    markup.row(btn_A, btn_C)
    markup.row(btn_B, btn_D)
    bot.register_next_step_handler(bot.send_message(chat_id, msg, parse_mode="html", reply_markup=markup),
                                   help_mistake_2)
def help_mistake_2(message):
    global right_answer_text
    global current_question
    chat_id = message.chat.id
    if message.text == right_answer_text:
        get_game_status(message)
    else:
        msg = (f'Вы ошиблись".\n'
               f'У вас еще одна попытка')
        markup = types.ReplyKeyboardMarkup()
        btn_A = types.KeyboardButton(f'{current_question[2]}')
        btn_B = types.KeyboardButton(f'{current_question[3]}')
        btn_C = types.KeyboardButton(f'{current_question[4]}')
        btn_D = types.KeyboardButton(f'{current_question[5]}')
        if message.text == current_question[2]:
            markup.add(btn_C)
            markup.row(btn_B, btn_D)
        elif message.text == current_question[3]:
            markup.row(btn_A, btn_C)
            markup.add(btn_D)
        elif message.text == current_question[4]:
            markup.add(btn_A)
            markup.row(btn_B, btn_D)
        elif message.text == current_question[3]:
            markup.row(btn_A, btn_C)
            markup.add(btn_B)
        bot.register_next_step_handler(bot.send_message(chat_id, msg, parse_mode="html", reply_markup=markup),
                                       get_game_status)

# Реализация подсказки "Замена вопроса"
def help_change(message):
    global game_level
    global current_question
    global current_price
    global right_answer_text
    global help_count
    chat_id = message.chat.id
    current_question = get_question(game_level)
    current_price = get_price(game_level)
    right_answer_num = current_question[7]
    right_answer_text = current_question[right_answer_num + 1]
    msg = (f'Вы выбрали подсказку "Замена вопроса".\n'
           f'Итак, новый вопрос:\n'
           f'<b><i>\"{current_question[1]}\"</i></b>\n')
    markup = types.ReplyKeyboardMarkup()
    btn_A = types.KeyboardButton(f'{current_question[2]}')
    btn_B = types.KeyboardButton(f'{current_question[3]}')
    btn_C = types.KeyboardButton(f'{current_question[4]}')
    btn_D = types.KeyboardButton(f'{current_question[5]}')
    btn_help = types.KeyboardButton(f'Получить подсказку')
    markup.row(btn_A, btn_C)
    markup.row(btn_B, btn_D)
    if help_count > 0:
        markup.add(btn_help)
    bot.register_next_step_handler(bot.send_message(chat_id, msg, parse_mode="html", reply_markup=markup),
                                   get_game_status)

# Правила игры
rules = ("Для победы в игре игроку необходимо верно ответить "
           "на 15 вопросов из различных областей знаний.\n\n"
           "Каждый вопрос имеет 4 варианта ответа, "
           "из которых только один является верным.\n\n"
           "Сложность вопросов постоянно возрастает.\n\n"
           "Время на раздумье над каждым вопросом у игрока не ограничено.\n\n"
           "Каждый из пятнадцати вопросов имеет конкретную денежную стоимость:\n\n"
           "3 000 000, 1 500 000, 800 000, 400 000, 200 000, 100 000, 50 000, "
           "25 000, 15 000, 10 000, 5 000, 3 000, 2 000, 1 000, 500.\n\n"
           "Все суммы являются заменяемыми, то есть, ответив на следующий вопрос "
             "не суммируются с суммой за ответ на предыдущий.\n\n"
             "В игре существует одна несгораемая сумма - "
             "её выбирают сами участники перед началом игры.\n\n"
             "Эта сумма остаётся у игроков даже при неправильном ответе на один из последующих вопросов.\n\n"
             "Игроку предлагаются 5 подсказок.\n"
             "Участники могут использовать только четыре из пяти подсказок по ходу игры:\n\n"
             "1. «Помощь зала» – каждый зритель в студии голосует за правильный, на его взгляд, ответ, "
             "а игроку предоставляется статистика голосования.\n\n"
             "2. «50 на 50» – компьютер убирает два неправильных ответа.\n\n"
             "3. «Звонок другу» – в течение 30 секунд игрок может посоветоваться "
             "с одним из пяти друзей, заявленных заранее.\n\n"
             "4. «Право на ошибку» – Игрок может дать два ответа на заданный вопрос. "
             "Если первый ответ игрока оказался правильным, подсказка всё равно считается использованной.\n\n"
             "5. «Замена вопроса» – игрок может заменить вопрос на другой того же уровня и той же стоимости.")

def game_exit(message):
    global user_Name
    msg = f'Всего доброго,<b>{user_Name}</b>!'
    markup = types.ReplyKeyboardMarkup()
    btn_good_bye = types.KeyboardButton(f'Вернуться в игру')
    markup.add(btn_good_bye)
    bot.register_next_step_handler(bot.send_message(message.chat.id, msg, parse_mode="html", reply_markup=markup),
                                   start_game)

# bot.polling(non_stop=True)

while(True):
    try:
        bot.polling(non_stop=True)
    except:
        print("Ошибка")