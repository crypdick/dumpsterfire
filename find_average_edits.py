#"481606"	[34, 15]
#"4816064"	[1, 1]
#"4816074"	[24, 16]
#"481608"	[45, 31]
#"481609"	[318, 113]
# above is what the file looks like 
import re

editors = 0
edits = 0
count = 0 
with open("results/job1_output.txt") as f:
	articles = f.readlines()
	for article in articles:
		pieces = article.split()
		clean_pieces = [re.sub('\W+', '', string) for string in pieces]
		count +=1
		editors += float(clean_pieces[2])
		edits += float(clean_pieces[1])
	print("\nProcessing Complete\n")
	average_editors = editors/count
	average_edits = edits/count


	
