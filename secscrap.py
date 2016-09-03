import csv
import os
import urllib.parse as urlparse
from requests import get
from io import BytesIO
from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.request import Request
from PIL import Image
from bs4 import BeautifulSoup

global imgext
imgext = ('jpeg', 'JPEG', 'jpg', 'JPG', 'gif', 'GIF', 'tiff', 'png', 'PNG')

global hdrs
hdrs = {'User-Agent': 'Mozilla / 5.0 (X11 Linux x86_64) AppleWebKit / 537.36 (\
        KHTML, like Gecko) Chrome / 52.0.2743.116 Safari / 537.36'}


def get_image_size(imgurl):
    # to find the image size(height and  width)
    # data = requests.get(imgurl).content
    # im = Image.open(BytesIO(data))
    urlbytedata = None
    try:
        urlbytedata = urlopen(Request(imgurl, data=None, headers=hdrs)).read()
    except HTTPError as err:
        if ((err.code == 404) or (err.code == 500) or (err.code == 503)):
            pass
        else:
            raise

    data = BytesIO(urlbytedata)
    im = Image.open(data)
    return im.size


def images(urlk):
    print("\n", urlk)

    # Reading URL and storing <img> tag
    r = get(urlk)
    statusCode = r.status_code
    
    if statusCode == 503:
        print("Internal Server Error..! Error Code: %d!" % statusCode)
        return

    bsobj = BeautifulSoup(r.content)
    imgtag = bsobj.find_all('img')  # Finding all <img> tag

    # Printing all image tag
    print("Now printing all <img> tag one by one")
    for i in imgtag:
        print(i)

    # Printing only required tag and value
    print("*" * 80)

    for link in imgtag:

        # Getting <src> attribute from <img> tag and storing it
        if link.get('src').startswith('.'):
            print("Invalid <src> path: starts with .(dot)", link.get('src'))
            srclink = link.get('src')[1:]
            continue
        else:
            srclink = link.get('src')

        if not(srclink.endswith(tuple(imgext))):
           print("SRC tag doesn't end with image extention", srclink)
           continue

        # print(srclink)
        imgurl = urlparse.urljoin(urllink, srclink)
        imgurl = imgurl.replace(' ', '%20')

        if get(imgurl).status_code == 404 or get(imgurl).status_code == 500:
            if get(imgurl).status_code == 404:
                print("URL %s is an INVALID URL" % imgurl)
            elif get(imgurl).status_code == 500:
                print("Internal Server Error with URL %s" % imgurl)

            print("Skiping to next link in <imgtag>")
            continue
        else:
            print("No Error Code for image url.. Proceeding to fetch image-size")

        print("Image URL", imgurl)
        imgheight = link.get('height')
        imgwidth = link.get('width')

        if not (imgheight and imgwidth):
            width, height = get_image_size(imgurl)
            print(width, height)
        else:
            width, height = imgwidth, imgheight
            
        filewriter(link, link.get('src'), link.get('alt'), height, width)


def urlFetch(url):
    global urllink
    urllink = url
    thepage = get(url)
    pageStatus=thepage.status_code

    if ((pageStatus == 404) or (pageStatus == 500) or (pageStatus == 503)):
            pass

    soupdata = BeautifulSoup(thepage.content)
    return subUrlFetch(soupdata)


# soup = urlFetch(urllink)
print("#" * 80)

extension = ('.pdf', '.doc', '.docx', '.txt', 'xls', 'xlsx')
urldict = {}
temp = []

# Fetching all sub-url from root domain
def subUrlFetch(soup):
    for ur in soup.findAll('a'):
        temp = ur.get('href')
        if (str(temp).startswith('http') and (not(str(temp).endswith(tuple(
           extension))))):
            urldict[temp] = 0
    print("Total", len(urldict), "link printed")
    for key in (x for x in urldict):
        images(key)

colHeader = ['url', 'src', 'alttext', 'imgheight', 'imgwidth']
colField = {'url': 'URL', 'src': 'SRC',
            'alttext': 'ALT Text', 'imgheight': 'IMG Height',
            'imgwidth': 'IMG Width'}


def filewriter(ul, src, alt, ht, wd):
    fileName = "pondiuni" + ".csv"
    if os.access(fileName, os.F_OK):
        fileMode = 'a+'
    else:
        fileMode = 'w'

    csvWriter = csv.DictWriter(open(fileName, fileMode), fieldnames=colHeader)

    if fileMode == 'w':
        csvWriter.writerow(colField)  # Writing Column Header

    # writing each row with data
    csvWriter.writerow({'url': ul, 'src': src, 'alttext': alt, 'imgheight': ht,
                        'imgwidth': wd})
    return


