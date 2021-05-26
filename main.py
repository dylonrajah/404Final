def load_reviews():
    badActionList = []
    badActionString = ""
    with open('CombinedVocabs/badAction.txt', 'r') as badAction:
        for line in badAction:
            badActionString += remove_combined_words(line) + " "
        badActionList.append(badActionString)
    print(badActionList)

def remove_combined_words(sentence):
    output = ""
    splitSentence = sentence.split(' ')
    for i in splitSentence:
        if i[1:] != i[1:].lower() and i[1:] != i[1:].upper():
            for j in range(1, len(i[1:])):
                if i[j] == i[j].upper() and i[j-1] == i[j-1].lower():
                    output += i[:j].lower() + " "
                    output += i[j:].lower() + " "
                    break
        else:
            output += i.lower() + " "
    return output


if __name__ == '__main__':

    sentence = "one two three fourFive six"
    print(remove_combined_words(sentence))

    load_reviews()
    #badAction, badComedy, badHorror, badRomance, badSciFi, goodAction, goodComedy, goodHorror, goodRomance, goodSciFi = load_reviews()