from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, redirect
)
import flask
import geneEd
import mysql
import mysql.connector


def get_from_form(name):
    """Get form['name']."""
    if name not in flask.request.form:
        print("Empty!")
        flask.abort(400)
    return flask.request.form[name]


def get_target():
    """Get ?target=URL."""
    target = flask.request.args.get('target')
    if not target:
        target = '/'
    return target


def login(connection):
    """Operation for login."""
    password_form = get_from_form('password')
    username_form = get_from_form('username')

    if (not password_form) or (not username_form):
        print("the username or password fields are empty")
        flask.abort(400)

    cnx = mysql.connector.connect(user='root', passwd='root', database='geneEd')
    cursor = cnx.cursor()
    cursor.execute("SELECT * FROM users WHERE username='" + username_form + "'")
    user = cursor.fetchone()
    if not user:
        print("username and password authentication fails")
        flask.abort(403)
    print(user)
    password = user[4]
    if password == password_form:
        flask.session[
            geneEd.app.config['SESSION_COOKIE_NAME']
        ] = username_form
        print("login success")
    else:
        print("username and password authentication fails")
        flask.abort(403)


bp = Blueprint('login', __name__, url_prefix='/user')


@bp.route('/login', methods=['GET', 'POST'])
def account_login():
    """For login."""
    if request.method == 'GET':
        return render_template('login.html')
    else:
        operation = get_from_form('operation')
        target = get_target()
        connection = mysql.connector.connect(user='root', passwd='root', database='geneEd')

        if operation == 'login':
            login(connection)

        return redirect('/')
