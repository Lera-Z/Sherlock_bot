import telebot
import config
from telebot import types
from db import *


bot = telebot.TeleBot(config.token)
hideBoard = types.ReplyKeyboardRemove(selective=True)


@bot.message_handler(commands=['start'])
def cmd_start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row('/get_answer', '/get_people', '/get_questions', '/get_classes')
    markup.row('/add_person', '/add_question', '/add_answer')
    bot.send_message(message.chat.id, "Привет! Это Шерлок-бот\n\nВыберите, что вы хотите сделать:", reply_markup=markup)


@bot.message_handler(commands=['stop', 'menu'])
def cmd_stop(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row('/get_answer', '/get_people', '/get_questions', '/get_classes')
    markup.row('/add_person', '/add_question', '/add_answer')
    bot.send_message(message.chat.id, "Выберите, что вы хотите сделать:", reply_markup=markup)


@bot.message_handler(commands=['get_answer'])
def retrieve_answer(m):
    bot.send_message(m.chat.id, '[ /stop чтобы вернуться к меню ]\n\nВыберите и введите id человека из предложенных ниже:', reply_markup=hideBoard)
    people = retrieve_people()
    # answers = retrieve_answers()
    text = '\n'.join(['{id}. {first} {middle} {last}'.format(id=str(x[0]), first=x[1], middle=x[3], last=x[2]) for x in people])
    bot.send_message(m.chat.id, text)
    bot.register_next_step_handler(m, choose_person)


def choose_person(m):
    person_id = m.text
    questions = get_questions_for_person(person_id)
    bot.send_message(m.chat.id, '[ /stop чтобы вернуться к меню ]\n\nВыберите и введите id вопроса из предложенных ниже, на который вы хотите получить ответ:', reply_markup=hideBoard)
    text = '\n'.join([str(x[0]) + '.' + ' ' + x[1] for x in questions])
    bot.send_message(m.chat.id, text)
    bot.register_next_step_handler(m, lambda msg: print_answers(m=msg, person_id=person_id))

def print_answers(m, person_id):
    question_id = m.text
    answer = get_answer(person_id, question_id)
    bot.send_message(m.chat.id, answer[0])


@bot.message_handler(commands=['add_question'])
def add_question(m):
    question = Question()
    bot.send_message(m.chat.id, '[ /add_class чтобы добавить новый класс ]\n[ /stop чтобы вернуться к меню ]\n\nВыберите и введите id классa из предложенных ниже:', reply_markup=hideBoard)
    classes = retrieve_classes()
    text = '\n'.join([str(x[0]) + ' ' + x[1] for x in classes])
    bot.send_message(m.chat.id, text)
    bot.register_next_step_handler(m, lambda msg: choose_class(m=msg, question=question))


def choose_class(m, question):
    if m.text not in ['/start', '/stop', '/menu', '/add_class']:
        question.question_class = m.text
        bot.send_message(m.chat.id, '[ /stop чтобы вернуться к меню ]\n\n Введите текст вопроса:',
                         reply_markup=hideBoard)
        bot.register_next_step_handler(m, lambda msg: add_text(m=msg, question=question))


def add_text(m, question):
    if m.text not in ['/start', '/stop', '/menu']:
        question.question_text = m.text
        question.add_to_db()
        bot.send_message(m.chat.id, '[ /menu чтобы вернуться к меню ]\n\nВопрос записан!')


@bot.message_handler(commands=['add_class'])
def add_class(m):
    bot.send_message(m.chat.id, 'Введите название класса:')
    bot.register_next_step_handler(m, add_new_class_to_db)


def add_new_class_to_db(m):
    text = m.text
    add_new_class(text)
    bot.send_message(m.chat.id, '[ /menu чтобы вернуться к меню ]\n\nКласс записан!')


@bot.message_handler(commands=['add_person'])
def add_person(m):
    person = Person()
    bot.send_message(m.chat.id, '[ /stop чтобы вернуться к меню ]\n\nВведите имя:', reply_markup=hideBoard)
    bot.register_next_step_handler(m, lambda msg: add_first_name(m=msg, person=person))


def add_first_name(m, person):
    if m.text not in ['/start', '/stop', '/menu']:
        person.first_name = m.text
        bot.send_message(m.chat.id, '[ /stop чтобы вернуться к меню ]\n\nВведите фамилию:')
        bot.register_next_step_handler(m, lambda msg: add_last_name(m=msg, person=person))


def add_last_name(m, person):
    if m.text not in ['/start', '/stop', '/menu']:
        person.last_name = m.text
        bot.send_message(m.chat.id, '[ /stop чтобы вернуться к меню ]\n\nВведите отчество:')
        bot.register_next_step_handler(m, lambda msg: add_middle_name(m=msg, person=person))


def add_middle_name(m, person):
    if m.text not in ['/start', '/stop', '/menu']:
        person.middle_name = m.text
        bot.send_message(m.chat.id, '[ /stop чтобы вернуться к меню ]\n\nВведите возраст:')
        bot.register_next_step_handler(m, lambda msg: add_age(m=msg, person=person))


def add_age(m, person):
    if m.text not in ['/start', '/stop', '/menu']:
        try:
            person.age = int(m.text)
            bot.send_message(m.chat.id, '[ /stop чтобы вернуться к меню ]\n\nВведите пол:')
            bot.register_next_step_handler(m, lambda msg: add_sex(m=msg, person=person))
        except ValueError:
            bot.send_message(m.chat.id, '[ /stop чтобы вернуться к меню ]\n\nНеверное число, попробуйте снова:')
            bot.register_next_step_handler(m, lambda msg: add_age(m=msg, person=person))


def add_sex(m, person):
    if m.text not in ['/start', '/stop', '/menu', '/add_age']:
        person.sex = 1 if m.text == 'Женский' else 0
        bot.send_message(m.chat.id, '[ /menu чтобы вернуться к меню ]\n\nВведите город:')
        bot.register_next_step_handler(m, lambda msg: add_city(m=msg, person=person))

def add_city(m, person):
    if m.text not in ['/start', '/stop', '/menu', '/add_age']:
        person.city = m.text
        bot.send_message(m.chat.id, '[ /menu чтобы вернуться к меню ]\n\nВведите номер телефона:')
        bot.register_next_step_handler(m, lambda msg: add_phone_num(m=msg, person=person))

def add_phone_num(m, person):
    if m.text not in ['/start', '/stop', '/menu', '/add_age']:
        person.phone = m.text
        bot.send_message(m.chat.id, '[ /menu чтобы вернуться к меню ]\n\nВведите веб-сайт:')
        bot.register_next_step_handler(m, lambda msg: add_web_site(m=msg, person=person))

def add_web_site(m, person):
    if m.text not in ['/start', '/stop', '/menu', '/add_age']:
        person.website = m.text
        person.add_to_db()
        bot.send_message(m.chat.id, '[ /menu чтобы вернуться к меню ]\n\nЧеловек записан!')

@bot.message_handler(commands=['get_people'])
def do_something(m):
    people = get_people()
    msg = '\n'.join([', '.join([str(item) for item in person]) for person in people])
    bot.send_message(m.chat.id, msg)


@bot.message_handler(commands=['get_classes'])
def get_questions(m):
    cls = retrieve_classes()
    text = '\n'.join([str(x[0]) + ' ' + x[1] for x in cls])
    bot.send_message(m.chat.id, text)


@bot.message_handler(commands=['get_questions'])
def get_questions(m):
    questions = retrieve_questions()
    text = '\n'.join([str(x[0]) + ' ' + x[1] for x in questions])
    bot.send_message(m.chat.id, text)

@bot.message_handler(commands=['add_answer'])
def add_answer(m):
    bot.send_message(m.chat.id, '[ /stop чтобы вернуться к меню ]\n\nВыберите и введите id человека из предложенных ниже:', reply_markup=hideBoard)
    people = retrieve_people()
    # answers = retrieve_answers()
    text = '\n'.join(['{id}. {first} {middle} {last}'.format(id=str(x[0]), first=x[1], middle=x[3], last=x[2]) for x in people])
    bot.send_message(m.chat.id, text)
    bot.register_next_step_handler(m, choose_person_add)


def choose_person_add(m):
    if m.text not in ['/start', '/stop', '/menu', '/add_age']:
        person_id = m.text
        questions = get_questions_for_person(person_id)
        bot.send_message(m.chat.id, '[ /stop чтобы вернуться к меню ]\n\nВыберите и введите id вопроса из предложенных ниже, на который вы хотите получить ответ:', reply_markup=hideBoard)
        text = '\n'.join([str(x[0]) + '.' + ' ' + x[1] for x in questions])
        bot.send_message(m.chat.id, text)
        bot.register_next_step_handler(m, lambda msg: choose_question(m=msg, person_id=person_id))
        print('person')

def choose_question(m, person_id):
    # print(m)
    # print(type(m))
    if m.text not in ['/start', '/stop', '/menu', '/add_age']:
        # print('quest')
        question_id = m.text
        bot.send_message(m.chat.id, '[ /stop чтобы вернуться к меню ]\n\nВведите текст ответа', reply_markup=hideBoard)
        bot.register_next_step_handler(m, lambda msg: write_new_answer_to_db(m=msg, person_id=person_id, question_id=question_id))

def write_new_answer_to_db(m, person_id, question_id):
    print(m)
    print(type(m))
    if m.text not in ['/start', '/stop', '/menu', '/add_age']:
        answer_text = m.text
        write_answer_to_db(person_id, question_id, answer_text)
        bot.send_message(m.chat.id, 'Ответ записан!')

if __name__ == '__main__':
    bot.polling(none_stop=True)
