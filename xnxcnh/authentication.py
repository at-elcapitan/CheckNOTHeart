# xnx-cnh (c) by Vladislav 'ElCapitan' Nazarov
# 
# xnx-cnh is licensed under a
# Creative Commons Attribution-NonCommercial-ShareAlike 3.0 Unported License.
# 
# You should have received a copy of the license along with this
# work.  If not, see <http://creativecommons.org/licenses/by-nc-sa/3.0/>.

import functools
from flask import (
    Blueprint, g, flash, redirect, render_template, request, session, url_for, abort
)
from werkzeug.security import check_password_hash
from .database import get_database

bp = Blueprint("authentication", __name__, "/auth")


@bp.route("/login", methods=('GET', 'POST'))
def login_form():
    if session.get('user_id') is not None:
        return redirect(url_for("index"))

    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        error = None
        database = get_database()
        
        user = database.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        
        if user == None:
            error = "Incorrect username"
        elif not check_password_hash(user['password'], password):
            error = "Incorrect password"

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))
        
        flash(error)

    return render_template('login.html')


@bp.before_app_request
def return_to_session():
    try:
        uid = session.get('user_id')

        if uid is None:
            g.user = None
            return
        
        req = get_database().execute('SELECT * FROM users WHERE id = ?', (uid,))
        g.user = req
        g.username = req.fetchone()['username']
    except:
        session.clear()
        return


@bp.route("/logout")
def logout():
    session.clear()
    return redirect('/login')


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('authentication.login_form'))
        
        return view(**kwargs)
    
    return wrapped_view


def check_admin(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('authentication.login_form'))
        
        if not bool(get_database().execute('SELECT admin_override FROM users WHERE id = ?', 
                                       (session['user_id'],)).fetchone()['admin_override']):
            abort(401)

        return view(**kwargs)
    
    return wrapped_view