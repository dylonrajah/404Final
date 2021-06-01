import re
import nltk
nltk.download('averaged_perceptron_tagger')

aspects = ['Screenplay', 'Music', 'Acting', 'Plot', 'Movie', 'Direction']
aspect_words = [
    ['scene', 'scenery', 'animation', 'violence', 'screenplay', 'action', 'animation', 'shot', 'visual', 'prop', 'camera', 'graphic', 'stunt', 'special effect', 'violent', 'violence'],
    ['music', 'score', 'lyric', 'sound', 'audio', 'musical', 'title track', 'sound effect', 'sound track', 'song'],
    ['acting', 'role playing', 'act', 'actress', 'actor', 'role', 'portray', 'character', 'villian', 'performance', 'performed', 'played', 'casting', 'cast'],
    ['plot', 'story', 'storyline', 'tale', 'romance', 'dialog', 'script', 'storyteller', 'ending', 'storytelling', 'revenge', 'betrayal', 'writing', 'twist', 'drama', 'dialogue'],
    ['movie', 'film', 'picture', 'moving picture', 'motion picture', 'show', 'picture show', 'pic', 'flick', 'romantic comedy', 'filmography'],
    ['directing', 'direct', 'direction', 'director', 'filmed', 'filming', 'film making', 'filmmaker', 'cinematic', 'edition', 'cinematography', 'edition', 'rendition']
]

#What aspects do people comment on for each genre
#Common aspects among movies
#common aspects among genres
#Talk about similarities?




def load_review(filePath):
    output = ""
    with open(filePath, encoding='utf8') as file:
        output = file.read().replace('\n', '')
        output = re.sub(r'\?+', '.', output)
        output = re.sub(r'\!+', '.', output)
        output = re.sub(r'\.+', '.', output)
        outputList = output.split(".")
    emptyIndices = []
    for i in range(len(outputList)):
        outputList[i] = outputList[i].strip()
        outputList[i] = outputList[i].lower()
        if outputList[i] == '':
            emptyIndices.append(i)
    for i in range(len(emptyIndices)):
        del outputList[emptyIndices[-(i+1)]]

    outputListTagged = []
    for i in range(len(outputList)):
        tokenizedSentence = nltk.word_tokenize(outputList[i])
        outputListTagged.append(nltk.pos_tag(tokenizedSentence))

    return outputListTagged

def extract_tags(taggedList):
    nouns = []
    for i in taggedList:
        for j in i:
            #print(j[1][0])
            if j[1][0] == 'N':
                nouns.append(j[0])

    return nouns

#def countAspectWords(list):
    #for i in list:


if __name__ == '__main__':

    badActionTags = load_review('CombinedVocabs/badAction.txt')
    goodDunkirk = load_review('GenreReviews/GoodActionReviews/goodDunkirk.txt')

    #for i in goodDunkirk:
        #print(i)

    extractedGoodDunkirk = extract_tags(goodDunkirk)
    print(extractedGoodDunkirk)
    #countAspectWords(extractedGoodDunkirk)


    
    badComedyTags = load_review('CombinedVocabs/badComedy.txt')
    badHorrorTags = load_review('CombinedVocabs/badHorror.txt')
    badRomanceTags = load_review('CombinedVocabs/badRomance.txt')
    badSciFiTags = load_review('CombinedVocabs/badSciFi.txt')
    goodActionTags = load_review('CombinedVocabs/goodAction.txt')
    goodComedyTags = load_review('CombinedVocabs/goodComedy.txt')
    goodHorrorTags = load_review('CombinedVocabs/goodHorror.txt')
    goodRomanceTags = load_review('CombinedVocabs/goodRomance.txt')
    goodSciFiTags = load_review('CombinedVocabs/goodSciFi.txt')