# -*- coding: UTF-8 -*-

import sys
import codecs
from math import log

class decoder(object):
	def __init__(self, modelfile,inputfile,dicfile):
		self.model = self.readmodel(modelfile)
		self.dataset = self.readinput(inputfile)
		self.postags = ['B','M','E','S']
		self.dic = {}
		self.sdic = {u'的'.encode('gbk'):1, u'（'.encode('gbk'):1, u'）'.encode('gbk'):1, u'不'.encode('gbk'):1, u'邓'.encode('gbk'):1 }
		self.readdic(dicfile)
	def readdic(self,f):
		for i in f:
			word = i.split(' ')[0]
			self.dic[word] = 1
			
	def readinput(self, f):
		tmp = []
		data = []
		for i in f:
			if i == '\r\n' or i == '\n':
				data.append(tmp)
				tmp = []
			else:
				i = i.replace('\r\n', '').replace('\n','')
				tmp.append(i)
				
		return data
	
	def format_trans(self, line):
		line = line.replace("Counter",'')
		line = line.replace("({",'')
		line = line.replace("})",'')
		line = line.replace("\n",'')
		line = line.replace("\r",'')
		line = line.replace("'",'')
		return line
		
	def dealbig(self, cha):
		cha = cha.replace("(",'')
		cha = cha.replace(")",'')
		cha = cha.replace(", ",'')
		return cha
	
	def readmodel(self, f):
		uni = f.readline()
		uni = self.format_trans(uni)
		uniarr = uni.split(", ")
		print uni
		self.unigram = {cha.split(': ')[0]:int(cha.split(': ')[1]) for cha in uniarr}
		
		big = f.readline()
		big = self.format_trans(big)
		bigarr = big.split(', (')
		self.bigram = {}
		for cha in bigarr:
			chaarr = cha.split(': ')
			a = self.dealbig(chaarr[0])
			b = int(chaarr[1])
			self.bigram[a[0],a[1]] = b
		
		coocsen = f.readline()
		coocsen = self.format_trans(coocsen)
		self.cooc = {}
		coocarr = coocsen.split(', (')
		for cha in coocarr:
			chaarr = cha.split(': ')
			a = self.dealbig(chaarr[0])
			b = int(chaarr[1])
			c = a[0:-1]
			c = ''.join(c.split('\\x'))
			try:
				c = c.decode('hex')
			except:
				d = c[:-1].decode('hex')
				d += c[-1]
				c = d
			self.cooc[c,a[-1]] = b
		
		wor = f.readline()
		wor = self.format_trans(wor)
		worarr = wor.split(', ')
		self.word = {cha.split(': ')[0]:int(cha.split(': ')[1]) for cha in worarr}
	
	
	def calc_prob(self,res1,res2,rat = 0.98):
		return log(rat * res1 + (1-rat)* res2)
	def emit(self, sen, i, tag):
		try:
			res1 = float(self.cooc[sen[i],tag])/self.unigram[tag]
		except:
			res1 = 0
			
		if i < (len(sen)-3):
			if self.dic.has_key(sen[i]+sen[i+1]) or self.dic.has_key(sen[i]+sen[i+1]+sen[i+2]) or self.dic.has_key(sen[i]+sen[i+1]+sen[i+2]+sen[i+3]):
				if tag == 'B':
					res1 = 1.0
				else:
					res1 = 0
		if i < (len(sen)-1) and i > 3:
			if self.dic.has_key(sen[i-1]+sen[i]) or self.dic.has_key(sen[i-2]+sen[i-1]+sen[i]) or self.dic.has_key(sen[i-3]+sen[i-2]+sen[i-1]+sen[i]):
				if tag == 'E':
					res1 = 1.0
				else:
					res1 = 0
		
		if i < (len(sen)-2) and i > 1:
			if self.dic.has_key(sen[i-1]+sen[i]+sen[i+1]) or self.dic.has_key(sen[i-2]+sen[i-1]+sen[i]+sen[i+1]):
				if tag == 'M':
					res1 = 1.0
				else:
					res1 = 0
		
		if self.sdic.has_key(sen[i]):
			if tag == 'S':
				res1 = 1.0
			else:
				res1 = 0
		if i == len(sen):
			if tag == 'B' or tag == 'M':
				res1 = 0
		
		
		
		res2 = 1.0/self.unigram[tag]
		return self.calc_prob(res1,res2)
	def trans(self, tag, tag1):
		a = self.unigram[tag]
		try:
			b = self.bigram[tag,tag1]
		
			res1 = float(a)/b
		except:
			res1 = 0
		
		res2 = 1.0/self.unigram[tag]
		'''
		if tag == 'B':
			if tag1 == 'S' or tag1 == 'B':
				return -float('inf')
		if tag == 'S':
			if tag1 == 'M' or tag1 == 'E':
				return -float('inf')
		if tag == 'M':
			if tag1 == 'S' or tag1 == 'B':
				return -float('inf')
		if tag == 'E':
			if tag1 == 'M' or tag1 == 'E':
				return -float('inf')
		'''		
		return self.calc_prob(res1,res2)
	
	def viterbi(self,sen):
		N, T = len(sen), len(self.unigram)
		
		score = [[-float('inf') for j in range(T)] for i in range(N)]
		path = [[-1 for j in range(T)] for i in range(N)]
		
		state = 0
		'''
		we have several here. 0 means last word has been finished, can only be changed to 0(S) or 1(B)
		1 means that we already have a B. next state can only be 0(E) or 1(M)
		'''
		for i, cha in enumerate(sen):
			if i == 0:
				for j, tag in enumerate(self.postags):
					score[0][j] = self.emit(sen, i, tag)
					
			else:
				for j, tag in enumerate(self.postags):
					best, best_t = -float('inf'), -1
					
					if (i + 1) < len(sen):
						a = self.emit(sen, i, tag)
					else:
						a = self.emit(sen, i, tag)	
					#print cha,tag,a
					for k, tag0 in enumerate(self.postags):
						b = score[i-1][k]
						'''
						if b == -float('inf'):
							continue
						if tag0 == 'B' or tag0 == 'M':
							if tag == 'S' or tag == 'B':
								continue
						else:
							if tag == 'M' or tag == 'E':
								continue
						'''
						b += self.trans(tag0,tag)
						if best < b:
							best = b
							best_t = k
					 
					score[i][j] = best + a
					path[i][j] = best_t
				#print score[i]
		best, best_t = -1e20, -1
		for j, tag in enumerate(self.postags):
			if best < score[len(sen)-1][j]:
				best = score[len(sen)-1][j]
				best_t = j
		result = [best_t]
		
		for i in range(len(sen)-1, 0, -1):
			result.append(path[i][best_t])
			best_t = path[i][best_t]
		result = [self.postags[t] for t in reversed(result)]
		#print result
		return result
		
	def decode(self, f):
		for sen in self.dataset:
			if len(sen)>0:
				res = self.viterbi(sen)
				output(sen, res, f)
			else:
				output([],[],f)
			
	

def output(sen, res, f):
	for i, word in enumerate(sen):
		f.write((word+' '+res[i]+'\n'))
	f.write('\n')

if __name__ == '__main__':
	modelfile = open(sys.argv[1],'r')
	datafile = open(sys.argv[2],'r')
	dicfile = open(sys.argv[3], 'r')
	outputfile = open(sys.argv[4],'wb')
	
	dec = decoder(modelfile, datafile, dicfile)
	
	dec.decode(outputfile)
	