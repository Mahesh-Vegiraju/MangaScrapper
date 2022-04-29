# import requests 
# from bs4 import BeautifulSoup
# import webbrowser, time

# #file_name = input("Enter manga filename: ")
# with open('manga_list.txt', 'r') as f:
# 	file_contents = f.readlines()

# #current_chapters_file = input("Enter chapter filename: ")
# current_chapters_file = 'chaps.txt'
# with open('chaps.txt', 'r') as f:
# 	current_chapters = f.readlines()

# #return_file = input("Enter return file: ")
# return_file = 'todays_manga.txt'

# today_manga_list = []

# for i, url in enumerate(file_contents):
# 	html = requests.get(url.rstrip()).text
# 	soup = BeautifulSoup(html, 'html.parser')
# 	try:
# 		latest_chapter_link = soup.find('a', class_ = 'chapter-name text-nowrap').get('href')
# 	except:
# 		print(url)
# 		quit()
# 	latest_chapter = latest_chapter_link.split('_')[-1]
# 	if (latest_chapter > current_chapters[i]):
# 		current_chapters[i] = latest_chapter + '\n'
# 		today_manga_list.append(latest_chapter_link)
# with open(return_file, 'w+') as f:
# 	f.truncate(0)
# 	for link in today_manga_list:
# 		f.writelines(link + '\n')
# with open(current_chapters_file, 'w+') as f:
# 	f.truncate(0)
# 	for chapter in current_chapters: 
# 		f.writelines(chapter)

# with open(return_file, 'r') as f:
# 	for i, link in enumerate(f):
# 		if i == 0:
# 			webbrowser.open(link.rstrip(), new = 1)
# 		else:
# 			webbrowser.open(link.rstrip(), new = 2)