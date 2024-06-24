import sqlite3
import json
from models.person import Person
from models.shiftsystem import Shiftsystem
from datetime import date
from typing import List
from settings import settings


class PersonDataAccess:

    def __init__(self):
        self.path = settings.DB_PATH
        self.connection = sqlite3.connect(self.path)
        self.cursor = self.connection.cursor()

    def create_person_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS 
            person (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                alias TEXT NOT NULL,
                shiftpattern_start_date TEXT NOT NULL,
                shiftsystem_id INTEGER,
                FOREIGN KEY (shiftsystem_id) REFERENCES shiftsystem (id)
            )
        """
        self.cursor.execute(query)
        self.connection.commit()

    def insert_person(self, person: Person):
        query = """
        INSERT INTO
            person (name, alias, shiftpattern_start_date, shiftsystem_id)
        VALUES
            (?, ?, ?, ?)
        """
        self.cursor.execute(query, (person.name,
                                    person.alias,
                                    person.shiftpattern_start_date.isoformat(),
                                    person.shiftsystem_id))
        self.connection.commit()
        self.connection.close()

    def get_one_person(self, id: int):
        query = """
        SELECT
            p.*, s.*
        FROM
            person AS p
        LEFT JOIN
            shiftsystem AS s
        ON
            s.id = p.shiftsystem_id
        WHERE
            p.id = ?
        """
        result = self.cursor.execute(query, (id,)).fetchone()
        try:
            shiftsystem = Shiftsystem(result[6], json.loads(result[7]), result[5])
        except TypeError:
            shiftsystem = None
        person = Person(result[1], result[2], date.fromisoformat(result[3]), result[0], result[5], shiftsystem)
        self.connection.close()
        return person

    def get_all_persons(self) -> List[Person]:
        query = """
        SELECT
            p.*, s.*
        FROM
            person AS p
        LEFT JOIN
            shiftsystem AS s
        ON
            s.id = p.shiftsystem_id
        """
        results = self.cursor.execute(query).fetchall()
        list_of_persons = []
        for result in results:
            try:
                shiftsystem = Shiftsystem(result[6], json.loads(result[7]), result[5])
            except TypeError:
                shiftsystem = None
            person = Person(result[1], result[2], date.fromisoformat(result[3]), result[0], result[5], shiftsystem)
            list_of_persons.append(person)
        self.connection.close()
        return list_of_persons

    def update_person(self, person: Person):
        query = """
        UPDATE
            person
        SET
            name = ?,
            alias = ?,
            shiftpattern_start_date = ?,
            shiftsystem_id = ?
        WHERE
            id = ?
        """
        self.cursor.execute(query, (person.name,
                                    person.alias,
                                    person.shiftpattern_start_date.isoformat(),
                                    person.shiftsystem_id,
                                    person.id))
        self.connection.commit()

    def delete_person(self, id: int):
        query = """
        DELETE FROM
            person
        WHERE
            id = ?
        """
        self.cursor.execute(query, (id,))
        self.connection.commit()
        self.connection.close()
