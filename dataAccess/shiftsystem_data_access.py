import sqlite3
import json
from models.shiftsystem import Shiftsystem
from settings import settings


class ShiftsystemDataAccess:
    def __init__(self):
        self.path = settings.DB_PATH
        self.connection = sqlite3.connect(self.path)
        self.cursor = self.connection.cursor()
        
    def create_shiftsystem_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS 
            shiftsystem (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                shiftpattern TEXT NOT NULL
            )
        """
        self.cursor.execute(query)
        self.connection.commit()
        
    def insert_shiftsystem(self, shiftsystem: Shiftsystem):
        query = """
        INSERT INTO
            shiftsystem (name, shiftpattern)
        VALUES
            (?, ?)
        """
        self.cursor.execute(query, (shiftsystem.name, json.dumps(shiftsystem.shiftpattern)))
        self.connection.commit()
        
    def get_one_shiftsystem(self, id: int):
        query = """
        SELECT
            *
        FROM
            shiftsystem
        WHERE
            id = ?
        """
        result = self.cursor.execute(query, (id,)).fetchone()
        return Shiftsystem(result[1], json.loads(result[2]), result[0])
    
    def get_all_shiftsystems(self):
        query = """
        SELECT
            *
        FROM
            shiftsystem
        """
        result = self.cursor.execute(query).fetchall()
        list_of_shiftsystems = [Shiftsystem(x[1], json.loads(x[2]), x[0]) for x in result]
        return list_of_shiftsystems
    
    def update_shiftsystem(self, shiftsystem: Shiftsystem):
        query = """
        UPDATE
            shiftsystem
        SET
            name = ?,
            shiftpattern = ?
        WHERE
            id = ?
        """
        self.cursor.execute(query, (shiftsystem.name, json.dumps(shiftsystem.shiftpattern), shiftsystem.id))
        self.connection.commit()
        
    def delete_shiftsystem(self, id: int):
        query = """
        DELETE FROM
            shiftsystem
        WHERE
            id = ?
        """
        self.cursor.execute(query, (id,))
        self.connection.commit()
