
import spacy
from spacy import displacy

# better preprocessing (remove numbers, fix joining of seperate words)
# detecting incorrect dependency from opinion words EX: plot NN twist compound
# add movie to movie aspect words

# opinion lexicon
# https://www.kaggle.com/nltkdata/opinion-lexicon

aspects = ['Screenplay', 'Music', 'Acting', 'Plot', 'Movie', 'Direction']
aspect_words = [
    ['scene', 'scenery', 'animation', 'violence', 'screenplay', 'action', 'animation', 'shot', 'visual', 'prop',
     'camera', 'graphic', 'stunt', 'special effect', 'violent', 'violence'],
    ['music', 'score', 'lyric', 'sound', 'audio', 'musical', 'title track', 'sound effect', 'sound track', 'song'],
    ['acting', 'role playing', 'act', 'actress', 'actor', 'role', 'portray', 'character', 'villian', 'performance',
     'performed', 'played', 'casting', 'cast'],
    ['plot', 'story', 'storyline', 'tale', 'romance', 'dialog', 'script', 'storyteller', 'ending', 'storytelling',
     'revenge', 'betrayal', 'writing', 'twist', 'drama', 'dialogue'],
    ['movie', 'film', 'picture', 'moving picture', 'motion picture', 'show', 'picture show', 'pic', 'flick',
     'romantic comedy', 'filmography'],
    ['directing', 'direct', 'direction', 'director', 'filmed', 'filming', 'film making', 'filmmaker', 'cinematic',
     'edition', 'cinematography', 'edition', 'rendition']
]

aspect_words_combined = ['scene', 'scenery', 'animation', 'violence', 'screenplay', 'action', 'animation', 'shot',
                         'visual', 'prop', 'camera', 'graphic', 'stunt', 'special effect', 'violent', 'violence',
                         'music', 'score', 'lyric', 'sound', 'audio', 'musical', 'title track', 'sound effect',
                         'sound track', 'song', 'acting', 'role playing', 'act', 'actress', 'actor', 'role', 'portray',
                         'character', 'villian', 'performance', 'performed', 'played', 'casting', 'cast', 'plot',
                         'story', 'storyline', 'tale', 'romance', 'dialog', 'script', 'storyteller', 'ending',
                         'storytelling', 'revenge', 'betrayal', 'writing', 'twist', 'drama', 'dialogue', 'movie',
                         'film', 'picture', 'moving picture', 'motion picture', 'show', 'picture show', 'pic', 'flick',
                         'romantic comedy', 'filmography', 'directing', 'direct', 'direction', 'director', 'filmed',
                         'filming', 'film making', 'filmmaker', 'cinematic', 'edition', 'cinematography', 'edition',
                         'rendition']


def get_opinion_dicts():
    with open('positive-words.txt', 'rb') as f:
        positive = f.read().splitlines()[30:]
    with open('negative-words.txt', 'rb') as f:
        negative = f.read().splitlines()[31:]
    return positive, negative


positive_words, negative_words = get_opinion_dicts()

# used for dependency visualization
nlp = spacy.load("en_core_web_sm")
# displacy.serve(doc, style="dep")
# serves on http://127.0.0.1:5000/

import re

# TOKENIZATION and DEPENDENCY PARSING on reviews

with open('MoreReviewsPerMovie/Action/Bad/NewbadDunkirk.txt', encoding='utf8') as f:
    text = f.read()
    text = text.lower()
    text = re.sub(r'\?+', '.', text)
    text = re.sub(r'\!+', '.', text)
    text = re.sub(r'\.+', '.', text)
    # print(text)
    print('---------------')
    doc = nlp(text)
    sentences = list(doc.sents)
    # displacy.serve(sentences, style="dep")
    for sentence in sentences:
        if len(sentence) > 2:
            print('|', sentence, '|')
            for token in sentence:
                if token.text in positive_words:  # and token.head.text in aspect_words_combined:
                    print(token, ': pos')
                    print(token.text, token.tag_, token.head.text, token.dep_)
                if token.text in negative_words:  # and token.head.text in aspect_words_combined:
                    print(token, ': neg')
                    print(token.text, token.tag_, token.head.text, token.dep_)

# DEPENDENCY PARSING EXAMPLE
# text = 'this Film had great acting.'
# doc = nlp(text)
# for token in doc:
# print(token.text, token.tag_, token.head.text, token.dep_)
