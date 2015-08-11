import codecs
import sys

inFile = codecs.open(sys.argv[1],'r','utf-8')
outFile = codecs.open(sys.argv[2],'w','utf-8')


def output(word, i, tag, output = outFile):
	outFile.write(word[i] + ' '+ tag +'\n')

if __name__ == "__main__":
	for line in inFile:
		if line == '\r\n':
			continue
		arr = line.split(" ")
		for word in arr:
			if not word == '\r\n' and len(word) > 0:
				if word[0] == '[':
					word = word [1:-1]
				for num, cha in enumerate(word):
					if cha == '/':
						word = word[0:num]
				length = len(word)
				
				if length == 1:
					output(word, 0, 'S')
				else:
					output(word, 0, 'B')
					for j in range(1, length -1):
						output(word, j, 'M')
					output(word, -1, 'E')
		outFile.write('\n')
		
	
	