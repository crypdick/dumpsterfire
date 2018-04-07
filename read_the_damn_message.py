from mrjob.job import MRJob
import re

def findWholeWord(w):
    return re.compile(r'\b({0})\b'.format(w), flags=re.IGNORECASE).search

class MRInitialProcess(MRJob):
	def mapper(self, _, line):
		try:
			if line[0:7] == "COMMENT":
				comment = line.lower()
				comment = comment.split(' ', 1)[1]
				#everything after COMMENT
				# if (findWholeWord('rant')(comment)) is not None:
				# 	yield 'rant', comment
				if (findWholeWord('canon')(comment)) is not None:
					yield 'canon', comment
				# if (findWholeWord('opinion')(comment)) is not None:
				# 	yield 'opinion', comment
				# if (findWholeWord('damn')(comment)) is not None:
				# 	yield 'damn', comment
				# if (findWholeWord('npov')(comment)) is not None:
				# 	yield 'npov', comment
		except Exception as e:
			pass

	def reducer(self, cursed_word, comments):
		for comment in comments:
			yield cursed_word, comment

if __name__ == "__main__":
	MRInitialProcess.run()
