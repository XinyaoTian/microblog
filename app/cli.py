from app import app
import os
# command for more argument
import click

# This file has been created for Command-Line Enhancements


@app.cli.group()
def translate():
    """Translation and localization commands"""
    pass


@translate.command()
def update():
    """Update all languages."""
    # I run them and make sure that the return value is zero,
    #  which implies that the command did not return any error.
    #  If the command errors, then I raise a RuntimeError,
    #  which will cause the script to stop.
    if os.system('pybabel extract -F babel.cfg -k _l -o messages.pot .'):
        raise RuntimeError('extract command failed')
    if os.system('pybabel update -i messages.pot -d app/translations'):
        raise RuntimeError('update command failed')
    os.remove('messages.pot')


@translate.command()
def compile():
    """Compile all languages."""
    if os.system('pybabel compile -d app/translations'):
        raise RuntimeError('compile command failed')


# The init command takes the new language code as an argument.
# Here is the implementation
@translate.command()
# This command uses the @click.argument decorator
# to define the language code.
@click.argument('lang')
def init(lang):
    """Initialize a new language."""
    if os.system('pybabel extract -F babel.cfg -k _l -o messages.pot .'):
        raise RuntimeError('extract command failed')
    if os.system('pybabel init -i messages.pot -d app/translations -l ' + lang):
        raise RuntimeError('init command failed')
    os.remove('messages.pot')
