import db
from .student import Student
from .tools import is_uuid


class Group:
    def __init__(self, _id, department=None, name=None, course=None, head=None):
        if not is_uuid(_id):
            raise ValueError(f'Некорректный идентификатор {_id}')
        self.id = str(_id)
        self.department = str(department) if is_uuid(department) else None
        self.name = name
        self.course = course
        self.head = str(head) if is_uuid(head) else None
        self.__connection__ = None

    @property
    def connection(self):
        if not self.__connection__:
            self.__connection__ = db.Connection()
        return self.__connection__

    @property
    def exists(self):
        return bool(self.connection.exec_query(__EXISTS_GROUP__, self.id)[0][0])

    def save(self):
        self.connection.exec_query(
            __UPD_GROUP__ if self.exists else __INS_GROUP__,
            self.id, self.department, self.name, self.course, self.head
        )
        return self

    def delete(self):
        self.connection.exec_query(__DEL_GROUP__, self.id)
        return True

    def read(self):
        response = self.connection.exec_query(__READ_GROUP__, self.id)
        if response:
            self.id, self.department, self.name, self.course, self.head = response[0]
        return self

    def read_students(self):
        response = self.connection.exec_query(__READ_GROUP_STUDENTS__, self.id)
        return [Student(*row) for row in response]

    def as_dict(self):
        return {
            'id': self.id,
            'department': self.department,
            'name': self.name,
            'course': self.course,
            'head': self.head
        }


__READ_GROUP__ = '''
SELECT * FROM "group" WHERE id = :1;
'''

__EXISTS_GROUP__ = '''
SELECT exists(SELECT 1 FROM "group" WHERE id = :1 LIMIT 1);
'''

__INS_GROUP__ = '''
INSERT INTO "group" (id, department, name, course, head)
VALUES (:1, :2, :3, :4, :5);
'''

__UPD_GROUP__ = '''
UPDATE "group"
SET department = coalesce(:2, department),
    name = coalesce(:3, name),
    course = coalesce(:4, course),
    head = coalesce(:5, head)
WHERE id = :1;
'''

__DEL_GROUP__ = '''
DELETE FROM "group"
WHERE id = :1;
'''

__READ_GROUP_STUDENTS__ = '''
SELECT * FROM student WHERE "group" = :1;
'''
