import flask
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, redirect, jsonify
)
import mysql.connector

bp = Blueprint('api', __name__, url_prefix='/api')


@bp.route('/like/<sym>', methods=['POST'])
def likeGene(sym):
    body = request.json
    print(body)
    if body['action'] == "Like":
        cnx = mysql.connector.connect(user='root', passwd='root', database='geneEd')
        cur = cnx.cursor()
        update = ("INSERT INTO favorites VALUES ('{0}', '{1}', NOW())".format(flask.session['id'], sym))
        try:
            cur.execute(update)
            cnx.commit()
        except:
            print("Failed to add to like table:",flask.session['id'], sym)
    else:
        cnx = mysql.connector.connect(user='root', passwd='root', database='geneEd')
        cur = cnx.cursor()
        update = ("DELETE FROM favorites WHERE user_id='{0}' AND symbol='{1}'".format(flask.session['id'], sym))
        cur.execute(update)
        cnx.commit()
        
    result = jsonify({'status': 'success'})
    return result

