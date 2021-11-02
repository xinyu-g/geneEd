from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, redirect
)
import mysql.connector


bp = Blueprint('search', __name__, url_prefix='/search')


# @bp.route('/result')
# def displaySearchResult(symbols):
#     return render_template('gene.html', symbols=symbols)


@bp.route('/genesymbol', methods=('GET','POST'))
def searchSymbol():
    if request.method == 'POST':
        sym = request.form['query']
        cnx = mysql.connector.connect(user='root', passwd='root', database='geneEd')
        cur = cnx.cursor()
        query = ("SELECT * FROM gene WHERE symbol LIKE '%" + sym + "%'")
        cur.execute(query)
        symbols = cur.fetchall()

        if symbols:
            return render_template('gene.html', symbols=symbols)

            # return redirect('/info/gene/'.format(symbols))
        return render_template('no_results.html',symbol=sym)
    else:
        return render_template('search.html')


    