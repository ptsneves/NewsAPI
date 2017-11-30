#!/usr/bin/python3

import random
import nltk
from nltk.corpus import names

def gender_feature(word):
  return {'last_letter' : word[-1],
          'last_2' : word[-2]
         }


def label_gender(gender):
  return [(name, gender) for name in names.words(gender + '.txt')]

def get_labeled_word(label_list):
  labeled_words = []
  for label in label_list:
    labeled_words.extend(label_gender(label))
  random.shuffle(labeled_words)
  return labeled_words

def get_featureset(extractor_function, label_list):
  labeled_words = get_labeled_word(label_list)
  return [(extractor_function(words), gender) for (words, gender) in labeled_words]


feature_set = get_featureset(gender_feature, ['male', 'female'])
test_set, train_set = feature_set[:500], feature_set[500:]
classifier = nltk.NaiveBayesClassifier.train(train_set)
print(nltk.classify.accuracy(classifier, test_set))
