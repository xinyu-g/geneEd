from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
import mysql.connector


bp = Blueprint('info', __name__, url_prefix='/info')

@bp.route('/gene/<sym>')
def showGenePage(sym):
    # sym = 'FOXP2'
    cnx = mysql.connector.connect(user='root', passwd='root', database='geneEd')
    cur = cnx.cursor()
    query = ("SELECT symbol,fullName,locus FROM gene WHERE symbol = '" + sym + "'")
    cur.execute(query)

    for (symbol,name,locus) in cur:
        return render_template('gene.html', symbol=symbol, fullName=name, location=locus)
    return render_template('gene_not_found.html', symbol=sym)