import sqlite3

DBFILE = 'sherlock.db'


class Person:
    def __init__(self):
        self.db = DBFILE
        self.first_name = None
        self.last_name = None
        self.middle_name = None
        self.age = None
        self.sex = None
        self.city = None
        self.phone = None
        self.website = None


    def add_to_db(self):
        with sqlite3.connect(DBFILE) as conn:
            conn.execute("PRAGMA foreign_keys = 1")

            person = (self.first_name, self.last_name, self.middle_name, self.age, self.sex, self.city, self.phone, self.website)

            q = conn.execute(
                'insert  into Person(first_name, last_name, middle_name, age, sex, city, phone, website) values (?,?,?,?,?,?,?,?)',
                person)
            person_id = q.lastrowid


def get_people():
    with sqlite3.connect(DBFILE) as conn:
        conn.execute("PRAGMA foreign_keys = 1")
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Person;')
        return cursor.fetchall()


class Question:
    def __init__(self):
        self.db = DBFILE
        self.question_text = None
        self.question_class = None

    def add_to_db(self):
        with sqlite3.connect(DBFILE) as conn:
            conn.execute("PRAGMA foreign_keys = 1")

            question = (self.question_text, self.question_class)

            q = conn.execute(
                'insert  into Question(question_text, question_class) values (?,?)',
                question)
            question_id = q.lastrowid



class Classes:
    def __init__(self):
        self.db = DBFILE
        self.text = None

def add_new_class(text):
    with sqlite3.connect(DBFILE) as conn:
        conn.execute("PRAGMA foreign_keys = 1")

        text = (text, )
        q = conn.execute(
            'insert  into Class(class) values (?)',
            text)
        class_id = q.lastrowid




def retrieve_classes():
    with sqlite3.connect(DBFILE) as conn:
        conn.execute("PRAGMA foreign_keys = 1")
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Class;')
        return cursor.fetchall()

def retrieve_questions():
    with sqlite3.connect(DBFILE) as conn:
        conn.execute("PRAGMA foreign_keys = 1")
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Question;')
        return cursor.fetchall()

def retrieve_people():
    with sqlite3.connect(DBFILE) as conn:
        conn.execute("PRAGMA foreign_keys = 1")
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Person;')
        return cursor.fetchall()

def get_questions_for_person(person_id):
    with sqlite3.connect(DBFILE) as conn:
        conn.execute("PRAGMA foreign_keys = 1")
        cursor = conn.cursor()
        cursor.execute('SELECT Answer.question_id, Question.question_text FROM Answer JOIN Question ON Answer.question_id = Question.id WHERE Answer.person_id = {};'.format(person_id))
        questions = cursor.fetchall()
        return questions


def get_answer(person_id, question_id):
    with sqlite3.connect(DBFILE) as conn:
        conn.execute("PRAGMA foreign_keys = 1")
        cursor = conn.cursor()
        cursor.execute('SELECT answer_text FROM Answer WHERE person_id = {} AND question_id = {};'.format(person_id, question_id))
        answer = cursor.fetchone()
        return answer

def write_answer_to_db(person_id, question_id, answer_text):
    with sqlite3.connect(DBFILE) as conn:
        conn.execute("PRAGMA foreign_keys = 1")
        answer = (person_id, question_id, answer_text)

        q = conn.execute(
            'insert  into Answer(person_id, question_id, answer_text) values (?,?,?)',
            answer)
        question_id = q.lastrowid