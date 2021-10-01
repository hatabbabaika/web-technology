import db
from .department import Department
from .tools import is_uuid


class Faculty:
    def __init__(self, _id, name=None, dean=None, info=None):
        if not is_uuid(_id):
            raise ValueError(f'Некорректный идентификатор {_id}')
        self.id = str(_id)
        self.name = name
        self.dean = dean
        self.info = info
        self.__connection__ = None

    @property
    def connection(self):
        if not self.__connection__:
            self.__connection__ = db.Connection()
        return self.__connection__

    @property
    def exists(self):
        return bool(self.connection.exec_query(__EXISTS_FACULTY__, self.id)[0][0])

    def save(self):
        self.connection.exec_query(
            __UPD_FACULTY__ if self.exists else __INS_FACULTY__,
            self.id, self.name, self.dean, self.info
        )
        return self

    def read(self):
        response = self.connection.exec_query(__READ_FACULTY__, self.id)
        if response:
            self.id, self.name, self.dean, self.info = response[0]
        return self

    def delete(self):
        self.connection.exec_query(__DEL_FACULTY__, self.id)
        return True

    def read_departments(self):
        response = self.connection.exec_query(__READ_FACULTY_DEPARTMENTS__, self.id)
        return [Department(*row) for row in response]

    def as_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'dean': self.dean,
            'info': self.info
        }


def get_faculties():
    connections = db.Connection()
    return [Faculty(*row) for row in connections.exec_query(__READ_FACULTIES__)]


__READ_FACULTIES__ = '''
SELECT * FROM faculty;
'''

__READ_FACULTY__ = '''
SELECT * FROM faculty WHERE id = :1;
'''

__EXISTS_FACULTY__ = '''
SELECT exists(SELECT 1 FROM faculty WHERE id = :1 LIMIT 1);
'''

__INS_FACULTY__ = '''
INSERT INTO faculty (id, name, dean, info)
VALUES (:1, :2, :3, :4);
'''

__UPD_FACULTY__ = '''
UPDATE faculty
SET name = coalesce(:2, name),
    dean = coalesce(:3, dean),
    info = coalesce(:4, info)
WHERE id = :1;
'''

__DEL_FACULTY__ = '''
DELETE FROM faculty
WHERE id = :1;
'''

__READ_FACULTY_DEPARTMENTS__ = '''
SELECT * FROM department WHERE faculty = :1;
'''