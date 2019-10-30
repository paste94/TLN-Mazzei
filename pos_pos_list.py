import numpy as np


class PosPosProbList:
    lst = []

    def __init__(self, tags_map, sentences):
        self.tags_map = tags_map
        self.sentences = sentences
        self.lst = self.pos_pos_probability()

    def __str__(self):
        s = ''
        for elem in self.lst:
            s += str(elem)
            s += '\n'
        return s

    def pos_pos_probability(self):
        posProbabilityList = []
        for tag1 in self.tags_map.keys():
            for tag2 in self.tags_map.keys():
                posProbabilityList.append(PosPosProbability(tag1, tag2))

        # Conta le occorrenze delle coppie POS -> POS
        for phrase in self.sentences:
            start_pos = self.find_pos_pos_position(
                    "START",
                    phrase[0]['upostag'],
                    posProbabilityList
                )
            posProbabilityList[start_pos].count += 1

            for i in range(1, len(phrase)):
                position = self.find_pos_pos_position(
                    phrase[i - 1]['upostag'],
                    phrase[i]['upostag'],
                    posProbabilityList
                )
                posProbabilityList[position].count += 1

            end_pos = self.find_pos_pos_position(
                phrase[len(phrase)-1]['upostag'],
                "END",
                posProbabilityList
            )
            posProbabilityList[end_pos].count += 1

        # Imposta le percentuali
        for elem in posProbabilityList:
            if self.tags_map[elem.previewTag] == 0:
                elem.probability = 1
            else:
                #print(elem.previewTag, ' --> ', elem.nextTag, ' = ', elem.count, ' / ', self.tags_map[elem.previewTag])
                elem.probability = 1+(elem.count / self.tags_map[elem.previewTag])

        return posProbabilityList


    @staticmethod
    def find_pos_pos_position(tag1, tag2, lst):
        for i in range(0, len(lst)):
            if lst[i].previewTag == tag1 and lst[i].nextTag == tag2:
                return i

    def P(self, prevTag, nextTag):
        for elem in self.lst:
            if elem.previewTag == prevTag and elem.nextTag == nextTag:
                return 1+elem.probability


class PosPosProbability:
    def __init__(self, previewTag, nextTag, probability=0, count=0):
        self.nextTag = nextTag
        self.previewTag = previewTag
        self.probability = probability
        # imposto a 1 per evitare una probabilità di 0!
        self.count = count

    def set_probability(self, probability):
        self.probability = probability

    def __str__(self):
        return self.previewTag + ' --> ' + self.nextTag + '; probability: ' + str(self.probability) + '; count: ' + \
               str(self.count)
