from mrjob.job import MRJob

class MRInitialProcess(MRJob):

	def mapper(self, _, line):
		if "REVISION" in line:
			revision_pieces = line.split()
			article_id = revision_pieces[1]
			revision_id = revision_pieces[2]
			editor = revision_pieces[6]
			yield(article_id, (revision_id, editor))

	def reducer(self, article, metadata):
		edit_count = 0
		for metadatum in metadata:
			edit_count += 1
		yield(article, edit_count)

if __name__ == "__main__":
	MRInitialProcess.run()
