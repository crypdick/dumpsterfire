from mrjob.job import MRJob

class MRInitialProcess(MRJob):

	def mapper(self, _, line):
	    
		num_bad_formatted_lines = 0

	    	# We only care about Revision lines
		if line[0:8] == "REVISION":

			revision_pieces = line.split()
			
			try:
				article_id = revision_pieces[1]
				#revision_id = revision_pieces[2]
				#articale_title = revision_pieces[3]
				#timestamp = revision_pieces[4]
				#editor = revision_pieces[5]
				editor_id = revision_pieces[6]
				
				yield article_id, editor_id

			except IndexError as e:
				print(e)


	def reducer(self, article_id, values):
		edit_count = 0
		unique_editor_ids = set()

		for editor_id in values:
			edit_count += 1
			
			if editor_id not in unique_editor_ids:
			    unique_editor_ids.add(editor_id)

		yield article_id, (edit_count, len(unique_editor_ids))

if __name__ == "__main__":
	MRInitialProcess.run()
