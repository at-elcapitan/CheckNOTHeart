# at-cnh (c) by Vladislav 'ElCapitan' Nazarov
# 
# at-cnh is licensed under a
# Creative Commons Attribution-NonCommercial-ShareAlike 3.0 Unported License.
# 
# You should have received a copy of the license along with this
# work.  If not, see <http://creativecommons.org/licenses/by-nc-sa/3.0/>.

import sqlite3
from flask import g, current_app
import flask
import click
from . import colors as c

def init_database():
    db = get_database()

    with current_app.open_resource("database.sql") as f:
        db.executescript(f.read().decode('utf8'))


def get_database():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


@click.command("init-db")
def on_init_database():
    init_database()

    print(f"[ {c.CGREEN}OK{c.CDEF} ] Database initialized.")


def close_database(*args):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def __init__(app: flask.Flask):
    app.teardown_appcontext(close_database)
    app.cli.add_command(on_init_database, "make")