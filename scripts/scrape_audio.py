# scrape_for_audio.py
# Goal: download all audio from a specified site and put it at specified location
# Ideas:    support - find other file formats (eg wav??)
#           download music that was uploaded today (hypebeast etc)
#           check if 404 is dead link or 1 time failure
#           automate user-agent lookup
#           requests.iter_content/print download progress
#           does passing headers actually work ?? ie according to requests doc: Authorization headers set with headers= will be overridden if credentials are specified in .netrc, which in turn will be overridden by the auth= parameter.
#           checking response status codes - if != 200 would be a catch all bad responses (and then some...)
#           spotify support - can't download spotify audio, but maybe include option to add to a playlist
#           add soundcloud support
from urllib.request import urlopen
from urllib.error import HTTPError
from http.client import IncompleteRead
from bs4 import BeautifulSoup
from requests import Session
import re
import os
import sys
import pafy
import time

################################################
####            Support Functions           ####
################################################
youtubeBool = False 
soundcloudBool = False
def setup(downloadDirectoryRes, youtubeRes, soundcloudRes):
    '''
    Description: verify download directory, determine whether or not to download youtube or soundcloud audio.
                 Safe to call createDirectoryForPage() after calling this.
    Parameters:  downloadDirectory: string that is path to location that downloads are put
                 youtubeRes:        the user's yes or no response to downloading youtube audio, default is no
                 soundcloudRes:     the user's yes or no response to downloading soundcloud audio, default is yes
    Returns:     None
    '''
    global downloadDirectory
    
    # Default option
    if downloadDirectoryRes is '':
        if sys.platform == "linux":
            homeDirectory = os.environ["HOME"]
        elif sys.platform == "win32":
            homeDirectory = os.environ["HOME"]
        downloadDirectory = homeDirectory + "\Downloads"

    # Verify user inputs
    while os.path.exists(downloadDirectoryRes) != True:
        user = input("Couldn't find " + downloadDirectoryRes + "! Should i make it (y/n)? ").upper()
        if user == 'Y':
            try:
                os.mkdir(downloadDirectoryRes)
            except FileNotFoundError:
                print("Sorry, I can't make that directory.")
                sys.exit()
        else:
            downloadDirectoryRes = input("Ok. Where should i put downloads? ")

    while youtubeRes != 'Y' and youtubeRes != 'N':
        youtubeRes = input("'%s' isn't valid. Do you want youtube audio? (y/n): " % youtubeRes).upper()
    while soundcloudRes != 'Y'and soundcloudRes != 'N':
        soundcloudRes = input("'%s' isn't valid. Do you want soundcloud audio (y/n)? " % soundcloudRes).upper()

    # Setup global variables
    if youtubeRes.upper() is 'Y':
        youtubeBool = True
    if soundcloudRes.upper() is 'Y':
        soundcloudBool = False
    else:
        print("Sorry, i can't download soundcloud audio currently. Maybe later.")
        
    downloadDirectory = downloadDirectoryRes
        
def getInternalLinks(bsObj, includeUrl):
    '''
    Description: Find links to that do include 'includeUrl' in host component of link
    '''
    internalLinks = []
    #Finds all links that begin with a "/"
    for link in bsObj.findAll("a", href=re.compile(r"^(http|www)?[//:.]+" + includeUrl + ".+\/(?!share=(facebook|tumblr|twitter|email))$")):
        if link.attrs['href'] is not None:
            if link.attrs['href'] not in internalLinks:
                internalLinks.append(link.attrs['href'])
    return internalLinks
            
def getExternalLinks(bsObj, excludeUrl):
    '''
    Description: Find links to that do not include 'excludeUrl' in host component of URL
    '''
    externalLinks = []

    pattern = re.compile(r'^(https?|www)[//:.]+(?!' + excludeUrl + ').+?\.com.+')
    for link in bsObj.findAll("a", href=pattern):
        if link.attrs['href'] is not None:
            if link.attrs['href'] not in externalLinks:
                externalLinks.append(link.attrs['href'])
   
    for link in bsObj.findAll("source", src=pattern):
        if link.attrs['src'] is not None:
            if link.attrs['src'] not in externalLinks:
                externalLinks.append(link.attrs['src'])

    # Soundcloud/youtube
    for link in bsObj.findAll("iframe", src=pattern):
        if link.attrs['src'] is not None:
            if link.attrs['src'] not in externalLinks:
                externalLinks.append(link.attrs['src'])
    
    return externalLinks

def splitAddress(address):
    '''
    Description: Return components of http link as list
    '''
    addressParts = address.replace("http://", "").replace("https://","").split("/")
    return addressParts

def getAudioFile(audioUrl):
    '''
    Description: Download audio file if file is directly available, ie link suffix is 'mp3', 'm4a' etc.
    '''
    response = urlopen(audioUrl)
    destinationFile = downloadDirectory + "\\" + splitAddress(audioUrl)[-1]
    audioFile = open(destinationFile, "wb")

    # Start
    print("Downloading audio file ...")
    start = time.clock()

    # Read and write
    data = response.read()
    audioFile.write(data)

    # End
    elapsed = time.clock() - start
    print("Took {:.02f} seconds to complete".format(elapsed))
    
def getYoutubeAudio(url):
    '''
    Description: Download audio of youtube (works for embedded video links too)
    '''
    if 'embed' in url:
        # convert embedded link to normal
        url = url.replace('embed/','watch?v=')
    video = pafy.new(url)
    print("Title is: %s" % video.title)
    best = video.getbestaudio()
    best.download(filepath=downloadDirectory,quiet=True)

def getSoundcloudAudio(url):
    '''
    Description: None yet. Waiting on approval to use API.
    '''    
    print("I can't download soundcloud audio yet.")

def renderSpotifyPlaylist():
    '''
    Description: None yet.
    '''    
    print("I can't produce spotify playlists yet.")

    
################################################
####                 Main                   ####
################################################
visited = []
def crawl(startingSite):
    '''
    Description: crawls through internal links starting at the link passed to function.
                 If audio file discovered, prompt user to download.
    '''

    time.sleep(3) # don't overwhelm servers
    
    if re.match(r"http://",startingSite) is None:
        startingSite = "http://" + startingSite

    try:
        session = Session()
        headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36",
                   "Accep-Language":"en-US"}
        req = session.get(startingSite, headers=headers)
    except ValueError:
        print("URL might not be valid. So I'm moving on")
        return

    bsObj = BeautifulSoup(req.text, "html.parser")
    externalLinks = getExternalLinks(bsObj,startingSite)
    internalLinks = getInternalLinks(bsObj,splitAddress(startingSite)[0])

    for link in externalLinks:
        done = False
        while done is not True:
            try:
                if 'youtube.com' in link and youtubeBool:
                    print("Found youtube video!")
                    getYoutubeAudio(link)
                elif 'soundcloud.com' in link and soundcloudBool:
                    print("Found soundcloud audio!")
                    getSoundcloudAudio(link)        
                else:
                    extension = link[-4:]
                    if extension == ".mp3":
                        extension = link[-4:]
                        print("Found an %s! Title is: %s" % (link[-3:], link.split("/")[-1]) )
                        getAudioFile(link)
                done = True
            except HTTPError:
                print("404! link might be dead or you might need to run me again.")
                done = True
            except IncompleteRead:
                print("Didn't read everything... i'll try again")
                done = False
    
    for link in internalLinks:
        if link not in visited:
            print("Next link is: " + link)     
            visited.append(link)
            crawl(link)

def main():

    argv = sys.argv
    argc = len(argv)
    if argc < 2:
        startUrlRes = input("What URL do you want to start at?: ")
    else:
        startUrlRes = argv[1]

    if argc < 3:
        downloadDirectoryRes = input("Where should i put downloaded files? (default is Downloads folder) ")
    else:
        downloadDirectoryRes = argv[2]

    if argc < 4:
        youtubeRes = input("Download youtube audio (y/n)? ").upper()
    else:
        youtubeRes = argv[3]
        
    if argc < 5:
        soundcloudRes = input("Download soundcloud audio (y/n)? ").upper()
    else:
        soundcloudRes = argv[4]

    setup(downloadDirectoryRes, youtubeRes, soundcloudRes)
    crawl(startUrlRes)

if __name__ == "__main__":
    main()
