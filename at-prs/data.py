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
from datetime import datetime
from .database import get_database
from .authentication import login_required

bp = Blueprint("index", __name__)


@bp.route('/', methods=('GET', 'POST'))
@login_required
def data_index():
    db = get_database()
    req = db.execute('SELECT first_name, last_name, last_press, last_rate, img_url, admin_override FROM users WHERE id = ?', (session['user_id'],)).fetchone()

    if request.method == "POST":
        highpr = request.form.get("highpr", None)
        lowpr = request.form.get("lowpr", None)
        hrate = request.form.get("heartrate", None)
        health = bool(request.form.get("health", False))
        error = None
        
        try: 
            highpr = int(highpr)
            lowpr = int(lowpr)
            hrate = int(hrate)
        except: error = "Preasure or heart rate must be a number"

        if error is None:
            db.execute('INSERT INTO data_press (date, press_high, press_low, heart_rate, user_state, user_id) VALUES (?, ?, ?, ?, ?, ?)',
                       (datetime.now(), highpr, lowpr, hrate, health, session['user_id']))
            db.execute('UPDATE users SET last_press = ?, last_rate = ? WHERE id = ?', (f'{highpr}/{lowpr}', hrate, session['user_id']))
            db.commit()
        
        return redirect(url_for('index.data_index'))

    return render_template('index.html', userid = session['user_id'], uinfo = req, isadmin = bool(req['admin_override']))


@bp.route('/about')
@login_required
def data_about():
    return render_template('about.html', userid = session['user_id'])


@bp.route('/data')
@login_required
def data():
    return render_template('data.html', userid = session['user_id'])