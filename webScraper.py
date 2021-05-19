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
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--incognito')
    options.add_argument('--headless')
    driver = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver", options=options)

    driver.get("https://www.imdb.com/title/tt0468569/reviews?ref_=tt_ov_rt")
    more_buttons = driver.find_element_by_class_name("moreLink")
    for x in range(len(more_buttons)):
        if more_buttons[x].is_displayed():
            driver.execute_script("arguments[0].click();",more_buttons[x])
            time.sleep(1)
    page_source = driver.page_source

    souper = BeautifulSoup(page_source,'lxml')

    counter = 0
    for item in souper.select(".review-container"):
        title = item.select(".title")[0].text
        review = item.select(".text")[0].text
        counter += 1
        print("Title: {}\n\nReview: {}\n\n".format(title, review))







    userReviewRatings = [tag.previous_element for tag in soup.find_all('span', attrs={'class': 'point-scale'})]

    n_index, p_index = minMax(list(map(int, userReviewRatings)))
    userReviewList = soup.find_all('a', attrs={'class': 'title'})
    userReviewFinal = []

    """
    for i in range(len(userReviewList)):
        temp = userReviewList[i]
        newLink = "https://www.imdb.com" + temp['href']
        userReviewFinal.append(newLink)
    """

    n_review = userReviewList[n_index]
    p_review = userReviewList[p_index]

    n_review_link = "https://www.imdb.com" + n_review['href']
    p_review_link = "https://www.imdb.com" + p_review['href']

    return n_review_link, p_review_link


global count
count = 0


def getReviewText(review_url):
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


def minMax(a):
    minpos = a.index(min(a))
    maxpos = a.index(max(a))

    return minpos, maxpos


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

    movie_review_list = list(itertools.chain(*movie_review_list))

    print("There are a total of " + str(len(movie_review_list)) + " individual movie reviews")
    print("Displaying 10 reviews")
    print(movie_review_list[:10])

    reviewText = [getReviewText(url) for url in movie_review_list]

    movieTitles = [getMovieTitle(url) for url in movie_review_list]

    review_sentiment = np.array(['negative', 'positive'] * (len(movie_review_list)//2))

    df = pd.DataFrame({'Movie': movieTitles, 'Link to Review': movie_review_list, 'User Review': reviewText, 'Sentiment':review_sentiment})

    # df.head()

    df.to_csv('UserReviewsComedy_BadSorta.csv', index=False)

    csvFile = 'UserReviewsComedy_BadSorta.csv'

    csvTotext(csvFile)
    print("Finish")
