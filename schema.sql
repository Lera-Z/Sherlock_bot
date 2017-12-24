create table Person (
  id			integer primary key autoincrement not null,
  first_name text not null,
  last_name text,
  middle_name text,
  age integer,
  sex boolean not null,
  city text,
--  birth_place text,
--  study_place text,
--  work_place text,
  phone text,
  website text
--  relationship_status text,
--  smoking integer,
--  alcohol integer,
--  about_me text

);

create table Lang (
    id			integer primary key autoincrement not null,
    language_name text
);

create table Speaker (
    id			integer primary key autoincrement not null,
    person_id integer,
    lang_id integer,
    FOREIGN KEY(person_id) REFERENCES Person(id),
    FOREIGN KEY(lang_id) REFERENCES Lang(id)
);

create table Question (
  id			integer primary key autoincrement not null,
  question_text text,
  question_class integer,
  FOREIGN KEY(question_class) REFERENCES Class(id)
);

create table Answer (
    id			integer primary key autoincrement not null,
    person_id integer,
    question_id integer,
    answer_text 		text,
    FOREIGN KEY(person_id) REFERENCES Person(id),
    FOREIGN KEY(question_id) REFERENCES Question(id)
);


create table Class (
    id			integer primary key autoincrement not null,
    class text
);



