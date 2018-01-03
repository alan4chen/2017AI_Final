
from indicator_predictor.data.indicator_keywords import idx2pihua
from indicator_predictor.preprocessor import reader_indicator_keywords_meaning, reader_indicator_keywords, jieba_process, fastText_sentence2vector, stopper
from indicator_predictor.rank_stock import stock_ids, stock_names, indicator_data, StockRankNum
from indicator_predictor.pihua import get_pihua, get_scores
from scipy import spatial

def cal_consine_sim(v1, v2):
    return  1 - spatial.distance.cosine(v1, v2)

# Keywords
indicator_keywords = reader_indicator_keywords()

# Meaning
indicator_keywords_meaning = reader_indicator_keywords_meaning()
indicator_meaning_jieba = jieba_process(indicator_keywords_meaning)
indicator_vectors = fastText_sentence2vector(indicator_meaning_jieba)

def classifier(sentence):
    sentence = stopper(sentence)
    if len(sentence) < 1 : return -2

    # Keywords
    select_indicator = [0] * len(indicator_keywords)
    for i in range(len(indicator_keywords)):
        for keyword in indicator_keywords[i]:
            if keyword in sentence:
                select_indicator[i] += 1
    if sum([x > 0 for x in select_indicator]) > 3:
        return -1
    elif sum([x > 0 for x in select_indicator]) > 0:
        return select_indicator.index(max(select_indicator))

    print(indicator_vectors)

    sen = jieba_process([sentence])
    print(sen)
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
    import random
    seed_num = len(sentence)
    random.seed(seed_num)

    idx = classifier(sentence)


    if idx == -1:
        return "嗯...你的要求條件太多了喲~ 請減少一些限制~"
    elif idx == -2:
        return "聽不懂你在說什麼耶~"

    ret = ""
    ret += random.choice(idx2pihua[idx]) + "\n" # 分類的說明

    ret += "目前我只會看台灣資訊產業的公司噢，我推薦的股票如下：\n\n"



    for stock_num in [StockRankNum[idx][x] for x in sorted(random.sample(range(5), 3))]:
        tmp = ""
        tmp += str(stock_ids[stock_num]) + " " + stock_names[stock_num] + "\n參考網址:" + "https://tw.stock.yahoo.com/q/q?s=" + str(stock_ids[stock_num]) + "\n"

        tmp += "推薦理由是:\n"
        tmp += get_pihua(stock_num, idx) + "\n"

        tmp += get_scores(stock_num, idx) + "\n"

        ret += tmp+"\n"
    return ret

if __name__ == "__main__":
    client_sentence = "賺很多 很賺錢的公司"
    p = handler(client_sentence)
    print(p)
    #
    client_sentence = "我想要很安全的公司"
    p = handler(client_sentence)
    print(p)
    #
    client_sentence = "本益比高"
    p = handler(client_sentence)
    print(p)

    # client_sentence = "許永真"
    # p = handler(client_sentence)
    # print(p)
    #
    client_sentence = "我想要比較便宜，可能被低估的~~"
    p = handler(client_sentence)
    print(p)

