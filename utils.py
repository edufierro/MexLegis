import os


def remove_temp(filepath):
    try:
        os.remove(filepath)
    except FileNotFoundError:
        pass
