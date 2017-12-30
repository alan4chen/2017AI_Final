import jieba
import jieba.analyse
jieba.set_dictionary('dict.txt.big')

stock_num_list = [2427,2453,2468,2471,2480,3029]
article_num_list = [5,5,1,1,2,1]
filename_to_name_dic={2427:"三商電",2453:"凌群",2468:"華經",2471:"資通",2480:"敦陽",3029:"零壹"}

file_name_dic = {}
top10_dic = {}

for i in range(len(stock_num_list)):
    for j in range(article_num_list[i]):
        file_name = "article/"+str(stock_num_list[i])+"-"+str(j+1)+".txt"
        f = open(file_name)
        #seg_list = jieba.cut(f.read(), cut_all=False)
        #print("Full Mode: " + "/ ".join(seg_list))  # 全模式
        tags = jieba.analyse.extract_tags(f.read(), topK=15, withWeight=True)
        for x, w in tags:
            print('%s %s' % (x, w))
        print()
        if stock_num_list[i] in file_name_dic:
            file_name_dic[i] = file_name_dic[i] + [file_name]
        else:
            file_name_dic[i] = [file_name]
        tag_dic = {}
        for (x, w) in tags:
            tag_dic[x] = w
        top10_dic[file_name] = tag_dic
        #print(",".join(tags))


query="我想要獲利高的股票"
tags = jieba.analyse.extract_tags(query, topK=15, withWeight=True)
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

print("minimum error = "+str(minimum_error)+", "+minimum_file_name)
print(minimum_file_name[8:12]+": "+filename_to_name_dic[int(minimum_file_name[8:12])])
print("term found:")
for i in term_dic:
    print(i+": "+str(term_dic[i]))