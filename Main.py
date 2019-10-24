from conllu import parse
from PosProbability import PosPosProbability, PosWordProbability


def main():
    file = open("UD_English-ParTUT/en_partut-ud-dev.conllu")
    try:
        sentences = parse(file.read())
    finally:
        file.close()

    # Crea mappa TAG - numero occorrenze
    tags_map = set_tags_map(sentences)

    # POS -> POS - Crea elenco di coppie di TAG con probabilità
    pos_pos_probability_list = pos_pos_probability(tags_map, sentences)

    # print(*pos_pos_probability_list, sep='\n')

    # POS -> WORD - Crea un elenco di probabilità associate a tag e parola
    pos_word_probability_list = pos_word_probability(sentences, tags_map)

    print(*pos_word_probability_list, sep='\n')


def set_tags_map(sentences):
    # Crea elenco di tutti i TAG nel corpus
    tags_map = {}
    for phrase in sentences:
        for word in phrase:
            if not word['upostag'] in tags_map.keys():
                tags_map[word['upostag']] = 1
            else:
                tags_map[word['upostag']] += 1
    return tags_map


def pos_pos_probability(tags_map, sentences):
    posProbabilityList = []
    for tag1 in tags_map.keys():
        for tag2 in tags_map.keys():
            posProbabilityList.append(PosPosProbability(tag1, tag2))

    # Conta le occorrenze delle coppie POS -> POS
    for phrase in sentences:
        for i in range(1, len(phrase)):
            position = find_pos_pos_position(phrase[i - 1]['upostag'], phrase[i]['upostag'], posProbabilityList)
            posProbabilityList[position].count += 1

    # Imposta le percentuali
    for elem in posProbabilityList:
        elem.probability = elem.count / tags_map[elem.previewTag]

    return posProbabilityList


def pos_word_probability(sentences, tags_map):
    lst = []
    for phrase in sentences:
        for word in phrase:
            index = find_pos_word_position(word['form'], word['upostag'], lst)
            if index == -1:
                lst.append(PosWordProbability(word['form'], word['upostag']))
            else:
                lst[index].count += 1

    # Imposta le percentuali
    for elem in lst:
        elem.probability = elem.count / tags_map[elem.tag]

    return lst


def find_pos_word_position(word, tag, lst):
    for i in range(0, len(lst)):
        if lst[i].word == word and lst[i].tag == tag:
            return i
    return -1


def find_pos_pos_position(tag1, tag2, lst):
    # print('cerco ' + str(tag1) + ' --> ' + str(tag2))
    for i in range(0, len(lst)):
        if lst[i].previewTag == tag1 and lst[i].nextTag == tag2:
            # print('Trovato ' + tag1 + ' --> ' + tag2 + ' in posizione ' + str(i))
            return i



if __name__ == '__main__':
    main()
