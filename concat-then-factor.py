#!/usr/bin/env python3

import string
import urllib.request
import sys

ADAMS_WEBSITE_URL = "http://www.countablethoughts.com/concat-then-factor/dl.py?"
RATE_LIMIT_MSG = "You've been rate-limited.  Work with other people to get the rest of the file pieces.\n"

def generate_urls():
    first_letter = "x"
    # string.ascii_lowercase just contains all the letters of the english alphabet
    for second_letter in string.ascii_lowercase:
        for third_letter in string.ascii_lowercase:
            for fourth_letter in string.ascii_lowercase:
                # exactly same output as below, just a performance optimization
                # print(first_letter + second_letter + third_letter + fourht_letter)
                letter_combination = ''.join([first_letter, second_letter, 
                    third_letter, fourth_letter])
                yield(ADAMS_WEBSITE_URL + letter_combination)
                
                # -1 style points
                if letter_combination == "xcge":
                    return

def get_digits_from_url(link):
    with urllib.request.urlopen(link) as response:
       return str(response.read(), "UTF-8")

def find_big_numbers(start_index, end_index):
    counter = 0
    # storing as string because I don't think python ints are big enough to store
    # entire number
    big_number = ""

    for link in generate_urls():
        if counter < start_index:
            counter += 1
            continue
        elif counter > end_index:
            return
        else:
            counter += 1

        new_digits = get_digits_from_url(link)
        if new_digits != RATE_LIMIT_MSG:
            print(new_digits)
        else:
            print("We've been rate limited: try later. Exiting now.")
            return

def main():
    if len(sys.argv) != 3:
        print("This tool requires two arguments: the start and end indexes of the range to fetch")
    else:
        start_index = int(sys.argv[1])
        end_index = int(sys.argv[2])
        find_big_numbers(start_index, end_index)

if __name__ == "__main__":
    main()
