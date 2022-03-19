import re
import random
import pickle
from collections import Counter
import string
import tqdm


existingcount = Counter(list(range(0, 201)))

# list of buggy files
ccode = []

#count = Counter([])
#for i in range(20):
#	fileindex = str(i+1)
#	with open('../code/mostFrequentPickle'+fileindex,'rb') as infile:
#		mf = pickle.load(infile)
#		count = count + mf
	
#mfm = count.most_common(500)
#mfmt = []
#for (token,counts) in mfm:
#	if token.isalpha() and len(token)>2:
#		mfmt.append(token)
#mfmt = mfmt[0:300]
#print(mfmt)
	
extend_size = 10

operations = ['add','rm','ch','dup']

printable = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ.'

types = ['int','short','long','byte','float','double','char','boolean','final','class','void','new','Integer','interface','false','true','if','else','abstract']
insertToken = []


for p in printable:
	insertToken.append(p)


def tok_change(s):
	

	de = random.randint(0,5)

	if de > 1 or s.isnumeric():
		s = ""
		return s
	if s in types:
		if de == 1:
			return random.choice(types)

			

	rg = int(len(s)/2-1)

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

def read_input(code,maxindex):

	variables = re.findall(r"[A-Za-z]+", code)
	if(len(variables) < 10):
		return ([],[])

	codeLines = code.split('\n')
	
	
	
	lineToChange = []
	for index,line in enumerate(codeLines):
		listline = re.findall(r"[A-Za-z]+|\t|\S| |.", line)
		if len(listline) > 50:
			return([],[])		
			
		for tok in listline:
			if tok.isalpha():
				lineToChange.append(index)
				break
	
	if len(lineToChange) < extend_size:
		return ([],[])
		
	
	
	linesToBreak = random.sample(lineToChange,extend_size)


	
	x = []
	yline = []


#	for i in range(len(codeLines)):
#		codeLines[i] = "<"+str(i)+">"+codeLines[i]

	for line in linesToBreak:
		current = codeLines[line]
		listline = re.findall(r"[A-Za-z0-9]+|\t|\S| |.", current)
			
		tokToChange = []
		for index,tok in enumerate(listline):
			if tok.isalnum():
				tokToChange.append(index)
		
		
		tid = random.choice(tokToChange)
		listline[tid] = tok_change(listline[tid])
		de = random.randint(0,10)
		if de >= 9:
			tid = random.choice(tokToChange)
			listline[tid] = tok_change(listline[tid])
			tid = random.choice(tokToChange)
			listline[tid] = tok_change(listline[tid])
			tid = random.choice(tokToChange)
			listline[tid] = tok_change(listline[tid])

		elif de >= 8:
			tid = random.choice(tokToChange)
			listline[tid] = tok_change(listline[tid])
			tid = random.choice(tokToChange)
			listline[tid] = tok_change(listline[tid])
		elif de >= 7:
			tid = random.choice(tokToChange)
			listline[tid] = tok_change(listline[tid])
	

		for i in range(len(codeLines)):
			codeLines[i] = "<"+str(i)+">"+codeLines[i]
		
		current = "<" + str(line) +">" +  "".join(listline)		

		m = maxindex
		if m == 20:
			m = random.randint(0,19)
			yline.append(20)
			current = codeLines[line]

		xleft = line - m
		xright = line + (20-m)

 		

		if xleft < 0:
			e = codeLines[0:line] + [current] + codeLines[line+1:xright]
			e = ["<L>" for i in range(20-len(e))] + e 
		else:
			e = codeLines[xleft:line] + [current] + codeLines[line+1:xright]


		if xright > len(codeLines):
			e = e + ["<R>" for i in range(20-len(e))] 

		x.append("\n".join(e))

		if not maxindex == 20:
			for i in range(20):
				if e[i] == current:
					yline.append(str(i))
					break
		
	if not len(yline) == len(x):
		exit()
	return (x,yline)
	
train_x = []
train_yline = []
maxindex = 15

prefix = 1	
for code in tqdm.tqdm(ccode):

	if(prefix%400000 == 0):
		with open('../newdata/new_trainx_'+str(int(prefix/400000)),'wb') as cap:
			pickle.dump(train_x,cap)			 
		with open('../newdata/new_trainyline_'+str(int(prefix/400000)),'wb') as cac:
			pickle.dump(train_yline,cac)

		print(len(train_x))
		print(len(train_yline))
		train_x = []
		train_yline = []

	prefix = prefix + 1	


	
	(xi,ylinei) = read_input(code,maxindex)
	
	if maxindex >= 20:
		maxindex = 0
	else:
		maxindex = maxindex + 1

	train_x.extend(xi)
	train_yline.extend(ylinei)

	
		
with open('../newdata/new_trainx_f','wb') as cap:
	pickle.dump(train_x,cap)
with open('../newdata/new_trainyline_f','wb') as cac:
	pickle.dump(train_yline,cac)


for i in range(100):
	print(train_yline[i])
	print(train_x[i])
	print()

print(len(train_x))


