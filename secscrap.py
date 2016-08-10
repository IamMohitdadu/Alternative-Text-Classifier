import csv
import os
import urllib.parse as urlparse
from io import BytesIO
from urllib.request import urlopen
from PIL import Image
from bs4 import BeautifulSoup
import requests

urllink = "http://www.pondiuni.edu.in/"


def get_image_size(imgurl):
    # to find the image size(height and   width)

    data = requests.get(imgurl).content
    im = Image.open(BytesIO(data))
    return im.size


def images(urlk):

    # Reading URL and storing <img> tag
    r = urlopen(urlk).read()
    bsobj = BeautifulSoup(r)
    imgtag = bsobj.find_all('img')

    # Printing all image tag
    i = 1
    for i in range(len(imgtag)):
        print(i, imgtag[i])

    # Printing only required tag and value
    print("*" * 80)

    for link in imgtag:
        srclink = str(link.get('src'))
        image = urlparse.urljoin(urllink, srclink)
        width, height = get_image_size(image)
        print(width, height)
        filewriter(link, link.get('src'), link.get('alt'), height, width)


def urlParse(url):
    thepage = urlopen(url)
    soupdata = BeautifulSoup(thepage, "lxml")
    return soupdata


soup = urlParse(urllink)
print("#" * 80)
extension = ('.pdf', '.doc', '.docx', '.txt', 'xls', 'xlsx')
urldict = {}
temp = []

# Fetching all sub-url from root domain
for ur in soup.findAll('a'):
    temp = ur.get('href')
    if (str(temp).startswith('http') and (not(str(temp).endswith(tuple(
       extension))))):
        urldict[temp] = 0

print('Printing URL List.....................................')
# for key in urldict:
#    print(key, urldict[key])

print("Total", len(urldict), "link printed")

colHeader = ['url', 'src', 'alttext', 'imgheight', 'imgwidth']
colField = {'url': 'URL', 'src': 'SRC',
            'alttext': 'ALT Text', 'imgheight': 'IMG Height',
            'imgwidth': 'IMG Width'}


def filewriter(ul, src, alt, ht, wd):
    fileName = "pondiuni" + ".csv"
    if os.access(fileName, os.F_OK):
        fileMode = 'a+'
    else:
        fileMode = 'wb'

    csvWriter = csv.DictWriter(open(fileName, fileMode), fieldnames=colHeader)

    if fileMode == 'wb':
        csvWriter.writerow(colField)

    csvWriter.writerow({'url': ul, 'src': src, 'alttext': alt, 'imgheight': ht,
                        'imgwidth': wd})

for key in (x for x in urldict):
    images(key)
