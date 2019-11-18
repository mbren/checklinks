# pipenv run python3 checklinks.py

import os, re, requests
# To install Requests:     pipenv install requests

from bs4 import BeautifulSoup 
# To install Beautiful Soup: pipenv install bs4

dirList = ['./en_US/api-rest']

ignoreList = ['https://MY-SERVER', 'http://my-server']

def fileGatherer(startDir):
    for root, dirs, files in os.walk(startDir):
        for file in files:
            if (file.lower().endswith('.html') or file.lower().endswith('.htm')):
                fileWithPath = root  + "/" + file
                print('\n\n' + fileWithPath)
                with open(fileWithPath, mode='r', encoding='utf-8') as f:
                    soup = BeautifulSoup(f, "html.parser")
                    for link in soup.find_all('a', href=True):
                        url = link['href']
                        if url in ignoreList:
                            print("Ignoring link " + url)
                        else:
                            print("Checking link " + url)
                            testUrl(url, file)
  
def testUrl(url, ckdFile):
    try:
        request = requests.get(url, allow_redirects=False)
        print(request.status_code)
        if request.status_code == 301:
            print("Redirect")
            # print(request.history[0].headers['Location']) 
        elif request.status_code != requests.codes.ok:
            print('BROKEN LINK? ' + url) 
    except requests.exceptions.MissingSchema as exc:
        #if URL starts with hash sign, append https:// the site base url and the current file being checked.
        if url.startswith("#"):
            all = "https://<SITE_BASE_URL>" + ckdFile + url
            print(all)
            testUrl(all, ckdFile)
        # #if URL starts with filename, append the https:// stuff to it before making call
        print("Invalid URL " + url)
    except requests.ConnectionError as exc:
        print("Broken Link? " + url)

def main():
    for startDir in dirList:
        fileGatherer(startDir)
    
if __name__ == '__main__':
    main()