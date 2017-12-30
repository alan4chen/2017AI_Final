
from data.indicator_keywords import idx2keywords
from preprocessor import reader_indicator_keywords, jieba_process, fastText_sentence2vector
from scipy import spatial

def cal_consine_sim(v1, v2):
    return  1 - spatial.distance.cosine(v1, v2)

indicator_keywords = reader_indicator_keywords()
indicator_jieba = jieba_process(indicator_keywords)
indicator_vectors = fastText_sentence2vector(indicator_jieba)

def classifier(sentence):

    # print(indicator_vectors)

    sen = jieba_process([sentence])
    sen = fastText_sentence2vector(sen)
    # print(sen)

    max_indicator = 0
    max_val = float('-inf')
    for i in range(len(indicator_keywords)):
        sim = cal_consine_sim(sen, indicator_vectors[i, :])
        print(sim)
        if sim > max_val:
            max_val = sim
            max_indicator = i
    return max_indicator

def handler(sentence):
    idx = classifier(sentence)
    return idx2keywords[idx]

if __name__ == "__main__":
    client_sentence = "賺很多 很賺錢的公司"
    p = handler(client_sentence)
    print(p)

    client_sentence = "很安全的公司"
    p = classifier(client_sentence)
    print(p)

    client_sentence = "本益比高"
    p = classifier(client_sentence)
    print(p)

    client_sentence = "許永真"
    p = classifier(client_sentence)
    print(p)

    client_sentence = "去死吧"
    p = classifier(client_sentence)
    print(p)

