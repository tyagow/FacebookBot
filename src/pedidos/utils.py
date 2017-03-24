import re

import time


def check_back_menu_action(message):
    if message == 'menu':
        return True
    return False


def time_valid(message):
    time_re = re.compile(r'^(([01]\d|2[0-3]):([0-5]\d)|24:00)$')
    m = time_re.search(message)
    return True if m else False


def isTimeFormat(input):
    try:
        time.strptime(input, '%H:%M')
        return True
    except ValueError:
        return False


def isDateTimeFormat(input):
    try:
        time.strptime(input, '%d/%m/%Y %H:%M')
        return True
    except ValueError:
        try:
            time.strptime(input, '%d/%m/%y %H:%M')
            return True
        except ValueError:
            return False
