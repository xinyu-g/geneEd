from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, redirect
)
import mysql.connector
import itertools 
import sys


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


@bp.route('/advancedsearch', methods=('GET','POST'))
def advanceSearch():

    if request.method == 'POST':
      
        gseq = request.form.get['gseq']
        mtype = request.form.get['mtype']
        gloc = request.form.get['gloc']
        pseq = request.form.get['pseq']
        dname = request.form.get['dname']
        tname = request.form.get['tname']
        tloc = request.form.get['tloc']
        cnx = mysql.connector.connect(user='root', passwd='root', database='geneEd')
        cur = cnx.cursor()
        query = ("SELECT * FROM gene WHERE symbol LIKE '%" + sym + "%'")

    else:
        return render_template('advancedSearchgeneral.html')

@bp.route('/advancedsearch/gene&inherit', methods=('GET','POST'))
def advanceSearch2():

    if request.method == 'POST':
 
        gseq = request.form.getlist('gseq')
        mtype = request.form.getlist('mtype')
        print(gseq, file=sys.stderr)
        print(mtype, file=sys.stderr)
        cnx = mysql.connector.connect(user='root', passwd='root', database='geneEd')
        cur = cnx.cursor()
        lst = []
        if gseq and mtype:
            lst = list(itertools.product(gseq, mtype))
        elif gseq:
            lst = list(itertools.product(gseq, ['recessive', 'X-linked', 'dominant']))
            
        print(lst, file=sys.stderr)
        # query = ("SELECT * FROM gene WHERE symbol LIKE '%" + sym + "%'")
        query = """
                SELECT g.symbol, mutationType,
                ROUND (  
                        (
                            LENGTH(p.diseaseName)
                            - LENGTH( REPLACE ( p.diseaseName, "'", "") )
                        ) / LENGTH("'") / 2
                    ) AS diseaseCount
                FROM gene g LEFT JOIN protein p USING (proteinName) LEFT JOIN disease d USING (diseaseName)
                WHERE g.sequence LIKE "%{}%" AND diseaseName <> "[]" AND mutationType = "{}"
                """
        entries = []
        for g, m in lst:
            cur.execute(query.format(g,m))
            entry = [t for t in cur]
            print(entry, file=sys.stderr)
            entries = entries + entry

        return render_template('advancedSearchResult2.html', entries=entries)

    else:
        return render_template('advancedSearch#2.html')



@bp.route('/advancedsearch/prot&disease', methods=('GET','POST'))
def advanceSearch3():

    if request.method == 'POST':
 
        dname = request.form.getlist('dname')
        mtype = request.form.getlist('mtype')
        cnx = mysql.connector.connect(user='root', passwd='root', database='geneEd')
        cur = cnx.cursor()
        lst = []
        if dname and mtype:
            lst = list(itertools.product(dname, mtype))
        elif dname:
            lst = list(itertools.product(dname, ['recessive', 'X-linked', 'dominant']))
            
        print(lst, file=sys.stderr)
        # query = ("SELECT * FROM gene WHERE symbol LIKE '%" + sym + "%'")
        query = """
                SELECT d.diseaseName, COUNT(p.proteinId), t.treatCount
                FROM protein p NATURAL JOIN disease d, 
                (SELECT d.diseaseName, COUNT(DISTINCT treatmentName) AS treatCount
                FROM disease d NATURAL JOIN treatment
                WHERE d.diseaseName <> '[]'
                GROUP BY d.diseaseName) t
                WHERE d.diseaseName LIKE '%{}%' 
                AND d.mutationType LIKE '%{}%'
                AND d.diseaseName = t.diseaseName
                GROUP BY d.diseaseName
                """
        entries = []
        for d, m in lst:
            cur.execute(query.format(d,m))
            entry = [t for t in cur]
            print(entry, file=sys.stderr)
            entries = entries + entry

        return render_template('advancedSearchResult3.html', entries=entries)

    else:
        return render_template('advancedSearch#3.html')


        

        
        




    