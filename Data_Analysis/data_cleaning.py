import pandas as pd
import os

results = os.listdir("Data/result")
samples = pd.read_csv("sample.csv",header=0,index_col=0)

result = []
for i in results:
    try:
        df = pd.read_csv("Data/result/"+i,header=0,dtype=str,lineterminator="\n")
        id = os.path.splitext(i)[0]
        sample = samples.loc[id]
        sent = df['labels'].value_counts().reindex(['positive','negative','neutral'], fill_value=0)
        result.append([id,sample["title"],sample["publish"],sample["views"],sent["positive"],sent["negative"],sent['neutral']])
    except Exception as e:
        print(i)
        print(e)
df = pd.DataFrame(result,columns = ["vid","title","publish","views","pos_count","neg_count",'neutral_count'])
df.to_csv('Data/_Summary.csv')