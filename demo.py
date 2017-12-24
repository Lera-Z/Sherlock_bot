import os
import sqlite3
from datetime import datetime

DBFILE = 'sherlock.db'
DBSCHEMA = 'schema.sql'


def create_db(dbfile, schemafile):
    print('create db:', dbfile)
    has_db = os.path.exists(dbfile)
    if has_db: 
        print('database exists, exit')
        return False

    with sqlite3.connect(dbfile) as conn:
        conn.execute("PRAGMA foreign_keys = 1")
        print('creating schema')
        schema = None
        with open(schemafile, 'rt') as f:
            schema = f.read()

        if schema is not None:
            conn.executescript(schema)

        print('schema created successfully')
    
    return True


def fill_db(dbfile):
    with sqlite3.connect(dbfile) as conn:
        conn.execute("PRAGMA foreign_keys = 1")
        print('filling database...')

        # --- Languages ---
        langs = [
            ('Английский',),
            ('Немецкий',),
            ('Литовский',)
        ]
        conn.executemany('insert into Lang(language_name) values (?)', langs)

        # --- Person ---
        person = ('Ivan', 'Ivanov', 'Alexandrovich', 27, 0, 'Moscow', '+99999', 'me.com')

        q = conn.execute('insert  into Person(first_name, last_name, middle_name, age, sex, city, phone, website) values (?,?,?,?,?,?,?,?)',
                         person)
        person_id = q.lastrowid

        # # --- Classes ---
        classes = [
            ('Еда',),
            ('Музыка',),]
        conn.executemany('insert into Class(class) values (?)', classes)

        eng_id = conn.execute('SELECT id FROM Lang WHERE language_name = "Английский"')
        # print('________')
        # print(eng_id.fetchone()[0])
        eng_id = eng_id.fetchone()[0]

        # --- Speaker ---
        person_langs = [
            (person_id, eng_id),
            # (person_id, ger_id),
        ]
        print(person_langs)
        conn.executemany('insert into Speaker(person_id, lang_id) values (?, ?)', person_langs)

        # --- Question ---

        class_id = conn.execute('SELECT id FROM Class WHERE class = "Еда"')
        class_id = class_id.fetchone()[0]
        questions = ('Твоя любимая еда?', class_id)
        conn.execute('insert into Question(question_text, question_class) values (?,?)', questions)

        # --- Answer ---

        class_id = conn.execute('SELECT id FROM Class WHERE class = "Еда"')
        class_id = class_id.fetchone()[0]
        questions = ('Твоя любимая еда?', class_id)
        conn.execute('insert into Question(question_text, question_class) values (?,?)', questions)

        question_id = 1
        person_id = 1
        answers = (person_id, question_id, 'Рыба')
        conn.execute('insert into Answer(person_id, question_id, answer_text) values (?,?,?)', answers)


def query_db(dbfile):
    with sqlite3.connect(dbfile) as conn:
        conn.execute("PRAGMA foreign_keys = 1")

        print('querying database...')

        print('--- Languages:')
        cursor = conn.cursor()
        cursor.execute('select * from Lang;')
        for row in cursor.fetchall():
            print(row)

        print('--- Person: ')
        cursor.execute('SELECT * FROM Person;')
        for row in cursor.fetchall():
            print(row)
        #
        print('--- Classes: ')
        cursor.execute('SELECT * FROM Class;')
        # cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")

        for row in cursor.fetchall():
            print(row)
        #

        print('--- Speakers: ')
        cursor.execute('SELECT * FROM Speaker;')
        for row in cursor.fetchall():
            print(row)

        print('--- Questions: ')
        cursor.execute('SELECT * FROM Question;')
        for row in cursor.fetchall():
            print(row)

        print('--- Answers: ')
        cursor.execute('SELECT * FROM Answer;')
        for row in cursor.fetchall():
            print(row)

def main():
    # --- prepare DB
    create_db(DBFILE, DBSCHEMA)
    fill_db(DBFILE)

    # --- query DB
    query_db(DBFILE)


if __name__ == '__main__':
    main()
