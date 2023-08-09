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
from .authentication import check_admin
from .database import get_database

bp = Blueprint("admin", __name__, "/admin")

@bp.route("/admin")
@check_admin
def admin_main():
    db = get_database()

    req = db.execute('SELECT admin_override FROM users WHERE id = ?', (session['user_id'],)).fetchone()
    data = db.execute('SELECT id, username, first_name, last_name FROM users').fetchall()

    return render_template("admin.html", g=g, userid = session['user_id'],
                           isadmin = bool(req['admin_override']), data=data)