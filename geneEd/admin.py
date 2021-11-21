import flask
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, redirect
)
import mysql.connector


def check_access():
    if 'username' not in session: flask.abort(403)
    cnx = mysql.connector.connect(user='root', passwd='root', database='geneEd')
    cursor = cnx.cursor()
    cursor.execute("SELECT * FROM users WHERE username='" + session['username'] + "'")
    user = cursor.fetchone()
    is_admin = user[5]
    if not is_admin: flask.abort(403)


bp = Blueprint('admin', __name__, url_prefix='/admin')


@bp.route('/portal', methods=('GET', 'POST'))
def adminPortal():
    check_access()
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
    check_access()
    name = request.form['fullName']
    locus = request.form['locus']
    popularity = request.form['popularity']
    print(popularity)
    cnx = mysql.connector.connect(user='root', passwd='root', database='geneEd')
    update = (
        "UPDATE gene SET fullName='{0}', locus='{1}', popularity={2} WHERE symbol='{3}'".format(name, locus, popularity,
                                                                                                sym))
    cur = cnx.cursor()
    cur.execute(update)
    cnx.commit()
    return redirect('/info/gene/{0}'.format(sym))


@bp.route('/newentry', methods=["POST"])
def createNewEntry():
    check_access()
    symbol = request.form['symbol']
    fullName = request.form['fullName']
    proteinId = request.form['proteinId']
    proteinName = request.form['proteinName']
    locus = request.form['locus']
    geneSequence = request.form['geneSequence']
    diseaseName = request.form['diseaseName']
    proteinSequence = request.form['proteinSequence']
    mutationType = request.form['mutationType']
    cnx = mysql.connector.connect(user='root', passwd='root', database='geneEd')
    cur = cnx.cursor()
    stmt0 = ("SELECT symbol FROM gene WHERE symbol='{0}'".format(symbol))
    cur.execute(stmt0)
    results = cur.fetchall()
    # silently insert new genes, show old one if it exists
    if len(results) == 0:
        stmt1 = ("INSERT INTO disease VALUES ('{0}', '{1}')".format(diseaseName, mutationType))
        stmt2 = ("INSERT INTO protein VALUES ('{0}', '{1}', '{2}', '{3}')".format(proteinId, proteinName, diseaseName,
                                                                                  proteinSequence))
        stmt3 = ("INSERT INTO gene VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', {6})".format(symbol, fullName,
                                                                                                  proteinId,
                                                                                                  proteinName, locus,
                                                                                                  geneSequence, 0))
        cur.execute(stmt1)
        cur.execute(stmt2)
        cur.execute(stmt3)
        cnx.commit()
    return redirect("/info/gene/{0}".format(symbol))


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
        return render_template('no_results.html', symbol=sym)


def deleteGene(sym):
    cnx = mysql.connector.connect(user='root', passwd='root', database='geneEd')
    cur = cnx.cursor()
    stmt0 = (
        "SELECT symbol, protein.proteinId, disease.diseaseName FROM (gene JOIN protein ON gene.proteinId=protein.proteinId) JOIN disease ON protein.diseaseName=disease.diseaseName WHERE symbol='{0}'".format(
            sym))
    cur.execute(stmt0)
    results = cur.fetchall()
    for (sym, proteinId, diseaseName) in results:
        delete0 = ("DELETE FROM disease WHERE diseaseName='{0}'".format(diseaseName))
        delete1 = ("DELETE FROM protein WHERE proteinId='{0}'".format(proteinId))
        delete2 = ("DELETE FROM gene WHERE symbol='{0}'".format(sym))
        cur.execute(delete2)
        cur.execute(delete1)
        cur.execute(delete0)
        cnx.commit()
    if cur.rowcount > 0:
        return render_template('deletesuccess.html', symbol=sym)
    else:
        return render_template('deletefail.html', symbol=sym)
