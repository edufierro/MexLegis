# -*- coding: utf-8 -*-

import os
from pathlib import Path
import click
from utils.click_utlis import error


def remove_temp(filepath):
    try:
        os.remove(filepath)
    except FileNotFoundError:
        pass


def check_create_output_folder(data_path, out_folder_name):

    path_folder = Path(data_path) / out_folder_name
    if path_folder.exists():
        error('Folder {} already exists at {}'.format(out_folder_name, data_path), fatal=True)
    else:
        path_folder.mkdir()

    return path_folder


def check_create_file_path(data_path, file_name):

    file_path = Path(data_path) / file_name
    if file_path.is_file():
        error('File {} exists in folder {}'.format(file_name, data_path), fatal=True)

    return file_path
