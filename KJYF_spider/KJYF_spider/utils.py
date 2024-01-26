import datetime


def format_str(s):
    n = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # '2023-03-29 20:11:42'
    return n + ">>>>>" + s
