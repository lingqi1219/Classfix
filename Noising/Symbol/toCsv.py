import pandas as pd
from sklearn.model_selection import train_test_split
import pickle
import string


code = []
line = []


codeN = []
lineN = []

# fixing no data
with open('../raw_data/on4','rb') as infile:
	codeN = codeN + pickle.load(infile)
with open('../raw_data/ony','rb') as infile:
	lineN = lineN + pickle.load(infile)

    

fast = []
total = 0
for i,c in enumerate(codeN):
	if b'\x00' in bytes(lineN[i],'utf-8') or b'\x00' in bytes(codeN[i],'utf-8') :
		continue
	fast.append([str(codeN[i]),str(lineN[i])])


df = pd.DataFrame(fast,columns=['input_text','target_text']) 
df.dropna()
df.astype(str)
#df['input_text'].astype(str)
#df['target_text'].astype(str)
train,valid = train_test_split(df,test_size=0.1)
#valid,test = train_test_split(valid,test_size=0.5)
train.to_csv('no/train3.csv')
valid.to_csv('no/valid.csv')
#test.to_csv('no/test.csv')

print(fast[0])
print()
print(fast[0][0])
print()
print(fast[0][1])


exit()

#fixing mask data
#with open('../raw_data/om4','rb') as infile:
#        code = code + pickle.load(infile)
#with open('../raw_data/omy','rb') as infile:
#        line = line + pickle.load(infile)


#fast = []
#for i,c in enumerate(code):
#        if b'\x00' in bytes(line[i],'utf-8') or b'\x00' in bytes(code[i],'utf-8') :
#                continue
#        fast.append([str(code[i]),str(line[i])])


#df = pd.DataFrame(fast,columns=['input_text','target_text'])
#df = df.dropna()
#df.astype(str)
##df['input_text'].astype(str)
##df['target_text'].astype(str)

train,valid = train_test_split(df,test_size=0.1)
valid,test = train_test_split(valid,test_size=0.5)
train.to_csv('mask/train.csv')
valid.to_csv('mask/valid.csv')
test.to_csv('mask/test.csv')


print(fast[0])
print()
print(fast[0][0])
print()
print(fast[0][1])



