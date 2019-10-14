# Copyright (C) 2011 by D+D Griffiths
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
import urllib
import urllib.request
import os
import re
import sys
import string
import unicodedata
import getopt
from xml.dom import minidom
import csv
from data import Result
urls = ["http://feeds.washingtonpost.com/rss/rss_election-2012",
        "http://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml",
        "http://rss.cnn.com/rss/cnn_topstories.rss",
        "http://feeds.foxnews.com/foxnews/latest"
        ]

results = []

phrase = ''
include_urls = True

score_dictionary = {}


pos_neg = '+'

if len(sys.argv) > 1:
    pos_neg = sys.argv[1]
with open('AFINN-111.txt') as f:
    for line in f:
        if (len(line) > 2):
            pair = line.split('\t')
            if (len(pair)>1):
                score_dictionary[pair[0].strip()] = (float) (pair[1])

with open('sentiments.csv') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
        score_dictionary [row[0]] = (float) (row[1])

with open('positive-words.txt') as f:
    for line in f:
        if (len(line) > 2):
            score_dictionary[line.strip()] = 1.0

with open('negative-words.txt') as f: 
    for line in f:
        if (len(line) > 2):
            score_dictionary[line.strip()] = -1.0

print (len(score_dictionary))

searcher = None
if len(phrase) > 2:
    searcher = re.compile(phrase, re.IGNORECASE)
for url in urls:
    feed = urllib.request.urlopen(url)
    #try:
    dom = minidom.parse(feed)
    forecasts = []
    for node in dom.getElementsByTagName('title'):
        if node.firstChild:
            txt = node.firstChild.wholeText

            if not searcher or searcher.search(txt):
                words = re.split('\W+', txt)
                current = Result(txt)
                txt = unicodedata.normalize('NFKD', txt).encode('ascii', 'ignore')
                #print(txt)

                for w in words:
                    if w in score_dictionary:
                        current.addDictionary(w, score_dictionary [w])
                #print ("Score = " + str(current.getScore()))
                if (current.getScore()!= 0):
                    results.append(current)
                if include_urls:
                    p = node.parentNode
                    link = p.getElementsByTagName('link')[0].firstChild.wholeText
                    current.setUrl(link)
                    #print("\t%s" % link)
    #except:
	    #sys.exit(1)


if pos_neg == '+':
    results.sort(key=lambda r: (r.getScore()))
else:
    results.sort(key=lambda r: (r.getScore()), reverse=True)
for i in range(1,min(len(results),5)):
	r = results[len(results) - i]
	print (r.getTitle()+"\n\tSCORE:" + str(r.getScore()))
	if include_urls:
		print("\t%s\n" % r.getUrl())
