# bzcat ../enwiki-20080103.main.bz2 |split --lines=900000 --verbose --numeric-suffixes 
FILES=/Akamai_scratch/richard/*
fire_script=/Akamai_scratch/team_shane_noah_richard_roger_youngkeun/mini_fires.py
for f in $FILES; do
     echo "$f started"
     (python3.6 $fire_script -r local --conf-path mrjob.conf $f >> /Akamai/dumpsterfire_datearticles.out) 
     echo "$f completed"
     rm -r $f
 done