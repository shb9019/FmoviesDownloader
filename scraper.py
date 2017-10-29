import urllib2
import sys
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException


search_input = sys.argv[1]
search_tokens = search_input.split(' ')
search_string = ''
for s in search_tokens:
	search_string += s + '+'
search_string = search_string.rstrip('+')

print "Searching..."

path_name = 'https://fmovies.se/search?keyword=' + search_string
hdr = {'User-Agent': 'Mozilla/5.0'}
req = urllib2.Request(path_name,headers = hdr)
page = urllib2.urlopen(req)
soup = BeautifulSoup(page,'html.parser')
browser = webdriver.PhantomJS('./phantomjs')
movie_box = soup.find('a',attrs = {'class':'name'})
movie_name = movie_box.text.strip()

if movie_name.lower() == search_input.lower() :
	print "Requested Movie/Series is Available"
	print "Proceeding to Download..."
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
	
	print 'Preparing to Download'

	for episode_link in episode_links:
		browser.get(episode_link)
		browser.findElement(By.cssSelector('.cover::before')).click();
		print "Waiting for page to load... \n"
		WebDriverWait(browser,10)
		#try:
		#	video = browser.find_element_by_xpath('//*[@id="jw"]/div[2]/video')
		#except Exception,e:
		browser.save_screenshot('screenshot.png')

	browser.close()
	browser.quit()	

else :
	print "Unavailable \nDid you mean? \n"	
	movie_suggestions = soup.find_all('a',attrs = {'class':'name'})
	for i in range(0,10) :
		print movie_suggestions[i].text.strip()

#for movie_name_box in movie_names_box:
	#movie_name = movie_name_box.text.strip()
	#movie_link = movie_name_box.get('href')
	#print movie_name
	#print 'https://fmovies.se' + movie_link
	#print '\n'

