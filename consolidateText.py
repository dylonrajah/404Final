import glob


def combine(path,name):


    read_files = glob.glob(path + "*.txt")

    with open(name, "wb") as outfile:
        for f in read_files:
            with open(f, "rb") as infile:
                outfile.write(infile.read())









if __name__ == "__main__":
    path = "/Users/dylonrajah/Desktop/404Final/GoodHorrorReviews/"
    combine(path,"goodHorror.txt")