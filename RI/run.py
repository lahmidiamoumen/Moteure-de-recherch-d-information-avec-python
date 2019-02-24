import re
import collections
import math
from lxml import etree

#--- @auther: LAHMIDI Abdelmoumene UMBB MASTER 1 TI02  ---#
#--  [Finished in 6.6s] --#

def count(str): #retourne le nbr de voy-cons
    return len(re.sub('[aeiou]((?![aeiou0-9]))', " ", str).split()) - 1

def extract(str):
    full = re.sub("[^\w]", " ", str).split() # Toknesation
    regex = re.compile('[0-9]+')
    d = []
    for x in full:
        if regex.match(x) or x in stopWord: # Elimination des mots vides
            continue
        x = re.sub('sses$', 'es', x)  # Normalisation
        x = re.sub('ies$', 'i', x)
        x = re.sub('s$', '', x)
        if x.endswith("ed") and count(re.sub('ed$', "", x)) > 0:
            x = re.sub("ed$", "", x)
        if x.endswith("ing") and count(re.sub('ing$', "", x)) > 0:
            x = re.sub("ing$", "", x)
        x = re.sub('y$', "i", x)
        if x.endswith("ational") and count(re.sub('ational$', "", x)) > 0:
            x = re.sub("ational$", "at", x)
        if x.endswith("tional") and count(re.sub('tional$', "", x)) > 0:
            x = re.sub("tional$", "tion", x)
        if x.endswith("izer") and count(re.sub('izer$', "", x)) > 0:
            x = re.sub("izer$", "ize", x)
        if x.endswith("alize") and count(re.sub('alize$', "", x)) > 0:
            x = re.sub("alize$", "al", x)
        if x.endswith("ize") and count(re.sub('ize$', "", x)) > 0:
            x = re.sub("ize$", "", x)
        d.append(x)
    return collections.Counter(d)

docs = etree.parse("Corpus_OHSUMED.txt", parser=etree.XMLParser(recover=True)).getroot()
stopWord = re.sub("\n", " ", open("stoplist.txt", 'r').read()).split()
data = []
invertedIndex = []
fichierInverse = {}
poids = {}

for child in docs.iterfind('DOC'): # list of {DOCi,{TITLESi terms},{ABSTRACTi terms}}
    title = extract(str(child.find('TITLE').text).lower())
    abstract = extract(str(child.find('ABSTRACT').text).lower())
    for key, value in collections.defaultdict(lambda: title + abstract)[0].items(): # poids[ti] le nbr d'un terme ti dans tt la corpus
        poids[key] = poids.get(key, 0) + 1    
    data.append({'doc': child.find('DOCNO').text, 'title': title, 'abstract': abstract})
   
lenData = len(data) # 2001 nbr of docs inside corpus
for t in data:  # list of {DOCi,{DOCi terms}}
    for term in t['abstract']:
        t['abstract'][term] = math.log10(lenData / poids[term]) * t['abstract'][term] / len(t['abstract']) # abstract wiegth tf * idf
    totals = {}
    for key, value in collections.defaultdict(lambda: list(t['abstract'].items()) + list(t['title'].items()))[0]: # eliminer les termes duplique dans un DOCi 
        totals[key] = totals.get(key, 0) + value
    invertedIndex.append({'docId': t['doc'], 'term': totals})

for tt in invertedIndex: # fichierInverse -> inverted index structure list not sorted
    for token in tt['term']:
        fichierInverse.update({token: fichierInverse.get(token, [])+[{'doc': tt['docId'], 'poids': tt['term'][token]}] })

print('advanc :',fichierInverse['advanc']) # example of a given term 'advanc'
