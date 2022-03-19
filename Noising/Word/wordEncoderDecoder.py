import re
import random
import pickle
from collections import Counter
import string
import tqdm



# list of files
ccode = []

	
extend_size = 10

operations = ['add','rm','ch','dup']

printable = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'

insertToken = []

types = ['int','short','long','byte','float','double','char','boolean','Integer']


for p in printable:
	insertToken.append(p)


def tok_change(s):


	de = random.randint(0,10)
	
	
	if s.isnumeric():
		return ""
	if de > 4:
		return ""
	
	if s in types:
		if de == 1:
			return random.choice(types)
	
	
	rg = int(len(s)/2)

	if rg < 2:
		num = 1
	else:
		num = random.randint(1,rg)

	for i in range(num):
		l = len(s)
		if l == 0:
			s = s + random.choice(insertToken)
			continue
			
		token_index = random.randint(0,l-1) 
		op = random.choice(operations)
		

		if op == 'add':
			s = s[:token_index] + random.choice(insertToken) + s[token_index:]

		if op == 'dup':
			s = s[:token_index] + s[token_index] + s[token_index:]
		
		if op == 'rm':
			s = s[:token_index] + s[token_index+1:]

		if op == 'ch':
			s = s[:token_index] + random.choice(insertToken) + s[token_index+1:]

		
	return s

def read_input(code):

	code = re.sub(' +', ' ',code)
	codeLines = code.split('\n')
	
	if len(codeLines) < 10:
		return ([],[],[],[])
	

	variables = re.findall(r"[A-Za-z0-9]+", code)

	if(len(variables) < 10):
		return ([],[],[],[])

	

	lineToChange = []
	for index,line in enumerate(codeLines):
		invalid = re.findall(r"[\*]|[*/]|[//]|[@]", line)
		if len(invalid)>= 1:
			continue	
			
		listline = re.findall(r"[A-Za-z]+|[0-9]+|\t|\S| |.", str(line))
		if len(listline) > 100:
			continue	
		
		for tok in listline:
			if tok.isalnum():
				lineToChange.append(index)
				break


	if len(lineToChange) < 1:
		return ([],[],[],[])
		
	

	linesToBreak = random.choices(lineToChange,k=extend_size)
	
	x4 = []
	x10 = []
	x20 = []
	y = []
	for line in linesToBreak:
		current = codeLines.copy()[line]
		
		listline = re.findall(r"[A-Za-z]+|[0-9]+|\t|\S| |.", current)
			
		tokToChange = []
		for index,tok in enumerate(listline):
			if tok.isalnum():
				tokToChange.append(index)
		
		
		tid = random.choice(tokToChange)
		listline[tid] = tok_change(listline[tid])
		de = random.randint(0,20)
		if de > 19:
			tid = random.choice(tokToChange)
			listline[tid] = tok_change(listline[tid])
			tid = random.choice(tokToChange)
			listline[tid] = tok_change(listline[tid])
			tid = random.choice(tokToChange)
			listline[tid] = tok_change(listline[tid])
		elif de > 18:
			tid = random.choice(tokToChange)
			listline[tid] = tok_change(listline[tid])
			tid = random.choice(tokToChange)
			listline[tid] = tok_change(listline[tid])
		elif de > 17:
			tid = random.choice(tokToChange)
			listline[tid] = tok_change(listline[tid])
		
		current = "".join(listline)	


		

		leftLines = []
		rightLines = []
		errorline = "<E>" + current
		for i in range(10):
			leftLines.append("")
			rightLines.append("")
		
		for i in range(10):
			if (line - 1 - i >= 0):
				leftLines[i] = "<L" + str(i) +">" +  codeLines[line - 1 - i] 
		for i in range(10):
			if (line + 1 + i < len(codeLines)):
				rightLines[i] = "<R" + str(i) + ">" + codeLines[line + 1 + i]

		leftLines.reverse()

		n20 = "\n".join(leftLines+[errorline]+rightLines)
		n10 = "\n".join(leftLines[-5:]+[errorline]+rightLines[0:5])	
		n4 = "\n".join(leftLines[-2:]+[errorline]+rightLines[0:2])

		x4.append(n4)
		x10.append(n10)
		x20.append(n20)
		y.append(codeLines.copy()[line])
	

	return (x4,x10,x20,y)
	
train_x4 = []
train_x10 = []
train_x20 = []
train_y = []


	
for code in tqdm.tqdm(ccode):

	(x4,x10,x20,yi) = read_input(str(code))

	train_x4.extend(x4)
	train_x10.extend(x10)
	train_x20.extend(x20)
	train_y.extend(yi)
	

import pandas as pd
from sklearn.model_selection import train_test_split


for i in range(100):
	print(train_x4[i])
	print()
	print(train_x10[i])
	print()
	print(train_x20[i])
	print()
	print(train_y[i])
	print("------------------------------------------")

code20 = train_x20
line = train_y
fast = []
for i,c in enumerate(code20):
        if b'\x00' in bytes(line[i],'utf-8') or b'\x00' in bytes(code20[i],'utf-8') :
                continue
        fast.append([str(code20[i]),str(line[i])])


df = pd.DataFrame(fast,columns=['input_text','target_text'])
df['input_text'].astype(str)
df['target_text'].astype(str)
df = df.dropna()
df = df.sample(frac = 1)
df.to_csv('wordseq20.csv')









#-------------------------------------------------------------------------------------
code4 = train_x4
line = train_y


fast = []
for i,c in enumerate(code4):
        if b'\x00' in bytes(line[i],'utf-8') or b'\x00' in bytes(code4[i],'utf-8') :
                continue
        fast.append([str(code4[i]),str(line[i])])


df = pd.DataFrame(fast,columns=['input_text','target_text'])
df['input_text'].astype(str)
df['target_text'].astype(str)
df = df.dropna()
df = df.sample(frac = 1)
#train,valid = train_test_split(df,test_size=0.05)
df.to_csv('wordseq4.csv')


#-------------------------------------------------------------------------------------

code10 = train_x10
line = train_y
fast = []
for i,c in enumerate(code10):
        if b'\x00' in bytes(line[i],'utf-8') or b'\x00' in bytes(code10[i],'utf-8') :
                continue
        fast.append([str(code10[i]),str(line[i])])


df = pd.DataFrame(fast,columns=['input_text','target_text'])
df['input_text'].astype(str)
df['target_text'].astype(str)
df = df.dropna()
df = df.sample(frac = 1)
df.to_csv('wordseq10.csv')

#-------------------------------------------------------------------------------------

	
