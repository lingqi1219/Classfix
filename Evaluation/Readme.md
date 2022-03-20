# How to evaluate


## Load the checkpoint

Load the pre-trained checkpoint by modifying variable 'model', or use the 'roberta-base' model from huggingface.
'''python
model = AutoModelForSequenceClassification.from_pretrained('./checkpoint',num_labels=num_labels)
'''

## input
For the evaluation, it takes a csv file as input. 
'''python
df = pd.read_csv('filename.csv', dtype={"Unnamed: 0": "O", "text": "string","label":"int"}, engine='python')
'''
This line create the panda dataframe. Change filename.csv to the evaluation data.

## output
The computed results will be print to the console, and saved in form a pickles.
