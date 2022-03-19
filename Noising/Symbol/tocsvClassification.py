import pandas as pd
from sklearn.model_selection import train_test_split
import pickle



codeN = []
lineN = []

code = []
line = []



with open('../raw_data/classnox','rb') as infile:
	codeN = codeN + pickle.load(infile)
with open('../raw_data/y','rb') as infile:
	lineN = lineN + pickle.load(infile)

with open('../raw_data/classmaskx','rb') as infile:
	code = code + pickle.load(infile)
with open('../raw_data/y','rb') as infile:
	line = line + pickle.load(infile)


for i in range(100):
	print(codeN[i])
	print(code[i])
       



print(len(code))
print(len(line))

print(len(codeN))
print(len(lineN))


cl = []
for i, c in enumerate(code):
	cl.append(["<code>"+code[i],line[i]])

df = pd.DataFrame(cl, columns = ['text','label']) 

df['label'] = df['label'].apply(lambda x: int(x))    
df['text'] = df['text'].apply(lambda x: str(x))

train,valid = train_test_split(df,test_size=0.1)
train = train.sample(frac = 1)
valid = valid.sample(frac = 1)
#valid,test = train_test_split(valid,test_size=0.5)
train.to_csv('counter/train_Classifier2.csv')
#valid.to_csv('counter/valid_Classifier.csv')
#test.to_csv('counter/test_Classifier.csv')



cl = []
for i, c in enumerate(code):
        cl.append(["<code>"+codeN[i],lineN[i]])

df = pd.DataFrame(cl, columns = ['text','label'])

df['label'] = df['label'].apply(lambda x: int(x))
df['text'] = df['text'].apply(lambda x: str(x))

train,valid = train_test_split(df,test_size=0.1)
train = train.sample(frac = 1)
valid = valid.sample(frac = 1)
#valid,test = train_test_split(valid,test_size=0.5)
train.to_csv('no/train_Classifier2.csv')
#valid.to_csv('no/valid_Classifier.csv')
#test.to_csv('no/test_Classifier.csv')


