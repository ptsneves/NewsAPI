#!/usr/bin/python3

class GoogleNGramDownloader():
  url = "http://storage.googleapis.com/books/ngrams/books/datasetsv2.html"
  url_regex = '(http://storage.googleapis.com/books/ngrams/books/googlebooks-eng-all-{}gram-20120701-.*?\.gz)'
  def __init__(self, n_gram):
    import urllib.request
    import re
    response = urllib.request.urlopen(GoogleNGramDownloader.url).read()
    matches = re.findall(url_regex.format(GoogleNGramDownloader.ngram), str(response))
    print(matches)

n = GoogleNGramDownloader('1')
