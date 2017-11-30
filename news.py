#!/usr/bin/python3

# -*- coding: utf-8 -*-

import http.client, urllib.parse, json
import nltk

# Verify the endpoint URI.  At this writing, only one endpoint is used for Bing
# search APIs.  In the future, regional endpoints may be available.  If you
# encounter unexpected authorization errors, double-check this value against
# the endpoint for your Bing Web search instance in your Azure dashboard.
host = "api.cognitive.microsoft.com"
path = "/bing/v7.0/news/search"

term = "Archer Daniels Midland"

class News:
  def __init__(self, key_file_name):
    self.key = self.GetAPIKey(key_file_name)

  def AssembleQuery(self, fields):
    query = "?"
    for k,v in fields.items():
      query += "{}={}&".format(k,v)
    return query[0:-1]

  def GetAPIKey(self, file_name):
    key = ""
    with open(file_name, "r") as f:
      key = str(f.read()).strip('\n')
    return key

  def BingWebSearch(self, search):
    "Performs a Bing Web search and returns the results."

    headers = {'Ocp-Apim-Subscription-Key': self.key}
    query = {'q' : urllib.parse.quote(search),
             'mkt' : 'en-us',
             'category' : 'Business',
             'sortBy' : 'Date'
            }
    print(self.AssembleQuery(query))
    conn = http.client.HTTPSConnection(host)
    conn.request("GET", path + self.AssembleQuery(query), headers=headers)
    response = conn.getresponse()
    headers = [k + ": " + v for (k, v) in response.getheaders()
                   if k.startswith("BingAPIs-") or k.startswith("X-MSEdge-")]
    return headers, response.read().decode("utf8")

  def RunExample(self, refresh_query=True):
    result = ""
    #refresh_query = False
    if refresh_query:
      print('Searching the Web for: ', term)
      headers, result = news.BingWebSearch(term)
      print("\nRelevant HTTP Headers:\n")
      print("\n".join(headers))
      print("\nJSON Response:\n")
      with open("cached_query", "w") as f:
        f.write(result)
    else:
      with open("cached_query", "r") as f:
        result = f.read()

    json_obj = json.loads(result)
    print(json.dumps(json_obj, indent=2))
  
news = News("bing-api.key")
news.RunExample(False)
