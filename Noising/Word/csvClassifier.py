import pandas as pd
from sklearn.model_selection import train_test_split
import pickle



code = []
line = []


for files in range(2):
	fileindex = str(files+1)
	with open('../newdata/new_trainx_'+fileindex,'rb') as infile:
		code = code + pickle.load(infile)
	with open('../newdata/new_trainyline_'+fileindex,'rb') as infile:
		line = line + pickle.load(infile)
       
with open('../newdata/new_trainx_f','rb') as infile:
	code = code + pickle.load(infile)
with open('../newdata/new_trainyline_f','rb') as infile:
	line = line + pickle.load(infile)


for i in range(100):	
	print(code[i])
	print(line[i])
	print()


print(len(code))
print(len(line))

dic = {'text':code, 'label':line}
df = pd.DataFrame(dic, columns = ['text','label']) 

df['label'] = df['label'].apply(lambda x: int(x))    

#df = df.sample(frac = 1)

train,valid = train_test_split(df,test_size=0.05)
#valid,test = train_test_split(valid,test_size=0.5)
train.to_csv('train_Classifier_new3.csv')
valid.to_csv('valid_Classifier_new.csv')
#test.to_csv('test_Classifier_new.csv')
