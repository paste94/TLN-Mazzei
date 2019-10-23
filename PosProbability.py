class PosProbability:
    def __init__(self, previewTag, tag, probability=0):
        self.tag = tag
        self.previewTag = previewTag
        self.probability = probability

    def set_probability(self, probability):
        self.probability = probability

    def __str__(self):
        return self.previewTag + ' --> ' + self.tag + '; probability: ' + str(self.probability)
