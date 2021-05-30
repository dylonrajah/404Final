import spacy
from spacy import displacy

#opinion lexicon
#https://www.kaggle.com/nltkdata/opinion-lexicon

def get_opinion_dicts():
    with open('positive-words.txt') as f:
        positive = f.read().splitlines()[30:]
    with open('negative-words.txt') as f:
        negative = f.read().splitlines()[31:]
    return positive, negative

positive_words, negative_words = get_opinion_dicts()

#used for dependency visualization
nlp = spacy.load("en_core_web_sm")
#displacy.serve(doc, style="dep")
#serves on http://127.0.0.1:5000/

import re

#TOKENIZATION and DEPENDENCY PARSING on reviews
with open('GenreReviews/BadActionReviews/badDunkirk.txt', encoding='utf8') as f:
    text = f.read()
    text = text.lower()
    text = re.sub(r'\?+', '.', text)
    text = re.sub(r'\!+', '.', text)
    text = re.sub(r'\.+', '.', text)
    #print(text)
    print('---------------')
    doc = nlp(text)
    sentences = list(doc.sents)
    #displacy.serve(sentences, style="dep")
    for sentence in sentences:
        print('|' , sentence , '|')
        for token in sentence:
            #print(token.text, token.tag_, token.head.text, token.dep_)
            if token.text in positive_words:
                print(token, ': pos')
            if token.text in negative_words:
                print(token, ': neg')

#DEPENDENCY PARSING EXAMPLE
text = 'this Film had great acting.'
doc = nlp(text)
for token in doc:
    print(token.text, token.tag_, token.head.text, token.dep_)