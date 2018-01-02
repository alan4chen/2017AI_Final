#!/bin/bash

pip install -r requirement

# prepare word2vec
mkdir indicator_predictor/word2vec
wget "https://www.dropbox.com/s/8kkuzccqsagobga/wiki.zh.vec.pickle?dl=0" -o indicator_predictor/word2vec/wiki.zh.vec.pickle

# run
# python server.py