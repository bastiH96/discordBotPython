from datetime import date
from models.shiftsystem import Shiftsystem


class Person:

    def __init__(self, name: str, 
                 alias: str, 
                 shiftpattern_start_date: date, 
                 id: int = None,
                 shiftsystem_id: int = None,
                 shiftsystem: Shiftsystem = None,
                 shiftpattern_iterator: int = 0):
        
        self.id = id
        self.name = name
        self.alias = alias
        self.shiftpattern_start_date = shiftpattern_start_date
        self.shiftsystem_id = shiftsystem_id
        
        self.shiftsystem = shiftsystem
        self.shiftpattern_iterator = shiftpattern_iterator
        