import jieba
import jieba.analyse
jieba.set_dictionary('indicator_predictor/jieba/dict.txt.big')
#jieba.set_dictionary('dict.txt.big')

stock_num_list = [2427,2453,2468,2471,2480,3029,3130,4994,5203,6112,6183,6214]
filename_to_name_dic={2427:"三商電",2453:"凌群",2468:"華經",2471:"資通",2480:"敦陽",3029:"零壹",
                      3130:"一零四", 4994:"傳奇", 5203:"訊連", 6112:"聚碩", 6183:"關貿", 6214:"精誠"}

top10_dic = {}

for i in range(len(stock_num_list)):
    file_name = "news_predictor/news/"+str(stock_num_list[i])+".txt"
    f = open(file_name, encoding='utf-8')
    #seg_list = jieba.cut(f.read(), cut_all=False)
    #print("Full Mode: " + "/ ".join(seg_list))  # 全模式
    tags = jieba.analyse.extract_tags(f.read(), topK=50, withWeight=True)

    # for x, w in tags:
    #     print('%s %s' % (x, w))

    tag_dic = {}
    for (x, w) in tags:
        tag_dic[x] = w
    top10_dic[file_name] = tag_dic
    #if stock_num_list[i] == 2468:
    #    for (x, w) in tags:
    #        print((x, w))


def ir_predictor(query):

    tags = jieba.analyse.extract_tags(query, topK=50, withWeight=True)
    query_list = []
    for x, w in tags:
        print('%s %s' % (x, w))
        query_list = query_list + [(x, w)]

    minimum_file_name = ""
    minimum_error = float('inf')
    term_dic = {}
    for i in top10_dic:
        error = 0.0
        tags = top10_dic[i]
        temp_dic = {}
        for j in range(len(query_list)):
            k = query_list[j]
            if k[0] in tags:
                error += (k[1] - tags[k[0]])**2
                temp_dic[k[0]] = tags[k[0]]
            else:
                error += k[1]**2
        if error < minimum_error:
            minimum_error = error
            minimum_file_name = i
            term_dic = temp_dic

    minimum_stock_index = int(minimum_file_name[20:24])

    # print("minimum error = "+str(minimum_error)+", "+minimum_file_name)

    # print(minimum_stock_index+": "+filename_to_name_dic[minimum_stock_index])

    # print("term found:")


    ret = "我找到的相關股票是: " + str(minimum_stock_index) + " " + filename_to_name_dic[minimum_stock_index] + "\n"
    ret += "參考網址： " + "https://tw.stock.yahoo.com/q/q?s=" + str(minimum_stock_index) + "\n"

    if len(term_dic) != 0:
        ret += "關鍵詞是： "

        for i in term_dic:
            ret += i + " "
            # print(i + ": " + str(term_dic[i]))
        ret += "\n"
        
        return ret
    else:
        return "no suitable stock found :("

if __name__ == "__main__":
    #query = "獲利"
    #print(ir_predictor(query))

    #query = "我想要跟電腦有關的股票"
    #print(ir_predictor(query))

    #query = "我想要跟機車有關的股票"
    #print(ir_predictor(query))

    #query = "我想要跟機器人有關的股票"
    #print(ir_predictor(query))

    query = "我想要人工智慧的股票"
    print(ir_predictor(query))
