import requests 
from selenium import webdriver

file_name = input("Enter manga filename: ")
with open(file_name, 'r') as f:
	file_contents = f.readlines()

current_chapters_file = input("Enter chapter filename: ")
with open(current_chapters_file, 'r') as f:
	current_chapters = f.readlines()

return_file = input("Enter return file: ")

PATH = '/Users/maheshvegiraju/Desktop/manganelo_Scrapper/manganeloScraper/chromedriver'
driver = webdriver.Chrome(PATH)

for i, url in enumerate(file_contents):
	driver.get(url)
	latest_chapter = driver.find_elements_by_xpath('/html/body/div[1]/div[3]/div[1]/div[4]/ul/li[1]/a')[0]
	chapter_title = latest_chapter.get_attribute('title')
	chapter_num = chapter_title.split(' ')[-1]
	if (chapter_num > current_chapters[i]):
		with open(current_chapters_file, 'w') as current_chapter:
			for j, chapter in enumerate(current_chapters):
				if j == i:
					print('hi')
					current_chapter.writelines(chapter_num)
				else:
					print('hello')
					current_chapter.writelines(chapter)
	with open(return_file, 'w') as f:
		f.writelines(latest_chapter.get_attribute('href') + '\n')

