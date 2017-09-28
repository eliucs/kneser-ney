"""

    utils.py

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