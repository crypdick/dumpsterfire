import json
from watson_developer_cloud import ToneAnalyzerV3
import csv

#{'document_tone': {'tones': [{'score': 0.699501, 'tone_id': 'anger', 'tone_name': 'Anger'}]}}
tone_analyzer = ToneAnalyzerV3(
    version ='2017-09-21',
    username ='7dc69397-4b99-4dd0-aba3-45ba6756a7e0',
    password ='UGPpv3Iw4NPj'
)
content_type = 'application/json'

dope_lines = []
csv_lines = []

with open('results/DUMPSTERFIRE_clean.txt', 'r') as f:
    content = f.readlines()
    for line in content:
        dope_lines.append(line)

for i in range(2500):
    text = dope_lines[i]
    tone = tone_analyzer.tone({"text": text},content_type)
    print(tone)
    for val in tone['document_tone']['tones']:
        anger = 0.0
        if val['tone_id'] == 'anger':
            anger = val['score']
    csv_lines.append([text, anger])



tone_analyzer = ToneAnalyzerV3(
    version ='2017-09-21',
    username ='adeb7ac5-a163-449d-96fe-9fa28b2dbad1',
    password ="hpiPFCTkDvPo"
)
for i in range(2500, 3437):
    text = dope_lines[i]
    tone = tone_analyzer.tone({"text": text},content_type)
    print(tone)
    for val in tone['document_tone']['tones']:
        anger = 0.0
        if val['tone_id'] == 'anger':
            anger = val['score']
    csv_lines.append([text, anger])

with open("dumpster_fire_sentiment.csv", "w") as f:
    writer = csv.writer(f)
    writer.writerows(csv_lines)



#text = 'Team, I know that times are tough! Product sales have been disappointing for the past three quarters. We have a competitive product, but we need to do a better job of selling it!'
#tone = tone_analyzer.tone({"text": text},content_type)
#print(tone['document_tone']['tones'])