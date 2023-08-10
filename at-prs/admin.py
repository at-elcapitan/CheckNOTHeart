# at-prs (c) by Vladislav 'ElCapitan' Nazarov
# 
# at-prs is licensed under a
# Creative Commons Attribution-NonCommercial-ShareAlike 3.0 Unported License.
# 
# You should have received a copy of the license along with this
# work.  If not, see <http://creativecommons.org/licenses/by-nc-sa/3.0/>.

from flask import (
    Blueprint, g, flash, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash
from .authentication import check_admin
from .database import get_database

bp = Blueprint("admin", __name__, "/admin")

@bp.route("/admin", methods=('GET', 'POST'))
@check_admin
def admin_main():
    db = get_database()

    if request.method == "POST":
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
                return redirect(url_for('admin.admin_users'))
            
            if request.form['DELETE'] == "U":
                print('u')
            

    req = db.execute('SELECT admin_override FROM users WHERE id = ?', (session['user_id'],)).fetchone()
    udata = db.execute('SELECT id, username, first_name, last_name FROM users').fetchall()
    mdata = db.execute('SELECT press_high, press_low, date, user_id, dt.id, u.username, user_state, heart_rate,' 
                       'arm FROM data_press dt INNER JOIN users u ON dt.user_id = u.id').fetchall()

    return render_template("admin.html", g=g, userid = session['user_id'],
                           isadmin = bool(req['admin_override']), udata=udata, mdata=mdata)