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
from datetime import datetime
from .database import get_database
from .authentication import login_required

bp = Blueprint("index", __name__)


@bp.route('/', methods=('GET', 'POST'))
@login_required
def data_index():
    db = get_database()
    req = db.execute('SELECT first_name, last_name, last_press, last_rate, img_url, admin_override FROM users WHERE id = ?', 
                    (session['user_id'],)).fetchone()
    
    data = db.execute('SELECT id, date, press_high, press_low, heart_rate, arm, user_state FROM data_press WHERE user_id = ?', (session['user_id'],)).fetchall()
    data.reverse()

    if request.method == "POST":
        if 'CREATE' in request.form:
            highpr = request.form.get("highpr", None)
            lowpr = request.form.get("lowpr", None)
            hrate = request.form.get("heartrate", None)
            health = bool(request.form.get("health", False))
            arm = request.form.get('arm', False)
            error = None

            '''if session['user_id'] == 1:
                flash("Can't write data to SYSTEM USER")
                error = True'''

            try: 
                highpr = int(highpr)
                lowpr = int(lowpr)
                hrate = int(hrate)
            except: 
                flash("Preasure or heart rate must be a number")
                error = True

            if not error:
                db.execute('INSERT INTO data_press (date, press_high, press_low, heart_rate, user_state, arm, user_id) VALUES (?, ?, ?, ?, ?, ?, ?)',
                        (datetime.now(), highpr, lowpr, hrate, health, arm, session['user_id']))
                db.execute('UPDATE users SET last_press = ?, last_rate = ? WHERE id = ?', (f'{highpr}/{lowpr}', hrate, session['user_id']))
                db.commit()
            
            return redirect(url_for('index.data_index'))

        if 'DELETE' in request.form:
            uid = request.form['id']
            
            data = db.execute('SELECT press_high, press_low, heart_rate FROM data_press WHERE user_id = ?', (1,)).fetchall()
            data.reverse()

            if data is not None and len(data) != 1:
                db.execute('UPDATE users SET last_press = ?, last_rate = ? WHERE id = ?', (f'{data[0]["press_high"]}/{data[0]["press_low"]}', data[0]['heart_rate'], session['user_id']))
            else:
                db.execute('UPDATE users SET last_press = ?, last_rate = ? WHERE id = ?', ('NONE', 'NONE', session['user_id']))
            db.execute('DELETE FROM data_press WHERE id = ?', (uid,))
            db.commit()
            return redirect(url_for('admin.admin_users'))
    return render_template('index.html', userid = session['user_id'], uinfo = req, isadmin = bool(req['admin_override']), data = data)

@bp.route('/data')
@login_required
def data():
    db = get_database()

    req = db.execute('SELECT admin_override FROM users WHERE id = ?', (session['user_id'],)).fetchone()
    data = db.execute('SELECT press_high, press_low, date FROM data_press WHERE user_id = ?', (session['user_id'],)).fetchall()

    return render_template('data.html', userid = session['user_id'], isadmin = bool(req['admin_override']), data=data)