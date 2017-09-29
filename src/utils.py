"""

    utils.py

    This module is for general utility/helper functions.

"""


def isNumber(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def log(statusText, status, text):
    if (status == 0):
        print('[*] ' + statusText + ':', text)
    else:
        print('[!] ' + statusText + ':', text)