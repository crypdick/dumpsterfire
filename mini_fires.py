# zcat ../enwiki-20080103.good.gz |  python3.6 test.py -r local --conf-path mrjob.conf  > fullfire.out && holla
from mrjob.job import MRJob
from mrjob.step import MRStep
from datetime import datetime
import dateutil.parser
import sys

class MRPotentialFires(MRJob):

    def mapper_init(self):
        """we made a list of articles that are dumpsters"""
        fname = "/Akamai_scratch/team_shane_noah_richard_roger_youngkeun/results/dumpsters_list.txt"
        with open(fname, "r") as f:
            self.filtered_articles = set(str(line.strip()) for line in f)
        # TODO FIXME remove after done with testing
        self.filtered_articles.add("6")
        self.filtered_articles.add("8")

    def mapper(self, _, line):
        """note: if we wanted to get better results, I think we shouldn't use midnight as the delimiter between days
        my guess is that the minimum of edits is sometime around 5am GMT.
        to figure this out, for each revision we should just output what hr of the day it was made and plot a histogram
        """
        if "REVISION" in line[:8]:  # don't need to search whole line
            revision_pieces = line.split()
            article_id = revision_pieces[1]
            # prefilter for articles we've whitelisted
            if article_id in self.filtered_articles:
                # #revision_id = revision_pieces[2]
                # # .date() throws out the hr-min-sec info
                # # can't use date as key so need to stringify first
                try:
                    date = str(dateutil.parser.parse(revision_pieces[4]).date())
                    editor_id = revision_pieces[6]
                    # put date first bc article_id is variable length, this way 
                    # it's easier to string split later
                    date_article = str((date, article_id))
                    yield ("THIS IS A TEST", ("ROGERYOLO420", 1))
                    yield ("THIS IS A TEST", ("NOAH_TEH_GANGSTAxoxo6969", 1))
                    yield (date_article, (editor_id, 1))
                except:  # there is strange fuckery in our dataset
                    with open('failures.log', 'a') as fail_log:
                        fail_log.write(str(line)+'\n')
                    pass

    def combiner(self, date_article, values):
        edit_counts = {}
        for (editor_id, edit_count) in values:
            edit_counts[editor_id] = edit_counts.get(editor_id, 0) + edit_count
        # MRjob can't pass full dictionaries (not serializable) so we gotta extract items
        try:
            for editor_id, count in edit_counts.items():
                yield (date_article, (editor_id, count))
        except:  # TODO figure out what is causing JSONDecodeError
            pass

    def reducer(self, date_article, values):
        # for v in values:
        #     yield (date_article, v)
        edit_counts = {}
        for (editor_id, edit_count) in values:
            # set default val to zero if key doesn't exist yet
            # this method has good time complexity
            edit_counts[editor_id] = edit_counts.get(editor_id, 0) + edit_count
        for editor_id, counts in edit_counts.items():
            if counts >= 4:
                yield (date_article, (editor_id, counts))

    def reducer_select_w_4more_edits(self, date_article, edit_counts):
        # filter for editors who made at least 4 edits in a day in this article
        candidates = []
        for editor_id, counts in edit_counts:
            candidates.append(editor_id)
        # if at least 2 editors made at least 4 edits apiece
        if len(candidates) >= 2:
            # final output is a list of article_ids, with each one having a list
            # of dates which we want to grab all revision comments
            # using space as key to make it easier to strip out crud later
            yield (" ", date_article)


    def steps(self):
        return [
            MRStep(mapper_init=self.mapper_init,
                   mapper=self.mapper,
                   combiner=self.combiner,
                   reducer=self.reducer),
            MRStep(reducer=self.reducer_select_w_4more_edits)
        ]


if __name__ == "__main__":
    MRPotentialFires.run()

