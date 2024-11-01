def is_int(number):
    try:
        tmp_num = int(number)
        return True
    except ValueError:
        return False

def is_float(number):
    try:
        tmp_num = float(number)
        return True
    except ValueError:
        return False