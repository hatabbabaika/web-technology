import db
from .group import Group
from .tools import is_uuid


class Department:
    def __init__(self, _id, faculty=None, name=None, head=None, info=None):
        if not is_uuid(_id):
            raise ValueError(f'Некорректный идентификатор {_id}')
        self.id = str(_id)
        self.faculty = str(faculty) if is_uuid(faculty) else None
        self.name = name
        self.head = head
        self.info = info
        self.__connection__ = None

    @property
    def connection(self):
        if not self.__connection__:
            self.__connection__ = db.Connection()
        return self.__connection__

    @property
    def exists(self):
        return bool(self.connection.exec_query(__EXISTS_DEPARTMENT__, self.id)[0][0])

    def save(self):
        self.connection.exec_query(
            __UPD_DEPARTMENT__ if self.exists else __INS_DEPARTMENT__,
            self.id, self.faculty, self.name, self.head, self.info
        )
        return self

    def delete(self):
        self.connection.exec_query(__DEL_DEPARTMENT__, self.id)
        return True

    def read(self):
        response = self.connection.exec_query(__READ_DEPARTMENT__, self.id)
        if response:
            self.id, self.faculty, self.name, self.head, self.info = response[0]
        return self

    def read_groups(self):
        response = self.connection.exec_query(__READ_DEPARTMENT_GROUPS__, self.id)
        return [Group(*row) for row in response]

    def as_dict(self):
        return {
            'id': self.id,
            'faculty': self.faculty,
            'name': self.name,
            'head': self.head,
            'info': self.info
        }


__READ_DEPARTMENT__ = '''
SELECT * FROM department WHERE id = :1;
'''

__EXISTS_DEPARTMENT__ = '''
SELECT exists(SELECT 1 FROM department WHERE id = :1 LIMIT 1);
'''

__INS_DEPARTMENT__ = '''
INSERT INTO department (id, faculty, name, head, info)
VALUES (:1, :2, :3, :4, :5);
'''

__UPD_DEPARTMENT__ = '''
UPDATE department
SET faculty = coalesce(:2, faculty),
    name = coalesce(:3, name),
    head = coalesce(:4, head),
    info = coalesce(:5, info)
WHERE id = :1;
'''

__DEL_DEPARTMENT__ = '''
DELETE FROM department
WHERE id = :1;
'''

__READ_DEPARTMENT_GROUPS__ = '''
SELECT * FROM "group" WHERE department = :1;
'''