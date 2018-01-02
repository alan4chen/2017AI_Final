
def reader_pihua():
    data = []
    tmp = None
    for line in open("indicator_predictor/data/pihua_data", "r").readlines():
        if len(line) < 3:
            continue
        if len(line) < 10:
            if tmp != None:
                data.append(tmp)
            tmp = list()
            continue
        else:
            tmp.append(line.replace("\n",""))
    return data
pihua_data = reader_pihua()

def reader_score():
    data = []
    for line in open('indicator_predictor/data/pihua_scores', 'r').readlines():
        splitted = line.replace("\n", "").split(",")[1:]
        data.append([int(x) for x in splitted])
    return data
scores = reader_score()

def get_scores(stock_num, type):
    star_num = scores[stock_num][type]
    return "我的評分是："+"★" * star_num + "☆"*(5-star_num)




def get_pihua(stock_num, type):
    if type == 0:
        return "\n".join(pihua_data[stock_num][:3])
    elif type == 1:
        return "\n".join(pihua_data[stock_num][3:5])
    elif type == 2:
        return "\n".join(pihua_data[stock_num][5:7])
    elif type == 3:
        return "\n".join(pihua_data[stock_num][7:9])
    elif type == 4:
        return "\n".join(pihua_data[stock_num][9:])


if __name__ == "__main__":
    # print(reader_pihua())
    # print(get_pihua(3,4))
    # print(scores)


    pass