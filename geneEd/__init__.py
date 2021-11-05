
from flask import Flask
from flask import render_template
from flask_wtf.csrf import CSRFProtect
from . import search, info, login, admin, register
from geneEd.app import *

app = create_app()

# def create_app():
#     app = Flask(__name__, instance_relative_config=True)
#     app.secret_key = 'very secret'
#     CSRFProtect(app)


#     app.register_blueprint(search.bp)
#     app.register_blueprint(info.bp)
#     app.register_blueprint(login.bp)
#     app.register_blueprint(admin.bp)
#     app.register_blueprint(register.bp)
#     app.config.from_object('geneEd.config')

#     @app.route('/')
#     def index():
#         # return 'Welcome to GeneEd'

#         return render_template('base.html')

#     return app