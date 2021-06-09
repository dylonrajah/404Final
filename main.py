import os
import re
import nltk
nltk.download('averaged_perceptron_tagger')
import spacy
from spacy import displacy
nlp = spacy.load("en_core_web_trf")

#load all the reviews in a usable way for use in the model
#get more aspect words
#filter out unwanted matches based on depencency
#bring model from test.py to main.py
#tally/evaluate results
#finalize conclusions:
    #What aspects do people comment on for each genre
    #Common aspects among movies
    #common aspects among genres
    #Talk about similarities?
#final report

aspects = ['Screenplay', 'Music', 'Acting', 'Plot', 'Movie', 'Direction']
aspect_words = [
    ['scene', 'scenery', 'animation', 'violence', 'screenplay', 'action', 'animation', 'shot', 'visual', 'prop', 'camera', 'graphic', 'stunt', 'special effect', 'violent', 'violence'],
    ['music', 'score', 'lyric', 'sound', 'audio', 'musical', 'title track', 'sound effect', 'sound track', 'song'],
    ['acting', 'role playing', 'act', 'actress', 'actor', 'role', 'portray', 'character', 'villian', 'performance', 'performed', 'played', 'casting', 'cast'],
    ['plot', 'story', 'storyline', 'tale', 'romance', 'dialog', 'script', 'storyteller', 'ending', 'storytelling', 'revenge', 'betrayal', 'writing', 'twist', 'drama', 'dialogue'],
    ['movie', 'film', 'picture', 'moving picture', 'motion picture', 'show', 'picture show', 'pic', 'flick', 'romantic comedy', 'filmography'],
    ['directing', 'direct', 'direction', 'director', 'filmed', 'filming', 'film making', 'filmmaker', 'cinematic', 'edition', 'cinematography', 'edition', 'rendition']
]

class Movie:
    def __init__(self, title, goodReviewTxt, badReviewTxt):
        self.title = title
        self.goodReview = goodReviewTxt
        self.badReview = badReviewTxt
    
    def set_scores(self, scores):
        self.scores = scores

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

if __name__ == '__main__':
    #load movies
    actionMovies = get_movies('Action')
    comedyMovies = get_movies('Comedy')
    horrorMovies = get_movies('Horror')
    romanceMovies = get_movies('Romance')
    scifiMovies = get_movies('SciFi')
    
    #evaluate aspect opinions using our model

    #display results