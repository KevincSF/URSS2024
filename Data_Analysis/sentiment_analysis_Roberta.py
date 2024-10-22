import re
import pandas as pd
import numpy as np
import torch
import csv
import os
from transformers import AutoTokenizer,AutoModelForSequenceClassification,Trainer
model_directory = os.path.join(os.curdir,"sentiment-roberta-large-english-3-classes")
tokenizer = AutoTokenizer.from_pretrained(model_directory)
model = AutoModelForSequenceClassification.from_pretrained(model_directory)
trainer = Trainer(model=model)


class Dataset:#Dataset for data cleaning, designed for the model
    def __init__(self, tokenized_texts):
        self.tokenized_texts = tokenized_texts
    
    def __len__(self):
        return len(self.tokenized_texts["input_ids"])
    
    def __getitem__(self, idx):
        return {k: v[idx] for k, v in self.tokenized_texts.items()}

def clean(dataframe:pd.DataFrame):
    dataframe["comment"] = dataframe["comment"].astype(str)
    dataframe["comment"] = dataframe["comment"].apply(lambda x:re.sub(r'https?://\S+', '(link removed)', x))
    dataframe["clean_comment"] = dataframe["comment"].str.lower()
    dataframe.dropna(subset=['clean_comment'],inplace = True,how='any')
    emoji_pattern = re.compile("["
            u"\U0001F600-\U0001F64F"
            u"\U0001F300-\U0001F5FF"
            u"\U0001F680-\U0001F6FF"
            u"\U0001F1E0-\U0001F1FF"
                            "]+", flags=re.UNICODE)
    special_char = r'[\u2000-\u206F\u2E00-\u2E7F\'!"#$%&()*+,\-.\/:;<=>?@\[\]^_`{|}~]'
    #Diacritic
    dropID = []
    for index, row in dataframe.iterrows():
        match = re.search(r"[À-ž]+", row["clean_comment"])
        if match and len(match.group())/len(row["clean_comment"])>=0.05:
            dropID.append(index)
            print(match)
            print(row["clean_comment"])
    dataframe.drop(index=dropID,inplace=True)
    #Emoji
    dataframe["clean_comment"]=dataframe["clean_comment"].apply(lambda x:re.sub(pattern=emoji_pattern,string = x,repl=" "))
    #Links:
    dataframe["clean_comment"]=dataframe["clean_comment"].apply(lambda x:re.sub(r"http\S+", " ", x))
    #Special characters
    dataframe["clean_comment"]=dataframe["clean_comment"].apply(lambda x:re.sub(pattern=special_char, string = x,repl = " "))
    dataframe["clean_comment"]=dataframe["clean_comment"].apply(lambda x:' '.join(re.findall(r'\w+', x)))#Only joining characters
    #Single characters
    dataframe["clean_comment"]=dataframe["clean_comment"].apply(lambda x:re.sub(r'\s+[a-zA-Z]\s+', ' ', x))
    #Extra spaces that might occur in previous process
    dataframe["clean_comment"].replace(r'^\s*$', np.nan, regex=True, inplace=True)
    dataframe.dropna(subset=['clean_comment'],inplace = True,how='any')
    dropID = []
    for index, row in dataframe.iterrows():
        if re.search(r"[^a-zA-Z0-9À-ž\s]+", row["clean_comment"]):
            print(row["clean_comment"])
            dropID.append(index)
    dataframe.drop(index=dropID,inplace=True)
    

def tokenize(df):
    tokenized  = tokenizer(df["clean_comment"].tolist(),truncation=True,padding=True)
    return Dataset(tokenized)

def get_sent(df,dataset):
    predictions = trainer.predict(dataset)
    preds = predictions.predictions.argmax(-1)
    scores = (np.exp(predictions[0])/np.exp(predictions[0]).sum(-1,keepdims=True)).max(1)
    df["pred"] = preds
    df["senti_score"] = scores
    df["labels"] = df["pred"].map(model.config.id2label)

def sentiment_analysis(name:str):
    process = ""
    try:
        df = pd.read_csv(f"Data/comments/{name}.csv",delimiter="|",header=0,dtype=str,encoding="utf-8",lineterminator="\n",quoting=csv.QUOTE_NONE)
        if(len(df["comment"])==0):
            print("no comment for:"+ name)
        process = "clean"
        clean(df)
        process = "tokenize"
        tokenized = tokenize(df)
        process = "get_sent"
        get_sent(df,tokenized)
        df['comment'].replace('', np.nan, inplace=True)
        df['comment'].replace(' ', np.nan, inplace=True)
        df.dropna(subset=['comment'],inplace = True,how='any')
        df.drop_duplicates(subset=['comment'],inplace = True)
        df.drop(columns=["clean_comment"],inplace=True)
        df.to_csv(f'Data/result/{name}.csv', index=False)
        print(name +" complete")
    except Exception as e:
        print("exception")
        print(name)
        print(process)
        print(e)
        print()
    
