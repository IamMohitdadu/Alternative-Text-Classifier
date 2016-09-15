import csv
import os
import time
import urllib.parse as urlparse
import requests
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
global errorcode
errorcode = (404, 500, 502, 503)
global urlNonedu
urlNonedu = ['google.com', 'youtube.com', 'facebook.com',
             'twitter.com', 'escortigdir.xyz', 'escortgaziantep.xyz', 'sedo.com', 'web-stat.com', 'gstatic.com', 'maruticomputers', 'supercounters.com',
             'gate-2016.in', 'easycounter.com']


def get_image_size(imgurl):
    # to find the image size(height and  width)
    # data = requests.get(imgurl).content
    # im = Image.open(BytesIO(data))
    urlbytedata = None
    '''
    try:
        urlbytedata = urlopen(Request(imgurl, data=None, headers=hdrs)).read()
    except HTTPError as err:
        if err.code in errorcode:
            pass
        else:
            raise
    '''
    # if imgurl.startswith('https'):
    req = requests.get(imgurl, verify=True, headers=hdrs, allow_redirects=True)
    # else:
    #     req = requests.get(imgurl, verify=False,
    #                        headers=hdrs, allow_redirects=True)

    if imgurl == req.url:
        urlbytedata = BytesIO(req.content)
        try:
            im = Image.open(urlbytedata)
            return im.size
        except IOError as err:
            print("IOError :", str(err))
            return (None, None)
    else:
        print("URL %s gets redirected...." % imgurl)
        return(None, None)


def images(urlk):
    print('\n')
    print(urlk)

    # Reading URL and storing <img> tag
    if any(domain in urlk for domain in urlNonedu):
        print("Non-edu url found....skipping to next url")
        return
    else:
        # if urlk.startswith('https'):
            # try:
        r = requests.get(urlk, headers=hdrs, verify=True)
        statusCode = r.status_code
        # except:
        # else:
        # r = requests.get(urlk, headers=hdrs, verify=False)
        # statusCode = r.status_code

    if statusCode == 503:
        print("Internal Server Error..! Error Code: %d!" % statusCode)
        return

    bsobj = BeautifulSoup(r.content)
    imgtag = bsobj.find_all('img')  # Finding all <img> tag

    # Printing all image tag
    print("Now Printing all <img> tag one by one")
    for i in imgtag:
        print(i)

    # Printing only required tag and value
    print("*" * 80)

    for link in imgtag:
        print(link.get('src'))
        if (link.get('src')) == None:
            continue
        else:
            pass

        # Getting <src> attribute from <img> tag and storing it
        if (link.get('src')).startswith('.'):
            print("Invalid <src> path: starts with .(dot)", link.get('src'))
            srclink = link.get('src')[1:]
            continue
        else:
            srclink = link.get('src')

        if not(srclink.endswith(tuple(imgext))):
            print("SRC tag doesn't end with a valid image extention", srclink)
            continue

        # print(srclink)
        imgurl = urlparse.urljoin(urllink, srclink)
        imgurl = imgurl.replace(' ', '%20')
        time.sleep(5)
        # if imgurl.startswith('https'):
        statusCode = requests.get(
            imgurl, headers=hdrs, verify=True).status_code
        # else:
        #     statusCode = requests.get(
        #         imgurl, headers=hdrs, verify=False).status_code

        if statusCode in errorcode:
            if statusCode == 404:
                print("URL %s is an INVALID URL" % imgurl)
            elif statusCode == 500:
                print("Internal Server Error with URL %s" % imgurl)
            elif statusCode == 502:
                print("Bad Gateway......Error with URL %s" % imgurl)
            elif statusCode == 503:
                print("Service Unavailable....Error with URL %s" % imgurl)

            print("Skiping to next link in <imgtag>")
            continue
        else:
            print("No Error Code for image url.. Proceeding to fetch image-size")

        print("Image URL is : ", imgurl)
        imgheight = link.get('height')
        imgwidth = link.get('width')

        if not(imgheight and imgwidth):
            width, height = get_image_size(imgurl)
            print(height, width)
        else:
            width, height = imgwidth, imgheight
            print(height, width)

        filewriter(link, link.get('src'), link.get('alt'), height, width)


def urlFetch(url):
    global urllink
    urllink = url
    # if url.startswith('https'):
    thepage = requests.get(url, verify=True, headers=hdrs)
    # else:
    # thepage = requests.get(url, verify=False, headers=hdrs)
    pageStatus = thepage.status_code

    if pageStatus in errorcode:
        return

    soupdata = BeautifulSoup(thepage.content)
    subUrlFetch(soupdata)


# soup = urlFetch(urllink)
print("#" * 80)

extension = ('.pdf', '.doc', '.docx', '.txt', 'xls', 'xlsx')
urldict = {}
temp = []


def subUrlFetch(soup):
    # Fetching all sub-url from root domain
    for ur in soup.findAll('a'):
        temp = ur.get('href')
        temp = str(temp)
        if (temp.startswith('http') and (not(temp.endswith(tuple(extension))))):
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
