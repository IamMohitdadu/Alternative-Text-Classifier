import csv
import os
import time
import urllib.parse as urlparse
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from io import BytesIO
from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.request import Request
from PIL import Image
from bs4 import BeautifulSoup

# to disable the Unverified HTTPS request "InsecureRequestWarning" warning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


global imgext
imgext = ('jpeg', 'JPEG', 'jpg', 'JPG', 'gif', 'GIF', 'tiff', 'png', 'PNG')

global hdrs
hdrs = {'User-Agent': 'Mozilla / 5.0 (X11 Linux x86_64) AppleWebKit / 537.36 (\
        KHTML, like Gecko) Chrome / 52.0.2743.116 Safari / 537.36'}

global certpath
certpath = 'gd_bundle-g2-g1.crt'

global extension
extension = ('.pdf', '.doc', '.docx', '.txt', '.xls', '.xlsx', '.css', '.zip','.PDF')

colHeader = ['imageurl', 'url', 'src', 'alttext', 'imgheight', 'imgwidth']
colField = {'imageurl': 'IMAGE URL', 'url': 'URL', 'src': 'SRC',
            'alttext': 'ALT Text', 'imgheight': 'IMG Height',
            'imgwidth': 'IMG Width'}

global errorcode
errorcode = (404, 500, 502, 503)

global url_list
url_list=[]

global imgLinkLists
imgLinkLists=[]


def get_image_size(imgurl, responseObj, nextUrl):
    '''
    Find the image size(height and width)
    '''
    # data = requests.get(imgurl).content
    # im = Image.open(BytesIO(data))
    urlbytedata = None
    '''
    try:
        responseObject = requests.get(imgurl, verify=certpath,
                                    headers=hdrs, timeout=30, allow_redirects=True)
    except requests.exceptions.Timeout as e:
        print("Time out Error while fetching image-size", str(e))
        return(None, None)
    '''

    if imgurl == nextUrl:
        urlbytedata = BytesIO(responseObj.content)
        try:
            im = Image.open(urlbytedata)
            return im.size
        except IOError as err:
            print("IOError :", str(err))
            return (None, None)
    else:
        print("URL %s gets redirected...." % imgurl)
        return(None, None)


def images(urlk,):
    print("\n", urlk)
    # Reading URL and storing <img> tag
    try:
        r = requests.get(urlk, verify=certpath, headers=hdrs, timeout=30)
        statusCode = r.status_code
    except requests.exceptions.Timeout as e:
        print("Timeout Error :", str(e))
        print("Moving to next url in urldict")
        return

    if statusCode == 503:
        print("Internal Server Error..! Error Code: %d!" % statusCode)
        return

    # soupdata = souping(r)
    soupdata = BeautifulSoup(r.content)
    imgtag = soupdata.find_all('img') # Finding all <img> tag

    print("****** ", len(imgtag), "imges found *******")
    for link in imgtag:
        #print(urlk + "/" + link.get('src'))
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
            print("xxxxx SRC tag doesn't end with a valid image extention xxxxx", srclink)
            continue

        print("\n<SRC>tag link :", srclink)
        imgurl = urlparse.urljoin(urlk, srclink)
        if imgurl in imgLinkLists:
            print("DUPLICATE IMAGE FOUND")
            continue
        else:
            imgLinkLists.append(imgurl)

        imgurl = imgurl.replace(' ', '%20')
        time.sleep(5)
        try:
            responseObj = requests.get(
                imgurl, verify=certpath, headers=hdrs, timeout=30, allow_redirects=True)
            statusCode = responseObj.status_code
            nextUrl = responseObj.url
        except requests.exceptions.SSLError as e:
            responseObj = requests.get(
                imgurl, verify=True, headers=hdrs, timeout=30, allow_redirects=True)
            statusCode = responseObj.status_code
            nextUrl = responseObj.url
        except requests.exceptions.Timeout as e:
            print("Timeout Error!", str(e))
            continue

        # print(statusCode)
        if statusCode in errorcode:
            if statusCode == 404:
                print(
                    "URL [ %s ] is an INVALID URL(not found on the server)" % imgurl)
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
            width, height = get_image_size(imgurl, responseObj, nextUrl)
        else:
            width, height = imgwidth, imgheight
        print("image Height : ", height)
        print("image Width  : ", width)

        if (height == None or width == None):  
            # height and width not found
            continue

        # Writes when height and Width found 
        filewriter(imgurl, link, link.get('src'),
                   link.get('alt'), height, width)
    return

'''
def souping(url):
    result = list()
    urlResponse = requests.get(url, verify=certpath, headers=hdrs)
    result.append(urlResponse.statusCode)
    result.append(BeautifulSoup(urlResponse.content))
    return result
'''

def url_crawler(url):
    '''
    Crawling website to find all Sub Links
    '''
    print("-------------------------Searching For Images-------------------------")
    images(url)
    print("-------------------------END Searching images-------------------------")

    try:
        responseObject = requests.get(url, verify=certpath, headers=hdrs, timeout=30)
        statusCode = responseObject.status_code
        if statusCode in errorcode:
            return

    except requests.exceptions.Timeout as e:
        print("Timeout error!", str(e))
        return
    
    # Fetching all sub-url from root domain
    #responseObject = requests.get(url, verify=certpath, headers=hdrs, timeout=30)
    #statusCode = responseObject.status_code

    # soupdata = souping(url)
    soupdata = BeautifulSoup(responseObject.content)

    for tags in soupdata.findAll('a'):  # Souping all <a href> tag
        linktag = str(tags.get('href'))
        # print("<a href> tag> ", linktag)
        '''
        if (linktag.startswith('/') and (not(linktag.endswith(tuple(extension))))):
            if ('=' not in linktag):
                abslink=urlparse.urljoin(url, linktag)
                if (abslink not in url_list):
                    url_list.append(abslink)
                    print(abslink)
        else: 
            continue
        '''
        abslink = urlparse.urljoin(url, linktag)
        #print("Absolute Link after join with seed link: ", abslink)
        if ((str(url) in abslink) and (not(abslink.endswith(tuple(extension))))):
            if (abslink not in url_list):
                url_list.append(abslink)
                print("New link added to list", abslink)
        '''
        if (temp.startswith('http') and (not(temp.endswith(tuple(extension))))):
            print(temp)
            tmp.append(temp)
        '''
        '''
        if (not(temp.endswith(tuple(extension)))):
            if (temp.startswith('http')):
                tmp.append(temp)
            else:
                temp = urlparse.urljoin(url, temp)
                tmp.append(temp)
        '''
    return


def url_fetch(mainUrl):
    url_list.append(urlparse.urljoin(mainUrl,"/"))
    for url in url_list:
        print("========================New Sub Url========================")
        print(url)
        url_crawler(url)
    print("Total", len(url_list), "sub link printed")

'''
    for key in (x for x in urlList):
        print(key, "++++ suburl ++++")
        if (key.startswith('mailto')):
            continue
        elif any(domain in key for domain in urlNonEdu):
            print("Non-edu url found....skipping to next url")
            continue
        try:
            statusCode = requests.get(
                key, verify=certpath, headers=hdrs, timeout=30).status_code
        except requests.exceptions.Timeout as e:
            print("Timeout error!", str(e))
            continue
        images(key)
'''

def filewriter(imgul, ul, src, alt, ht, wd):
    fileName = "dataset" + ".csv"
    if os.access(fileName, os.F_OK):
        fileMode = 'a+'
    else:
        fileMode = 'w'

    csvWriter = csv.DictWriter(open(fileName, fileMode), fieldnames=colHeader)

    if fileMode == 'w':
        csvWriter.writerow(colField)  # Writing Column Header

    if alt == " ":
        alt = "Alt text not defined"

    # writing each row with data
    csvWriter.writerow({'imageurl': imgul, 'url': ul, 'src': src, 'alttext': alt, 'imgheight': ht,
                        'imgwidth': wd})
    return