import os
import sys

for c in range(1,9):
	bigc = float(c)/8
	bigc = str(bigc)
	
	os.system("New-Item ./res/train"+bigc+" -type file")
	os.system("New-Item ./res/dev"+bigc+" -type file")
	
	
	os.system("crf_learn.exe -p 4 -c "+bigc+" ./template "+sys.argv[1]+" ./model/"+bigc)
	
	os.system("crf_test.exe -m ./model/"+bigc+" ./corpus/train_without_crf >> ./res/train"+bigc)
	os.system("crf_test.exe -m ./model/"+bigc+" ./corpus/dev_without_crf >> ./res/dev"+bigc)


	os.system("python ./eval.py ./corpus/train_ans_crf ./res/train"+bigc+" >>./eval/train"+bigc)
	os.system("python ./eval.py ./corpus/dev_ans_crf ./res/dev"+bigc+" >>./eval/dev"+bigc)
	