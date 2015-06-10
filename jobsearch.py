''' ****************************************************************

							Get Job Titles 
  ----------------------------------------------------------------
  I should have written this at the start of my job search. Pretty
  simple idea, but might be real tricky to implement. This script
  will automate my search for openings at a company by matching 
  patterns to position titles on indeed.com.
  
  Input company name. Formatted list of titles that i might 
  qualify for. 
  
  At this point, the script only verifies that a keyword, from 
  list of keywords below, is in the position title.
  
  Later, i'll parse the job descriptions for specific requirements
  (c++, python, linux, unix, related degree, electrical engineering
   etc.)
  
  jsearch(...)
  	jsearch(string) --> strings is name of company
  
  Procedure (4 steps):
    1) search "company name" on indeed.com
	
		btw: url dissected
		http://www.youtube.com/watch?v=DBJ7mBxi8LM&list=FLjtfXY-PoLnBtJTrAVIHR3A&index=5

			Protocol – http://
			
			Subdomain – www.
			
			Domain – youtube.com/
			
			Path to file – watch
			
			Query string – ?v=DBJ7mBxi8LM&list=FLjtfXY-PoLnBtJTrAVIHR3A&index=5
			(name/value pairs!!)
	
		From:
			http://maps.google.com/maps?q=62+4th+St+NW,+Winter+Haven,+FL&hl=en&sll=27.698638,-83.804601&sspn=22.576023,34.453125&oq=62+4th+st+nw,+&hnear=62+4th+St+NW,+Winter+Haven,+Florida+33881&t=m&z=17
		To:
			http://maps.google.com/maps?q=62+4th+St+NW,+Winter+Haven,+FL
	
	
	2) skim thru position titles (what is common html attribute of job
	    posting links??)
	3) go to next page
	4) repeat prev 2 until no more next
  
  to do:
	why does + become %2B ??? -- > encodings
	validate that company of job posting is company searched
		maybe try regex to look for title w/o certain postfix/prefix!!
		instead of searching for affirmative
	parse job descriptions and match based on job requirements
  
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
	
	try:
		res.raise_for_status() # halt if content is bad (raises exception)
	except Exception as exc:
		print('There was a problem: %s' % (exc))
		sys.exit(0)
	
	soup = BeautifulSoup(res.text) # + is escaped HERE !!!!!!! 
	
	# Find matches in job post titles
	print "Page " + str(i) + " results:"
	print "-----------------------------"
	for tag in soup.find_all('h2', attrs = {'class' : 'jobtitle'}):
		a = tag.findChild('a')
		if a['itemprop'] != [] and a['itemprop'] == 'title':
			if re.match(jobtitle_pre, a.text) != None:
				print a.text.encode("utf8")
			# elif re.match(jobtitle_post, a.text) != None:
				# print a.text
	
	# Go to next page
	if soup.find_all('span', text=re.compile(r'^Next')) != []: # verify there's a next page
		next_url = CorrectURL(iurl + soup.find_all('span', text=re.compile(r'^Next'))[0].parent['href'])
		res = requests.get(next_url)
	else:
		break
	i += 1

print "Search ended."