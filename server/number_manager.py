#!/usr/bin/env python3

import os
import sqlite3
import string
import random
from pathlib import Path

DB_LOCATION = "dog-numbers.db"
CREATE_TABLE_QUERY = '''CREATE TABLE big_numbers
             (id tinytext, mystery_number text)'''
ADD_UNKNOWN_BIG_NUMBER_ROW = "INSERT INTO big_numbers VALUES (?, 'unknown')"

class NumberManager:
    def __init__(self):
        DB_file = Path(DB_LOCATION)
        self.create_DB_if_needed(DB_file)

    # return the number of letters in the range xaaa ... xcge, inclusive
    def get_combinations(self):
        all_letter_combinations = []
        first_letter = "x"
        # string.ascii_lowercase just contains all the letters of the english alphabet
        for second_letter in string.ascii_lowercase:
            for third_letter in string.ascii_lowercase:
                for fourth_letter in string.ascii_lowercase:
                    # exactly same output as below, just a performance optimization
                    # print(first_letter + second_letter + third_letter + fourht_letter)
                    letter_combination = ''.join([first_letter, second_letter,
                        third_letter, fourth_letter])
                    yield(letter_combination)

                    # -1 style points
                    if letter_combination == "xcge":
                        return

    def create_DB_if_needed(self, DB_file):
        if not DB_file.exists():
            DB_directory = DB_file.parent
            os.makedirs(str(DB_directory), exist_ok=True)

            # create the database file
            temp_connection = sqlite3.connect(str(DB_file))
            cursor = temp_connection.cursor()

            # create the table to store the numbers
            cursor.execute(CREATE_TABLE_QUERY)
            # populate the table, with all numbers unknown
            for letter_combination in self.get_combinations():
                cursor.execute(ADD_UNKNOWN_BIG_NUMBER_ROW, (letter_combination, ))

            # save and close
            temp_connection.commit()
            temp_connection.close()

    def get_a_unknown_number_index(self):
        conn = sqlite3.connect(DB_LOCATION)
        c = conn.cursor()
        unknown_numbers = c.execute("SELECT * from big_numbers WHERE mystery_number = 'unknown'")

        rows = unknown_numbers.fetchall()

        if len(rows) != 0:
            conn.close()
            return random.choice(rows)[0]
        else:
            conn.close()
            raise Error("All numbers discovered")

    def now_known_number(self, index, not_so_mystery_number):
        conn = sqlite3.connect(DB_LOCATION)
        c = conn.cursor()
        c.execute("UPDATE big_numbers SET mystery_number = ? WHERE id = ?", 
                (not_so_mystery_number, index))
        conn.commit()
        conn.close()

    def get_number(self, index):
        conn = sqlite3.connect(DB_LOCATION)
        c = conn.cursor()
        number = c.execute("SELECT * from big_numbers WHERE id = ?", (index, )).fetchone()

        if number:
            return number[1]
        else:
            raise ArgumentError

    def how_many_known(self):
        conn = sqlite3.connect(DB_LOCATION)
        c = conn.cursor()
        unknown_numbers = c.execute("SELECT * from big_numbers WHERE mystery_number = 'unknown'")
        result = unknown_numbers.fetchall()
        conn.close()
        return len(result)
