# at-cnh (c) by Vladislav 'ElCapitan' Nazarov
# 
# at-cnh is licensed under a
# Creative Commons Attribution-NonCommercial-ShareAlike 3.0 Unported License.
# 
# You should have received a copy of the license along with this
# work.  If not, see <http://creativecommons.org/licenses/by-nc-sa/3.0/>.

# (c) AT PROJECT Limited 2023
# at-cnh made by ElCapitan

from datetime import timedelta
from flask import Flask as fl
import os

def create_app():
    app = fl(__name__)

    app.config.from_mapping(
        SECRET_KEY = 'dev',
        DATABASE = os.path.join(app.instance_path, 'db.sqlite')
    )

    app.permanent_session_lifetime = timedelta(minutes=20)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import database
    database.__init__(app)

    from . import authentication
    app.register_blueprint(authentication.bp)

    from . import data
    app.register_blueprint(data.bp)
    app.add_url_rule('/', endpoint='index')

    from . import user
    app.register_blueprint(user.bp)

    from . import admin
    app.register_blueprint(admin.bp)

    return app