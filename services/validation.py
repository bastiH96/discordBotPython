from typing import List
from datetime import date
import re


class Validator:

    @staticmethod
    def are_integers(items: List) -> bool:
        try:
            for item in items:
                int(item)
            return True
        except ValueError:
            return False

    @staticmethod
    def is_valid_date(year: int, month: int, day: int) -> bool:
        try:
            date(year, month, day)
            return True
        except OverflowError:
            return False

    @staticmethod
    def is_valid_shiftpattern(shift_pattern: str) -> bool:
        regex_pattern = re.compile(r"^(F12|N12|F|S|N|-|SN|)$")

        if "," in shift_pattern and "\n" not in shift_pattern:
            for shift in shift_pattern.replace(" ", "").split(","):
                if not re.match(regex_pattern, shift):
                    return False
            return True

        elif "\n" in shift_pattern and "," not in shift_pattern:
            for shift in shift_pattern.replace(" ", "").split("\n"):
                if not re.match(regex_pattern, shift):
                    return False
            return True

        else:
            return False


