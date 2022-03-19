import re
import random
from collections import Counter
bracket_symbols = ['(',')','[',']','{','}',';',',','.',':','"','+']
#print(len(bracket_symbols))

extend_size = 1
max_lines = 20

delimiter_random = [-1,-1,0,1,2]



def break_line(s):
	changeAble = []
	for index,tok in enumerate(s):
		if tok in bracket_symbols:
			changeAble.append(index)
	

	
	if len(changeAble)>1:
		
		# shuffle the lines
		random.shuffle(changeAble)
		changeAble = changeAble[0]
		action = random.choice(delimiter_random)

		
		if action == 1:
			#replace

			append = random.choice(bracket_symbols)
			s = s[:changeAble] + append + s[changeAble + 1:]

		elif action == 2:
			#add

			append = random.choice(bracket_symbols)

			s = s[:changeAble+1] + append + s[changeAble+1:]

		elif action == 0:
			#duplicate

			s = s[:changeAble] + s[changeAble] + s[changeAble:]

		elif action == -1:
			#remove

			s = s[:changeAble] + s[changeAble + 1:]

	else:
		append = random.choice(bracket_symbols)
		s = s + append
	return s

	


def create_data(codeAsLine,toRepairIndex,maxindex):
	
	classcode = []
	labels = []
	orCode = []
	orLine = []
	indd = []
	for i in toRepairIndex:
		indd.append(i)
		line = codeAsLine[i]
		newCode = codeAsLine.copy()
		if maxindex >= 20:
			m = random.randint(0,19)
			xleft = i - m
			xright = i + (20-m)
			if xleft < 0:
				e = codeAsLine[0:i] + [line] + codeAsLine[i+1:xright]
				e = ["<L>" for j in range(20-len(e))] + e
			else:
				e = codeAsLine[xleft:i] + [line] + codeAsLine[i+1:xright]
			if xright > len(codeAsLine):
				e = e + ["<R>" for j in range(20-len(e))]
			classcode.append("\n".join(e))
			labels.append(str(20))
			continue
			
		line = break_line(line) 
		
		n = random.randint(0,10)
		if n > 9:
			line = break_line(line)
			line = break_line(line)
			line = break_line(line)
		elif n > 8:
			line = break_line(line)
			line = break_line(line)
		elif n > 6:
			line = break_line(line)


		newCode[i] = line
		orCode.append( "\n".join(newCode))
		orLine.append(codeAsLine[i])

		xleft = i - maxindex
		xright = i + (20-maxindex) 

		
		if xleft < 0:
			e = codeAsLine[0:i] + [line] + codeAsLine[i+1:xright]
			e = ["<L>" for j in range(20-len(e))] + e 
		else:
			e = codeAsLine[xleft:i] + [line] + codeAsLine[i+1:xright]
			
		if xright > len(codeAsLine):
			e = e + ["<R>" for j in range(20-len(e))] 

		classcode.append("\n".join(e))
		
		for j in range(20):
			if e[j] == line:
				labels.append(str(j))
				break
				
	
	
		if not len(classcode) == len(labels):
			exit()
		if not len(orCode) == len(orLine):
			exit()

	return(classcode,labels,orCode,orLine,indd)





def read_input(code,linecount,maxindex):


	codeAsLineI = code.split('\n')
	codeAsLine = []
	
	for snip in codeAsLineI:
		snip = snip.rstrip('\x00')
		if snip.isspace():
			if random.random() < 0.3:
				codeAsLine.append("")
		else:
			codeAsLine.append(snip)
	
	changeAbleLine = []
	
	# check if the line contains delimiters
	for index,line in enumerate(codeAsLine):
		
		if line.isspace() or line == "":
			changeAbleLine.append(index)
			continue
			
		for tok in line:
			if tok in bracket_symbols:
				changeAbleLine.append(index)
				break 
				

	
	# check if the file is modifyable
	#if len(changeAbleLine) < 1:
	#	return([],[],[])

	toRepairIndex = random.choices(changeAbleLine,k=extend_size)

	
	(classcode,y,orCode,orLine,ind) = create_data(codeAsLine,toRepairIndex,maxindex)
	
	return (classcode,y,linecount,orCode,orLine,ind)
	
	

#code = "hi\nPublic.static line1()\n line2 {}\n i,line3,()mr:\n no line4 to change\n here lin5 as well"

