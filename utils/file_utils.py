# -*- coding: utf-8 -*-

import os
from pathlib import Path
import click

def remove_temp(filepath):
    try:
        os.remove(filepath)
    except FileNotFoundError:
        pass


class FolderExistsError(Exception):
    pass


def check_create_output_folder(out_folder):

    path_folder = Path(out_folder)
    if path_folder.exists():
        raise FolderExistsError()
    else:
        path_folder.mkdir()

    return path_folder



