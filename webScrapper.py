import requests 
from selenium import webdriver
import webbrowser, time

#file_name = input("Enter manga filename: ")
with open('manga_list.txt', 'r') as f:
	file_contents = f.readlines()

#current_chapters_file = input("Enter chapter filename: ")
current_chapters_file = 'chaps.txt'
with open('chaps.txt', 'r') as f:
	current_chapters = f.readlines()

#return_file = input("Enter return file: ")
return_file = 'todays_manga.txt'

today_manga_list = []

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")

PATH = '/Users/maheshvegiraju/Desktop/manganelo_Scrapper/manganeloScraper/chromedriver'
driver = webdriver.Chrome(PATH, options = chrome_options)

for i, url in enumerate(file_contents):
	driver.get(url)
	latest_chapter = driver.find_elements_by_xpath('/html/body/div[1]/div[3]/div[1]/div[4]/ul/li[1]/a')[0]
	chapter_title = latest_chapter.get_attribute('href')
	chapter_title = chapter_title.split('_')
	chapter_num = chapter_title[-1]
	if (chapter_num > current_chapters[i]):
		current_chapters[i] = chapter_num + '\n'
		today_manga_list.append(latest_chapter.get_attribute('href'))
with open(return_file, 'w+') as f:
	f.truncate(0)
	for link in today_manga_list:
		f.writelines(link + '\n')
with open(current_chapters_file, 'w+') as f:
	f.truncate(0)
	for chapter in current_chapters: 
		f.writelines(chapter)
driver.quit()

with open(return_file, 'r') as f:
	for i, link in enumerate(f):
		if i == 0:
			webbrowser.open(link.rstrip(), new = 1)
		else:
			webbrowser.open(link.rstrip(), new = 2)