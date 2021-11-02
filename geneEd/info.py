from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
import mysql.connector


bp = Blueprint('info', __name__, url_prefix='/info')

@bp.route('/gene')
def showGenePage(symbols):
    sym = 'FOXP2'
    cnx = mysql.connector.connect(user='root', passwd='root', database='geneEd')
    cur = cnx.cursor()
    query = ("SELECT symbol,fullName,locus FROM gene WHERE symbol = '" + sym + "'")
    cur.execute(query)
    symbols = cur.fetchall()

    if symbols:
        return render_template('gene.html', symbols=symbols)
    return render_template('gene_not_found.html', symbol=sym)