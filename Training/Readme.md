# How to use

## Training Classification
To train the classifier, we need 'train_Classifier.csv' generated by the noising method. The training data should be saved in the same directory of the training script.
```python
dataset = load_dataset('csv', data_files={'train':'train_Classifier.csv','test':'valid_Classifier.csv'}, cache_dir="cache",prefix = lib.no_default)
```

'python trainClassification.py' to run the file.

All checkpoints will be saved in  'result' folder.




## Training Encoder decoder
To train the encoder decoder model, we need 'train_new.csv' file.
```python
dataset = load_dataset('csv', data_files={'train':'train_Classifier.csv','test':'valid_Classifier.csv'}, cache_dir="cache",prefix = lib.no_default)
```

'python trainEncoderDecoder.py' to start training.

All checkpoints will be saved in  'result' folder.

## Train from a pre-trained checkpoint
Save the pre-trained checkpoint in directory checkpoint#### and rename the model directory.
```python
#Classification
model = AutoModelForSequenceClassification.from_pretrained("checkpoint-class",num_labels=num_labels)

#EncoderDecoder
roberta_shared = EncoderDecoderModel.from_pretrained("checkpoint-seq")
roberta_shared = EncoderDecoderModel.from_encoder_decoder_pretrained("checkpoint-seq", "checkpoint-seq", tie_encoder_decoder=True)
```

If no pre-trained checkpoint available, we can download the 'roberta-base' checkpoint from huggingface.

```python
#Classification
model = AutoModelForSequenceClassification.from_pretrained("roberta-base",num_labels=num_labels)

#EncoderDecoder
roberta_shared = EncoderDecoderModel.from_encoder_decoder_pretrained("roberta-base", "roberta-base", tie_encoder_decoder=True)
```

