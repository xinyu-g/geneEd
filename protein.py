#!/usr/bin/env python3


import os
import sys
import json
import xml.etree.ElementTree

import entrezpy.conduit
import entrezpy.base.result
import entrezpy.base.analyzer
from bs4 import BeautifulSoup

class ProteinRecord:

	def __init__(self):
		self.pid = None
		self.pname = None
		self.pSquence = None


class ProteinResult(entrezpy.base.result.EutilsResult):
	def __init__(self, response, request):
		super().__init__(request.eutil, request.query_id, request.db)
		self.protein_records = {}

	def size(self):
		"""Implement virtual method :meth:`entrezpy.base.result.EutilsResult.size`
		returning the number of stored data records."""
		return len(self.protein_records)

	def isEmpty(self):
		"""Implement virtual method :meth:`entrezpy.base.result.EutilsResult.isEmpty`
		to query if any records have been stored at all."""
		if not self.protein_records:
			return True
		return False

	def get_link_parameter(self, reqnum=0):
		"""Implement virtual method :meth:`entrezpy.base.result.EutilsResult.get_link_parameter`.
		Fetching a pubmed record has no intrinsic elink capabilities and therefore
		should inform users about this."""
		print("{} has no elink capability".format(self))
		return {}

	def dump(self):
		"""Implement virtual method :meth:`entrezpy.base.result.EutilsResult.dump`.

		:return: instance attributes
		:rtype: dict
		"""
		return {self:{'dump':{'protein_records':[x for x in self.protein_records],
									'query_id': self.query_id, 'db':self.db,
									'eutil':self.function}}}

	def add_protein_record(self, protein_record):
		"""The only non-virtual and therefore PubmedResult-specific method to handle
		adding new data records"""
		self.protein_records[protein_record.pid] = protein_record


class proteinAnalyzer(entrezpy.base.analyzer.EutilsAnalyzer):

	def __init__(self):
		super().__init__()

	def init_result(self, response, request):
		if self.result is None:
			self.result = ProteinResult(response, request)

	def analyze_error(self, response, request):
		print(json.dumps({__name__:{'Response': {'dump' : request.dump(),
													'error' : response.getvalue()}}}))

	def analyze_result(self, response, request):
		self.init_result(response, request)
		
		soup = BeautifulSoup(response, 'xml')
		# print(response)
		ProteinRec = ProteinRecord()
		if t := soup.find_all('TSeq_accver', limit=1):
			ProteinRec.pid = t[0].text
		if t := soup.find_all('TSeq_sequence', limit=1):
			ProteinRec.pSquence = t[0].text
		if t := soup.find_all('TSeq_defline', limit=1):
			ProteinRec.pname = t[0].text
		self.result.add_protein_record(ProteinRec)


email = 'zhuzhuoerbilly@gmail.com'
api = '15035947eb5eba07c081a0c90fc48acdb609'
c = entrezpy.conduit.Conduit(email, api, threads=5)


geneList = ['APOE',
			'APP',
			'PSEN1']
geneSearch = [{'db':'gene', 'term': x + '[sym] AND human[ORGN]'} for x in geneList]

for query in geneSearch:
    fetchProtein = c.new_pipeline()

    sid = fetchProtein.add_search(query)
    lid = fetchProtein.add_link({'cmd':'neighbor_history', 'db':'protein'}, dependency=sid)
    lid = fetchProtein.add_search({'cmd':'neighbor_history'}, dependency=lid)
    fid = fetchProtein.add_fetch({'retmax': 1, 'retmode':'xml','rettype':'fasta'}, dependency=lid, analyzer=proteinAnalyzer())
    protein_res = c.run(fetchProtein).get_result()
    
    for i in protein_res.protein_records:
        print('protein id: {}'.format(protein_res.protein_records[i].pid))
        print('protein name: {}'.format(protein_res.protein_records[i].pname))
        print('protein sequence: {}'.format(protein_res.protein_records[i].pSquence[:30]))