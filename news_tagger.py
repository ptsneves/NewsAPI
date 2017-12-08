#!/usr/bin/python3
import nltk

class NewsTagger(nltk.tag.api.TaggerI):
  FLOATING_POINT_REGEX = (r'[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?.', 'NUM')

  def __init__(self):
    from nltk.corpus import brown
    brown_tagged_sents = brown.tagged_sents()

    self.t_default = nltk.DefaultTagger('None')
    self.t_regexp = nltk.RegexpTagger([NewsTagger.FLOATING_POINT_REGEX], backoff = self.t_default)
    self.t_bigram = nltk.BigramTagger(brown_tagged_sents, backoff = self.t_regexp)

  def loadFromFile(news_tagger_pickle_file):
    with open(news_tagger_pickle_file) as f:
      return pickle.load(f)

  def saveToFile(self, fileName):
    with open(fileName, 'w') as f:
      pickle.dump(self, f)

  def __enter__(self, autosave = None):
    self.autosave = autosave
    return self

  def __exit__(self, exc_type, exc_value, traceback):
    if self.autosave:
      self.saveToFile(self.autosave)

  def tag_sents(self, sentences):
    return self.t_bigram.tag_sents(tokens)

  def tag(self, tokens):
    return self.t_bigram.tag(tokens)

with NewsTagger() as t:
  print(t.tag(["Hello", "world"]))

