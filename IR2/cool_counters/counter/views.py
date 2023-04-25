from django.shortcuts import render, get_object_or_404
from .models import Counter
from django.shortcuts import render
from django.shortcuts import HttpResponse
import json
import requests
from bs4 import BeautifulSoup
import re
import math
from collections import Counter
import html
import pandas as pd
import nltk
nltk.download('punkt')
import nltk
import math 
from collections import Counter
import os
import numpy


def index(request):
	q = request.GET.get("q", None)
	if(q =='' or q is None):
		value = ['NOT FOUND']
	else:
		value = load_file(q.lower())
	try: 
		context = {'statuses':value }
		return render(request, 'counter/index.html', context)

	except: 
		return render(request, 'counter/index.html', {})


#!/usr/bin/python
# -*- coding: utf-8 -*-


def tokenize_this(document, url,list_of_words_query):
    url_word_map = {}
    words = re.findall(r'\b\w+\b', document)
    word_freq = Counter(words)
    inner_list = {}
    for i in word_freq.keys():
        inner_list[i] = word_freq[i]
        list_of_words_query[i] = 0
    url_word_map[url] = inner_list
    return url_word_map


def dot_product(vector1, vector2):
    return sum([x * y for (x, y) in zip(vector1, vector2)])


def euclidean_length(vector):
    return math.sqrt(sum([x ** 2 for x in vector]))


def cosine_similarity(vector1, vector2):
    dot_product_value = dot_product(vector1, vector2)
    length1 = euclidean_length(vector1)
    length2 = euclidean_length(vector2)

    cosine_similarity_value = dot_product_value / (length1 * length2)
    return cosine_similarity_value


def load_file(query):
    print("starting")
    script_dir = os.path.dirname(__file__)
    rel_path = "file/"
    abs_file_path = os.path.join(script_dir, rel_path)
    print(abs_file_path)
    url_word_map = None
    list_of_words = None
    with open(abs_file_path + 'url_data.json') as f:
        url_word_map = json.load(f)

    with open(abs_file_path + 'no_of_words.json') as f:
        list_of_words = json.load(f)
    final_set = {}
    list_of_words_query = {}
    tokenize_map = tokenize_this(query, 'query',list_of_words_query)
    query_map = {}
    final_query_map = {}
    for (x, y) in list_of_words.items():
        value = tokenize_map.get('query').get(x)
        if value is None:
            query_map[x] = 0.0
        else:
            query_map[x] = value
    url_word_map['query'] = query_map
    df_map = {}
    df_map_final = {}

    for words in list_of_words:
        word_frequency = 0
        for x in url_word_map.values():
            if x.get(words) is not None:
                word_frequency = word_frequency + 1
        df_map[words] = math.log10(len(url_word_map) / word_frequency)

    for word in list_of_words.keys():
        inner_map_temp = {}
        for (url, map) in url_word_map.items():
            if map.get(word) is not None:
                inner_map_temp[url] = map.get(word) * df_map[word]
        df_map_final[word] = inner_map_temp
    return process(df_map_final)

def process(df_map_final):
    script_dir = os.path.dirname(__file__)
    rel_path = "file/"
    abs_file_path = os.path.join(script_dir, rel_path)
    print(abs_file_path)

    df_df = pd.DataFrame(df_map_final)
    df_df.to_csv(abs_file_path + 'tf_idf.csv')

    df_df = pd.read_csv(abs_file_path + 'tf_idf.csv').fillna(0)
    df_df_query = df_df.query("`Unnamed: 0` == 'query'")
    query_vector = None
    for (index, row) in df_df_query.iterrows():
        num_array_query = row.to_numpy()
        query_vector = numpy.delete(num_array_query, 0)

    df_df = df_df.query("`Unnamed: 0` != 'query'")
    url_final_map = {}
    for (index, row) in df_df.iterrows():
        num_array = row.to_numpy()
        vector2 = numpy.delete(num_array, 0)
        sim = cosine_similarity(query_vector, vector2)
        url_final_map[num_array[0]] = sim

    sortedDict = sorted(url_final_map, reverse=True)
    a1_sorted_keys = sorted(url_final_map, key=url_final_map.get, reverse=True)
    final_list = []
    for i,r in enumerate(a1_sorted_keys):
        if(i>4):
            break
        else:
            final_list.append(r)

    return final_list
