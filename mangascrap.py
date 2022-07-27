import sys
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import csv

# Takes in a string that is the name of the file containing the mangas and the chapter numbers
# And returns a list of lists containing the manga name in the first position and the chapter num in the second
def get_mangas(manga: str) -> [[str, float]]:
	manga_num = []
	with open(manga, 'r+') as f:
		for line in csv.reader(f, delimiter="\t"):
			manga_num.append([line[0], line[1]])
	return manga_num

# Updates the manga file with the new chapters. Takes in the file name as well as the list of strings
# containing the updated names and chapter numbers. Does not return anything
def update_file(manga: str, to_write: [str]):
	with open(manga, 'r+') as f:
		f.seek(0)
		f.truncate(0)
		f.seek(0)

		for i in to_write:
			f.write(i)

# Given the name of a manga, this function will open all the chapters new chapters, even if there are multiple
# new chapters. It also takes in the current chapter number
def get_new_chapters_bulk(manga: str, current_chapter: str):
	chaps_to_open = []

	driver = webdriver.Firefox(executable_path="./geckodriver")
	driver.get("https://mangakakalot.com/")
	search_bar = driver.find_element_by_class_name("searchi")

	search_bar.send_keys(manga)
	time.sleep(1.5)
	result = driver.find_element_by_xpath("//div[@id='search_result']/ul/a[1]").get_attribute("href") # the link of the first result of the search

	search_bar.clear()
	driver.execute_script("window.open('');")
	driver.switch_to.window(driver.window_handles[1])
	driver.get(result)

	time.sleep(2)

	latest_chap = ""

	if "manganato" in result:
		print("manganato")
		latest_chap = driver.find_element_by_xpath("//div[@class='panel-story-chapter-list']/ul/li[1]/a").text.split(' ')[1].strip(":")
	elif "mangakakalot" in result:
		print("mangakakalot")
		latest_chap = driver.find_element_by_xpath("//div[@class='chapter-list']/div/span/a[1]").text.split(' ')[1].strip(":") # for mangakakalot
	elif "manganelo" in result:
		print("manganelo")
	else:
		print("not programmed for this website: " + result)
		driver.close()
		sys.exit()

	if latest_chap > current_chapter:
	# gets the next sequential chapter 
		i = 0
		while latest_chap > current_chapter:
			i += 1 
			if "manganato" in result:
				print("manganato")
				latest_chap = driver.find_element_by_xpath("//div[@class='panel-story-chapter-list']/ul/li[" + str(i) + "]/a").text.split(' ')[1].strip(":")
				if latest_chap == current_chapter:
					continue
				chaps_to_open.append(driver.find_element_by_xpath("//div[@class='panel-story-chapter-list']/ul/li[" + str(i) + "]/a").get_attribute("href")) # adding chapter link to new_chapters
			elif "mangakakalot" in result:
				print("mangakakalot")
				latest_chap = driver.find_element_by_xpath("//div[@class='chapter-list']/div/span/a[" + str(i) + "]").text.split(' ')[1].strip(":") # for mangakakalot
				if latest_chap == current_chapter:
					continue
				chaps_to_open.append(driver.find_element_by_xpath("//div[@class='chapter-list']/div/span/a[" + str(i) + "]").get_attribute("href")) # for mangakakalot
			elif "manganelo" in result:
				print("manganelo")
				print("not implemented yet!")
				print("skipping over this!")

	for i in chaps_to_open:
		driver.execute_script("window.open('');") # open new tab
		driver.switch_to.window(driver.window_handles[-1]) # switch to new tab
		driver.get(i) # open the link of the first result

	driver.switch_to.window(driver.window_handles[0]) # switch to and close the search tab
	driver.close()

	driver.switch_to.window(driver.window_handles[0]) # switch to and close the search tab
	time.sleep(1)
	driver.close() # closing the manga home page
	driver.switch_to.window(driver.window_handles[-1]) # switch to first manga chapter to read

		# print(i)
		# 	if "manganato" in result:
		# 		print("manganato")
		# 		latest_chap = driver.find_element_by_xpath("//div[@class='panel-story-chapter-list']/ul/li[" + str(i-1) + "]/a").text.split(' ')[1].strip(":")
		# 	elif "mangakakalot" in result:
		# 		print("mangakakalot")
		# 		latest_chap = driver.find_element_by_xpath("//div[@class='chapter-list']/div/span/a[" + str(i-1) + "]").text.split(' ')[1].strip(":") # for mangakakalot
		# 	elif "manganelo" in result:
		# 		print("manganelo")


# Takes in a list of lists where the inner list contains the manga name in the first position and 
# the chapter num in the second and visits mangakakalot and checks if there is any new chapters 
# that have to be opened and returns a list containing strings to write back to the file
def visit_website(manga_num: [[str, float]]) -> [str]:
	new_chapters = [] # list of the new chapter urls to open at the end of the program
	current_manga = [] # list of the rewritten values of the chapters
	manga_website = "https://mangakakalot.com/"

	driver = webdriver.Firefox(executable_path="./geckodriver")
	driver.get(manga_website)
	search_bar = driver.find_element_by_class_name("searchi")

	for line in manga_num:
		try:
			search_bar.send_keys(line[0])
		except:
			print("error not correct format")
			print(line)
			sys.exit()

		time.sleep(1.5) # waiting for list to show up, should probably change this to waiting dynamic time rather than static

		try:
			result = driver.find_element_by_xpath("//div[@id='search_result']/ul/a[1]").get_attribute("href") # the link of the first result of the search
		except:
			print("could not find the manga " + line[0] + ". Skipping to the next manga")
			search_bar.clear()
			continue

		search_bar.clear()
		driver.execute_script("window.open('');")
		driver.switch_to.window(driver.window_handles[1])
		driver.get(result)

		time.sleep(2)

		latest_chap = ""

		if "manganato" in result:
			print("manganato")
			latest_chap = driver.find_element_by_xpath("//div[@class='panel-story-chapter-list']/ul/li[1]/a").text.split(' ')[1].strip(":")
		elif "mangakakalot" in result:
			print("mangakakalot")
			latest_chap = driver.find_element_by_xpath("//div[@class='chapter-list']/div/span/a[1]").text.split(' ')[1].strip(":") # for mangakakalot
		elif "manganelo" in result:
			print("manganelo")
		else:
			print("not programmed for this website: " + result)
			driver.close()
			sys.exit()

		if latest_chap > line[1]:
		# gets the next sequential chapter 
			i = 1
			while latest_chap > line[1]:
				i += 1 
				if "manganato" in result:
					print("manganato")
					latest_chap = driver.find_element_by_xpath("//div[@class='panel-story-chapter-list']/ul/li[" + str(i) + "]/a").text.split(' ')[1].strip(":")
				elif "mangakakalot" in result:
					print("mangakakalot")
					latest_chap = driver.find_element_by_xpath("//div[@class='chapter-list']/div/span/a[" + str(i) + "]").text.split(' ')[1].strip(":") # for mangakakalot
				elif "manganelo" in result:
					print("manganelo")

			print(i)
			if "manganato" in result:
				print("manganato")
				latest_chap = driver.find_element_by_xpath("//div[@class='panel-story-chapter-list']/ul/li[" + str(i-1) + "]/a").text.split(' ')[1].strip(":")
			elif "mangakakalot" in result:
				print("mangakakalot")
				latest_chap = driver.find_element_by_xpath("//div[@class='chapter-list']/div/span/a[" + str(i-1) + "]").text.split(' ')[1].strip(":") # for mangakakalot
			elif "manganelo" in result:
				print("manganelo")

			current_manga.append(line[0] + '\t' + latest_chap + '\n') # updating the manga.txt file

			if "manganato" in result:
				new_chapters.append(driver.find_element_by_xpath("//div[@class='panel-story-chapter-list']/ul/li[" + str(i-1) + "]/a").get_attribute("href")) # adding chapter link to new_chapters
			elif "mangakakalot" in result:
				new_chapters.append(driver.find_element_by_xpath("//div[@class='chapter-list']/div/span/a[" + str(i-1) + "]").get_attribute("href")) # for mangakakalot
			elif "manganelo" in result:
				print("not implemented yet!")
				print("skipping over this!")
			else:
				print("not programmed for this website: " + result)
				sys.exit()

		elif (latest_chap <= line[1]):
			current_manga.append(line[0] + '\t' + line[1]  + '\n') # updating the manga.txt file
			print("all caught up on " + line[0])

		driver.close() # close tab and switch to the search tab
		driver.switch_to.window(driver.window_handles[0])

		time.sleep(2) # can get rid of this, only there for debugging

	for i in new_chapters:
		driver.execute_script("window.open('');") # open new tab
		driver.switch_to.window(driver.window_handles[-1]) # switch to new tab
		driver.get(i) # open the link of the first result

	driver.switch_to.window(driver.window_handles[0]) # switch to and close the search tab
	driver.close()

	return current_manga

if __name__ == "__main__":
    # new_chap()
    # file = "test.txt"
    # updated_list = visit_website(get_mangas("test.txt"))
    # update_file(file, updated_list)
    get_new_chapters_bulk("Spy X Family", "60")


            