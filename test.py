import spacy
from spacy import displacy

#DEPENDENCY
text = "When Sebastian Thrun started working on self-driving cars at Google in 2007, few people outside of the company took him seriously."

#used for dependency visualization
nlp = spacy.load("en_core_web_sm")
doc = nlp(text)
#displacy.serve(doc, style="dep")
#serves on http://127.0.0.1:5000/

import re

#TOKENIZATION
with open('GenreReviews/BadActionReviews/badDunkirk.txt', encoding='utf8') as f:
    text = f.read()
    text = text.lower()
    text = re.sub(r'\?+', '.', text)
    text = re.sub(r'\!+', '.', text)
    text = re.sub(r'\.+', '.', text)
    print(text)
    print('---------------')
    doc = nlp(text)
    for token in doc:
        if token.
    sentences = list(doc.sents)
    for i in sentences:
        print('|' , i , '|')

#DEPENDENCY PARSING
text = 'this Film had great acting.'
doc = nlp(text)
for token in doc:
    if token.is_punct:
        print(token, ' is a punct!')
for token in doc:
    print(token.text, token.tag_, token.head.text, token.dep_)