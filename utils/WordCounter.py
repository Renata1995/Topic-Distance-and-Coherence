class WordCounter:
    def countWords(self, corpus, key):
        totalFrequency = 0
        for doc in corpus:
            for word in doc:
                if word[0] == key:
                    totalFrequency += word[1]
        return totalFrequency

    def totalWords(self, corpus):
        total = 0
        for doc in corpus:
            total += sum([w[1] for w in doc])
        return total

    def countWords2(self, token_list, key):
        return token_list.count(key)

    def countWords3(self, corpus, key):
        totalFrequency = 0
        for doc in corpus:
            if key in doc.keys():
                totalFrequency += doc[key]
        return totalFrequency
