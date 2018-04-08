# zcat ../enwiki-20080103.good.gz |  python3.6 test.py -r local --conf-path mrjob.conf  > fullfire.out && holla
from mrjob.job import MRJob
from mrjob.step import MRStep
from datetime import datetime
import dateutil.parser


class MRGrabDumpsterFires(MRJob):

    def mapper_init(self):
        """we made a list of articles that are dumpsters"""
        fname = "/Akamai_scratch/team_shane_noah_richard_roger_youngkeun/results/dumpsterfire_datearticles.out.clean"
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
                sentence =  line.replace('"', '') \
                    .replace("'", "") \
                    .replace('(', '') \
                    .replace(')', '')
                sentence = ''.join(sentence.split()) # removes every kind of whitespace
                date_str, article_id = sentence.split(',')
                if article_id in self.articleID_dates:
                    self.articleID_dates[article_id].append(date_str)
                else:
                    self.articleID_dates[article_id] = [date_str]

            # FIXME delete later
            # manual injection of Anarchism articles for testing purposes
            #self.articleID_dates["12"] = ["2002-10-02", "2002-09-09",
            #                              "2002-12-11",
            #                              "2002-10-28", "2002-10-03"]

    def mapper(self, _, line):
        revision_pieces = line.split("")
        """
        index 0
        "REVISION 12 1906487 Anarchism 2003-12-08T20:18:19Z Sam_Francis 6103"
        index 10
        "COMMENT Anyone who opposes government on principle is considered an anarchist."	""
        """
        # remove the leading 8 chars and strip decorations
        revision_info = revision_pieces[0][8:].replace('"', '').strip().split()
        article_id = revision_info[0]

        # TODO get more data from revision info?
        if article_id in self.articleID_dates:
            # if True:  # FIXME remove in production
            datetimez = revision_info[3]
            date = str(dateutil.parser.parse(datetimez).date())
            if date in self.articleID_dates[article_id]:
                # if True:  # FIXME remove in production
                article_title = revision_info[2]
                editor_username = revision_info[4]
                editor_id = revision_info[5]
                # get comments
                # remove leading 7 chars
                comment = revision_pieces[10][7:]
                key_str = "\t".join((article_id, article_title, date))
                val_string = "\t".join((editor_username, editor_id, comment))
                yield (key_str, val_string)

    def reducer(self, key, values):
        for v in values:
            yield (key, v)


if __name__ == "__main__":
    MRGrabDumpsterFires.run()
