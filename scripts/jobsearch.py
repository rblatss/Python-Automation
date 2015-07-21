''' ****************************************************************

						Find a Job via Indeed
		-----------------------------------------------------
  Procedure:
    0) read query name and search it via indeed.com	
    1) create output txt file for query
	2) skim thru position titles and write to text
	3) go to next page
	4) repeat prev 2 until no more next
    5) repeat 0 - 4 for all queries
	
**************************************************************** '''

from bs4 import BeautifulSoup
import os, re, requests, sys

# Function used to replace %2B w/ + in URL
def CorrectURL(url):
	return "+".join(url.split("%2B"))

def main():
	try:
		os.mkdir('jobs')
	except OSError:
		pass
	
	# Read query names
	file_handle = open("../data/queries.txt", 'r')
	queries_list = file_handle.readlines()
	file_handle.close()
	
	for query in queries_list:
		query = query[:-1] # throw out '\n'
		
		# Request Indeed.com
		
		''' keys = ['q', 'l']
		values = [ '+'.join(query.split(' ')), '98136']
		complete_query = dict(zip(keys, values)) '''
		search_url = "https://www.indeed.com"
		
		# function did bad stuff when passed query as arg 2
		res = requests.get(search_url + "/jobs?q=" + '+'.join(query.split(' ')) + '&l=98136')
		
		# Criteria for a match
		jobtitle = re.compile(r"(.*)(([Ss]oftware)|([Ee]lectrical)|([Ff]irmware))+\s?(Development)?\s?([Ee]ngineer|[Dd]eveloper)+(.*)")
		
		# Iterate thru all pages of search results and write job titles to .txt file
		i = 1
		next_page = True
	
		output = open(os.path.join('jobs', query + ".txt"), 'w')
		while(next_page):
			try:
				res.raise_for_status() # halt if content is bad
			except Exception as exc:
				print('There was a problem: %s' % (exc))
				sys.exit(0)
			
			soup = BeautifulSoup(res.text)
			
			# Find matches in job post titles and write to output file
			output.write("Page " + str(i) + " results:\n")
			output.write("-----------------------------\n")
			for tag in soup.find_all('h2', attrs = {'class' : 'jobtitle'}):
				a = tag.findChild('a')
				if a['itemprop'] != [] and a['itemprop'] == 'title':
					if re.match(jobtitle, a.text) != None:
						output.write(a.text.encode('utf8','ignore') + " - " + tag.next_sibling.next_sibling.text.encode('utf8', 'ignore') + "\n")
			
			# Go to next page
			if soup.find_all('span', text=re.compile(r'^Next')) != []: # verify there's a next page
				try:
					next_url = CorrectURL(search_url + soup.find_all('span', text=re.compile(r'^Next'))[0].parent['href'])
					res = requests.get(next_url)
				except KeyError:
					print "Incomplete search for " + query + " at page " + str(i)
					next_page = False
					continue
			else:
				next_page = False
			i += 1
		
		output.close()
	
	print "Search ended."
	
if __name__ == "__main__":
	main()