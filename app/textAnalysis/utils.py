import re
from htmlentitydefs import name2codepoint
from nltk import clean_html
import os


def unescape(text):
    def fixup(m):
        text = m.group(0)
        if text[:2] == "&#":
            # character reference
            try:
                if text[:3] == "&#x":
                    return unichr(int(text[3:-1], 16))
                else:
                    return unichr(int(text[2:-1]))
            except ValueError:
                pass
        else:
            try:
                text = unichr(name2codepoint[text[1:-1]])
            except KeyError:
                pass
        return text # leave as is
    return re.sub("&#?\w+;", fixup, text)

def clean(text):
    text = clean_html(text)
    text = unescape(text)
    text = re.sub(r"[.,_+=)(*&\^/?><:;!@#$%\]\}\[\{\"\'\~\`]", r' ', text)
    return text


def stopwords():
    stwordfile = os.path.abspath(os.path.dirname('.'))+"/textAnalysis/stopwords.txt"  
    words = open(stwordfile,'r').read().decode('utf-8')
    return set(words.split())
    
# def words(corpus):
#     words = []
#     documents = corpus
#     for (d,c) in documents:
#         words += d
#     return words