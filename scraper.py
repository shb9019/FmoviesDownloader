import urllib2
import sys
import time
import shlex
import subprocess
import os
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

search_input = sys.argv[1]
stream_method = sys.argv[2]

search_tokens = search_input.split(' ')
search_string = ''
for s in search_tokens:
	search_string += s + '+'
search_string = search_string.rstrip('+')

print "Searching for " + search_input + "..."

file_name = 'geckodriver'

path_name = 'https://fmovies.se/search?keyword=' + search_string
hdr = {'User-Agent': 'Mozilla/5.0'}
req = urllib2.Request(path_name,headers = hdr)
page = urllib2.urlopen(req)
soup = BeautifulSoup(page,'html.parser')

browser = webdriver.Firefox(executable_path = os.path.abspath(file_name))
movie_box = soup.find('a',attrs = {'class':'name'})
movie_name = movie_box.text.strip()

if movie_name.lower() == search_input.lower() :
	print "Requested Movie/Series is Available\n"
	print "Proceeding to Obtain Links..."
	path_name = 'https://fmovies.se' + movie_box.get('href')
	req = urllib2.Request(path_name,headers = hdr)
	page = urllib2.urlopen(req)
	soup = BeautifulSoup(page,'html.parser')
	servers_list = soup.select('#servers .server')
	server_number = len(servers_list)
	episodes_box = soup.select('.episodes li a')
	episodes_number = (len(episodes_box))/server_number
	episode_links = []

	for i in range(episodes_number):
		episode_link = 'https://fmovies.se' + episodes_box[i].get('href')
		episode_links.append(episode_link)

	if episodes_number != 1:
		print "Number of Episodes: " + episodes_number + '\n'

	print 'Preparing to Download'
	
	i = 1
	links = []
	for episode_link in episode_links:
		if episodes_number != 1:
			print 'Downloading episode ' + str(i)
		browser.get(episode_link)
		element = WebDriverWait(browser,10).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='player']")))
		if episodes_number != 1:
			print "Obtained Episode. Proceeding to get link"
		else:
			print "Obtained Movie. Proceeding to get link"
		clickable = browser.find_element_by_id("player")
		clickable.find_element_by_xpath('.//*').click()
		time.sleep(5)
		link = browser.find_element_by_xpath('//*[@id="jw"]/div[2]/video').get_attribute('src')
		links.append(link)
		i += 1
		print "Obtained Link\n"

	browser.close()
	links_string = ''
	i = 1
	for link in links:
		if episodes_number != 1:
			print 'Downloading episode' + str(i) + 'to Local'
		else:
			print 'Downloading movie to Local'
		subprocess.call (shlex.split('bash ./download.sh ' + link + ' "' + search_input + '"'))
		i += 1

	print 'Downloaded all files'
	browser.quit()

else :
	print "Unavailable \nDid you mean? \n"	
	movie_suggestions = soup.find_all('a',attrs = {'class':'name'})
	for movie in movie_suggestions:
		print movie.text.strip()