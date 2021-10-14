#!/usr/bin/env python3


import os
import sys
import json
import xml.etree.ElementTree
from pathlib import Path



import entrezpy.conduit
import entrezpy.base.result
import entrezpy.base.analyzer
from bs4 import BeautifulSoup

class GeneRecord:

	def __init__(self):
		self.geneId = None
		self.seqId = None
		self.seqStart = None
		self.seqEnd = None
		self.sequence = None
		self.accver = None
		self.phenotype = None
		self.loc = None



class GeneResult(entrezpy.base.result.EutilsResult):
	
	def __init__(self, response, request):
		super().__init__(request.eutil, request.query_id, request.db)
		self.gene_records = {}

	def size(self):
		"""Implement virtual method :meth:`entrezpy.base.result.EutilsResult.size`
		returning the number of stored data records."""
		return len(self.gene_records)

	def isEmpty(self):
		"""Implement virtual method :meth:`entrezpy.base.result.EutilsResult.isEmpty`
		to query if any records have been stored at all."""
		if not self.gene_records:
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
		return {self:{'dump':{'gene_records':[x for x in self.gene_records],
									'query_id': self.query_id, 'db':self.db,
									'eutil':self.function}}}

	def add_gene_record(self, gene_record):
		"""The only non-virtual and therefore PubmedResult-specific method to handle
		adding new data records"""
		self.gene_records[gene_record.geneId] = gene_record



class GeneAnalyzer(entrezpy.base.analyzer.EutilsAnalyzer):
	"""Derived class of :class:`entrezpy.base.analyzer.EutilsAnalyzer`"""

	def __init__(self):
		super().__init__()

	def init_result(self, response, request):
		
		if self.result is None:
			self.result = GeneResult(response, request)

	def analyze_error(self, response, request):
		
		print(json.dumps({__name__:{'Response': {'dump' : request.dump(),
													'error' : response.getvalue()}}}))

	def analyze_result(self, response, request):
		
		self.init_result(response, request)
		
		soup = BeautifulSoup(response, 'xml')
		geneRec = GeneRecord()
		geneRec.geneId = int(soup.find('Gene-track_geneid').string)
		if t := soup.find_all('Gene-ref_desc', limit=1):
			geneRec.phenotype = t[0].text
		if t := soup.find_all('Seq-id_gi', limit=1):
			geneRec.seqId = t[0].text
		if t := soup.find_all('Seq-interval_from', limit=1):
			geneRec.seqStart = t[0].text
		if t := soup.find_all('Seq-interval_to', limit=1):
			geneRec.seqEnd = t[0].text
		if t := soup.find_all('Gene-commentary_accession', limit=1):
			geneRec.accver = t[0].text
		if t:= soup.find_all('Gene-ref_maploc', limit=1):
			geneRec.loc = t[0].text
		
		self.result.add_gene_record(geneRec)


class SeqRecord:
	
	def __init__(self):
		self.accver = None
		self.sid = None
		self.taxid = None
		self.orgname = None
		self.defline = None
		self.seqLen = None
		self.sequence = None
	

class SeqResult(entrezpy.base.result.EutilsResult):

	def __init__(self, response, request):
		super().__init__(request.eutil, request.query_id, request.db)
		self.seq_records = {}

	def size(self):
		
		return len(self.seq_records)

	def isEmpty(self):
		
		if not self.seq_records:
			return True
		return False

	def get_link_parameter(self, reqnum=0):
		
		print("{} has no elink capability".format(self))
		return {}

	def dump(self):
		
		return {}
		return {self:{'dump':{'seq_records':[x for x in self.seq_records],
									'query_id': self.query_id, 'db':self.db,
									'eutil':self.function}}}
	def add_seq_record(self, seq_record):
		
		self.seq_records[seq_record.sid] = seq_record

class SeqAnalyzer(entrezpy.base.analyzer.EutilsAnalyzer):
	

	def __init__(self):
		super().__init__()

	def init_result(self, response, request):
		
		if self.result is None:
			self.result = SeqResult(response, request)

	def analyze_error(self, response, request):
		
		print(json.dumps({__name__:{'Response': {'dump' : request.dump(),
													'error' : response.getvalue()}}}))

	def analyze_result(self, response, request):
		
		self.init_result(response, request)
		
		soup = BeautifulSoup(response, 'xml')
		seqRec = SeqRecord()
		if t := soup.find('TSeq_accver'):
			seqRec.accver = t.text 
		if t := soup.find('TSeq_sid'):
			seqRec.sid = t.text
		if t := soup.find('TSeq_taxid'):
			seqRec.taxid = t.text
		if t := soup.find('TSeq_orgname'):
			seqRec.orgname = t.text
		if t := soup.find('TSeq_length'):
			seqRec.seqLen = int(t.text)
		if t := soup.find('TSeq_defline'):
			seqRec.defline = t.text
		if t := soup.find('TSeq_sequence'):
			seqRec.sequence = t.text

		self.result.add_seq_record(seqRec)

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

# email = 'zhuzhuoerbilly@gmail.com'
# api = '15035947eb5eba07c081a0c90fc48acdb609'
# c = entrezpy.conduit.Conduit(email, api, threads=5)



# geneList = ['APOE',
# 			'APP',
# 			'PSEN1',
# 			'SRY']
# geneSearch = [{'db':'gene', 'term': x + '[sym] AND human[ORGN]'} for x in geneList]

# genes = {}

# for index in range(len(geneList)):
	
# 	gene = {'geneSym': geneList[index]}
# 	query = geneSearch[index]
# 	fetchGene = c.new_pipeline()
# 	sid = fetchGene.add_search(query)
# 	lid = fetchGene.add_link({'cmd':'neighbor_history', 'db':'Nucleotide'}, dependency=sid)
# 	lid = fetchGene.add_search({'cmd':'neighbor_history'}, dependency=lid)
# 	fid = fetchGene.add_fetch({'retmax': 1, 'retmode':'xml','rettype':'fasta'}, dependency=lid, analyzer=SeqAnalyzer())
	
# 	fetchG = c.new_pipeline()
# 	sid1 = fetchG.add_search(query)
# 	fid1 = fetchG.add_fetch({'retmax': 1, 'retmode':'xml','rettype':'fasta'}, dependency=sid1, analyzer=GeneAnalyzer())
	

# 	fetchProtein = c.new_pipeline()
# 	sid2 = fetchProtein.add_search(query)
# 	lid2 = fetchProtein.add_link({'cmd':'neighbor_history', 'db':'protein'}, dependency=sid2)
# 	lid2 = fetchProtein.add_search({'cmd':'neighbor_history'}, dependency=lid2)
# 	fid2 = fetchProtein.add_fetch({'retmax': 1, 'retmode':'xml','rettype':'fasta'}, dependency=lid2, analyzer=proteinAnalyzer())
# 	protein_res = c.run(fetchProtein).get_result()
	
	
# 	g_res = c.run(fetchG).get_result()

# 	for i in g_res.gene_records:
# 		gene.update({
# 			'phenotype': g_res.gene_records[i].phenotype,
# 			'geneLoc': g_res.gene_records[i].loc
# 		})
	
# 	res = c.run(fetchGene).get_result()

	
# 	for i in res.seq_records:
# 		gene.update({
# 			'geneSeq': res.seq_records[i].sequence
# 		})
		

# 	for i in protein_res.protein_records:
# 		gene.update({
# 			'proteinId': protein_res.protein_records[i].pid,
# 			'proteinName': protein_res.protein_records[i].pname,
# 			'proteinSeq': protein_res.protein_records[i].pSquence
# 			})
	


# with open("output.json", "w") as outfile:
# 	json.dump(genes, outfile)