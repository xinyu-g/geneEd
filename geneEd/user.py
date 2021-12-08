import flask
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, redirect, jsonify
)
import mysql.connector

bp = Blueprint('user', __name__, url_prefix='/user')

@bp.route('/profile', methods=['GET'])
def renderProfile():
    if 'id' not in flask.session:
        return render_template('not_logged_in.html')
    
    user_id = flask.session['id']

    cnx = mysql.connector.connect(user='root', passwd='root', database='geneed', host='104.155.175.84')
    cur = cnx.cursor()
    query1 = ("SELECT username, create_time, is_admin FROM users WHERE id = {0}".format(user_id))
    query2 = ("SELECT DISTINCT symbol, fullName, createDate, popularity FROM users NATURAL JOIN favorites NATURAL JOIN gene WHERE user_id = {0}".format(user_id))
    query3 = ("SELECT DISTINCT symbol, fullName, popularity FROM users NATURAL JOIN recommend NATURAL JOIN gene WHERE user_id = {0}".format(user_id))
    cur.execute(query1)
    user_info = cur.fetchall()[0]
    cur.execute(query2)
    user_favs = cur.fetchall()
    cur.execute(query3)
    user_rcmd = cur.fetchall()

    return render_template('user_profile.html', user_favs=user_favs, username=user_info[0], create_date=user_info[1],
                           admin=(False if user_info[2] == None else True), user_rcmd=user_rcmd)