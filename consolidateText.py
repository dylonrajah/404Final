import glob
import re
import textwrap


def combine(path, name):
    read_files = glob.glob(path + "*.txt")

    with open(name, "wb") as outfile:
        for f in read_files:
            with open(f, "rb") as infile:
                outfile.write(infile.read())


def removePunc(path):
    file1 = open(path, 'r')
    Lines = file1.readlines()
    my_file = open("goodHorror.txt", "w")

    count = 0
    # Strips the newline character
    for line in Lines:
        count += 1
        res = re.sub(r'[^\w\s]', '', line)
        res = '\n'.join(textwrap.wrap(res, 100, break_long_words=False))
        my_file.write(res)



if __name__ == "__main__":
    path = "/Users/dylonrajah/Desktop/404Final/MoreReviewsPerMovie/SciFi/Good/"
    combine(path,"newGoodSciFi.txt")
    #removePunc(path)
