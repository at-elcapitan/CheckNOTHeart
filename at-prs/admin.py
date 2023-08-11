# at-cnh (c) by Vladislav 'ElCapitan' Nazarov
# 
# at-cnh is licensed under a
# Creative Commons Attribution-NonCommercial-ShareAlike 3.0 Unported License.
# 
# You should have received a copy of the license along with this
# work.  If not, see <http://creativecommons.org/licenses/by-nc-sa/3.0/>.

from flask import (
    Blueprint, g, flash, redirect, render_template, request, session, url_for
)
from werkzeug.security import generate_password_hash
from .authentication import check_admin
from .database import get_database

bp = Blueprint("admin", __name__, "/admin")

@bp.route("/admin", methods=('GET', 'POST'))
@check_admin
def admin_main():
    db = get_database()
    
    if request.method == "POST":
        print(request.form)

        if 'DELETE' in request.form:
            if request.form['DELETE'] == "M":
                data_id = request.form['id']
                uid = request.form['uid']
                print(uid)

                data = db.execute('SELECT press_high, press_low, heart_rate FROM data_press WHERE user_id = ?', (uid,)).fetchall()
                data.reverse()

                if data is not None and len(data) != 1:
                    db.execute('UPDATE users SET last_press = ?, last_rate = ? WHERE id = ?', (f'{data[1]["press_high"]}/{data[1]["press_low"]}', data[1]['heart_rate'], uid))
                else:
                    db.execute('UPDATE users SET last_press = ?, last_rate = ? WHERE id = ?', ('NONE', 'NONE', uid))

                db.execute('DELETE FROM data_press WHERE id = ?', (data_id,))
                db.commit()
                
            
            if request.form['DELETE'] == "U":
                uid = int(request.form.get("id"))
                error = False

                if uid == 1:
                    flash("Can not delete system user (root).")
                    error = True

                if not error:
                    db.execute('DELETE FROM users WHERE id = ?', (uid,))
                    db.commit()
            
            return redirect(url_for('admin.admin_main'))

            
        if 'CREATE' in request.form:
            fname = request.form.get("first-name", None)
            lname = request.form.get("last-name", None)
            uname = request.form.get("username", None)
            password = request.form.get("password", None)
            admin_override = bool(request.form.get("admin-override", None))
            error = False

            if password is None:
                flash("Error: can not get password from form.")
                error = True

            if len(password) < 6:
                flash("Error: password can not be less than 7 chars.")
                error = True

            if uname is None:
                flash("Error: can not get username from form.")
                error = True

            if uname in db.execute("SELECT username FROM users").fetchall():
                flash("Error: user exists.")
                error = True

            if not error:
                db.execute('INSERT INTO users (username, password, first_name, last_name, admin_override) VALUES (?, ?, ?, ?, ?)', 
                           (uname, generate_password_hash(password), fname, lname, admin_override))
                db.commit()

            return redirect(url_for('admin.admin_main'))

    req = db.execute('SELECT admin_override FROM users WHERE id = ?', (session['user_id'],)).fetchone()
    udata = db.execute('SELECT id, username, first_name, last_name FROM users').fetchall()
    mdata = db.execute('SELECT press_high, press_low, date, user_id, dt.id, u.username, user_state, heart_rate,' 
                       'arm FROM data_press dt INNER JOIN users u ON dt.user_id = u.id').fetchall()

    return render_template("admin.html", g=g, userid = session['user_id'],
                           isadmin = bool(req['admin_override']), udata=udata, mdata=mdata)