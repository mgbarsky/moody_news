class Result():

    def __init__(self, title="", url="", score=0.0):
        self.title = title
        self.url = url
        self.hour = score
        self.dictionary = {}

    def getTitle(self):
        return self.title

    def getUrl(self):
        return self.url

    def getScore(self):
        self.score = 0.0
        for w in self.dictionary:
            self.score += self.dictionary [w]
        return self.score

    def setTitle(self, title):
        self.title = title

    def setUrl(self, url):
        self.url = url

    def setScore(self, score):
        self.score = score

    def addDictionary (self, key, val):
        if key not in self.dictionary:
            self.dictionary[key] = val
        else:
            self.dictionary[key] += val

    def __str__(self):
        return "%s: score:%f" % (self.title, self.score)

    def __repr__(self):
        return (str(self))