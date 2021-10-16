from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, redirect
)
import mysql.connector


bp = Blueprint('admin', __name__, url_prefix='/admin')

@bp.route('/portal', methods=('GET','POST'))
def adminPortal():
    if request.method == 'POST':
        sym = request.form['query']
        action = request.form['action']
        if action == 'view':
            return redirect('/info/gene/{0}'.format(sym))
        elif action == 'update':
            return updateGene(sym)
        elif action == 'delete':
            return deleteGene(sym)
            
    else:
        cnx = mysql.connector.connect(user='root', passwd='root', database='geneEd')
        query = ("SELECT symbol, fullName, popularity FROM gene ORDER BY popularity DESC, symbol LIMIT 10")
        cur = cnx.cursor()
        cur.execute(query)
        top10 = [t for t in cur]
        return render_template('adminportal.html', top10=top10)

@bp.route('/updategene/<sym>', methods=['POST'])
def updateGeneDatabase(sym):
    name = request.form['fullName']
    locus = request.form['locus']
    popularity = request.form['popularity']
    print(popularity)
    cnx = mysql.connector.connect(user='root', passwd='root', database='geneEd')
    update = ("UPDATE gene SET fullName='{0}', locus='{1}', popularity={2} WHERE symbol='{3}'".format(name, locus, popularity, sym))
    cur = cnx.cursor()
    cur.execute(update)
    cnx.commit()
    return redirect('/info/gene/{0}'.format(sym))

def updateGene(sym):
    cnx = mysql.connector.connect(user='root', passwd='root', database='geneEd')
    cur = cnx.cursor()
    query = ("SELECT symbol, fullName, locus, popularity FROM gene WHERE symbol = '" + sym + "'")
    cur.execute(query)
    items = [c for c in cur]
    count = len(items)
    if count > 0:
        symbol, name, locus, popularity = items[0]
        return render_template('updategene.html', symbol=symbol, name=name, locus=locus, popularity=popularity)
    else:
        return render_template('no_results.html',symbol=sym)

def deleteGene(sym):
    cnx = mysql.connector.connect(user='root', passwd='root', database='geneEd')
    delete = ("DELETE FROM gene WHERE symbol = '" + sym + "'")
    cur = cnx.cursor()
    cur.execute(delete)
    if cur.rowcount > 0:
        return render_template('deletesuccess.html', symbol=sym)
    else:
        return render_template('deletefail.html', symbol=sym)