from mrjob.job import MRJob
import re

def findWholeWord(w):
    return re.compile(r'\b({0})\b'.format(w), flags=re.IGNORECASE).search

class MRInitialProcess(MRJob):
    def mapper(self, _, line):
        try:
            word = line.split()[0]
            yield word, 1
        except Exception as e:
            pass

    def reducer(self, cursed_word, cases):
        total = 0
        for case in cases:
            total += case
        yield cursed_word, total

if __name__ == "__main__":
    MRInitialProcess.run()
