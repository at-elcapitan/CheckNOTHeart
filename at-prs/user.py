# at-cnh (c) by Vladislav 'ElCapitan' Nazarov
# 
# at-cnh is licensed under a
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

bp = Blueprint("user", __name__)


@bp.route('/user/<int:userid>')
@login_required
def user_page(userid):
    return f'<a href="/">Home</a>{userid}'