from mrjob.job import MRJob
import datetime import datetime

class MRPotentialFires(MRJob):

	def mapper_init(self):
        with open("results/dumpsters_list.txt", "r") as f:
            self.filtered_articles = set(f.readlines())

	def mapper(self, _, line):
		if "REVISION" in line[:8]:  # don't need to search whole line
			revision_pieces = line.split()
			article_id = revision_pieces[1]
			if article_id in self.filtered_articles:
		    	#revision_id = revision_pieces[2]
                date_time = datetime.strptime(revision_pieces[4]).date()
		    	editor = revision_pieces[6]
		    	yield(date_time, (editor, 1))

    def combiner(self, date_time, values):
        edit_counts = {}
        for (editor_id, edit_count) in values:
            edit_counts[editor_id] = edit_counts.get(editor_id, 0) + edit_count
        for id, count in edit_counts.items():
            yield (date_time, id, count)

	def reducer(self, date, values):
        edit_counts = {}
        for (editor_id, edit_count) in values:
            # set default val to zero if key doesn't exist yet
            # this method has good time complexity
            edit_counts[editor_id] = edit_counts.get(editor_id, 0) + edit_count
		yield(date, edit_counts)

    def reducer_final(self, date, edit_counts):
        pass

if __name__ == "__main__":
	MRPotentialFires.run()
