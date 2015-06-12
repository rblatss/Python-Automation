﻿''' ****************************************************************

							Get Job Titles 
  ----------------------------------------------------------------
  I should have written this at the start of my job search. Pretty
  simple idea, but useful. This script automates a search for job openings 
  on indeed.com.
    
  At this point, the script only verifies that the title has a combination
  of software/electrical and engineer/developer.
  
  Later, i'll parse the job descriptions for specific requirements
  (c++, python, linux, unix, related degree, electrical engineering
   etc.)
  
  Procedure (4 steps):
    1) search "company name" on indeed.com
	
		btw: url dissected
		http://www.youtube.com/watch?v=DBJ7mBxi8LM&list=FLjtfXY-PoLnBtJTrAVIHR3A&index=5

			Protocol � http://
			
			Subdomain � www.
			
			Domain � youtube.com/
			
			Path to file � watch
			
			Query string � ?v=DBJ7mBxi8LM&list=FLjtfXY-PoLnBtJTrAVIHR3A&index=5
			(name/value pairs!!)
	
		
		From:
			http://maps.google.com/maps?q=62+4th+St+NW,+Winter+Haven,+FL&hl=en&sll=27.698638,-83.804601&sspn=22.576023,34.453125&oq=62+4th+st+nw,+&hnear=62+4th+St+NW,+Winter+Haven,+Florida+33881&t=m&z=17
		To:
			http://maps.google.com/maps?q=62+4th+St+NW,+Winter+Haven,+FL
		* These are the same
	
	2) skim thru position titles
	3) go to next page
	4) repeat prev 2 until no more next
  
  to do:

	2) validate that company of job posting is company searched
		maybe try regex to look for title w/o certain postfix/prefix
		instead of searching for affirmative
	3) parse job descriptions and match based on job requirements
	  
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
	
	try:
		res.raise_for_status() # halt if content is bad (raises exception)
	except Exception as exc:
		print('There was a problem: %s' % (exc))
		sys.exit(0)
	
	soup = BeautifulSoup(res.text)
	
	# Find matches in job post titles
	print "Page " + str(i) + " results:"
	print "-----------------------------"
	for tag in soup.find_all('h2', attrs = {'class' : 'jobtitle'}):
		a = tag.findChild('a')
		if a['itemprop'] != [] and a['itemprop'] == 'title':
			if re.match(jobtitle, a.text) != None:
				print a.text.encode("utf8")
	
	# Go to next page
	if soup.find_all('span', text=re.compile(r'^Next')) != []: # verify there's a next page
		next_url = CorrectURL(iurl + soup.find_all('span', text=re.compile(r'^Next'))[0].parent['href'])
		res = requests.get(next_url)
	else:
		next_page = False
	i += 1

print "Search ended."