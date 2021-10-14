from flask import Flask

def create_app():
    app = Flask(__name__, instance_relative_config=True)

    from . import search

    app.register_blueprint(search.bp)

    @app.route('/')
    def index():
        return 'Welcome to GeneEd'

    return app
