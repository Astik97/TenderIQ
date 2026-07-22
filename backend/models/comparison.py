class Comparison:

    def __init__(self,tender1,tender2,similarity,report):

        self.tender1 = tender1

        self.tender2 = tender2

        self.similarity = similarity

        self.report = report

    def __repr__(self):

        return f"Comparison({self.similarity}%)"