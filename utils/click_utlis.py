import click
import sys


def message(msg, **kwargs):
    click.secho(msg, **kwargs)


def warn(msg):
    message(msg, fg='yellow')


def info(msg):
    message(msg, fg='cyan', err=True)


def error(error_msg, fatal=False):
    click.secho(error_msg, fg='red', err=True)
    if fatal:
        sys.exit(1)
