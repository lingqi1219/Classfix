import nltk
import torch
import numpy as np
import os
import wandb
os.environ["WANDB_DISABLED"] = "true"
os.environ['TOKENIZERS_PARALLELISM']='false'
import pandas._libs.lib as lib


from transformers import AutoTokenizer
from transformers import RobertaConfig, RobertaModel, RobertaTokenizerFast

tokenizer = RobertaTokenizerFast.from_pretrained("../../../model/standard")

def preprocess_function(examples):
    return tokenizer(examples['text'], truncation=True, max_length=512)

from datasets import load_dataset, load_metric, list_metrics

print(lib.no_default)

dataset = load_dataset('csv', data_files={'train':'train_Classifier.csv','test':'valid_Classifier.csv'}, cache_dir="cache",prefix = lib.no_default)

batch_size = 8

metric = load_metric('accuracy')


encoded_dataset = dataset.map(preprocess_function, batched=True)




print('dataset done\n')

from transformers import AutoModelForSequenceClassification, TrainingArguments, Trainer

num_labels = 21

model = AutoModelForSequenceClassification.from_pretrained("result/checkpoint-18780",num_labels=num_labels)

metric_name = "accuracy"

print("------------------------------------------------- \n LearningRate:")
lr = 5e-6
print(lr)
print("-------------------------------------------------")

args = TrainingArguments(
    'result',
    evaluation_strategy = "epoch",
    eval_steps = 20000,
    save_strategy = 'epoch',
    logging_strategy = "steps",
    logging_steps = 10000,
    learning_rate=lr,
    per_device_train_batch_size=batch_size,
    per_device_eval_batch_size=batch_size,
    num_train_epochs=10,
    weight_decay=0.1,
    load_best_model_at_end=True,
    metric_for_best_model=metric_name,
    gradient_accumulation_steps = 128,
    ignore_data_skip = True,
)





def compute_metrics(eval_pred):
    predictions, labels = eval_pred
    predictions = np.argmax(predictions, axis=1)
    return metric.compute(predictions=predictions, references=labels)
    

trainer = Trainer(
    model,
    args,
    train_dataset=encoded_dataset['train'],
    eval_dataset=encoded_dataset['test'],
    tokenizer=tokenizer,
    compute_metrics=compute_metrics
)

trainer.train()
trainer.save_model()
