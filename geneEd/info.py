from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
import mysql.connector


bp = Blueprint('info', __name__, url_prefix='/info')

@bp.route('/gene/<sym>')
def showGenePage(sym):
    cnx = mysql.connector.connect(user='root', passwd='root', database='geneEd')
    cur = cnx.cursor()
    query = ("SELECT symbol,fullName,locus, popularity FROM gene WHERE symbol = '" + sym + "'")
    cur.execute(query)
    results = cur.fetchall()

    if len(results) == 1:
        symbol, name, locus, popularity = results[0]
        update = ("UPDATE gene SET popularity = popularity + 1 WHERE symbol = '" + sym + "'")
        # single line updates are already transactions so we don't need one here
        cur.execute(update)
        cnx.commit()
        results = []
        if 'id' in session.keys():
            query = ("SELECT * FROM favorites WHERE user_id='{0}' AND symbol='{1}'".format(session['id'], symbol))
            cur.execute(query)
            try:
                results = cur.fetchall()
            except:
                results = []
        likeButtonText = ''
        showLikeButton = False
        if 'username' in session.keys():
            showLikeButton = True
            if len(results) > 0:
                likeButtonText = 'Liked'
            else:
                likeButtonText = 'Like'
        print('showLikeButton',showLikeButton)
        return render_template('gene.html', symbol=symbol, fullName=name, location=locus, popularity=popularity+1, likeButtonText=likeButtonText, showLikeButton=showLikeButton)
    elif len(results) > 1:
        # TODO render a page that lets the user choose whihc one they want to view
        return "multple genes"
    else:
        return render_template('gene_not_found.html', symbol=sym)