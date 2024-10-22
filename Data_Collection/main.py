from scraper import *
import csv
import time
import random
import os
from sentiment_analysis_Roberta import sentiment_analysis
import pandas as pd
api = youtubeAPI(DEVELOPER_KEY="")
print("authorized")
playlistId = ""
response = api.get_videos(playlistid=playlistId,max_result=350)

print(response)

sample = api.request_details(response)
keys = sample[0].keys()
print(sample)
test_sample = open("sample.csv", 'w')
writer = csv.DictWriter(test_sample,fieldnames=keys)
writer.writeheader()
for row in sample:
    writer.writerow(row)

for vid in sample:
    time.sleep(random.randrange(1,10)/100)
    api.get_comments(vid=vid["vid"],max_result=10000)
    
selected = []
file = open('sample.csv', 'r')
reader = csv.DictReader(file)
for row in reader:
    selected.append(row["vid"])

results = os.listdir("Data/result")
process = []
completed = [os.path.splitext(video)[0] for video in results]
for vid in selected:
    if vid not in completed:
        process.append(vid)
        sentiment_analysis(vid)
    else:
        print(f"{vid} already completed")
        
        
print(process)