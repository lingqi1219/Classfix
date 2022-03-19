import datasets
from datasets import Dataset
from transformers import RobertaTokenizer, EncoderDecoderModel, RobertaTokenizerFast
import pandas._libs.lib as lib
import pandas as pd
import re



df = pd.read_csv('test4.csv', dtype={"Unnamed: 0": "O", "input_text": "string","target_text":"string"})

df = df.dropna()
test_data = Dataset.from_pandas(df)



rouge = datasets.load_metric("rouge")

def compute_metrics(pred):
    labels_ids = pred.label_ids
    pred_ids = pred.predictions

    # all unnecessary tokens are removed
    pred_str = tokenizer.batch_decode(pred_ids, skip_special_tokens=True)
    labels_ids[labels_ids == -100] = tokenizer.pad_token_id
    label_str = tokenizer.batch_decode(labels_ids, skip_special_tokens=True)

    rouge_output = rouge.compute(predictions=pred_str, references=label_str, rouge_types=["rouge2"])["rouge2"].mid

    return {
        "rouge2_precision": round(rouge_output.precision, 4),
        "rouge2_recall": round(rouge_output.recall, 4),
        "rouge2_fmeasure": round(rouge_output.fmeasure, 4),
    }


#tokenizer = RobertaTokenizerFast.from_pretrained("/proj/snic2020-5-668/users/x_ziyxi/model/standard")
tokenizer = RobertaTokenizerFast.from_pretrained("../../model/standard")


molcheck = "./new/new"

print(molcheck)
model = EncoderDecoderModel.from_pretrained(molcheck)
model.to("cuda")


# only use 16 training examples for notebook - DELETE LINE FOR FULL TRAINING
test_data = test_data.select(range(555))

batch_size = 4  # change to 64 for full evaluation

# map data correctly
def generate_summary(batch):
    # Tokenizer will automatically set [BOS] <text> [EOS]
 
    inputs = tokenizer(batch["input_text"], padding="max_length", truncation=True, max_length=512, return_tensors="pt")
    input_ids = inputs.input_ids.to("cuda")
    attention_mask = inputs.attention_mask.to("cuda")

    outputs = model.generate(input_ids, attention_mask=attention_mask)

    # all special tokens including will be removed
    output_str = tokenizer.batch_decode(outputs, skip_special_tokens=True)

    batch["pred"] = output_str
    
    return batch



results = test_data.map(generate_summary, batched=True, batch_size=batch_size, remove_columns=["input_text"])

pred_str = results["pred"]
label_str = results["target_text"]

#for i in range(len(pred_str)):
#	print("predt:" + pred_str[i])
#	print("label:" + label_str[i])
#	print()

rouge_output = rouge.compute(predictions=pred_str, references=label_str, rouge_types=["rouge2"])["rouge2"].mid
print(rouge_output)


from nltk.metrics import *
#from scipy.spatial import distance

print(molcheck)

acc = 0
correct = 0
#print(label_str)
resultList = [0 for i in range(555)]
print(len(pred_str))
goodlist = []
for i in range(len(pred_str)):
	p = pred_str[i].split()
	ref = label_str[i].split()
	
	pl = len(p)
	pr = len(ref)
	
	
	
	if pl < pr:
		for j in range(pr-pl):
			p.append('')
	elif pr < pl:
		for j in range(pl-pr):
			ref.append('')
			
	acc = acc + accuracy(p,ref)
	
	if p == ref:
		correct = correct + 1
		resultList[i] = 1
		goodlist.append(i)	
	else:
		ref2 = re.sub(' ', '',label_str[i])
		ref2 = re.sub('[\t]','',ref2)
		p2 = re.sub(' ', '',pred_str[i])
		p2 = re.sub('[\t]','',p2)
		if p2 == ref2:
			correct = correct + 1
			resultList[i] = 1	
			goodlist.append(i)	

	
	

print(goodlist)

acc = acc / len(pred_str)
print(correct)
correct = correct / len(pred_str)
print('nltk accuracy: ' + str(acc))
print('full repair: '+ str(correct))
print(len(pred_str))


import pickle
with open('word4.pkl', 'wb') as f:
	pickle.dump(resultList, f)
print(resultList)
with open('result4.pkl', 'wb') as f:
	pickle.dump(pred_str, f)
