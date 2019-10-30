from conllu import parse
from pip._vendor.distlib.compat import raw_input

from pos_word_list import PosWordProbList
from pos_pos_list import PosPosProbList
import numpy as np
from nltk.stem import WordNetLemmatizer
#import nltk
#nltk.download('wordnet')


def main():
    file = open("UD_English-ParTUT/en_partut-ud-train.conllu")
    try:
        sentences = parse(file.read())
    finally:
        file.close()

    print('Caricamento...')

    # Crea mappa TAG - numero occorrenze
    tags_map = set_tags_map(sentences)

    # POS -> POS - Crea elenco di coppie di TAG con probabilità
    pos_pos_probability_list = PosPosProbList(tags_map, sentences)

    # POS -> WORD - Crea un elenco di probabilità associate a tag e parola
    pos_word_probability_list = PosWordProbList(tags_map, sentences)

    #show menu
    menu = {}
    menu['1'] = "The black droid then lowers Vader's mask and helmet onto his head."
    menu['2'] = "These are not the droids your looking for."
    menu['3'] = "Your friends may escape, but you are doomed."
    menu['4'] = "Valutazione test set"
    menu['5'] = "Confronto baseline"
    menu['6'] = "Termina"
    while True:
        options = menu.keys()
        for entry in options:
            print(entry, menu[entry])

        selection = raw_input("Please Select:")
        if selection == '1':
            phrase = 'The black droid then lowers Vader \'s mask and helmet onto his head .'
            pos_tagging = viterbi(phrase, pos_pos_probability_list, pos_word_probability_list, tags_map)

            print(phrase)
            print(pos_tagging)
        elif selection == '2':
            phrase = 'These are not the droids your looking for .'
            pos_tagging = viterbi(phrase, pos_pos_probability_list, pos_word_probability_list, tags_map)

            print(phrase)
            print(pos_tagging)
        elif selection == '3':
            phrase = 'Your friends may escape , but you are doomed .'
            pos_tagging = viterbi(phrase, pos_pos_probability_list, pos_word_probability_list, tags_map)

            print(phrase)
            print(pos_tagging)
        elif selection == '4':
            file = open("UD_English-ParTUT/en_partut-ud-test.conllu")
            try:
                test_sentences = parse(file.read())
            finally:
                file.close()

            # Get all phrases
            equals = 0
            tot = 0
            for sent in test_sentences:
                phrase = ''
                for word in sent:
                    phrase = phrase + word['form'] + ' '
                pos = viterbi(phrase, pos_pos_probability_list, pos_word_probability_list, tags_map)
                #print(phrase)
                #print(pos)

                for i in range(0, len(pos)):
                    if pos[i] == sent[i]['upostag']:
                        equals += 1
                    tot += 1

            print('Accuracy:', equals, '/', tot, '=', (equals/tot*100), '%')

        elif selection == '5':
            print('DA FARE')
            #test_baseline()
        elif selection == '6':
            break
        else:
            print("Selezione non permessa!")


def set_tags_map(sentences):
    # Crea elenco di tutti i TAG nel corpus
    tags_map = {"START": 0, "END": 0}
    for phrase in sentences:
        tags_map['START'] += 1
        tags_map['END'] += 1
        for word in phrase:
            if not word['upostag'] in tags_map.keys():
                tags_map[word['upostag']] = 1
            else:
                tags_map[word['upostag']] += 1
    return tags_map


def viterbi(phrase, pos_pos_probability, pos_word_probability, tags_map):
    """
        Applica l'algoritmo di Viterbi per trovare il POS tagging di una frase

        Args:
            phrase (String): La frase da analizzare
            pos_pos_probability (Object): Oggetto che contiene le probabilità delle transizioni fra tags
            pos_word_probability (Object): Oggetto che contiene le probabilità delle parole associate ad un tag
            tags_map (Dict): Mappa di tag

        Returns:
            Array di tags applicati alla frase passata come argomento.
    """
    words = phrase.split(' ')
    lemmas = []

    #Lemmatize words
    lemmatizer = WordNetLemmatizer()
    for i in range(0, len(words)):
        #print(words[i], " :", lemmatizer.lemmatize(words[i]))
        if len(words[i]) > 0:
            lemmas.append(lemmatizer.lemmatize(words[i]))

    matrix = {}

    for tag in tags_map.keys():
        matrix[tag] = {
            'prob': np.ones(len(lemmas)),
            'prev_tag': [''] * (len(lemmas))
        }

    # Initialization step
    for s in tags_map.keys():
        pos_pos = pos_pos_probability.P('START', s)
        pos_word = pos_word_probability.P(s, lemmas[0])
        if pos_word == -1 and s != 'PROPN':
            matrix[s]['prob'][0] = 1
            matrix[s]['prev_tag'][0] = '-'
        else:
            if pos_word == -1 and s == 'PROPN':
                pos_word = 1
            matrix[s]['prob'][0] = pos_pos * pos_word
            matrix[s]['prev_tag'][0] = 'START'

    # Recursion step
    for t in range(1, len(lemmas)):
        for s in tags_map.keys():
            if s != 'START' and s != 'END':
                pos_word = float(pos_word_probability.P(s, lemmas[t]))
                if pos_word == -1 and s != 'PROPN':
                    matrix[s]['prob'][t] = 1
                    matrix[s]['prev_tag'][t] = '-'
                else:
                    if pos_word == -1 and s == 'PROPN':
                        pos_word = 1
                    matrix[s]['prob'][t], matrix[s]['prev_tag'][t] = find_max(matrix, t-1, s, pos_word, pos_pos_probability)

    # Print matrix
    '''
    np.set_printoptions(precision=2)
    for elem in matrix:
        if elem == 'X' or elem == '_':
            print(elem, '\t\t', matrix[elem])
        else:
            print(elem, '\t', matrix[elem])
    '''

    # Termination step
    _, end_tag = find_max(matrix, len(lemmas) - 1, 'END', 1, pos_pos_probability)

    # Create array for return
    pos_tagging = [''] * len(lemmas)
    pos_tagging[len(lemmas) - 1] = end_tag
    prev_tag = matrix[end_tag]['prev_tag'][len(lemmas) - 1]

    for i in range(len(lemmas) - 2, -1, -1):
        pos_tagging[i] = prev_tag
        prev_tag = matrix[prev_tag]['prev_tag'][i]

    return pos_tagging


def find_max(matrix, index, next_tag, pos_word, pos_pos_probability):
    """
        Trova il massimo valore da inserire nella cella selezionata.

        Args:
            matrix (dict): La matrice su cui operare
            index (int): L'indice della colonna su cui opera la funzione. Si riferisce al tempo t-1 della funzione chiamante
            next_tag (string): tag della parola di cui vogliamo trovare il massimo
            pos_word (float): probabilità pos_word
            pos_pos_probability (PosPosProbList): Elenco dell probabilità pos_pos

        Returns:
            float: Il massimo valore otenuto
            string: Il TAG associato al massimo valore ottenuto
    """
    max_val = float("-inf")
    max_tag = ''
    for prev_tag in matrix.keys():
        if prev_tag != 'END' and prev_tag != 'START':
            pos_pos = pos_pos_probability.P(prev_tag, next_tag)
            #if next_tag == 'END':
                #print('POS POS:', (matrix[prev_tag]['prob'][index] * pos_pos), 'TAG: ', prev_tag)
            new_probability = matrix[prev_tag]['prob'][index] * pos_pos * pos_word
            if new_probability > max_val:
                max_val = new_probability
                max_tag = prev_tag
    return max_val, max_tag


if __name__ == '__main__':
    main()
