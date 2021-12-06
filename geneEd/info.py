from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
import mysql.connector


bp = Blueprint('info', __name__, url_prefix='/info')

@bp.route('/gene/<sym>')
def showGenePage(sym):
    cnx = mysql.connector.connect(user='root', passwd='root', database='geneEd')
    cur = cnx.cursor()
    # symbol,fullName,locus, popularity
    query = ("""SELECT symbol, fullName, proteinId, locus, G.sequence, popularity, P.proteinName, P.sequence, diseaseName 
                FROM gene G JOIN protein P USING (proteinId) NATURAL JOIN disease where symbol = '{}'""")
    cur.execute(query.format(sym))
    genes = cur.fetchall()

    # if not genes:
    #     query2 = ("SELECT * FROM gene WHERE symbol = '" + sym + "'")
    #     cur.execute(query2)
    #     genes = cur.fetchall()

    if len(genes) >= 1:
        if len(genes) > 1:
            genes = genes[:1]
        # symbol, name, locus, popularity = results[0]
        update = ("UPDATE gene SET popularity = popularity + 1 WHERE symbol = '" + sym + "'")
        # single line updates are already transactions so we don't need one here
        cur.execute(update)
        cnx.commit()

        results = []
        if 'id' in session.keys():
            query = ("SELECT * FROM favorites WHERE user_id='{0}' AND symbol='{1}'".format(session['id'], sym))
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
#         return render_template('gene.html', symbol=symbol, fullName=name, location=locus, popularity=popularity+1, likeButtonText=likeButtonText, showLikeButton=showLikeButton)
        return render_template('gene.html', entries=genes, likeButtonText=likeButtonText, showLikeButton=showLikeButton, symbol=sym)

    # elif len(genes) > 1:
    #     # TODO render a page that lets the user choose whihc one they want to view
    #     return "multple genes"
    else:
        query2 = ("SELECT symbol,fullName,locus, popularity, sequence FROM gene WHERE symbol = '" + sym + "'")
        cur.execute(query2)
        res = cur.fetchall()
        if res:
            return render_template('gene_w0match.html', entries=res)
        return render_template('gene_not_found.html', symbol=sym)