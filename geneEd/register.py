from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, redirect
)
import mysql
import mysql.connector


bp = Blueprint('register', __name__, url_prefix='/user')


@bp.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cnx = mysql.connector.connect(user='root', passwd='root', database='geneed', host='104.155.175.84')
        cursor = cnx.cursor()
        cursor.execute("SELECT * FROM users WHERE username='" + username + "'")
        user = cursor.fetchone()

        if user:
            msg = 'Account already exist!'
        else:
            cursor.execute('INSERT INTO users (username, password) VALUES (%s, %s)', (username, password,))
            cnx.commit()
            msg = 'You have successfully registered!'
    # elif request.method == 'POST':
        # msg = 'Please fill out the form!'

    return render_template('register.html', msg=msg)
