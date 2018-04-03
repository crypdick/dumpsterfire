from mrjob.job import MRJob
import datetime import datetime

class MRPotentialFires(MRJob):

    def mapper_init(self):
        """we made a list of articles that are dumpsters"""
        with open("results/dumpsters_list.txt", "r") as f:
            self.filtered_articles = set(f.readlines())

    def mapper(self, _, line):
        if "REVISION" in line[:8]:  # don't need to search whole line
            revision_pieces = line.split()
            article_id = revision_pieces[1]
            if article_id in self.filtered_articles:
                #revision_id = revision_pieces[2]
                # .date() throws out the hr-min-sec info
                date_time = datetime.strptime(revision_pieces[4]).date()
                editor_id = revision_pieces[6]
                yield((date_time, article_id), (editor_id, 1))

    def combiner(self, date_time_article, values):
        edit_counts = {}
        for (editor_id, edit_count) in values:
            edit_counts[editor_id] = edit_counts.get(editor_id, 0) + edit_count
        for editor_id, count in edit_counts.items():
            yield (date_time_article, (editor_id, count))

    def reducer(self, datetime_article, values):
        edit_counts = {}
        for (editor_id, edit_count) in values:
            # set default val to zero if key doesn't exist yet
            # this method has good time complexity
            edit_counts[editor_id] = edit_counts.get(editor_id, 0) + edit_count
        yield (datetime_article, edit_counts)

    def reducer_final(self, datetime_article, edit_counts):
        # filter for editors who made at least 4 edits in a day in this article
        filtered_dict = {k: v for k, v in edit_counts.items() if v >= 4}
        # if at least 2 editors made at least 4 edits
        if len(filtered_dict) >= 2:
            date_time, article_id = datetime_article
            # final output is a list of article_ids, with each one having a list
            # of dates which we want to grab all revision comments
            yield (article_id, datetime)

if __name__ == "__main__":
    MRPotentialFires.run()
