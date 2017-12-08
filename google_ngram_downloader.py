#!/usr/bin/python3

import os
import utils
import enum

class GoogleNGramDownloader():

  index_url = "http://storage.googleapis.com/books/ngrams/books/datasetsv2.html"
  url_regex = '(http://storage.googleapis.com/books/ngrams/books/googlebooks-eng-all-{}gram-20120701-[a-z]*?\.gz)'
  dataset_path = "datasets/tags/google-ngram/"
  index_fn = os.path.join(dataset_path, os.path.basename(index_url))
  tagged_words_fn = os.path.join(dataset_path, "tagged-words.pickdict")

  def __init__(self, n_gram):
    import re
    self.tagged_words = {}
    utils.download(GoogleNGramDownloader.index_url, GoogleNGramDownloader.index_fn, False)
    with open(GoogleNGramDownloader.index_fn, "r") as f:
      self.urls = re.findall(GoogleNGramDownloader.url_regex.format(n_gram), str(f.read()))

  def getDatasetPath(self, url):
    return os.path.join(GoogleNGramDownloader.dataset_path, os.path.basename(url))

  def download(self):
    for url in self.urls:
      file_name = self.getDatasetPath(url)
      utils.download(url, file_name)

  def unpackFile(self, url):
    import gzip

    class FieldEnum(enum.Enum):
      NGRAM = 0
      YEAR = 1
      MATCH_COUNT = 2
      VOLUME_COUNT = 3

    class POSEnum(enum.Enum):
      ADJ = 0
      ADP = 1
      ADV = 2
      CONJ = 3
      DET = 4
      NOUN = 5
      NUM = 6
      PRON = 7
      PRT = 8
      VERB = 9

    def splitGram(gram):
      stop_pos = gram.rfind('_')
      if stop_pos == -1:
        return None, None

      return gram[:stop_pos], gram[stop_pos + 1:]

    fn = self.getDatasetPath(url)
    if not os.path.exists(fn):
      return {}

    tagged_words = {}
    with gzip.open(fn, 'r') as f:
      print("Unpacking {}".format(fn), fn)
      for line in f:
        line_split = line.decode('utf-8').split()
        word, pos = splitGram(line_split[FieldEnum.NGRAM.value])
        if not word: # Not interested in untagged words
          continue

        #self.tagged_words[word] = [pos, split[1:]]
        if word not in tagged_words.keys():
          tagged_words[word] = [ pos, line_split[1:] ]
        else:
          tagged_words[word].append([ pos, line_split[1:] ])

    return tagged_words

  def unpack(self):
    import multiprocessing as mp
    pool = mp.Pool(processes = 4)
    results = pool.map(self.unpackFile, self.urls)

    for r in results:
      self.tagged_words.update(r)

    with open(GoogleNGramDownloader.tagged_words_fn, "wb") as f:
      import pickle
      pickle.dump(self.tagged_words, f)

  def getTaggedWords(self):
    if self.tagged_words:
      return self.tagged_words
    elif os.path.exists(GoogleNGramDownloader.tagged_words_fn):
      with open(GoogleNGramDownloader.tagged_words_fn, "rb") as f:
        import pickle
        return pickle.load(f)
    else:
      self.download()
      self.unpack()
      return self.tagged_words


n = GoogleNGramDownloader('1')
d = n.getTaggedWords()
