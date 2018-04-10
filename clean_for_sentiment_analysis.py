import csv
fname = "results/DUMPSTERFIRE_COMMENTS.txt"

empty = 0
good = 0
good_lines = []
with open(fname) as f:
    content = f.readlines()
    for line in content:
        stuff = (line.split()[1:])
        stuff = ' '.join(stuff)
        stuff = stuff.replace("\\t", " ")
        stuff = stuff.split()[2:]
        stuff = ' '.join(stuff)
        if stuff == '"':
            empty +=1
        elif stuff[-3:] == '*/"':
            empty +=1
        else:
            if "*/" in stuff:
                stuff = stuff.split('*/')[1]
            if "BOT" in stuff or "minor change" in stuff or "Revert to revision" in stuff:
                pass
            else:
                good_lines.append(stuff)

for line in good_lines:
    print(line)
