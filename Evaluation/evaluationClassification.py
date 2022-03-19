import nltk
import torch
import numpy as np
import os
import wandb
os.environ["WANDB_DISABLED"] = "true"
os.environ['TOKENIZERS_PARALLELISM']='false'

import pandas as pd
from datasets import Dataset

from transformers import AutoTokenizer
from transformers import RobertaConfig, RobertaModel, RobertaTokenizerFast
#tokenizer = RobertaTokenizerFast.from_pretrained("../model/standard")
tokenizer = RobertaTokenizerFast.from_pretrained("../model/standard")



def preprocess_function(examples):
   #return tokenizer(examples['text'], truncation=True, max_length = 512)
    return tokenizer(examples['text'], truncation=True, max_length=512)

from datasets import load_dataset, load_metric, list_metrics
import numpy as np

#dataset = load_dataset('csv',data_files={'train':'../aug/trainClassifier.csv','test':'../aug/validClassifier.csv'}, cache_dir="./cache")
#import pandas._libs.lib as lib
#dataset = load_dataset('csv',data_files={'test':'symbol_no_test.csv'}, cache_dir="./cache",prefix = lib.no_default)

df = pd.read_csv('word_no_test.csv', dtype={"Unnamed: 0": "O", "text": "string","label":"int"}, engine='python')

df = df.dropna()
dataset = Dataset.from_pandas(df)
print(dataset)


batch_size = 4

metric = load_metric('accuracy')


print('dataset done\n')

from transformers import AutoModelForSequenceClassification, TrainingArguments, Trainer

num_labels = 21
model = AutoModelForSequenceClassification.from_pretrained('./new/checkpoint-19003',num_labels=num_labels)

metric_name = "accuracy"




def compute_metrics(eval_pred):
    predictions, labels = eval_pred

    predictions = np.argmax(predictions, axis=1)

    return metric.compute(predictions=predictions, references=labels)
    

model.to("cuda")

batch_size = 4  # change to 64 for full evaluation

print("New")

softmax = torch.nn.Softmax(dim = 1)


correct = 0
current = []
 
# map data correctly
def generate_summary(batch):

    inputs = tokenizer(batch["text"], padding="max_length", truncation=True, max_length=512, return_tensors="pt")
 
    inputs.to("cuda")
    outputs = model(**inputs)
    o = softmax(outputs.logits)
    outputs = torch.argmax(o,dim=1).item()

    label = batch['label']

    global correct

    #print(outputs)
    if label == outputs:
    	correct = correct + 1
    	current.append(1)
    else:
    	current.append(0)
    	#print(batch["text"])
    	print(outputs)
    	print("--------------------------------")

    batch["pred"] = outputs
    
    return batch



results = dataset.map(generate_summary, batched=False, batch_size=batch_size)

print(correct)
#print(current)

import pickle
with open('result.pkl', 'wb') as f:
	pickle.dump(current, f)
