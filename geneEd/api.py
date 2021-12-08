import logging
import flask
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, redirect, jsonify
)
import mysql.connector

bp = Blueprint('api', __name__, url_prefix='/api')


@bp.route('/like/<sym>', methods=['POST'])
def likeGene(sym):
    body = request.json
    if body['action'] == "Like":
        cnx = mysql.connector.connect(user='root', passwd='root', database='geneed', host='104.155.175.84')
        cur = cnx.cursor()
        update = ("INSERT INTO favorites VALUES ('{0}', '{1}', NOW())".format(flask.session['id'], sym))
        try:
            cur.execute("set session sql_mode='';")
            cur.execute(update)
            cnx.commit()
            logging.info('User {0} liked gene {1}'.format(flask.session['id'], sym))
            print('User {0} liked gene {1}'.format(flask.session['id'], sym))
        except Exception as e:
            logging.error("Failed to add to like table: {}".format(e),flask.session['id'], sym)
            print("Failed to add to like table: {}".format(e),flask.session['id'], sym)
    else:
        cnx = mysql.connector.connect(user='root', passwd='root', database='geneed', host='104.155.175.84')
        cur = cnx.cursor()
        update = ("DELETE FROM favorites WHERE user_id='{0}' AND symbol='{1}'".format(flask.session['id'], sym))
        cur.execute(update)
        cnx.commit()
        
    result = jsonify({'status': 'success'})
    return result

