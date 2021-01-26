from __future__ import unicode_literals, print_function
import plac 
import random
from pathlib import Path
import spacy
import json
from tqdm import tqdm
import pandas as pd

def prepare_data():
    df = pd.read_csv('Datasets/Entities_dataset_2.csv')
    l1 = []
    l2 = []
    for i in range(0, len(df['sentence'])):
        l1.append(df['sentence'][i])
        ents = []
        labels = df['label'][i].split()
        start = df['start'][i].split()
        end = df['end'][i].split()
        for x in range(0, len(labels)):
            ents.append((int(start[x]),int(end[x]), labels[x]))
        l2.append({"entities": ents})
    return list(zip(l1, l2))

TRAIN_DATA = prepare_data()

print(TRAIN_DATA)

# Setting up the model
model = None
output_dir = Path("E:\\Projects\\RESTAURANT_CHATBOT\\Model")
n_iter=200

#load the Model

if model is not None:
    nlp = spacy.load(model)
    print("Loaded model '%s'" % model)
else:
    nlp = spacy.blank('en')
    print("Created blank 'en' model")

#set up the pipeline

if 'ner' not in nlp.pipe_names:
    ner = nlp.create_pipe('ner')
    nlp.add_pipe(ner, last=True)
else:
    ner = nlp.get_Pipe('ner')

for _, annotations in TRAIN_DATA:
    for ent in annotations.get('entities'):
        ner.add_label(ent[2])

other_pipes = [pipe for pipe in nlp.pipe_names if pipe != 'ner']
with nlp.disable_pipes(*other_pipes):  # only train NER
    optimizer = nlp.begin_training()
    for itn in range(n_iter):
        random.shuffle(TRAIN_DATA)
        losses = {}
        for text, annotations in tqdm(TRAIN_DATA):
            nlp.update(
                [text],  
                [annotations],  
                drop=0.5,  
                sgd=optimizer,
                losses=losses)
        print(itn,losses)

for text, _ in TRAIN_DATA:
    print("text: {} \t".format(text), end='')
    doc = nlp(text)
    print('Entities: ', [(ent.text, ent.label_) for ent in doc.ents])

if output_dir is not None:
    output_dir = Path(output_dir)
    if not output_dir.exists():
        output_dir.mkdir()
    nlp.to_disk(output_dir)
    print("Saved model to", output_dir)