from rutermextract import TermExtractor

class analyzer():
    def __init__(self, text, label):
        self.nested = label
        self.text = text

        self.term_extractor = TermExtractor()

    def analyze(self):
        keywords = list()
        for term in self.term_extractor(self.text, nested=self.nested):
            keyword = list()
            temp = ''
            i = 1
            for word in term.words:
                temp += str(word)
                if i < len(term.words): temp += ' '
                i += 1
            keyword.append(term.count)
            keyword.append(term.normalized)
            keyword.append(temp)

            keywords.append(keyword)

        return keywords