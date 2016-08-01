from bs4 import BeautifulSoup
from urllib.request import urlopen
import urllib.parse
# import requests


def images(url):
    r = urlopen(url).read()
    bsobj = BeautifulSoup(r)
    print(type(r))
    imgtag = bsobj.find_all('img')
    
    #print(imgtag)
    print(type(imgtag))
    print("*"* 80)
    for i in range(len(imgtag)):
        print(i, imgtag[i])
    
    print("*"* 80)
    imgsrc = bsobj.find_all('src')
    for item in imgsrc:
        print (item)
    for link in bsobj.find_all('img'):
        print(link, link.get('alt'), link.get('height'), link.get('width'))

def make_soup(url):
    thepage = urlopen(url)
    soupdata=BeautifulSoup(thepage, "html.parser")
    return soupdata
temp=[]
i = 1
soup=make_soup('http://www.pondiuni.edu.in')
for img in soup.findAll('a'):
    temp=img.get('href')
    if str(temp).startswith('http'):
        print(i,temp)
        i+= 1
    print("#"* 80)
"""    for tag in range(len(temp)):
        print("^"*80)
        images(temp[tag])
"""