#!/usr/bin/python3

def appendTimestamToFileName(base_fn):
  import time
  t = time.gmtime()
  f_name = "{}-{}-{}-{}-{}-{}-{}".format(base_fn, t.tm_year, t.tm_mon,
    t.tm_mday, t.tm_hour, t.tm_min, t.tm_sec)
  return f_name

def download(url, output_fn = None, check_size = True):
  import urllib.request
  import os

  def isSameFile(output_fn):
    r = False
    if output_fn and os.path.exists(output_fn):
      if check_size:
        file_size = int(urllib.request.urlopen(url).info().get('Content-Length', -1))
        r = file_size == os.path.getsize(output_fn)
      else:
        r = True
    return r

  #https://stackoverflow.com/a/13895723/227990
  def reporthook(blocknum, blocksize, totalsize):
    import sys
    readsofar = blocknum * blocksize
    if totalsize > 0:
        percent = readsofar * 1e2 / totalsize
        s = "\r%s %5.1f%% %*d / %d" % (
            url, percent, len(str(totalsize)), readsofar, totalsize)
        sys.stderr.write(s)
        if readsofar >= totalsize: # near the end
            sys.stderr.write("\n")
    else: # total size is unknown
        sys.stderr.write("read %d\n" % (readsofar,))

  if isSameFile(output_fn):
    print("{} already exists. Download skipping".format(output_fn))
    return

  ret_fn, headers = urllib.request.urlretrieve(url, output_fn, reporthook)

  if not output_fn:
    with open(ret_fn, "r") as f:
      r = f.read()
    os.remove(ret_fn)
    return r

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
