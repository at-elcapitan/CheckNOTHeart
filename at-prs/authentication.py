# at-prs (c) by Vladislav 'ElCapitan' Nazarov
# 
# at-prs is licensed under a
# Creative Commons Attribution-NonCommercial-ShareAlike 3.0 Unported License.
# 
# You should have received a copy of the license along with this
# work.  If not, see <http://creativecommons.org/licenses/by-nc-sa/3.0/>.

import functools
from flask import (
    Blueprint, g, flash, redirect, render_template, request, session, url_for
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
    uid = session.get('user_id')

    if uid is None:
        g.user = None
        return
    
    g.username = get_database().execute('SELECT username FROM users WHERE id = ?', (uid,)).fetchone()['username']
    g.user = get_database().execute('SELECT * FROM users WHERE id = ?', (uid,))


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