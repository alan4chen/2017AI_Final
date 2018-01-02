
import csv
import numpy as np

columns_name = "代號,名稱,營收成長率,淨利成長率,營運現金流量成長率,負債比率,固定資產,資產報酬率,股東權益報酬率,資產周轉率,應收帳款周轉率,本益比,每股營收比"
def stock_indicator_reader():
    data = []
    stock_ids = []
    stock_names = []
    for line in open('./data/indicator_data.csv', 'r').readlines()[1:]:
        splitted = line.split(",")
        stock_ids.append(int(splitted[0]))
        stock_names.append(splitted[1])
        data.append([float(x) for x in splitted[2:]])

    # Normalize indicator
    data = np.array(data)
    data -= data.mean(axis = 0)
    data /= data.std(axis = 0)

    # average
    col1 = ((data[:,0] + data[:,1] + data[:,2])/3)[:, np.newaxis]
    col2 = ((data[:,3] + data[:,4])/2)[:, np.newaxis]
    col3 = ((data[:,5] + data[:,6])/2)[:, np.newaxis]
    col4 = ((data[:,7] + data[:,8])/2)[:, np.newaxis]
    col5 = ((data[:, 9] + data[:, 10]) / 2)[:, np.newaxis]

    return stock_ids, stock_names, np.concatenate((col1, col2, col3, col4, col5), axis=1)

stock_ids, stock_names, indicator_data = stock_indicator_reader()


def getStockRankNum(aspect):
    if aspect in [0,2,3]:
        return np.argsort(indicator_data[:,aspect], axis=-1, kind='quicksort', order=None)[::-1]
    else:
        return np.argsort(indicator_data[:, aspect], axis=-1, kind='quicksort', order=None)
StockRankNum = []
for i in range(5):
    StockRankNum.append(getStockRankNum(i))

if __name__ == "__main__":
    print(stock_ids)
    print(stock_names)
    print(indicator_data)
    print(indicator_data.shape)

    print(StockRankNum)