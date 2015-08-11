For English readme content, please roll down.

####这是一个建立在HMM模型上的中文分词程序

######程序说明：
+ 本程序基于python2.7.10 windows环境 目前有些编码问题[注1]
+ HMM目录下有两个脚本 hmm.py 用来训练模型，会生成../model/hmmmodel 文件。viterbi.py用来进行解码，会生成../res/hmmres文件
+ 语料格式全部采用CRF++中的格式
+ 使用方法 python hmm.py $trainingFilePath $modelPath	python viterbi.py $modelPath $testFilePath $dictPath $outputPath


+ 在formatScript下是语料格式处理脚本。用来在不同的语料格式之间做转换。

+ eval目录下是一个分词评价脚本，可以计算P，R和F三个指标。同样只支持CRF++的语料格式。

+ 在根目录下附送了一个用来给CRF++调参的脚本。在windows下将CRF++加入path就可以正常使用了。

+ corpus目录下面是语料。这里为了方便要复现实验的同学，一并将语料上传。

######效果：
+基于HMM和字典，目前F值在0.9左右。

注1：目前支持的文本编码是ANSI编码（因为是在windows下面使用）。但问题是python直接输出的文件好像不是这个标准编码的，需要先转UTF8再转ANSI才能正常使用。
下一个版本准备同一成UTF8编码。