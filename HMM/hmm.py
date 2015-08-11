import sys
import collections
from math import log
class HMM(object):
	def __init__(self, training_data):
		self.senset = []
		self.tagset = []
		self.f = training_data
		self.readTrainingSet()
		self.trainModel()
	def readTrainingSet(self):
		sen = []
		tag = []
		for i in self.f:
			if not i == '\r\n' and not i == '\n':
				i = i.replace('\t',' ')
				i = i.replace('\r\n','')
				i = i.replace('\n', '')
				arr = i.split(' ')
				sen.append(arr[0])
				tag.append(arr[1])
			else:
				self.senset.append(sen)
				self.tagset.append(tag)
				sen = []
				tag = []
		

	def trainModel(self):
		self.unigram = collections.Counter()
		self.bigram = collections.Counter()
		self.cooc = collections.Counter()
		self.word = collections.Counter()
		
		for i,sen in enumerate(self.senset):
			self.word.update(sen)
			for j,cha in enumerate(sen):
				self.cooc[cha,self.tagset[i][j]]+=1
		for j in self.tagset:
			self.unigram.update(j)
			for i in range(1,len(j)):
				self.bigram[j[i-1],j[i]]+=1
		self.postags = ['B','M','E','S']
	def calc_prob(self,res1,res2,rat = 0.5):
		return log(rat * res1 + (1-rat)* res2)
	def emit(self, cha, tag):
		a = self.unigram[tag]
		b = self.cooc[cha,tag]
		res1 = float(a)/b
		
		res2 = 1.0/b
		
		return self.calc_prob(res1,res2)
	def trans(self, tag, tag1):
		a = self.unigram[tag]
		b = self.unigram[tag1]
		
		res1 = float(a)/b
		
		res2 = 1.0/unigram[tag]
		
		return calc_prob(res1,res2)
		


if __name__ == '__main__':
	inputfile = open(sys.argv[1],'r')
	
	hmm = HMM(inputfile)
	hmm.trainModel()
	print hmm.unigram
	print hmm.bigram
	print hmm.cooc
	print hmm.word