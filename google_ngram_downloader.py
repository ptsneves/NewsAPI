#!/usr/bin/python3

import os
import utils
import enum

class GoogleNGramDownloader():
  class FieldEnum(enum.Enum):
    NGRAM = 0
    YEAR = 1
    MATCH_COUNT = 2
    VOLUME_COUNT = 3

  index_url = "http://storage.googleapis.com/books/ngrams/books/datasetsv2.html"
  url_regex = '(http://storage.googleapis.com/books/ngrams/books/googlebooks-eng-all-{}gram-20120701-.*?\.gz)'
  dataset_path = "datasets/tags/google-ngram/"
  index_fn = os.path.join(dataset_path, os.path.basename(index_url))

  def __init__(self, n_gram):
    import re
    utils.download(GoogleNGramDownloader.index_url, GoogleNGramDownloader.index_fn)
    with open(GoogleNGramDownloader.index_fn, "r") as f:
      self.urls = re.findall(GoogleNGramDownloader.url_regex.format(n_gram), str(f.read()))

  def getDatasetPath(sef, url):
    return os.path.join(GoogleNGramDownloader.dataset_path, os.path.basename(url))

  def download(self):
    for url in self.urls:
      file_name = self.getDatasetPath(url)
      utils.download(url, file_name)

  def unpack(self):
    import gzip

    for url in self.urls:
      fn = self.getDatasetPath(url)
      if os.path.exists(fn):
        with gzip.open(fn, 'r') as f:
          for line in f:
            split = line.decode('utf-8').split()
            word_type_split = split[0].split('_')
            if len(word_type_split) > 1:
              print(split)

n = GoogleNGramDownloader('1')
n.unpack()
