from msilib.schema import tables
from os import link
from tkinter import wantobjects
from unicodedata import name
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import csv

new_chapters = []
current_manga = []
manga_website = "https://mangakakalot.com/"

with open('manga.txt', 'r') as f:
    driver = webdriver.Firefox(executable_path="./geckodriver")
    driver.get(manga_website)
    search_bar = driver.find_element_by_class_name("searchi")
    for line in csv.reader(f, delimiter="\t"):
        search_bar.send_keys(line[0])
        time.sleep(1.5)
        result = driver.find_element_by_xpath("//div[@id='search_result']/ul/a[1]").get_attribute("href")
        driver.execute_script("window.open('');")
        driver.switch_to.window(driver.window_handles[1])
        driver.get(result)
        time.sleep(2)
        latest_chap = driver.find_element_by_xpath("//div[@class='panel-story-chapter-list']/ul/li[1]/a").text
        # latest_chap = driver.find_element_by_xpath("//div[@class='chapter-list']/div/span/a[1]").get_attribute("href") # for mangakakalot
        print(latest_chap)
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        time.sleep(2)

        # current plan for the scrapper
        # go to the base website
        # for every manga
        #     search for the manga name
        #     assume that the first reccomdation is the manga that we want and get its link
        #     open new tab 
        #     open the said url on that tab
        #     if the url is manganelo using manganelo xpath
        #         find the current chapter
        #     elif the url is mangakakalot
        #         find the current chapter using mangakakalot xpath
        #     compare current chapter to stored stored chapter
        #         if greater, then add the link to current chapter to new_chapters, and update value in the file
        #         else continue

        # close current driver
        # open new driver and open up all the links in new chapters

            
    driver.close()
            