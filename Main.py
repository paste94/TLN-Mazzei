from conllu import parse

file = open("UD_English-ParTUT/en_partut-ud-dev.conllu")

try:
    sentences = parse(file.read())
    listOfTags = []

    # Calculate POS Probability
    # se ad esempio vogliamo sapere quale è la probabilità che ad un verbo t(i−1) segua un nome t(i) mi è suffciente
    # contare nel mio corpus quante volte ad un verbo segue un nome, e andare a dividere per il numero di verbi che
    # compaiono nel corpus

    # Elenco di tutti i TAG nel corpus
    for phrase in sentences:
        for word in phrase:
            if not word['upostag'] in listOfTags:
                listOfTags.append(word['upostag'])

    posProbability = []
    for tag1 in listOfTags:
        for tag2 in listOfTags:
            posProbability.append()

    print(listOfTags)


finally:
    file.close()
