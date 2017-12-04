#!/usr/bin/python3

import nltk
from nltk import tokenize
from nltk import tag
import pickle
import os
import time

def append_timestamp_to_file_name(base_fn):
    t = time.gmtime()
    f_name = "{}-{}-{}-{}-{}-{}-{}".format(base_fn, t.tm_year, t.tm_mon,
      t.tm_mday, t.tm_hour, t.tm_min, t.tm_sec)
    return f_name


from html.parser import HTMLParser
#https://stackoverflow.com/questions/753052/strip-html-from-strings-in-pythoni
class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.strict = False
        self.convert_charrefs= True
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

class HumanEvaluator:
  Dataset_Path = "./datasets/tags/"
  def __init__(self):
    pass
    #print(str(self.tokenized_sentences))
    #self.pos_sentences = tag.pos_tag_sents(self.tokenized_sentences)
    #print(self.pos_sentences)

  def print_selected(self, tagged_sentence):
    tag_found = False
    d = []
    for word, custom_tag in tagged_sentence:
      if custom_tag != None:
        tag_found = True
        print(word, end=' ')

    if tag_found:
      print()

  def get_raw_data(self, raw_input_data):
    path_w_prefix = Dataset_Path + raw_input_data

    path = None
    if os.path.exists(path_w_prefix):
      path = path_w_prefix
    elif os.path.exists(raw_input_data):
      path = raw_input_data

    if path:
      with open(path, "r") as f:
        return f.read()
    else:
      return raw_input_data

  def tokenize_raw_text(self, raw_input_data):
    text = strip_tags(str(get_raw_data(raw_input_data)))
    sentences = tokenize.sent_tokenize(text)
    tokenized_sentences = []
    for sentence in sentences:
      tokenized_sentences.append(tokenize.word_tokenize(sentence))

    return { 'text' : text,
             'sentences' : sentences,
             'tokenized-sentences' : tokenized_sentences
            }

  def classify_sentence(self, raw_input_data, text_tag):
    classified_sentences  = []
    token_data = self.tokenize_raw_text(raw_input_data)
    for sentence in token_data['tokenized-sentences']:
      classified_sentence = []
      accepted = False
      while(not accepted):
        classified_sentence = []
        for i, word in enumerate(sentence):
          print(i, word)
        r = input("Select the indexes of words that are in the class {}\n".format(text_tag))

        for i, word in enumerate(sentence):
          r_split = r.split()
          classified_sentence.append((word, text_tag if str(i) in r_split else None))


        self.print_selected(classified_sentence)
        accepted = True if input("Accept? y/n: ") in ['y', ''] else False

      classified_sentences.append(classified_sentence)

    f_name = append_timestamp_to_file_name(text_tag)

    with open(f_name, 'wb') as fp:
      pickle.dump(classified_sentences, fp)

  def get_classified_words(self, text_tag, dump_file):
    path = os.path.join(HumanEvaluator.Dataset_Path, text_tag, dump_file)
    with open(path, 'rb') as f:
      return pickle.load(f)

  def show_classified_words(self, dump_file):
    r = self.get_classified_words(dump_file)
    for sentence in r:
      self.print_selected(sentence)

def untag_sentences(tagged_sentences):
  untagged_sentences = []
  for s in tagged_sentences:
    untagged_sentences.append(nltk.tag.util.untag(s))

  return untagged_sentences

ev = HumanEvaluator()
tagged_sentences = []
tagged_sentences.extend(ev.get_classified_words('part-of-assignment',
  'part-of-assignment-2017-12-2-17-22-12'))

tagged_sentences.extend(ev.get_classified_words('part-of-assignment',
  'part-of-assignment-2017-12-2-18-38-11'))

untagged_sentences = untag_sentences(tagged_sentences)

from nltk.corpus import brown
brown_tagged_sents = brown.tagged_sents(categories='news')


t_default = nltk.DefaultTagger('NN')

FLOATING_POINT_REGEX = (r'[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?.', 'NUM')
t_regexp = nltk.RegexpTagger([FLOATING_POINT_REGEX], backoff = t_default)
t_bigram = nltk.BigramTagger(brown_tagged_sents, backoff = t_regexp)
print(t_bigram.tag_sents(untagged_sentences))

#ev.classify_sentence("ADM", "part-of-assignment")
#ev.show_classified_words('part-of-assignment-2017-12-2-18-38-11')
