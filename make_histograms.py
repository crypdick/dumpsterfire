import re
import matplotlib.pyplot as plt
import numpy as np

article_ids = []
editors = []
edits = []

with open("results/job1_output.txt") as f:
    articles = f.readlines()
    for article in articles:
        pieces = article.split()
        clean_pieces = [re.sub('\W+', '', string) for string in pieces]
        editors.append( float(clean_pieces[2]))
        edits.append( float(clean_pieces[1]))
        article_ids.append(int(clean_pieces[0]))

# plt.hist(edits, range = [1,100], bins = 150)
# plt.ylabel('Number of edits')
# plt.yscale('log')
# plt.savefig('edits_histogram.png')
# plt.close()
#
# plt.scatter(edits, editors)
# plt.xscale('log')
# plt.yscale('log')
# plt.savefig("edits_vs_editors_scatter.png")
# plt.close()

# PDFs and CDFs to pick cut-offs
edits_orig = np.array(edits)
first_filter = (edits_orig>20) & (edits_orig < 1000)
edits = edits_orig[first_filter]

editors_orig = np.array(editors)
editors = editors_orig[first_filter]
second_filter = (editors>10) & (editors<100)
editors = editors[second_filter]
# go back to filter edits
edits = edits[second_filter]

print("array shapes", np.shape(editors_orig), np.shape(edits_orig))

# do same for article_ids, this will be important later
#article_ids = article_ids[first_filter][second_filter]

# # if binwidth = 1 then density plot will also be a PDF
# edits_bins = np.arange(np.floor(edits.min()), np.ceil(edits.max()))
# editors_bins = np.arange(np.floor(editors.min()), np.ceil(editors.max()))
#
# # commenting out this method. It works, but the PDFs are invisible because there
# # are too many bins
# edit_probabilities, _ = np.histogram(edits, bins=edits_bins, density=True)
# editor_probabilities, _ = np.histogram(editors, bins=editors_bins, density=True)

# method 2, with wider bins
edit_density, edits_bins = np.histogram(edits, bins=500, density=True)
edit_density, edits_bins = edit_density, edits_bins
edit_probabilities = edit_density/edit_density.sum()
edit_cdf = edit_probabilities.cumsum()

editor_density, editors_bins = np.histogram(editors, bins=500, density=True)
editor_density, editors_bins = editor_density, editors_bins  # exclude if not at least 10 editors
editor_probabilities = editor_density/editor_density.sum()
editor_cdf = edit_probabilities.cumsum()

# print(editors_bins)
# print(edits_bins)

def find_critical_value(arr, bins, percentage=0.05):
    # iterator = np.nditer(arr)
    # while not iterator.finished:
    for i, x in enumerate(arr):
        if x > percentage:
            print("percentage surpassed at {}%, index {}, value {}".format(x, i, bins[i]))
            print("previous val at index {} was {}% {}".format(i-1, arr[i-1], bins[i-1]))
            print("next stop at {}%, index {}, value {}".format(arr[i+1], i+1, bins[i+1]))
            return bins[i]

# print(find_critical_value(edit_cdf, edits_bins))
# print(find_critical_value(editor_cdf, editors_bins))

# fig, ((ax1, ax3), (ax2, ax4)) = plt.subplots(nrows=2, ncols=2, sharex=False, figsize=(8,4))
# edits_widths = edits_bins[:-1] - edits_bins[1:]
# ax1.bar(edits_bins[1:], edit_probabilities, width=edits_widths)
# ax2.bar(edits_bins[1:], edit_probabilities.cumsum(), width=edits_widths)
#
# editor_widths = editors_bins[:-1] - editors_bins[1:]
# ax3.bar(editors_bins[1:], editor_probabilities, width=editor_widths)
# ax4.bar(editors_bins[1:], editor_probabilities.cumsum(), width=editor_widths)
#
# ax1.set_ylabel('PDFs')
# ax2.set_ylabel('CDFs')
# ax2.set_xlabel('Edits')
# ax4.set_xlabel('Editors')
# fig.tight_layout()
# plt.savefig("edits_editors_pdfcdf.png")
#

# based on the graphs, the long tails begin at about 200 edits and 100 editors
# we will filter articles based on that.
dumpsters = np.array(article_ids)[(edits_orig < 200) & (editors_orig < 100)]
#print("dumpsters", dumpsters)
np.savetxt('dumpsters_list.txt', dumpsters)