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
from .database import get_database
from .authentication import login_required

bp = Blueprint("index", __name__)


@bp.route('/')
@login_required
def data_index():
    return render_template('index.html', userid = session['user_id'])


@bp.route('/about')
@login_required
def data_about():
    return render_template('about.html', userid = session['user_id'])


@bp.route('/data')
@login_required
def data():
    return render_template('data.html', userid = session['user_id'])