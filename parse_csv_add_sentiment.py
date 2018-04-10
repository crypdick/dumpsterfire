import json
from watson_developer_cloud import ToneAnalyzerV3
import csv

tone_analyzer = ToneAnalyzerV3(
    version ='2017-09-21',
    username ='cca4c744-6896-4249-9e09-bfec01c1ce7f',
    password ='Uir2RkbAayXO'
)
content_type = 'application/json'

cursed_dict = {}
with open('samples_for_SA/cursed_words_sentiment_analysis.csv', 'r') as csvfile:
    cursedreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in cursedreader:
        key = row[1].strip('"')
        value = ''.join(row[2:]).strip('"')
        value = value.replace("/*", "")
        value = value.replace("*/", "")
        if key in cursed_dict:
            cursed_dict[key].append(value)
        else:
            cursed_dict[key] = [value]
for curse in cursed_dict['canon']:
    print(curse)
 


#text = 'Team, I know that times are tough! Product sales have been disappointing for the past three quarters. We have a competitive product, but we need to do a better job of selling it!'
#tone = tone_analyzer.tone({"text": text},content_type)
#print(tone['document_tone']['tones'])