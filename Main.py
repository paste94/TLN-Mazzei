from conllu import parse

from PosProbability import PosProbability

file = open("UD_English-ParTUT/en_partut-ud-dev.conllu")

try:
    sentences = parse(file.read())

    # Calculate POS Probability
    # se ad esempio vogliamo sapere quale è la probabilità che ad un verbo t(i−1) segua un nome t(i) mi è suffciente
    # contare nel mio corpus quante volte ad un verbo segue un nome, e andare a dividere per il numero di verbi che
    # compaiono nel corpus

    # Elenco di tutti i TAG nel corpus
    listOfTags = []
    for phrase in sentences:
        for word in phrase:
            if not word['upostag'] in listOfTags:
                listOfTags.append(word['upostag'])

    # Elenco di coppie di TAG con probabilità (di default la probabilità è impostata a 0)
    posProbabilityList = []
    for tag1 in listOfTags:
        for tag2 in listOfTags:
            posProbabilityList.append(PosProbability(tag1, tag2))

finally:
    file.close()
