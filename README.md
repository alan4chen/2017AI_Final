# TW Stock Recommendation BOT - 2017AI_Final
Stock share is a popular investment tool in the contemporary era. In general, a stock investor needs to understand and analyze lots of financial statements as well as annual reports, and to monitor the stock market from time to time. We note this problem and thus try to build a stock-recommendation chat-bot that is able to analyze user’s semantics and list the top-3 ranking stocks. The main goal of this chat-bot is to help users to quickly get the most recommended stock given a specific query. The detail of our approach is described in the “method” section below.

## Setup
* Install Python3.5 or higher version
* Install requirement
```
pip install -r requirements.txt
```
* Create indicator_predictor/word2vec/ directory
```
mkdir indicator_predictor/word2vec/
```
* Download wiki.zh.vec.pickle and place it in word2vec directory
```
wget https://www.dropbox.com/s/8kkuzccqsagobga/wiki.zh.vec.pickle?dl=0
```

## Usage
### Run Server
```
python server.py
```

## Method
- Retrieval Method (Vector Space Model)
- Indicator Method (Word2Vec & Financial Analysis)

## Poster
![Poster](poster.png)
