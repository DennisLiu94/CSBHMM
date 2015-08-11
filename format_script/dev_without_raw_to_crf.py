import codecs
import sys

if __name__ == "__main__":
	inFile = codecs.open(sys.argv[1],'r','utf-8')
	outFile = codecs.open(sys.argv[2],'w','utf-8')
	for line in inFile:
		if line ==  '\r\n' or line == '\n':
			continue
		for word in line:
			if not word == '\r' and not word == '\n':
				outFile.write(word+'\n')
		outFile.write('\n')
		
	
	