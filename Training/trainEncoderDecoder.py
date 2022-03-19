import nltk
import torch
import os
import pandas as pd
from datasets import Dataset


os.environ["TOKENIZERS_PARALLELISM"] = "false"
os.environ["WANDB_DISABLED"] = "true"
os.environ['TRANSFORMERS_CACHE'] = '../cache'

from transformers import RobertaTokenizerFast
tokenizer = RobertaTokenizerFast.from_pretrained("../standard")

from datasets import load_dataset

import pandas._libs.lib as lib

#train_data = load_dataset('csv',data_files = 'train_new.csv',split="train",cache_dir="../cache",engine='python', encoding = "utf-8", prefix = lib.no_default,error_bad_lines=False,skip_blank_lines = True)

df = pd.read_csv('train_new.csv', dtype={"Unnamed: 0": "O", "input_text": "string","target_text":"string"})
df = df.dropna()
train_data = Dataset.from_pandas(df)

print(train_data)


print("Starting tokenization")

batch_size = 8  # change to 16 for full training
encoder_max_length = 512
decoder_max_length = 64

def process_data_to_model_inputs(batch):                                                                                                  
    inputs = tokenizer(batch["input_text"], padding="max_length", truncation=True, max_length=encoder_max_length)
    outputs = tokenizer(batch["target_text"], padding="max_length", truncation=True, max_length=decoder_max_length)                                                                      
    batch["input_ids"] = inputs.input_ids                                                               
    batch["attention_mask"] = inputs.attention_mask                                                     
    batch["decoder_input_ids"] = outputs.input_ids                                                      
    batch["labels"] = outputs.input_ids.copy()                                                          
                                                                         
    batch["labels"] = [                                                                                 
        [-100 if token == tokenizer.pad_token_id else token for token in labels] for labels in batch["labels"]
    ]                     
    batch["decoder_attention_mask"] = outputs.attention_mask                                                                              
                                                                                                         
    return batch  

train_data = train_data.map(
    process_data_to_model_inputs, 
    batched=True, 
    batch_size=batch_size, 
    remove_columns=["input_text", "target_text"],
)
train_data.set_format(
    type="torch", columns=["input_ids", "attention_mask", "decoder_input_ids", "decoder_attention_mask", "labels"],
)


from transformers import EncoderDecoderModel

roberta_shared = EncoderDecoderModel.from_pretrained("./new/checkpoint-4000")
#roberta_shared = EncoderDecoderModel.from_encoder_decoder_pretrained("../../model/nomask", "../../model/nomask", tie_encoder_decoder=True)

# set special tokens
roberta_shared.config.decoder_start_token_id = tokenizer.bos_token_id                                             
roberta_shared.config.eos_token_id = tokenizer.eos_token_id

from transformers import Seq2SeqTrainer
from transformers import TrainingArguments
from dataclasses import dataclass, field
from typing import Optional
import datasets

lr = 5e-7

print("----------------------------")
print(lr)    
print("----------------------------")
training_args = Seq2SeqTrainingArguments(
    #output_dir="./result",
    output_dir = "./new",    
    per_device_train_batch_size=batch_size,
    per_device_eval_batch_size=batch_size,
    logging_steps=2000,  # set to 2000 for full training
    save_steps = 2000,  # set to 500 for full training
    warmup_steps=10,  # set to 3000 for full training
    num_train_epochs = 10,
    save_strategy = 'steps',
    overwrite_output_dir=True,
    learning_rate = lr,
    save_total_limit=10,
    weight_decay = 0.1,
    evaluation_strategy = "no",
    gradient_accumulation_steps = 128,
    ignore_data_skip = True,

)

# instantiate trainer
trainer = Seq2SeqTrainer(
    model=roberta_shared,
    args=training_args,
    train_dataset=train_data,
)
trainer.train()
#roberta_shared.save_pretrained("./71")
