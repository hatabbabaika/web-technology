import db
from .tools import is_uuid


class Student:
    def __init__(self, _id, group=None, last_name=None, first_name=None, patronymic=None):
        if not is_uuid(_id):
            raise ValueError(f'Некорректный идентификатор {_id}')
        self.id = str(_id)
        self.group = str(group) if is_uuid(group) else None
        self.last_name = last_name
        self.first_name = first_name
        self.patronymic = patronymic
        self.__connection__ = None

    @property
    def connection(self):
        if not self.__connection__:
            self.__connection__ = db.Connection()
        return self.__connection__

    @property
    def exists(self):
        return bool(self.connection.exec_query(__EXISTS_STUDENT__, self.id)[0][0])

    def save(self):
        self.connection.exec_query(
            __UPD_STUDENT__ if self.exists else __INS_STUDENT__,
            self.id, self.group, self.last_name, self.first_name, self.patronymic
        )
        return self

    def delete(self):
        self.connection.exec_query(__DEL_STUDENT__, self.id)
        return True

    def read(self):
        response = self.connection.exec_query(__READ_STUDENT__, self.id)
        if response:
            self.id, self.group, self.last_name, self.first_name, self.patronymic = response[0]
        return self

    def as_dict(self):
        return {
            'id': self.id,
            'group': self.group,
            'last_name': self.last_name,
            'first_name': self.first_name,
            'patronymic': self.patronymic
        }


__READ_STUDENT__ = '''
SELECT * FROM student WHERE id = :1;
'''

__EXISTS_STUDENT__ = '''
SELECT exists(SELECT 1 FROM student WHERE id = :1 LIMIT 1);
'''

__INS_STUDENT__ = '''
INSERT INTO student (id, "group", last_name, first_name, patronymic)
VALUES (:1, :2, :3, :4, :5);
'''

__UPD_STUDENT__ = '''
UPDATE student
SET "group" = coalesce(:2, "group"),
    last_name = coalesce(:3, last_name),
    first_name = coalesce(:4, first_name),
    patronymic = coalesce(:5, patronymic)
WHERE id = :1;
'''

__DEL_STUDENT__ = '''
DELETE FROM student
WHERE id = :1;
'''
