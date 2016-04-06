import random
from math import log
fPosTrain="hotelPosT-train.txt"
fNegTrain="hoteNegT-train.txt"
fTestset="Twitter-test-set.txt"

fExtraPosList="ExtraPosList.txt"
fExtraNegList="ExtraNegList.txt"
laplacianConstant=1
minLengthOfWord=16

ExtraPosList=open(fExtraPosList,"r")
ExtraPosList=ExtraPosList.readlines()
ExtraPosList=list(set(ExtraPosList[0].split()))

ExtraNegList=open(fExtraNegList,"r")
ExtraNegList=ExtraNegList.readlines()
ExtraNegList=list(set(ExtraNegList[0].split()))

f_vader_sentiment_lexicon=open("vader_sentiment_lexicon.txt","r")
vader_sentiment_lexicon=f_vader_sentiment_lexicon.readlines()
vader_sentiment_lexicon_pos=[]
vader_sentiment_lexicon_neg=[]
#vader_sentiment_lexicon=vader_sentiment_lexicon[440:]

for each in vader_sentiment_lexicon:
	each= each.split("\t")
	if(each[1]>0 and len(each[0])>minLengthOfWord):
		vader_sentiment_lexicon_pos.append(each[0])
	elif(each[1]<0 and len(each[0])>minLengthOfWord):
		vader_sentiment_lexicon_neg.append(each[0])
	else:
		pass


def getFiles(s1,s2):
	fPTrain=open(s1,"r")
	fNTrain=open(s2,"r")
	PTrain=fPTrain.readlines()
	NTrain=fNTrain.readlines()
	fPTrain.close()
	fNTrain.close()
	return PTrain,NTrain
def get90p90n9test(s1,s2):#also randomize
	'''
	random.shuffle(s1)#random
	random.shuffle(s2)#random
	'''
	
	PTrain90=s1
	NTrain90=s2
	PNTest9=open(fTestset,"r")
	PNTest9=PNTest9.readlines()
	return PTrain90,NTrain90,PNTest9
def filterOutIds(s1,s2):
	PTrain90=[]
	NTrain90=[]
	PNTest9=[]
	for index,each in enumerate(s1):
		each=each.split()
		del each[0]



		#Add the list of words in a single sentence only 
		if (index ==0):
			each=each+ExtraPosList
		#till here
			#add the vader_sentiment_lexicon_pos list here
			each=each+vader_sentiment_lexicon_pos



		each=[x.lower() for x in each]		
		PTrain90.append(each)
	for index,each in enumerate(s2):
		each=each.split()
		del each[0]
		#Add the list of words in a single sentence only
		if(index==0):
			each=each+ExtraNegList
		#till here
			#add the vader_sentiment_lexicon_neg list here
			each=each+vader_sentiment_lexicon_neg

		each=[x.lower() for x in each]	
		NTrain90.append(each)
	return 	PTrain90,NTrain90#,PNTest9
def vocabGlobal(s1,s2):
	vocab=[]
	for each in s1:
		for every in each:
			vocab.append(every)
	vocab=set(vocab)
	vocab=list(vocab)
	for each in s2:
		for every in each:
			vocab.append(every)
	vocab=set(vocab)
	vocab=list(vocab)
	#print "lenVocab in pos in global= ",len(vocab)

	return vocab
def calcPrior():
	posPrior=95.0/189
	negPrior=94.0/189
	#Change the prior
	return posPrior,negPrior

def uniqueDocs(s1,s2):
	PTrainr=[]
	NTrainr=[]
	for each in s1:
		each=set(each)
		each=list(each)
		PTrainr.append(each)
	for each in s2:
		each=set(each)
		each=list(each)
		NTrainr.append(each)
	return PTrainr,NTrainr
	

def probPOS(s1,s2):
	dictPOS={}
	gPosList=[]
	for each in s1:
		for every in each:
			gPosList.append(every)
	lenVocab=len(s2)
	print "lenVocab in pos= ",lenVocab
	totalPOSWords=len(gPosList)
	for each in s2:
		dictPOS[each]= (gPosList.count(each) + 1.0) / (totalPOSWords+ float(lenVocab))
	return dictPOS,totalPOSWords


def probNEG(s1,s2):
	dictNEG={}
	gNegList=[]
	for each in s1:
		for every in each:
			gNegList.append(every)
	lenVocab=len(s2)
	print "lenVocab in neg= ",lenVocab

	totalNEGWords=len(gNegList)
	for each in s2:
		dictNEG[each]=(gNegList.count(each) + 1.0) / (totalNEGWords + float(lenVocab))
	return dictNEG,totalNEGWords

def trainingSet(PNTest9):
	testIdText=[]
	for each in PNTest9:
		each=each.split()
		testIdText.append([each[0]," ".join(each[1:])])
	
	return testIdText

"""Function to create list data structure """	
def classify(testIdText,totalPOSWords,totalNEGWords,lenVocab):
	counter=0
	count=0
	
	posOrNeg=""

	PosVal=0.0
	NegVal=0.0
	notMatched=[]
	for each in testIdText:
		print each
		
		id_= each[0]
		each[1]=each[1].split()
		
		#POS
		for every in each[1]:
			if( every not in vocab):#vocab??
				dictPOS[every]=1.0 / (totalPOSWords + float(lenVocab))

			PosVal=PosVal+ log(dictPOS[every],10)
		PosVal=PosVal + log(posPrior,10)
		#NEG
		for every in each[1]:
			if(every not in vocab):
				dictNEG[every]=1.0 / (totalNEGWords +float(lenVocab))

			NegVal=NegVal + log(dictNEG[every],10)
		NegVal=NegVal+ log(negPrior,10)
		if (PosVal > NegVal):
			posOrNeg="POS"

			#print id_,"\t", "POS"

		else:
			posOrNeg="NEG"
			#print id_,"\t","NEG"
		print id_,"\t",posOrNeg
		counter=counter+1
		posOrNeg=""
		PosVal=0.0
		NegVal=0.0  
	print "percentage = ", (count/50.0)*100.0
	print notMatched
		

if __name__ == '__main__':
	PTrain,NTrain=getFiles(fPosTrain,fNegTrain) #Loads the files 
	PTrainr,NTrainr,PNTest9=get90p90n9test(PTrain,NTrain)
	PTrainr,NTrainr=filterOutIds(PTrainr,NTrainr)
	vocab= vocabGlobal(PTrainr,NTrainr)
	posPrior,negPrior=calcPrior()
	PTrainr,NTrainr=uniqueDocs(PTrainr,NTrainr)
	POS=[]
	NEG=[]
	dictPOS,totalPOSWords=probPOS(PTrainr,vocab)
	dictNEG,totalNEGWords=probNEG(NTrainr,vocab)
	testIdText=trainingSet(PNTest9)
	#print len(dictPOS),len(dictNEG),len(vocab)
	classify(testIdText,totalPOSWords,totalNEGWords,len(vocab))