import re
import nltk
nltk.download('averaged_perceptron_tagger')

aspects = ['Screenplay', 'Music', 'Acting', 'Plot', 'Movie', 'Direction']
aspect_words = [
    ['scene', 'scenery', 'animation', 'violence', 'screenplay', 'action', 'animation', 'shot', 'visual', 'prop', 'camera', 'graphic', 'stunt', 'special effect', 'violent', 'violence'],
    ['music', 'score', 'lyric', 'sound', 'audio', 'musical', 'title track', 'sound effect', 'sound track', 'song'],
    ['acting', 'role playing', 'act', 'actress', 'actor', 'role', 'potray', 'character', 'villian', 'performance', 'performed', 'played', 'casting', 'cast'],
    ['plot', 'story', 'storyline', 'tale', 'romance', 'dialog', 'script', 'storyteller', 'ending', 'storytelling', 'revenge', 'betrayal', 'writing', 'twist', 'drama', 'dialog'],
    ['movie', 'film', 'picture', 'moving picture', 'motion picture', 'show', 'picture show', 'pic', 'flick', 'romantic comedy'],
    ['directing', 'direct', 'direction', 'director', 'filmed', 'filming', 'film making', 'filmmaker', 'cinematic', 'edition', 'cinematography', 'edition', 'rendition']
]

def load_review(fileName):
    output = ""
    with open('CombinedVocabs/' + fileName) as badAction:
        output = badAction.read().replace('\n', '')
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

if __name__ == '__main__':
    badActionTags = load_review('badAction.txt')
    badComedyTags = load_review('badComedy.txt')
    badHorrorTags = load_review('badHorror.txt')
    badRomanceTags = load_review('badRomance.txt')
    badSciFiTags = load_review('badSciFi.txt')
    goodActionTags = load_review('goodAction.txt')
    goodComedyTags = load_review('goodComedy.txt')
    goodHorrorTags = load_review('goodHorror.txt')
    goodRomanceTags = load_review('goodRomance.txt')
    goodSciFiTags = load_review('goodSciFi.txt')