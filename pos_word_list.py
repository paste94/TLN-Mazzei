import numpy as np


class PosWordProbList:
    lst = []

    def __init__(self, tags_map, sentences):
        self.tags_map = tags_map
        self.sentences = sentences
        self.lst = self.pos_word_probability()

    def __str__(self):
        s = ''
        for elem in self.lst:
            s += str(elem)
            s += '\n'
        return s

    def pos_word_probability(self):
        lst = []
        for phrase in self.sentences:
            for word in phrase:
                index = self.find_pos_word_position(word['form'], word['upostag'], lst)
                if index == -1:
                    lst.append(PosWordProbability(word['form'], word['upostag']))
                else:
                    lst[index].count += 1

        # Imposta le percentuali
        for elem in lst:
            if self.tags_map[elem.tag] == 0:
                elem.probability = 1
            else:
                elem.probability = 1+(elem.count / self.tags_map[elem.tag])

        return lst

    @staticmethod
    def find_pos_word_position(word, tag, lst):
        for i in range(0, len(lst)):
            if lst[i].word == word and lst[i].tag == tag:
                return i
        return -1

    def P(self, tag, word):
        for elem in self.lst:
            if elem.tag == tag and elem.word == word:
                return 1+elem.probability
        return -1


class PosWordProbability:
    def __init__(self, word, tag, probability=0, count=0):
        self.word = word
        self.tag = tag
        self.probability = probability
        self.count = count # imposto a 1 per evitare una probabilità di 0!

    def set_probability(self, probability):
        self.probability = probability

    def __str__(self):
        prob = str(self.probability)
        c = str(self.count)
        return self.word + ' --> ' + self.tag + '; probability: ' + prob + '; count: ' + c
