import requests
from bs4 import BeautifulSoup
from nltk.sentiment import SentimentIntensityAnalyzer
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd

from textblob import TextBlob
import time


def getReviews(url):

    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    all = soup.find(id="main")

    # Get the title of the movie
    # all = soup.find(id="main")
    parent = all.find(class_="parent")
    name = parent.find(itemprop="name")
    url = name.find(itemprop='url')
    film_title = url.get_text()
    print(film_title)

    # Get the title of the review
    title_rev = all.select(".title")
    title = [t.get_text().replace("\n", "") for t in title_rev]

    # for i in range(len(title)):
    # print(title[i])

    # Get the review
    review_rev = all.select(".content .text")
    review = [r.get_text() for r in review_rev]

    return review


def createText(total, genre, type):
    longString = ""
    for i in range(len(total)):
        longString = longString + total[i]

    text_file = open(type + genre + ".txt", "w")
    n = text_file.write(longString)
    text_file.close()


if __name__ == "__main__":

    genre = "Action"
    moviesList = ["The Dark Knight", "Inception", "The Matrix", "Gladiator", "OldBoy"]

    totalGood = []
    totalBad = []

    for movie in moviesList:
        # Set the web browser
        driver = webdriver.Chrome(executable_path=r"/Users/dylonrajah/Desktop/404Final/chromedriver")

        # Go to Google
        driver.get("https://www.google.com/")

        # Enter the keyword
        driver.find_element_by_name("q").send_keys(movie + " imdb")
        time.sleep(3)

        # Click the google search button
        driver.find_element_by_name("btnK").send_keys(Keys.ENTER)
        time.sleep(3)

        # Click the link
        driver.implicitly_wait(20)
        driver.find_element_by_class_name("yuRUbf").click()
        driver.implicitly_wait(20)
        print("here??")

        # Click the user reviews
        driver.find_element_by_xpath(
            "/html/body/div[4]/div/div[2]/div[5]/div[1]/div[2]/div/div[2]/div[3]/div[1]/div[2]/span/a[1]").click()

        # Scrap IMBD review

        driver.implicitly_wait(20)
        driver.find_element_by_xpath(
            "/html/body/div[4]/div/div[2]/div[3]/div[1]/section/div[2]/div[1]/form/div/div[3]/select/option[11]").click()

        goodUrl = driver.current_url
        goodReview = getReviews(goodUrl)
        totalGood.append(goodReview)

        driver.implicitly_wait(20)
        driver.find_element_by_xpath(
            "/html/body/div[4]/div/div[2]/div[3]/div[1]/section/div[2]/div[1]/form/div/div[3]/select/option[2]").click()


        badUrl = driver.current_url
        badReview = getReviews(badUrl)
        totalBad.append(badReview)

        driver.close()

    createText(totalGood,genre,"good")
    createText(totalBad,genre,"bad")
