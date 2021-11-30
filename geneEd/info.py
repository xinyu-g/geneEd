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
    results = cur.fetchall()

    if not results:
        query2 = ("SELECT * FROM gene WHERE symbol = '" + sym + "'")
        cur.execute(query2)
        results = cur.fetchall()

    if len(results) == 1:
        # symbol, name, locus, popularity = results[0]
        update = ("UPDATE gene SET popularity = popularity + 1 WHERE symbol = '" + sym + "'")
        # single line updates are already transactions so we don't need one here
        cur.execute(update)
        cnx.commit()
        return render_template('gene.html', entries=results)
    elif len(results) > 1:
        # TODO render a page that lets the user choose whihc one they want to view
        return "multple genes"
    else:
        return render_template('gene_not_found.html', symbol=sym)