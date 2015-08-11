import sys
import codecs


#first file is ans, second file is res
corr = 0
total_res = 0
total_ans = 0
try:
	ansString = sys.argv[1]
	resString = sys.argv[2]
except:
	i = 0

#read a sentence and put it in a list
def readSen(f):
	l = []
	for j in f:
		if j == '\r\n' or j == '\n':#pay attention to the diff of windows and linux. Fucking microsoft
			break
		else:
			l.append(j)
		
	return l
	
#prepare for counting 	
def getWord(l):
	d = []
	tmp = ''
	for i,cha in enumerate(l):
		
		cha = cha.replace('\t',' ')
		cha = cha.replace('\r\n','\n')#these replacements are for the possible format difference between linux and windows
		arr = cha.split(' ')
		if arr[1] == 'S\n':
			d.append([arr[0],i])
		else:
			if arr[1] == 'E\n':
				tmp = tmp + arr[0]
				d.append([tmp, i])
				tmp = ''
			else:
				tmp = tmp + arr[0]
	return d
	
def getP(ans,res):
	global corr
	global total_ans
	global total_res
	total_ans += len(ans)
	total_res += len(res)
	
	
	j = 0
	i = 0
	while i < len(ans) and j < len(res):
		if ans[i][0] == res[j][0] and ans[i][1] == res[j][1]:
			corr+=1
			#print i,len(ans)
			#print res[j][0]
			i+=1
			j+=1
		else:
			if ans[i][1] > res[j][1]:
				j +=1
			else:
				if ans[i][1] < res[j][1]:
					i +=1
				else:
					i +=1
					j +=1
					
	
if __name__ == '__main__':
	ansFile = open(ansString,'r')
	resFile = open(resString,'r')
	ans = "R&R"
	global corr
	global total_res
	global total_ans
	count = 1
	while not len(ans) == 0:
		ans = readSen(ansFile)
		res = readSen(resFile)
	
		ansWord = getWord(ans)
		resWord = getWord(res)
	
		getP(ansWord,resWord)	
	
	p = float(corr)/total_res
	r = float(corr)/total_ans
	print p,r,(p*r*2)/((p+r))		