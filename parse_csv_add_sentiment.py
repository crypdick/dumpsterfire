import json
from watson_developer_cloud import ToneAnalyzerV3

tone_analyzer = ToneAnalyzerV3(
    version ='2017-09-21',
    username ='02527f80-5bbe-43fd-8fca-068c7eb9e929',
    password ='ASK_SHANE'
)

text = 'Team, I know that times are tough! Product sales have been disappointing for the past three quarters. We have a competitive product, but we need to do a better job of selling it!'
content_type = 'application/json'

tone = tone_analyzer.tone({"text": text},content_type)


print(tone['document_tone']['tones'])