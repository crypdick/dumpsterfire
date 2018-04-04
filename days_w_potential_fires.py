from mrjob.job import MRJob
from mrjob.step import MRStep
from datetime import datetime
import dateutil.parser
import sys


class MRPotentialFires(MRJob):

    def mapper_init(self):
        """we made a list of articles that are dumpsters"""
        with open(
                "/home/richard2/Akamai_scratch/team_shane_noah_richard_roger_youngkeun/results/dumpsters_list.txt",
                "r") as f:
            self.filtered_articles = set(str(f.readlines()))

    def mapper(self, _, line):
        if "REVISION" in line[:8]:  # don't need to search whole line
            revision_pieces = line.split()
            article_id = revision_pieces[1]
            # prefilter for articles we've whitelisted
            # yield (article_id, article_id in self.filtered_articles)
            if article_id in self.filtered_articles:
                # revision_id = revision_pieces[2]
                # .date() throws out the hr-min-sec info
                date = str(dateutil.parser.parse(revision_pieces[4]).date())
                editor_id = revision_pieces[6]
                date_article = str((date, article_id))
                yield (date_article, (editor_id, 1))

    def combiner(self, date_article, values):
        edit_counts = {}
        for (editor_id, edit_count) in values:
            edit_counts[editor_id] = edit_counts.get(editor_id, 0) + edit_count
        for editor_id, count in edit_counts.items():
            yield (date_article, (editor_id, count))

    def reducer(self, date_article, values):
        # my_d = {}
        # for v in values:
        #    my_d[str(datetime_article)] = v
        # yield (str(datetime_article), str(my_d))
        edit_counts = {}
        for (editor_id, edit_count) in values:
            # set default val to zero if key doesn't exist yet
            # this method has good time complexity
            edit_counts[editor_id] = edit_counts.get(editor_id, 0) + edit_count
        for editor_id, counts in edit_counts.items():
            yield (date_article, (editor_id, counts))

    def reducer_select_w_4more_edits(self, date_article, edit_counts):
        # filter for editors who made at least 4 edits in a day in this article
        candidates = []
        for editor_id, counts in edit_counts:
            if counts >= 4:
                candidates.append(editor_id)
        # if at least 2 editors made at least 4 edits
        if len(candidates) >= 2:
            # final output is a list of article_ids, with each one having a list
            # of dates which we want to grab all revision comments
            yield (None, date_article)

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