import time
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
import re
from selenium import webdriver
import pandas as pd
import numpy as np
import itertools
import csv

pd.options.display.max_colwidth = 500


def getSoup(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    return soup


def getReviews(soup):
    userReviewList = soup.find_all('a', attrs={'class': 'title'})
    userReviewFinal = []

    for i in range(len(userReviewList)):
        temp = userReviewList[i]
        newLink = "https://www.imdb.com" + temp['href']
        userReviewFinal.append(newLink)

    return userReviewFinal


global count
count = 0


def getReviewText(review_url):
    print(review_url)
    global count
    soup = getSoup(review_url)
    count += 1
    print(count)
    tag = soup.find('div', attrs={'class': 'text show-more__control'})
    print(type(tag))
    return tag.getText()


def getMovieTitle(review_url):
    soup = getSoup(review_url)
    tag = soup.find('h1')
    print("--------------" + list(tag.children)[1].getText() + "-----------------------")
    return list(tag.children)[1].getText()


def csvTotext(csvFile):
    movie_list = []
    lines_list = []
    review_line = ' '

    with open(csvFile) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        stringy = " "
        for row in csv_reader:
            if line_count == 0:
                print(f'Column names are {", ".join(row)}')
                line_count += 1
            else:
                if row[0] not in movie_list:
                    movie_list.append(row[0])

                temp = row[2]

                temp = temp.lower()
                # temp = ''.join([i for i in temp if not i.isdigit()])   #This line removes numbers if we want that
                stringy = stringy + " " + temp

                line_count += 1
        print(f'Processed {line_count} lines.')

        with open('badComedySorta.txt', 'w') as textFile:
            textFile.write(stringy)


if __name__ == "__main__":
    url = "https://www.imdb.com/search/title/?title_type=feature&user_rating=0.0,10.0&num_votes=50000,&genres=thriller&view=simple&sort=user_rating,asc "

    movies = getSoup(url)

    movies = movies.find_all('a', attrs={'class': None})

    movies = [tag.attrs['href'] for tag in movies
              if tag.attrs['href'].startswith('/title') & tag.attrs['href'].endswith('/')]

    movies = list(dict.fromkeys(movies))

    print("There are a total of " + str(len(movies)) + " movie titles")
    print("Displaying 10 titles")
    print(movies[:10])

    base_url = "https://www.imdb.com"
    movie_links = [base_url + tag + 'reviews' for tag in movies]

    print("There are a total of " + str(len(movies)) + " movie user reviews")
    print("Displaying 10 reviews")
    print(movie_links[:10])

    movie_soup = [getSoup(link) for link in movie_links]

    movie_review_list = [getReviews(movie_soup) for movie_soup in movie_soup]
    print(len(movie_review_list))

    print("There are a total of " + str(len(movie_review_list)) + " individual movie reviews")
    print("Displaying 10 reviews")
    print(movie_review_list[:10])



    reviewText = [getReviewText(url) for url in movie_review_list]

    movieTitles = [getMovieTitle(url) for url in movie_review_list]

    df = pd.DataFrame({'Movie': movieTitles, 'Link to Review': movie_review_list, 'User Review': reviewText})

    # df.head()

    df.to_csv('UserReviewsComedy_BadSorta.csv', index=False)

    csvFile = 'UserReviewsComedy_BadSorta.csv'

    csvTotext(csvFile)
    print("Finish")
