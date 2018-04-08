from mrjob.job import MRJob

class MRInitialProcess(MRJob):
    def mapper(self, _, line):
        try:
            if line[0:7] == "COMMENT":
                yield 'count', 1
        except Exception as e:
            pass

    def reducer(self, count, comments):
        count = 0
        for comment in comments:
            count +=1
        yield 'total article count:', count

if __name__ == "__main__":
    MRInitialProcess.run()
