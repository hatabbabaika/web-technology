from .connection import Connection


def create():
    con = Connection()
    con.exec_query('''
    CREATE TABLE IF NOT EXISTS student (
        id UUID PRIMARY KEY,
        "group" UUID NOT NULL,
        last_name TEXT NOT NULL,
        first_name TEXT NOT NULL,
        patronymic TEXT
    );
    ''')
    con.exec_query('''
    CREATE INDEX IF NOT EXISTS group_students ON student ("group");
    ''')

    con.exec_query('''
    CREATE TABLE IF NOT EXISTS "group" (
        id UUID PRIMARY KEY,
        department UUID NOT NULL,
        name TEXT NOT NULL,
        course INTEGER NOT NULL,
        head UUID NOT NULL
    );
    ''')
    con.exec_query('''
    CREATE INDEX IF NOT EXISTS department_groups ON "group" (department);
    ''')

    con.exec_query('''
    CREATE TABLE IF NOT EXISTS department (
        id UUID PRIMARY KEY,
        faculty UUID NOT NULL,
        name TEXT NOT NULL,
        head TEXT NOT NULL,
        info TEXT
    );
    ''')
    con.exec_query('''
    CREATE INDEX IF NOT EXISTS faculty_departments ON department (faculty);
    ''')

    con.exec_query('''
    CREATE TABLE IF NOT EXISTS faculty (
        id UUID PRIMARY KEY,
        name TEXT NOT NULL,
        dean TEXT NOT NULL,
        info TEXT
    );
    ''')

    del con

