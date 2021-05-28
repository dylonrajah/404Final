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

    driver.find_element_by_xpath("/html/body/div[4]/div/div[2]/div[3]/div[1]/section/div[2]/div[4]/div/button").click()
    #driver.find_element_by_xpath("/html/body/div[4]/div/div[2]/div[3]/div[1]/section/div[2]/div[4]/div/button").click()


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
        for j in range((len(total[i]))):
            longString = longString + total[i][j]

    text_file = open(type + genre + ".txt", "w")
    n = text_file.write(longString)
    text_file.close()


if __name__ == "__main__":



    totalGood = []
    totalBad = []



    movie = "grown ups"






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
    driver.find_element_by_xpath("/html/body/div[7]/div/div[9]/div[1]/div/div[2]/div[2]/div/div/div[1]/div/div/div/div/div/div[1]/a").click()
    driver.implicitly_wait(20)

    # Click the user reviews
    driver.find_element_by_xpath(
            "/html/body/div[4]/div/div[2]/div[5]/div[1]/div[2]/div/div[1]/div[1]/div[1]/a[3]").click()

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

    createText(totalGood,movie,"good")
    createText(totalBad,movie,"bad")
