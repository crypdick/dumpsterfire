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
                date_time = datetime.strptime(revision_pieces[4])
		    	editor = revision_pieces[6]
		    	yield(date_time, (editor, 1))

	def reducer(self, article, metadata):

		edit_count = 0
		for metadatum in metadata:
			edit_count += 1
		yield(article, edit_count)

if __name__ == "__main__":
	MRPotentialFires.run()
