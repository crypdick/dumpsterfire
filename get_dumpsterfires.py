# zcat ../enwiki-20080103.good.gz |  python3.6 test.py -r local --conf-path mrjob.conf  > fullfire.out && holla
from mrjob.job import MRJob
from mrjob.step import MRStep
from datetime import datetime
import dateutil.parser

class MRGrabDumpsterFires(MRJob):

    def mapper_init(self):
        """we made a list of articles that are dumpsters"""
        fname = "/home/shit/bin/ds_shit/distributed/dumpsterfire/results/toy_dumpsterfire.out"
        with open(fname, "r") as f:
            """
            example output from previous job:

            " "	"('2001-10-04', '649')"
            " "	"('2001-11-17', '632')"
            " "	"('2002-01-05', '652')"
            " "	"('2002-01-25', '652')"
            " "	"('2002-02-02', '615')"
            """
            self.articleID_dates = {}
            for line in f.readlines():
                date_str, article_id = line.replace('"', '') \
                                             .replace("'","") \
                                             .replace('(', '') \
                                             .replace(')','') \
                                             .split(',')
                if article_id in self.articleID_dates:
                    self.articleID_dates[article_id].append(date_str)
                else:
                   self.articleID_dates[article_id] = [date_str]

            # FIXME delete later
            # manual injection of Anarchism articles for testing purposes
            self.articleID_dates["12"] = ["2002-10-02", "2002-09-09", "2002-12-11",
                                               "2002-10-28", "2002-10-03"]

    def mapper(self, _, line):
        """note: if we wanted to get better results, I think we shouldn't use midnight as the delimiter between days
        my guess is that the minimum of edits is sometime around 5am GMT.
        to figure this out, for each revision we should just output what hr of the day it was made and plot a histogram
        """
        revision_pieces = line.split("")
        """
        index 0
        "REVISION 12 1906487 Anarchism 2003-12-08T20:18:19Z Sam_Francis 6103"
        index 10
        "COMMENT Anyone who opposes government on principle is considered an anarchist."	""
        """
        # remove the leading 8 chars and strip decorations
        revision_info = revision_pieces[0][8:].replace('"', '').strip().split()
        article_id, datetimez = revision_info[0], revision_info[3]
        # TODO get more data from revision info?
        # if article_id in self.articleID_dates:
        if True:  # FIXME remove in production
            date = str(dateutil.parser.parse(datetimez).date())
            # if date in self.articleID_dates[article_id]:
            if True:  # FIXME remove in production
                # get comments
                # remove leading 7 chars
                comments = revision_pieces[10][7:]
                # TODO: what data do we want? do we want human-readable article title?
                # timestamps? editor ids?
                yield (article_id, (datetimez, comments))

    def reducer(self, key, values):
        for v in values:
            yield (key, v)


if __name__ == "__main__":
    MRGrabDumpsterFires.run()

