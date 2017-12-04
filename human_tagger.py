#!/usr/bin/python3

import nltk
from nltk import tokenize
from nltk import tag
import pickle
import os
import utils

class HumanTagger:
  Dataset_Path = "./datasets/tags/"
  def __init__(self):
    pass
    #print(str(self.tokenized_sentences))
    #self.pos_sentences = tag.pos_tag_sents(self.tokenized_sentences)
    #print(self.pos_sentences)

  def printSelected(self, tagged_sentence):
    tag_found = False
    d = []
    for word, custom_tag in tagged_sentence:
      if custom_tag != None:
        tag_found = True
        print(word, end=' ')

    if tag_found:
      print()

  def getRawData(self, raw_input_data):
    path_w_prefix = HumanTagger.Dataset_Path + raw_input_data

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

  def tokenizeRawText(self, raw_input_data):
    text = utils.HTMLStripper.stripTags(str(self.getRawData(raw_input_data)))
    sentences = tokenize.sent_tokenize(text)
    tokenized_sentences = []
    for sentence in sentences:
      tokenized_sentences.append(tokenize.word_tokenize(sentence))

    return { 'text' : text,
             'sentences' : sentences,
             'tokenized-sentences' : tokenized_sentences
            }

  def classifySentence(self, raw_input_data, text_tag):
    classified_sentences  = []
    token_data = self.tokenizeRawText(raw_input_data)
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


        self.printSelected(classified_sentence)
        accepted = True if input("Accept? y/n: ") in ['y', ''] else False

      classified_sentences.append(classified_sentence)

    f_name = utils.appendTimestamToFileName(text_tag)

    with open(f_name, 'wb') as fp:
      pickle.dump(classified_sentences, fp)

  def getClassifiedWords(self, text_tag, dump_file):
    path = os.path.join(HumanTagger.Dataset_Path, text_tag, dump_file)
    with open(path, 'rb') as f:
      return pickle.load(f)

  def showClassifiedWords(self, dump_file):
    r = self.getClassifiedWords(dump_file)
    for sentence in r:
      self.printSelected(sentence)

  def runShowClassifiedWordsExample():
    ev = HumanTagger()
    tagged_sentences = []
    tagged_sentences.extend(ev.getClassifiedWords('part-of-assignment',
      'part-of-assignment-2017-12-2-17-22-12'))

    tagged_sentences.extend(ev.getClassifiedWords('part-of-assignment',
      'part-of-assignment-2017-12-2-18-38-11'))

    print (tagged_sentences)

  def runClassifiySentenceExample():
    ev = HumanTagger()
    ev.classifySentence("datasets/texts/ADM", "part-of-assignment")

#HumanTagger.runClassifiySentenceExample()
#HumanTagger.runShowClassifiedWordsExample()
