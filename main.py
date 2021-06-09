import os
import re
import nltk
nltk.download('averaged_perceptron_tagger')
import spacy
from spacy import displacy
#nlp = spacy.load("en_core_web_trf")
nlp = spacy.load("en_core_web_sm")

#TODO
#get more aspect words
#filter out unwanted matches based on depencency
#combine good and bad reviews?
#finalize conclusions:
    #What aspects do people comment on for each genre
    #Common aspects among movies
    #common aspects among genres
    #Talk about similarities?
#final report

#aspect and their terms
aspects = ['Screenplay', 'Music', 'Acting', 'Plot', 'Movie', 'Direction']
aspect_words = [
    ['scene', 'scenery', 'animation', 'violence', 'screenplay', 'action', 'animation', 'shot', 'visual', 'prop', 'camera', 'graphic', 'stunt', 'special effect', 'violent', 'violence'],
    ['music', 'score', 'lyric', 'sound', 'audio', 'musical', 'title track', 'sound effect', 'sound track', 'song'],
    ['acting', 'role playing', 'act', 'actress', 'actor', 'role', 'portray', 'character', 'villian', 'performance', 'performed', 'played', 'casting', 'cast'],
    ['plot', 'story', 'storyline', 'tale', 'romance', 'dialog', 'script', 'storyteller', 'ending', 'storytelling', 'revenge', 'betrayal', 'writing', 'twist', 'drama', 'dialogue'],
    ['movie', 'film', 'picture', 'moving picture', 'motion picture', 'show', 'picture show', 'pic', 'flick', 'romantic comedy', 'filmography'],
    ['directing', 'direct', 'direction', 'director', 'filmed', 'filming', 'film making', 'filmmaker', 'cinematic', 'edition', 'cinematography', 'edition', 'rendition']
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

#load opinion words
def get_opinion_lists():
    with open('Opinions/positiveWords.txt') as f:
        positive = f.read().splitlines()
    with open('Opinions/negativeWords.txt') as f:
        negative = f.read().splitlines()[31:]
    return positive, negative

positive_words, negative_words = get_opinion_lists()

class Movie:
    def __init__(self, title, goodReviewTxt, badReviewTxt):
        self.title = title
        self.goodReview = goodReviewTxt
        self.badReview = badReviewTxt
    
    def set_scores(self, goodPositiveScores, goodNegativeScores, badPositiveScores, badNegativeScores):
        self.goodPositiveScores = goodPositiveScores
        self.goodNegativeScores = goodNegativeScores
        self.badPositiveScores = badPositiveScores
        self.badNegativeScores = badNegativeScores

#preprocesses review and loads it in
def load_review(filePath):
    review = ""
    with open(filePath, encoding='utf8') as f:
        review = f.read()
        review = review.lower()
        review = re.sub(r'\?+', '.', review)
        review = re.sub(r'\!+', '.', review)
        review = re.sub(r'\.+', '.', review)
    return review

#populates list of Review classes that contains good and bad reviews for each movie in the genre
def get_movies(genreString):
    #get title names
    titleList = []
    with os.scandir('MoreReviewsPerMovie/'+genreString+'/Good') as entries:
        for entry in entries:
            titleList.append(entry.name[:-4])
    #create Review classes
    movieList = []
    for title in titleList:
        goodReview = load_review('MoreReviewsPerMovie/'+genreString+'/Good/'+title+'.txt')
        badReview = load_review('MoreReviewsPerMovie/'+genreString+'/Bad/'+title+'.txt')
        movie = Movie(title, goodReview, badReview)
        movieList.append(movie)
    return movieList

#extract opinion based aspect scores for a movie
def model(movie):
    goodDoc = nlp(movie.goodReview)
    badDoc = nlp(movie.badReview)
    goodSentences = list(goodDoc.sents)
    badSentences = list(badDoc.sents)
    goodPositiveScores = [0, 0, 0, 0, 0, 0]
    goodNegativeScores = [0, 0, 0, 0, 0, 0]
    badPositiveScores = [0, 0, 0, 0, 0, 0]
    badNegativeScores = [0, 0, 0, 0, 0, 0]
    for sentence in goodSentences:
        if len(sentence) > 2:
            for token in sentence:
                for child in token.children:
                    if child.text in positive_words:
                        for i in range(len(aspect_words)):
                            if token.text in aspect_words[i]:
                                goodPositiveScores[i] += 1
                    if child.text in negative_words:
                        for i in range(len(aspect_words)):
                            if token.text in aspect_words[i]:
                                goodNegativeScores[i] += 1
    for sentence in badSentences:
        if len(sentence) > 2:
            for token in sentence:
                for child in token.children:
                    if child.text in positive_words:
                        for i in range(len(aspect_words)):
                            if token.text in aspect_words[i]:
                                badPositiveScores[i] += 1
                    if child.text in negative_words:
                        for i in range(len(aspect_words)):
                            if token.text in aspect_words[i]:
                                badNegativeScores[i] += 1

    movie.set_scores(goodPositiveScores, goodNegativeScores, badPositiveScores, badNegativeScores)

if __name__ == '__main__':
    #load movies
    actionMovies = get_movies('Action')
    comedyMovies = get_movies('Comedy')
    #horrorMovies = get_movies('Horror')
    romanceMovies = get_movies('Romance')
    scifiMovies = get_movies('SciFi')

    #evaluate aspect opinions using our model
    for i in range(len(actionMovies)):
        model(actionMovies[i])
        model(comedyMovies[i])
        model(romanceMovies[i])
        model(scifiMovies[i])

    #display results