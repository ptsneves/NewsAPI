
class NewsTagger(nltk.tag.api.TaggerI):
  NewsTagger.FLOATING_POINT_REGEX = (r'[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?.', 'NUM')

  def __init__(self, autosave=False):
    from nltk.corpus import brown
    brownTaggedSents = brown.taggedSents(categories='news')

    self.tDefault = nltk.DefaultTagger('None')
    self.tRegexp = nltk.RegexpTagger([FLOATING_POINT_REGEX], backoff = tDefault)
    self.tBigram = nltk.BigramTagger(brownTaggedSents, backoff = tRegexp)
    print(tBigram.tagSents(untaggedSentences))

    self.autosave = autosave

  def loadFromFile(newsTaggerPickleFile):
    with open(newsTaggerPickleFile) as f:
      return pickle.load(f)

  def saveToFile(self,fileName):
    with open(fileName, 'w') as f:
      pickle.dump(self)

  def __enter__(self, autosave = True):
    self.autosave = autosave

  def __exit__(self):
    if self.autosave:
      saveToFile(
NewsTagger t(true)

