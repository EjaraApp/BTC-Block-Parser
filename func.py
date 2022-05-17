#!/usr/bin/env python3

from subprocess import check_output, CalledProcessError, STDOUT
import os

def cli(command):
    try:
        output = check_output(command, stderr=STDOUT).decode()
    except CalledProcessError as e:
        output = e.output.decode()
    return output

def get_file_ext(file_name):
    return file_name.split('.')[-1]

def is_file_ext(file_name, ext):
    return True if get_file_ext(file_name) == ext else False

def get_file_name(file_path):
    return os.path.basename(file_path)

def remove_file_ext(file_name):
    return file_name.split('.')[-2]

def path_exists(path):
    if os.path.exists(path):
        return True
    return False
