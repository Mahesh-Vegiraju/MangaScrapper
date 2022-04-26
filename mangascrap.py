import sys
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import csv

new_chapters = [] # list of the new chapter urls to open at the end of the program
current_manga = [] # list of the rewritten values of the chapters
manga_website = "https://mangakakalot.com/"

with open('manga.txt', 'r+') as f:
    driver = webdriver.Firefox(executable_path="./geckodriver")
    driver.get(manga_website)
    search_bar = driver.find_element_by_class_name("searchi")

    for line in csv.reader(f, delimiter="\t"):

        search_bar.send_keys(line[0])

        time.sleep(1.5) # waiting for list to show up, should probably change this to waiting dynamic time rather than static

        result = driver.find_element_by_xpath("//div[@id='search_result']/ul/a[1]").get_attribute("href") # the link of the first result of the search
        driver.execute_script("window.open('');") # open new tab
        driver.switch_to.window(driver.window_handles[1]) # switch to new tab
        driver.get(result) # open the link of the first result

        time.sleep(2) # wait for chapter list to load, might not need this
        latest_chap = ""

        if "manganato" in result:
            print("manganato")
            latest_chap = driver.find_element_by_xpath("//div[@class='panel-story-chapter-list']/ul/li[1]/a").text.split(' ')[1]
        elif "mangakakalot" in result:
            print("mangakakalot")
            # latest_chap = driver.find_element_by_xpath("//div[@class='chapter-list']/div/span/a[1]").get_attribute("href") # for mangakakalot
        elif "manganelo" in result:
            print("manganelo")
        else:
            print("not programmed for this website: " + result)
            driver.close()
            sys.exit()
  
        if (latest_chap > line[1]):

            current_manga.append(line[0] + '\t' + latest_chap + '\n') # updating the manga.txt file
            new_chapters.append(driver.find_element_by_xpath("//div[@class='panel-story-chapter-list']/ul/li[1]/a").get_attribute("href")) # adding chapter link to new_chapters

        elif (latest_chap <= line[1]):

            current_manga.append(line[0] + '\t' + line[1]  + '\n') # updating the manga.txt file
            print("all caught up on " + line[0])

        driver.close() # close tab and switch to the search tab
        driver.switch_to.window(driver.window_handles[0])

        time.sleep(2) # can get rid of this, only there for debugging

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

    for i in new_chapters:
        driver.execute_script("window.open('');") # open new tab
        driver.switch_to.window(driver.window_handles[1]) # switch to new tab
        driver.get(i) # open the link of the first result

    f.seek(0)
    f.truncate(0)
    f.seek(0)
    for i in current_manga:
        f.write(i)

    time.sleep(2)
    driver.quit()


            