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
    return render_template('index.html')