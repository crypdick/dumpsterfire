import re
import statistics
import matplotlib.pyplot as plt
import numpy as np

editors = []
edits = []

with open("results/job1_output.txt") as f:
    articles = f.readlines()
    for article in articles:
        pieces = article.split()
        clean_pieces = [re.sub('\W+', '', string) for string in pieces]
        editors.append( float(clean_pieces[2]))
        edits.append( float(clean_pieces[1]))
    plt.hist(editors, range=[1, 100], bins=150)
    plt.ylabel('Number of unique editors')
    plt.savefig('editor_histogram.png')
    
    plt.hist(edits, range = [1,100], bins = 150)
    plt.ylabel('Number of edits')
    plt.savefig('edits_histogram.png')
    
