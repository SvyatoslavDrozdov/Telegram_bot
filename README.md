# Телеграм бот

Данный бот предназначен для создания анимаций движения тел в гравитационном поле Солнца.

В меню бота представлены 6 команд:

1) <b>Стандартные тела</b> - позволяет создать анимацию движения одного из стандартных тел. Список стандартных тел
   можно посмотреть во встроенной кнопке "Список стандартных тел". Стандартные тела создаются при ручном запуске файла
   standard_objects.py и не могут быть изменены при помощи интерфейса бота.
2) <b>Свое тело</b> - позволяет создать анимацию движения тела по заданным пользователем характеристикам в формате
   <b> x, y, v_x, v_y, end_time </b>, где

    - x это координата тела по оси абсцисс в начальный момент времени.
    - y это координата тела по оси ординат в начальный момент времени.
    - v_x это проекция скорости тела на ось абсцисс в начальный момент времени.
    - v_y это проекция скорости тела на ось ординат в начальный момент времени.
    - end_time это конечное время.
      Все величины указываются в системе единиц СИ.

3) <b>Добавить тело</b> - позволяет добавить характеристики тела в таблицу данных тел пользователя. Характеристики
   указываются в формате представленном ранее. В дальнейшем при помощи опции "Выбрать тело" можно будет строить
   анимацию движения по этим данным.
4) <b>Выбрать тело</b> - позволяет создать анимацию движения тела по заданным при помощи опции "Добавить тело"
   характеристикам. Так же при выполнении этой команды появляется встроенная кнопка "Список существующих объектов",
   нажав на которую пользователь может увидеть список всех созданных им объектов. Для выполнения расчета требуется
   отправить боту сообщение с названием одного из тел имеющихся в таблице данных тел пользователя.
5) <b>Удалить тело</b> - позволяет удалить тело из таблицы данных тел пользователя.
6) <b>Помощь</b> - выводит сообщение с пояснением команд.

***Уточнения:***

1) При отправке ботом анимации движения тела он также отправляет данные по которым была построена анимация.
2) При задании начальных условий и времени расчета следует иметь в виду, что если эти данные ведут к сингулярному
   решению или к решению, сопряженному с большими вычислительными трудностями, то бот не будет решать соответствующее
   уравнение динамики, а выведет сообщение "Сингулярное решение" и вернет пользователя в главное меню.
3) Команда /start возвращает пользователя в главное меню.

***Структура проекта:***

Данный проект состоит из следующих файлов с кодом на python _teleBot.py_, _ERK2_l.py_, _animation.py_, 
_standard_objects.py_.

1) Файл __teleBot.py__ содержит основной код бота. В нем находится основная логика программы и описание работы кнопок.
2) Файл __ERK2_l.py__ находится в директории _solver_. В этом файле реализован алгоритм решения дифференциального
   уравнения динамики тела, находящегося в центральном поле. Для решения использован явный метод Рунге-Кутты 2-го
   порядка с разбиением вдоль интегральной кривой.
   (Что отражено в названии <b>ERK2_l:</b> <b>E</b>xplicit <b>R</b>unge-<b>K</b>utta method of the <b>2</b>nd order with steps
   along the <b>l</b>ength of the integral curve.)
3) Файл __animation.py__ находится в директории _animations_. В этом файле реализовано создание анимации движения 
тела на основании решения уравнения динамики движения тела с начальными условиями переданными пользователем.
4) Файл __standard_objects.py__ содержит код для создания таблицы стандартных тел. Он корректируется и запускается
вручную когда требуется изменить базу данных стандартных тел. 

Так же в проекте присутствует база данных __database.db__ в которой существуют следующие таблицы:
1) standard_obj - таблица стандартных объектов.
2) "user_name" - таблица с именем пользователя в telegram. Таких таблиц может быть не ограничено много. В каждой
подобной таблице хранятся данные об объектах, которые задал пользователь. 

***Запуск проекта:***
1) Для работы вам понадобится установить интерпретатор python версии 3.12
2) Скачать файлы из данного репозитория. 
3) Установить требуемые библиотеки командой pip install -r requirements.txt.
4) Запустить файл __teleBot.py__.