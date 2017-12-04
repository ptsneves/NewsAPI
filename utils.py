import time

def appendTimestamToFileName(base_fn):
    t = time.gmtime()
    f_name = "{}-{}-{}-{}-{}-{}-{}".format(base_fn, t.tm_year, t.tm_mon,
      t.tm_mday, t.tm_hour, t.tm_min, t.tm_sec)
    return f_name

from html.parser import HTMLParser
#https://stackoverflow.com/questions/753052/strip-html-from-strings-in-pythoni
class HTMLStripper(HTMLParser):
  def __init__(self):
    self.strict = False
    self.convert_charrefs= True
    self.fed = []
    self.reset()

  def handle_data(self, d):
    self.fed.append(d)

  def get_data(self):
    return ''.join(self.fed)

  def stripTags(html):
    s = HTMLStripper()
    s.feed(html)
    return s.get_data()

def untagSentences(tagged_sentences):
  import nltk
  untagged_sentences = []
  for s in tagged_sentences:
    untagged_sentences.append(nltk.tag.util.untag(s))

  return untagged_sentences

