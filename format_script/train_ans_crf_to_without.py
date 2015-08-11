import codecs
import sys
'''
inputfile = codecs.open(sys.argv[1], 'r', 'utf-8')
outputfile = codecs.open(sys.argv[2],'wb','utf-8')
'''

inputfile = open(sys.argv[1], 'r')
outputfile = open(sys.argv[2],'wb')

for i in inputfile:
	if not i == '\n' and not i == '\r\n':
		word = i.split(" ")[0]
		outputfile.write(word+'\n')
	else:
		outputfile.write('\n')