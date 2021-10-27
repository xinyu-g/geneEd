from flask import Flask
from . import search, info, login

app = Flask(__name__, instance_relative_config=True)


app.register_blueprint(search.bp)
app.register_blueprint(info.bp)
app.register_blueprint(login.bp)
app.config.from_object('geneEd.config')


@app.route('/')
def index():
    return 'Welcome to GeneEd'

