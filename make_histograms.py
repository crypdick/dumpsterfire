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
    
plt.hist(edits, range = [1,100], bins = 150)
plt.ylabel('Number of edits')
plt.savefig('edits_histogram.png')

plt.scatter(edits, editors)
plt.savefig("edits_vs_editors_scatter.png")

# PDFs and CDFs to pick cut-offs
edits = np.array(edits)
editors = np.array(editors)

# if binwidth = 1 then density plot will also be a PDF
edits_bins = np.arange(np.floor(edits.min()), np.ceil(edits.max()))
editors_bins = np.arange(np.floor(editors.min()), np.ceil(editors.max()))

edit_probabilities, _ = np.histogram(edits, bins=edits_bins, density=True)
editor_probabilities, _ = np.histogram(editors, bins=editors_bins, density=True)

fig, ((ax1, ax3), (ax2, ax4)) = plt.subplots(nrows=2, ncols=2, sharex=True, figsize=(8,4))
edits_widths = edits_bins[:-1] - edits_bins[1:]
ax1.bar(edits_bins[1:], edit_probabilities, width=edits_widths)
ax2.bar(edits_bins[1:], edit_probabilities.cumsum(), width=edits_widths)

editor_widths = editors_bins[:-1] - editors_bins[1:]
ax3.bar(editors_bins[1:], editor_probabilities, width=editor_widths)
ax4.bar(editors_bins[1:], editor_probabilities.cumsum(), width=editor_widths)

ax1.set_ylabel('PDFs')
ax3.set_ylabel('CDFs')
ax3.set_xlabel('Edits')
ax4.set_xlabel('Editors')
fig.tight_layout()
plt.savefig("edits_editors_pdfcdf.png")
