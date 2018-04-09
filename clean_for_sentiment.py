import csv

fname = "results/sample_dumpsterfires.out"
clean_lines = []
nonempty_lines = []
final_analysis = []
with open(fname) as f:
    content = f.readlines()
    for line in content:
        clean_lines.append(line.split('"')[1::2]) # the [1::2] is a slicing which extracts odd values
    for line in clean_lines:
        if not line[1]:
            pass # comment is empty
        else:
            nonempty_lines.append( (line[0], ''.join(line[1:]) ))
    for date, comment in nonempty_lines:
        article_id, date = date.split(',')[1], date.split(',')[0]
        final_analysis.append( (article_id, date, comment) )
with open('results/dumpsterfire_out.clean.csv','w') as out:
    csv_out=csv.writer(out)
    csv_out.writerow(['id','date', 'comment'])
    for row in final_analysis:
        csv_out.writerow(row)
