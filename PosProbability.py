class PosPosProbability:
    def __init__(self, previewTag, nextTag, probability=0, count=1):
        self.nextTag = nextTag
        self.previewTag = previewTag
        self.probability = probability
        self.count = count # imposto a 1 per evitare una probabilità di 0!

    def set_probability(self, probability):
        self.probability = probability

    def __str__(self):
        return self.previewTag + ' --> ' + self.nextTag + '; probability: ' + str(self.probability) + '; count: ' + \
               str(self.count)


class PosWordProbability:
    def __init__(self, word, tag, probability=0, count=1):
        self.word = word
        self.tag = tag
        self.probability = probability
        self.count = count # imposto a 1 per evitare una probabilità di 0!

    def set_probability(self, probability):
        self.probability = probability

    def __str__(self):
        return self.word + ' --> ' + self.tag + '; probability: ' + str(self.probability) + '; count: ' + \
               str(self.count)
