

import jieba
jieba.set_dictionary("jieba/dict.txt.big")
import numpy as np
import csv
import os

import _pickle
from stopper import CHAR_TO_REMOVE

DATA_CATCHED = True

def jieba_process(sentences):
    """ return list of list of jieba words
             :param path:
             :return:

             input: [['大', '家', '好'], [....]]
             output: [['大家', '好'], [...]]
             """
    ret = []
    for sentence in sentences:
        splitted = list(jieba.cut("".join(sentence)))
        ret.append(splitted)
    return ret


def fastText_get_vectorDict(path = './wiki.zh.vec'):
    """ return word2vec dict

    :param path:
    :return:
    """

    pickle_path = './word2vec/wiki.zh.vec.pickle'
    if DATA_CATCHED == True and os.path.isfile(pickle_path):
        print("-- return cached wiki.zh.vec.pickle --")
        return _pickle.load(open(pickle_path, 'rb'))

    vectorDict = dict()

    f = open(path)
    flag = False
    for idx, line in enumerate(f.readlines()):
        if flag:
            line = line.translate({ord(i): None for i in CHAR_TO_REMOVE})
            splitted = line.split(" ")[:-1]
            vectorDict[splitted[0]] = np.array(list(map(float, splitted[1:])))
        else:
            flag = True
        if idx % 100 == 0:
            print(idx, ' / ', 332647)

    "-- Load fastText Completed --"
    _pickle.dump(vectorDict, open(pickle_path, 'wb'))
    return vectorDict


def fastText_sentence2vector(sentences):
    """ process sentences (list of list of words) into matrix of (samples, vector)
    :param sentences:
    :return:
    """
    vectorDict = fastText_get_vectorDict()

    matrix = np.zeros(shape=(len(sentences), 300))
    for idx, sentence in enumerate(sentences):
        counter = 0
        tmp_arr = np.zeros(shape=(300))
        for word in sentence:
            if word == "\n":
                break
            if word in vectorDict:
                tmp_arr += vectorDict[word]
                counter += 1
            else:
                for w in word:
                    if w in vectorDict:
                        tmp_arr += 1. / len(word) * vectorDict[w]
                        counter += 1. / len(word)
        matrix[idx, :] = tmp_arr / counter

        if (idx+1) % 10000 == 0:
            print(idx, ' / ', len(sentences))
    return matrix

def reader_indicator_keywords():
    from data.indicator_keywords import keywords as keywords_data
    ret = []
    for keywords in keywords_data:
        splitted = keywords.split(" ")
        ret.append(splitted)
    return ret
