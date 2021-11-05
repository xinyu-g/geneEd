from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, redirect
)
import mysql.connector


bp = Blueprint('search', __name__, url_prefix='/search')



@bp.route('/genesymbol', methods=('GET','POST'))
def searchSymbol():
    if request.method == 'POST':
        sym = request.form['query']
        cnx = mysql.connector.connect(user='root', passwd='root', database='geneEd')
        cur = cnx.cursor()
        query = ("SELECT * FROM gene WHERE symbol LIKE '%" + sym + "%'")
        cur.execute(query)
        entries = [t for t in cur]

        if entries:
            return render_template('searchresults.html', entries=entries)

            # return redirect('/info/gene/'.format(symbols))
        return render_template('no_results.html',symbol=sym)
    else:
        return render_template('search.html')


@bp.route('/advanced', method=('GET','POST'))
def advanceSearch():
    if request.method == 'POST':
        gseq = request.form['gseq']
        mtype = request.form['mtype']
        




    