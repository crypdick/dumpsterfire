#"481606"	[34, 15]
#"4816064"	[1, 1]
#"4816074"	[24, 16]
#"481608"	[45, 31]
#"481609"	[318, 113]
# above is what the file looks like 
import re
import statistics

editors = []
edits = []

with open("results/job1_output.txt") as f:
	articles = f.readlines()
	for article in articles:
		pieces = article.split()
		clean_pieces = [re.sub('\W+', '', string) for string in pieces]
		editors.append( float(clean_pieces[2]))
		edits.append( float(clean_pieces[1]))
	print("\nProcessing Complete\n")
	editors_med = statistics.median(editors)
	edits_med = statistics.median(edits)
	print("Median number of unique editors is " + str(editors_med))
	print("Median number of edits is " + str(edits_med)) 
	
