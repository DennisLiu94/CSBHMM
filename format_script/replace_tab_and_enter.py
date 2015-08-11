import codecs
import sys
inputfile = codecs.open(sys.argv[1], 'r','utf-8')
outputfile = codecs.open(sys.argv[2],'wb','utf-8')
for i in inputfile:
	outputfile.write(i.replace('\t',' ').replace('\r\n','\n'))