from telebot import types
import telebot
import sqlite3
from animations.animation import make_anime

bot = telebot.TeleBot('6351925279:AAGEtsKqKqkym6kEw-CK1N5lY3CvFSsAtyI')


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    btn_1 = types.KeyboardButton("Стандартное тело")
    btn_2 = types.KeyboardButton("Свое тело")
    btn_3 = types.KeyboardButton("Выбрать тело")
    btn_4 = types.KeyboardButton("Добавить тело")
    btn_5 = types.KeyboardButton("Удалить тело")
    btn_6 = types.KeyboardButton("Помощь")
    markup.row(btn_1, btn_2, btn_3)
    markup.row(btn_4, btn_5, btn_6)

    bot.send_message(message.chat.id, "Меню действий:", reply_markup=markup)

    bot.register_next_step_handler(message, on_click)


def on_click(message):
    msg = message.text
    if message.text == '/start':
        start(message)
    elif msg == "Стандартное тело":  # Button 1
        open_standard_object(message)

    elif msg == 'Свое тело':  # Button 2
        enter_initial_condition(message)

    elif msg == 'Добавить тело':  # Button 3
        add_initial_condition(message)

    elif msg == 'Выбрать тело':  # Button 4
        read_data(message)

    elif msg == 'Удалить тело':  # Button 5
        delete_body(message)

    elif msg == 'Помощь':  # Button 6
        help_button(message)

    else:
        bot.send_message(message.chat.id, "Команда не распознана")
        start(message)


# Button 1: "Стандартное тело" -----------------------------------------------------------------------------------------

def open_standard_object(message):
    inline_btn_1 = telebot.types.InlineKeyboardButton("Список стандартных тел", callback_data='sub_button')
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(inline_btn_1)
    bot.send_message(message.chat.id, "Введите название интересующего вас объекта", reply_markup=markup)

    bot.register_next_step_handler(message, enter_body_name)


def enter_body_name(message):
    obj_name = message.text.strip()

    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    cur.execute("SELECT * FROM standard_obj WHERE name='%s'" % obj_name)
    object_info = cur.fetchall()
    conn.commit()
    cur.close()
    conn.close()
    data = message.text.split(",")
    if data[0] != "/start":
        if len(object_info) == 1:
            x_0 = float(object_info[0][2])
            y_0 = float(object_info[0][3])
            v_x_0 = float(object_info[0][4])
            v_y_0 = float(object_info[0][5])
            end_time = float(object_info[0][6])

            bot.send_message(message.chat.id, f"{obj_name}, {x_0:.3}, {y_0:.3}, {v_x_0:.3}, {v_y_0:.3}, {end_time:.3}")
            bot.send_message(message.chat.id, f"x_0 = {x_0:.3} (м),     y_0 = {y_0:.3} (м)")
            bot.send_message(message.chat.id, f"v_x_0 = {v_x_0:.3} (м/c),     v_y_0 = {v_y_0:.3} (м/c)")
            bot.send_message(message.chat.id, f"end_time = {end_time:.3} (с)")

            make_anime(x_0, y_0, v_x_0, v_y_0, end_time, "my_calculation")

            img = open(r'animations/my_calculation.gif', 'rb')
            bot.send_video(message.chat.id, img, None)
            img.close()
        else:
            bot.send_message(message.chat.id, "Объект не найден")
    start(message)


@bot.callback_query_handler(func=lambda call: call.data == 'sub_button')
def callback(call):
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    cur.execute("SELECT name FROM standard_obj")
    objects = cur.fetchall()

    info = ""
    for el in objects:
        info += f"{el[0]}\n"

    cur.close()
    conn.close()

    bot.send_message(call.message.chat.id, info)


# Button 2: "Свое тело" ------------------------------------------------------------------------------------------------
def enter_initial_condition(message):
    bot.send_message(message.chat.id, "Введите начальные условия в формате: x, y, v_x, v_y, end_time")
    bot.register_next_step_handler(message, enter_initial_condition_continue)


def not_singular(x, y, v_x, v_y):
    x, y, v_x, v_y = float(x), float(y), float(v_x), float(v_y)
    if x != 0:
        tg_yx = y / x
    else:
        tg_yx = "infinity"

    if v_x != 0:
        tg_vv = v_y / v_x
    else:
        tg_vv = "infinity"
    if tg_yx == tg_vv:
        return False

    r = (x ** 2 + y ** 2) ** 0.5
    if r <= 1e8:
        return False
    return True


def enter_initial_condition_continue(message):
    data = message.text.split(",")
    if data[0] != "/start":
        try:
            x_0, y_0, v_x_0, v_y_0, end_time_0 = data
            x_0 = float(x_0)
            y_0 = float(y_0)
            v_x_0 = float(v_x_0)
            v_y_0 = float(v_y_0)
            end_time = float(end_time_0)

            if not_singular(x_0, y_0, v_x_0, v_y_0):
                result = make_anime(x_0, y_0, v_x_0, v_y_0, end_time, "my_calculation")
                if result:
                    img = open(r'animations/my_calculation.gif', 'rb')
                    bot.send_video(message.chat.id, img, None)
                    img.close()
                else:
                    bot.send_message(message.chat.id, "Сингулярное решение")
            else:
                bot.send_message(message.chat.id, "Сингулярное решение")
        except ValueError:
            bot.send_message(message.chat.id, "Некорректные данные")
    start(message)


# Button 3: "Добавить тело" --------------------------------------------------------------------------------------------
def add_initial_condition(message):
    bot.send_message(message.chat.id, "Введите начальные условия в формате: название, x, y, v_x, v_y, end_time")
    bot.register_next_step_handler(message, add_initial_condition_continue)


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def check_data(data):
    if len(data) == 6:
        object_name, x_0, y_0, v_x_0, v_y_0, end_time = data
        if is_number(x_0) and is_number(y_0) and is_number(v_x_0) and is_number(v_y_0) and is_number(end_time):
            if float(end_time) > 0:
                if not_singular(x_0, y_0, v_x_0, v_y_0):
                    return True
    return False


def add_initial_condition_continue(message):
    user_name = message.from_user.username
    data = message.text.split(",")

    if data[0] != "/start":
        if check_data(data):
            object_name, x_0, y_0, v_x_0, v_y_0, end_time = data
            object_name = object_name.strip()
            x_0 = float(x_0)
            y_0 = float(y_0)
            v_x_0 = float(v_x_0)
            v_y_0 = float(v_y_0)
            end_time = float(end_time)

            conn = sqlite3.connect("database.db")
            cur = conn.cursor()
            user_name = str(user_name)
            cur.execute(
                """CREATE TABLE IF NOT EXISTS '%s' (
                id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                name varchar(50),
                x decimal,
                y decimal,
                v_x decimal,
                v_y decimal,
                end_time decimal
                )""" % user_name)

            cur.execute("SELECT name FROM '%s'" % user_name)
            objects = cur.fetchall()

            if not (object_name,) in objects:
                cur.execute(
                    f"INSERT INTO '%s' (name, x, y, v_x, v_y, end_time) VALUES ('%s', '%s', '%s', '%s', '%s', '%s')" % (
                        user_name, object_name, x_0, y_0, v_x_0, v_y_0, end_time))
                conn.commit()
                cur.close()
                conn.close()
                bot.send_message(message.chat.id, "Объект добавлен в базу данных")
            else:
                bot.send_message(message.chat.id, "Объект с таким именем уже существует")
        else:
            bot.send_message(message.chat.id, "Некорректные данные")
    start(message)


# Button 4: "Выбрать тело" ---------------------------------------------------------------------------------------------
def read_data(message):
    user_name = message.chat.username
    user_name = str(user_name)
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    cur.execute(
        """CREATE TABLE IF NOT EXISTS '%s' (
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        name varchar(50),
        x decimal,
        y decimal,
        v_x decimal,
        v_y decimal,
        end_time decimal
        )""" % user_name)

    cur.execute("SELECT name FROM '%s'" % user_name)
    objects = cur.fetchall()

    cur.close()
    conn.close()

    if objects:
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton("Список существующих объектов", callback_data="objects"))
        bot.send_message(message.chat.id, "Введите название интересующего вас объекта", reply_markup=markup)

        bot.register_next_step_handler(message, read_data_continue)
    else:
        bot.send_message(message.chat.id, "Нет зарегистрированных объектов")
        start(message)


@bot.callback_query_handler(func=lambda call: call.data == 'objects')
def callback(call):
    user_name = call.message.chat.username
    user_name = str(user_name)

    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    cur.execute("SELECT name FROM '%s'" % user_name)
    objects = cur.fetchall()

    info = ""
    for el in objects:
        info += f"{el[0]}\n"

    cur.close()
    conn.close()

    bot.send_message(call.message.chat.id, info)


def read_data_continue(message):
    data = message.text.strip()
    user_name = message.from_user.username

    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    user_name = str(user_name)

    cur.execute("SELECT * FROM '%s' WHERE name='%s'" % (user_name, data))
    object_info = cur.fetchall()
    conn.commit()
    cur.close()
    conn.close()
    data = message.text.split(",")
    if data[0] != "/start":
        if object_info:
            obj_name = object_info[0][1]
            x_0 = float(object_info[0][2])
            y_0 = float(object_info[0][3])
            v_x_0 = float(object_info[0][4])
            v_y_0 = float(object_info[0][5])
            end_time = float(object_info[0][6])

            bot.send_message(message.chat.id, f"{obj_name}: {x_0:.3}, {y_0:.3}, {v_x_0:.3}, {v_y_0:.3}, {end_time:.3}")
            bot.send_message(message.chat.id, f"x_0 = {x_0:.3} (м),     y_0 = {y_0:.3} (м)")
            bot.send_message(message.chat.id, f"v_x_0 = {v_x_0:.3} (м/c),     v_y_0 = {v_y_0:.3} (м/c)")
            bot.send_message(message.chat.id, f"end_time = {end_time:.3} (с)")

            result = make_anime(x_0, y_0, v_x_0, v_y_0, end_time, "my_calculation")
            if result:
                img = open(r'animations/my_calculation.gif', 'rb')
                bot.send_video(message.chat.id, img, None)
                img.close()
            else:
                bot.send_message(message.chat.id, "Сингулярное решение")
        else:
            bot.send_message(message.chat.id, "Объект не найден")
    start(message)


# Button 5: "Удалить тело" ---------------------------------------------------------------------------------------------
def delete_body(message):
    user_name = message.chat.username
    user_name = str(user_name)
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    cur.execute(
        """CREATE TABLE IF NOT EXISTS '%s' (
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        name varchar(50),
        x decimal,
        y decimal,
        v_x decimal,
        v_y decimal,
        end_time decimal
        )""" % user_name)

    cur.execute("SELECT name FROM '%s'" % user_name)
    objects = cur.fetchall()

    cur.close()
    conn.close()

    if objects:
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton("Список существующих объектов", callback_data="objects"))
        bot.send_message(message.chat.id, "Введите название объекта, который вы хотите удалить.", reply_markup=markup)

        bot.register_next_step_handler(message, delete_body_continue)
    else:
        bot.send_message(message.chat.id, "Нет зарегистрированных объектов")
        start(message)


def delete_body_continue(message):
    user_name = message.from_user.username
    data = message.text.strip()
    if data != "/start":
        conn = sqlite3.connect("database.db")
        cur = conn.cursor()
        user_name = str(user_name)

        cur.execute("SELECT * FROM '%s' WHERE name='%s'" % (user_name, data))
        objects = cur.fetchall()
        if objects:
            cur.execute("DELETE FROM '%s' WHERE name = '%s'" % (user_name, data))
            bot.send_message(message.chat.id, "Объект удален.")
        else:
            bot.send_message(message.chat.id, "Объект не найден.")
        conn.commit()
        cur.close()
        conn.close()

    start(message)


# Button 6: "Help" -----------------------------------------------------------------------------------------------------

def help_button(message):
    help_text = """
Данный бот предназначен для создания анимаций движения тел в гравитационном поле Солнца.

В меню бота представлены 6 команд:

<b>1) Стандартное тело</b> - позволяет создать анимацию движения одного из стандартных тел. Список стандартных тел
   можно посмотреть во встроенной кнопке "Список стандартных тел". Стандартные тела создаются при ручном запуске файла
   standard_objects.py и не могут быть изменены при помощи интерфейса бота.
   
<b>2) Свое тело</b> - позволяет создать анимацию движения тела по заданным пользователем характеристикам в формате
   <b> x, y, v_x, v_y, end_time </b>, где

   - x это координата тела по оси абсцисс в начальный момент времени.
   - y это координата тела по оси ординат в начальный момент времени.
   - v_x это проекция скорости тела на ось абсцисс в начальный момент времени.
   - v_y это проекция скорости тела на ось ординат в начальный момент времени.
   - end_time это конечное время.
     Все величины указываются в системе единиц СИ.

<b>3) Добавить тело</b> - позволяет добавить характеристики тела в базу данных тел пользователя. Характеристики 
указываются в формате представленном ранее. В дальнейшем при помощи опции "Выбрать тело" можно  будет строить 
анимацию движения по этим данным. 

<b>4) Выбрать тело</b> - позволяет создать анимацию движения тела по заданным при помощи опции "Добавить тело" 
характеристикам. Так же при выполнении этой команды появляется встроенная кнопка "Список существующих объектов",
нажав на которую пользователь может увидеть список всех созданных им объектов. Для выполнения расчета требуется 
отправить боту сообщение с названием одного из тел имеющихся в базе данных тел пользователя.

<b>5) Удалить тело</b> - позволяет удалить тело из базы данных тел пользователя.

<b>6) Помощь</b> - выводит сообщение с пояснением команд.

<b><em>Уточнения:</em></b> 
<b> 1) </b> При отправке ботом анимации движения тела он также отправляет данные по которым была построена анимация.
<b> 2) </b> При задании начальных условий и времени расчета следует иметь в виду, что если эти данные ведут к сингулярному
решению или к решению, сопряженному с большими вычислительными трудностями, то бот не будет решать соответствующее
уравнение динамики, а выведет сообщение "Сингулярное решение" и вернет пользователя в главное меню.
<b> 3) </b> Команда /start возвращает пользователя в главное меню.
    """

    bot.send_message(message.chat.id, help_text, parse_mode='html')
    start(message)


bot.infinity_polling()
