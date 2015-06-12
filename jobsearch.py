<<<<<<< HEAD
﻿''' ****************************************************************
=======
''' ****************************************************************
>>>>>>> d127c54643d957da9dfcd8dd86d3ea1ddc390801

							Get Job Titles 
  ----------------------------------------------------------------
  I should have written this at the start of my job search. Pretty
<<<<<<< HEAD
  simple idea, but useful. This script automates a search for job openings 
  on indeed.com.
    
  At this point, the script only verifies that the title has a combination
  of software/electrical and engineer/developer.
=======
  simple idea, but might be tricky to implement. This script
  will automate my search for openings at a company by matching 
  patterns to position titles on indeed.com.
  
  At this point, the script only verifies that a keyword, from 
  list of keywords below, is in the position title.
>>>>>>> d127c54643d957da9dfcd8dd86d3ea1ddc390801
  
  Later, i'll parse the job descriptions for specific requirements
  (c++, python, linux, unix, related degree, electrical engineering
   etc.)
  
  Procedure (4 steps):
    1) search "company name" on indeed.com
	
		btw: url dissected
		http://www.youtube.com/watch?v=DBJ7mBxi8LM&list=FLjtfXY-PoLnBtJTrAVIHR3A&index=5

<<<<<<< HEAD
			Protocol � http://
			
			Subdomain � www.
			
			Domain � youtube.com/
			
			Path to file � watch
			
			Query string � ?v=DBJ7mBxi8LM&list=FLjtfXY-PoLnBtJTrAVIHR3A&index=5
			(name/value pairs!!)
	
		
=======
			Protocol – http://
			
			Subdomain – www.
			
			Domain – youtube.com/
			
			Path to file – watch
			
			Query string – ?v=DBJ7mBxi8LM&list=FLjtfXY-PoLnBtJTrAVIHR3A&index=5
			(name/value pairs!!)
	
>>>>>>> d127c54643d957da9dfcd8dd86d3ea1ddc390801
		From:
			http://maps.google.com/maps?q=62+4th+St+NW,+Winter+Haven,+FL&hl=en&sll=27.698638,-83.804601&sspn=22.576023,34.453125&oq=62+4th+st+nw,+&hnear=62+4th+St+NW,+Winter+Haven,+Florida+33881&t=m&z=17
		To:
			http://maps.google.com/maps?q=62+4th+St+NW,+Winter+Haven,+FL
		* These are the same
	
	2) skim thru position titles
	3) go to next page
<<<<<<< HEAD
	4) repeat prev 2 until no more next
  
  to do:

	2) validate that company of job posting is company searched
		maybe try regex to look for title w/o certain postfix/prefix
		instead of searching for affirmative
	3) parse job descriptions and match based on job requirements
=======
	4) repeat prev 2 until no more next pages
  
  to do:
	1) replace CorrectURL with more pythonic code
	2) validate that company of job posting is company searched
		maybe try regex to look for title w/o certain postfix/prefix!!
		instead of searching for affirmative
	3) parse job descriptions and match based on job requirements
  
  Criteria for a match:
	keywords:
	  software OR electrical
	AND
	  development OR nothing
	AND
	  developer OR engineer
	AND
	  (prefix)
  	  entry level
  	  new grad
  	  recent grad
  	  junior
  	  jr.
  	  
	  (postfix)
	  i
	  I
	  1
  
  Examples of position titles to match:
	Software Engineer I
	software developer 1
	entry level c++/junior developer
	c++/junior entry level developer
	Principle Software Engineer-BigIQ
>>>>>>> d127c54643d957da9dfcd8dd86d3ea1ddc390801
	  
  This script was written using Notepad++ (text, block manipulation,
  autoindent etc.), command prompt (pass args to script) and IDLE
  (test individual functions).

**************************************************************** '''

from bs4 import BeautifulSoup
import re, requests, sys

# Get args
if(len(sys.argv) < 1):
	print "Format: python jobsearch.py [company name]"
	sys.exit(0)

# Indeed Search
keys = ['q', 'l']
values = [ ('+'.join(sys.argv[1:]) ), '98136']
query = dict(zip(keys, values))

iurl = "https://www.indeed.com"
res = requests.get(iurl + "/jobs", query)

# Criteria for a match (job title, correct company name)
<<<<<<< HEAD
main = r"[A-z0-9\s]*(([Ss]oftware)|([Ee]lectrical))+\s?(Development)?\s?([Ee]ngineer|[Dd]eveloper)+[A-z0-9\s]*"
jobtitle = re.compile(main)
company = ' '.join(sys.argv[1:])

# Function used to replace %2B w/ + in URL
def CorrectURL(url):
	return "+".join(url.split("%2B"))

# Iterate thru all pages of search results and print job titles
i = 1
next_page = True
while(next_page):
=======
prefix = r"((Entry Level)|(New Grad)|(Recent Grad)|(Junior)|(Jr))+";
postfix = r"(I|i|1)+"
main = r"[A-z0-9\s]*(([Ss]oftware)|([Ee]lectrical))+\s?(Development)?\s?([Ee]ngineer|[Dd]eveloper)+[A-z0-9\s]*"
jobtitle_pre = re.compile(main)
company = ' '.join(sys.argv[1:])

# Function used to replace %2B w/ + in URL (not at all pythonic)
def CorrectURL(url):
	new_url = ""
	i = 0
	while i < len(url):
		if i < len(url) - 3 and url[i:i+3] == "%2B":
			i += 2
			new_url += '+'
		else:
			new_url += url[i]
		i += 1

	return new_url

# Iterate thru all pages of search results and print job titles
i = 1
while(1):
>>>>>>> d127c54643d957da9dfcd8dd86d3ea1ddc390801
	
	try:
		res.raise_for_status() # halt if content is bad (raises exception)
	except Exception as exc:
		print('There was a problem: %s' % (exc))
		sys.exit(0)
	
<<<<<<< HEAD
	soup = BeautifulSoup(res.text)
=======
	soup = BeautifulSoup(res.text) # + is escaped HERE !!!!!!! 
>>>>>>> d127c54643d957da9dfcd8dd86d3ea1ddc390801
	
	# Find matches in job post titles
	print "Page " + str(i) + " results:"
	print "-----------------------------"
	for tag in soup.find_all('h2', attrs = {'class' : 'jobtitle'}):
		a = tag.findChild('a')
		if a['itemprop'] != [] and a['itemprop'] == 'title':
<<<<<<< HEAD
			if re.match(jobtitle, a.text) != None:
				print a.text.encode("utf8")
=======
			if re.match(jobtitle_pre, a.text) != None:
				print a.text.encode("utf8")
			# elif re.match(jobtitle_post, a.text) != None:
				# print a.text
>>>>>>> d127c54643d957da9dfcd8dd86d3ea1ddc390801
	
	# Go to next page
	if soup.find_all('span', text=re.compile(r'^Next')) != []: # verify there's a next page
		next_url = CorrectURL(iurl + soup.find_all('span', text=re.compile(r'^Next'))[0].parent['href'])
		res = requests.get(next_url)
	else:
<<<<<<< HEAD
		next_page = False
	i += 1

print "Search ended."
=======
		break
	i += 1

print "Search ended."
>>>>>>> d127c54643d957da9dfcd8dd86d3ea1ddc390801
