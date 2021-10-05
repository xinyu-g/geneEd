import requests

apiKey = 'RmWP24dgQ0ua8kJ485oPFw'
host = 'https://api.omim.org/api/'


def sign():
    data = {
        'apiKey': apiKey,
        'format': 'python'
    }
    url = host + 'apiKey'
    r = requests.request('POST', url, data=data)


def split(dname, aname):
    dlst = list()
    if dname.get(aname):
        if dname[aname].find(';;;') != -1:
            for lst in dname[aname].split(';;;'):
                dlst.append(lst.split(';;')[-1])
        else:
            dlst.append(dname[aname].split(';;')[-1])
                
    return dlst

def getGene(geneSym):
    params = {
        'search': f'approved_gene_symbol:{geneSym}',
        'include': ['seeAlso', 'geneMap', 'externalLinks'],
        'format': 'json',
        'start': 0,
        'limit': 10,
        'apiKey': apiKey
    }
    url = host + 'entry/search'
    r = requests.request('GET', url, params=params)
    res = r.json()
    if not res['omim']['searchResponse']['entryList']:
        return None
    res = res['omim']['searchResponse']['entryList'][0]['entry']
    # geneMap = res['geneMap']
    # externalLinks = res['externalLinks']
    gene = {
        'geneSym': geneSym,
        'geneName': None,
        'phenotype': None,
        'phenotypeInheritance': None,
        'diseases': list()
    }
    if res.get('geneMap'):
        geneMap = res['geneMap']
        if geneMap.get('geneName'):
            gene.update({'geneName': geneMap['geneName']})
        if geneMap.get('phenotypeMapList'):
            gene.update({
                'phenotype': geneMap['phenotypeMapList'][0]['phenotypeMap']['phenotype'],
                'phenotypeInheritance': geneMap['phenotypeMapList'][0]['phenotypeMap']['phenotypeInheritance']
            })
    if res.get('externalLinks'):
        externalLinks = res['externalLinks']
        if externalLinks.get('nbkIDs'):
            gene['diseases'] += split(externalLinks, 'nbkIDs')
        elif externalLinks.get('ordrDiseases'):
            gene['diseases'] += split(externalLinks, 'ordrDiseases')
        elif externalLinks.get('omiaIDs'):
            gene['diseases'] += split(externalLinks, 'omiaIDs')
    return gene



