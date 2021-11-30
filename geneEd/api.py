import flask
from datetime import datetime
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
        now = datetime.now()
        formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')
        update = ("INSERT INTO favorites VALUES ('{0}', '{1}', NOW())".format('cs411', sym))
        try:
            cur.execute(update)
            cnx.commit()
        except:
            pass
    else:
        cnx = mysql.connector.connect(user='root', passwd='root', database='geneEd')
        cur = cnx.cursor()
        now = datetime.now()
        formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')
        update = ("DELETE FROM favorites WHERE userName='{0}' AND symbol='{1}'".format('cs411', sym))
        cur.execute(update)
        cnx.commit()
        
    result = jsonify({'status': 'success'})
    return result

