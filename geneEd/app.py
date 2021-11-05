
from flask import Flask, request
from flask import render_template
# from flask_wtf.csrf import CSRFProtect
from . import search, info, login, admin, register

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    # app.secret_key = 'very secret'
    # CSRFProtect(app)
    
    app.config.from_object('geneEd.config')
    app.register_blueprint(search.bp)
    app.register_blueprint(info.bp)
    app.register_blueprint(login.bp)
    app.register_blueprint(admin.bp)
    app.register_blueprint(register.bp)
    

    @app.route('/', methods=('GET','POST'))
    def index():
        # return 'Welcome to GeneEd'
        if request.method == 'POST':
            if request.form['query']:
                return render_template('needCategory.html')
        return render_template('base.html')

    return app