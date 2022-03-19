import pickle
import os
import tqdm
import re
from collections import Counter
import augData4 as ag

count = Counter([])

for i in range(20):
	fileindex = str(i+1)
	with open('../code/mostFrequentPickle'+fileindex,'rb') as infile:
		mf = pickle.load(infile)
		count = count + mf


liteMaskList = ['(',')','[',']','{','}',';',',','.',':','"','+',' ','!','=','-','*','#','@','/','_','<','>','?','!','%','^','%','<R>','<L>']

most_common_token = count.most_common(300)


most_common_t = []
for (token,counts) in most_common_token:
	if token.isalpha():
		most_common_t.append(token)

heavy_mask = liteMaskList + most_common_t

classnox = []
classmaskx = []
y = []

om4 = []
om10 = []
om20 = []
omy = []

on4 = []
on10 = []
on20 = []
ony =[]


lines200=[]
for i in range(200):
	lines200.append(i)
	
linecount = Counter(lines200)
maxindex = 15

for files in range(20):
	fileindex = str(files+1)
	print(fileindex)
	with open('../code/compileAbleCodePickle'+fileindex,'rb') as infile:
		ccode = pickle.load(infile)

	for code in tqdm.tqdm(ccode):
		
		# sort long files
		codeLines = code.split('\n')
		codeLines2 = []
		
		for cl11 in codeLines:
			if not cl11.isspace():
				codeLines2.append(cl11)
		
		
		if(len(codeLines2))>200 or (len(codeLines2))<10:
			continue
			
		code = '\n'.join(codeLines2)
		
		#no masking
		(classx,classy,linecount,orCode,orLine,ind) = ag.read_input(code,linecount,maxindex)
		
		if maxindex >= 20:
			maxindex = 0
		else:
			maxindex = maxindex + 1
			
		# start masking

		mclass = []
		for sample in classx:
			mask = []
			cl = re.findall(r"<L>|<R>|out|println|printf|print|System|[A-Za-z]+|\n|\t|\S| |.", sample)
			for token in cl:
				if token in heavy_mask:
					mask.append(token)
				elif token.isspace():
					mask.append(token)
				
				else:
					mask.append("M")
					
			mclass.append("".join(mask))



		classnox.extend(classx)
		classmaskx.extend(mclass)
		y.extend(classy)

		

		mOrCode = []
		mYline = []
		for sample in orCode:
			mask = []
			cl = re.findall(r"out|println|printf|print|System|[A-Za-z]+|\n|\t|\S| |.", sample)
			for token in cl:
				if token in heavy_mask:
					mask.append(token)
				elif token.isspace():
					mask.append(token)
				else:
					mask.append("M")
			mOrCode.append("".join(mask))
                        
			mask = []
			c2 = re.findall(r"out|println|printf|print|System|[A-Za-z]+|\n|\t|\S| |.", orLine[0])
			for token in c2:
				if token in heavy_mask:
					mask.append(token)
				elif token.isspace():
					mask.append(token)
				else:
					mask.append("M")
			mYline.append("".join(mask))
		
				

		if len(orLine) == 0:
			continue


		
		codeLines = orCode[0].split('\n')	


		leftLines = []
		rightLines = []
		errorline = "<E>" + codeLines[ind[0]]
		for i in range(10):
			leftLines.append("")
			rightLines.append("")
		
		for i in range(10):
			if (ind[0] - 1 - i >= 0):
				leftLines[i] = "<L" + str(i) +">" +  codeLines[ind[0] - 1 - i] 
		for i in range(10):
			if (ind[0] + 1 + i < len(codeLines)):
				rightLines[i] = "<R" + str(i) + ">" + codeLines[ind[0] + 1 + i]

		leftLines.reverse()

		n20 = "\n".join(leftLines+[errorline]+rightLines)
		n10 = "\n".join(leftLines[-5:]+[errorline]+rightLines[0:5])	
		n4 = "\n".join(leftLines[-2:]+[errorline]+rightLines[0:2])
		on4.append(n4)
		on10.append(n10)
		on20.append(n20)



		codeLines = mOrCode[0].split('\n')

		leftLines = []
		rightLines = []
		errorline = "<E>" + codeLines[ind[0]]
		for i in range(10):
			leftLines.append("")
			rightLines.append("")
		for i in range(10):
			if (ind[0] - 1 - i >= 0):
				leftLines[i] = "<L" + str(i) +">" +  codeLines[ind[0] - 1 - i]
		for i in range(10):
			if (ind[0] + 1 + i < len(codeLines)):
				rightLines[i] = "<R" + str(i) + ">" + codeLines[ind[0] + 1 + i]

		leftLines.reverse()

		m20 = "\n".join(leftLines+[errorline]+rightLines)
		m10 = "\n".join(leftLines[-5:]+[errorline]+rightLines[0:5])
		m4 = "\n".join(leftLines[-2:]+[errorline]+rightLines[0:2])
		#print(m4)
		#print(n4 + "\n")
		#print(mYline[0])
		#print(orLine[0]+"\n")
		#print(m10+"\n")
		#print(n10+"\n")
		#print(m20)
		#print(n20)
		
		om4.append(m4)
		om10.append(m10)
		om20.append(m20)
		omy.append(mYline[0])
		ony.append(orLine[0])






with open('raw_data/classnox','wb') as f:
	pickle.dump(classnox,f)

with open('raw_data/classmaskx','wb') as f:
	pickle.dump(classmaskx,f)

with open('raw_data/y','wb') as f:
	pickle.dump(y,f)


for x in (classnox,classmaskx,y):
	print(len(x))

for i in range(50):
	print(classnox[i])
	print(y[i])
	print("---------------------")



print("All completed")




for x in (on4,on10,on20,om4,om10,om10,ony,omy):
        print(len(x))




with open('raw_data/on4','wb') as f:
        pickle.dump(on4,f)

with open('raw_data/on10','wb') as f:
        pickle.dump(on10,f)

with open('raw_data/on20','wb') as f:
        pickle.dump(on20,f)

with open('raw_data/ony','wb') as f:
        pickle.dump(ony,f)


with open('raw_data/om4','wb') as f:
        pickle.dump(om4,f)

with open('raw_data/om10','wb') as f:
        pickle.dump(om10,f)

with open('raw_data/om20','wb') as f:
        pickle.dump(om20,f)

with open('raw_data/omy','wb') as f:
        pickle.dump(omy,f)

print("All completed")


