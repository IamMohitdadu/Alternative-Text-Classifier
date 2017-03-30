import csv
import random
import os
import sys
import logging
import time
import socket
import tldextract as tld
import urllib.parse as urlparse
import requests
from io import BytesIO
from PIL import Image
from bs4 import BeautifulSoup

global imgext
imgext = ('bmp', 'BMP', 'jpeg', 'JPEG', 'jpg', 'JPG', 'gif', 'GIF', 'tiff', 'TIFF', 'png', 'PNG')

#global hdrs
#hdrs = {'User-Agent': 'Mozilla / 5.0 (X11 Linux x86_64) AppleWebKit / 537.36 (\
#        KHTML, like Gecko) Chrome / 52.0.2743.116 Safari / 537.36'}

global certpath
certpath = 'gd_bundle-g2-g1.crt'

global fileExtension
fileExtension = ('.pdf', '.PDF', '.rar', '.RAR', '.doc', '.docx', '.txt', '.xls', '.xlsx', '.css', '.csv', '.zip','.ZIP', '.wmv', '.WMV', '.swf', '.SWF', '.db', '.mp4', '.MP4', '.wav')

colHeader = ['imageurl', 'url', 'src', 'alttext', 'imgheight', 'imgwidth']
colField = {'imageurl': 'IMAGE URL', 'url': '<img> TAG', 'src': 'SRC',
            'alttext': 'ALT Text', 'imgheight': 'IMG Height',
            'imgwidth': 'IMG Width'}

global errorcode
errorcode = (404, 500, 502, 503)

global urlList
urlList = []

global imgLinkSet
imgLinkSet = set()

#logging.basicConfig(level=logging.DEBUG) # Print connection log

userAgentString = ['Mozilla/5.0 (X11; Linux x86_64; Debian) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.52 Safari/537.36 OPR/15.0.1147.100', 'Mozilla / 5.0 (X11 Linux x86_64); AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:33.0) Gecko/20100101 Firefox/33.0', 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2376.0 Safari/537.36 OPR/31.0.1857.0', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36 OPR/32.0.1948.25', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_0) AppleWebKit/600.3.10 (KHTML, like Gecko) Version/8.0.3 Safari/600.3.10', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.38 Safari/537.36', 'Mozilla/5.0 (X11; Linux x86_64; Ubuntu 14.04.2 LTS) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.0 Maxthon/1.0.5.3 Safari/537.36', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36 OPR/18.0.1284.68', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.124 Safari/537.36', 'Opera/12.80 (Windows NT 5.1; U; en) Presto/2.10.289 Version/12.02', 'Opera/9.80 (X11; Linux i686; Ubuntu/14.10) Presto/2.12.388 Version/12.16']


def random_user_agent(userAgentlist):
    ua = random.choice(userAgentlist) # generate random user agent from userAgentlist.
    return ua

 
def getimgSize(imgurl, responseObj, nextUrl):
    '''
    Find the image size(height and width)
    '''
    urlbytedata = None

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


def images(urlk):
    print(urlk)
    # Reading URL and storing <img> tag
    s = requests.Session()
    hdrs = {'User-Agent': random_user_agent(userAgentString)}
    try:
        responseObj = s.get(urlk, verify=certpath, headers=hdrs, timeout=20, stream=False)
    except (requests.exceptions.SSLError) as e:
        responseObj = s.get(urlk, verify=True, headers=hdrs, timeout=20, stream=False)
    except (requests.exceptions.ConnectionError, requests.exceptions.HTTPError, requests.exceptions.SSLError) as e:
        print(repr(e))
        print("Skipping to next ur")
        return
    except (requests.exceptions.InvalidSchema)  as e:
        print("Invalid URL Schema", repr(e))
        print("Skipping to next url")
        return
    except (socket.timeout, requests.exceptions.Timeout) as e:
        print("Time out Error!", repr(e))
        print("Skipping to next url")
        return
    except (requests.exceptions.ReadTimeout) as e:
        print(str(e))
        return
    except:
        print("Someting unexpected happend while sending request to server..!", sys.exc_info()[0])
        return
    
    if not(responseObj.ok):
        print("Oops! something unexpected happened..! please check error Code for more info.")
        print("Error Code: {}" .format(responseObj.status_code))
        return
    
    # soupdata = souping(r)
    soupdata = BeautifulSoup(responseObj.content, 'lxml')
    imgtag = soupdata.find_all('img', src=True) # Finding all <img> tag

    print("****** ", len(imgtag), "<img> tags found *******")
    for link in imgtag:
        #print(urlk + "/" + link.get('src'))

        # Getting <src> attribute from <img> tag and storing it
        if (link.get('src')).startswith(('.', ' ')):
            print("Invalid <src> path: starts with .(dot) or space( )", link.get('src'))
            srclink = link.get('src')[1:]
            continue
        else:
            srclink = link.get('src')

        if not(srclink.endswith(tuple(imgext))):
            print("<src> attribute ends with an invalid image extention", srclink)
            continue

        #print("\n<src> attribute :", srclink)
        imgurl = urlparse.urljoin(urlk, srclink)
        if imgurl in imgLinkSet :
            print("DUPLICATE IMAGE FOUND", imgurl)
            continue
        else:
            imgLinkSet.add(imgurl)

        baseDomain = tld.extract(urlk).registered_domain
        if baseDomain not in imgurl:
            continue
        imgurl = imgurl.replace(' ', '%20')
        try:
            responseObject = s.get(
                imgurl, verify=certpath, headers=hdrs, timeout=20, allow_redirects=True, stream=False)
            nextUrl = responseObject.url
        except (requests.exceptions.SSLError) as e:
            responseObject = s.get(
                imgurl, verify=True, headers=hdrs, timeout=20, allow_redirects=True, stream=False)
            nextUrl = responseObject.url
        except (requests.exceptions.ConnectionError, requests.exceptions.HTTPError) as e:
            print("Oops! Something unexpected happened", repr(e))
            continue
        except requests.exceptions.InvalidSchema as e:
            print("Invalid URL Schema", repr(e))
            continue
        except (socket.timeout, requests.exceptions.Timeout) as e:
            print("Time out Error!", str(e))
            continue
        except (requests.exceptions.ReadTimeout) as e:
            print(str(e))
            continue

        '''
        if statusCode in errorcode:
            if statusCode == 404:
                print("URL [ %s ] is an INVALID URL(not found on the server)" % imgurl)
            elif statusCode == 500:
                print("Internal Server Error with URL %s" % imgurl)
            elif statusCode == 502:
                print("Bad Gateway......Error with URL %s" % imgurl)
            elif statusCode == 503:
                print("Service Unavailable....Error with URL %s" % imgurl)

            print("Skiping to next link in <imgtag>")
            continue
        '''
        if not(responseObject.ok):
            print("Someting bad happened while requesting image url due to network error..Skipping to next image url", imgurl)
            continue

        print("Image URL is : ", imgurl)
        imgheight = link.get('height')
        imgwidth = link.get('width')

        if not(imgheight and imgwidth):
            width, height = getimgSize(imgurl, responseObject, nextUrl)
        else:
            width, height = imgwidth, imgheight
        print("image Height : ", height)
        print("image Width : ", width)

        if (height == None or width == None):
            # height and width not found
            continue

        # Writes when height and Width found.
        fileWriter(imgurl, link, link.get('src'),
                   link.get('alt'), height, width)
    return

'''
def souping(url):
    # This function is for future use and it is incomplete as of now.
    result = list()
    urlResponse = requests.get(url, verify=certpath, headers=hdrs)
    result.append(urlResponse.statusCode)
    result.append(BeautifulSoup(urlResponse.content))
    return result
'''

def urlCrawler(url):
    '''
    Crawling website to find all Sub Links
    '''
    global s
    s = requests.Session()
    
    print("-------------------------Searching For Images-------------------------")
    images(url)
    print("----------END Searching images--------Addition of suburl to urlSET started-----------")
    ua = {'User-Agent': random_user_agent(userAgentString)}
    time.sleep(5)
    try:
        responseObject = s.get(url, verify=certpath, headers=ua, timeout=20)
    except (requests.exceptions.SSLError) as e:
        responseObject = s.get(url, verify=True, headers=ua, timeout=20)
    except (requests.exceptions.ConnectionError, requests.exceptions.HTTPError) as e:
        print("Connection Error", str(e))
        return
    except (requests.exceptions.InvalidSchema) as e:
        print("Invalid URL Schema", str(e))
        return
    except (socket.timeout, requests.exceptions.Timeout) as e:
        print("Time out Error!", str(e))
        return
    
    
    if not(responseObject.ok):
            print("Oops! something unexpected happened..! please check error Code for more info.")
            print("Error Code: {}" .format(responseObject.status_code)) 
            return
    # Fetching all sub-url from root domain
  
    # soupdata = souping(url)
    soupdata = BeautifulSoup(responseObject.content, 'lxml')
    aTag = soupdata.find_all('a', href=True)
    #print(aTag)
    baseDomain = tld.extract(url).registered_domain
    for tags in aTag: # Souping all <a href> tag
        linktag = str(tags.get('href'))
        if not(linktag) or linktag.startswith(('.', ' ' , 'javascript', 'Javascript', 'JavaScript', 'JAVASCRIPT')):
            #print("Invalid href value {}".format(linktag))
            continue
        #print("<a href> tag> ", linktag)

        if baseDomain not in linktag:
            if linktag.startswith('http') or (linktag.startswith('www')):
                print("THIRD-PARTY URL FOUND!", linktag)
                continue
            elif not(linktag.endswith(tuple(fileExtension))):
                abslink = urlparse.urljoin(url, linktag)
            else:
                continue
        elif not(linktag.endswith(tuple(fileExtension))):
            if linktag.startswith('www') or linktag.startswith('http'):
                abslink = linktag
        else:
            continue
         
        # print("Absolute URL after joining with url taken from <href> attrib: ", abslink)

        #if(baseDomain in abslink ):
        if abslink not in urlList and not(abslink.startswith('https://mail')):
            urlList.append(abslink)
            print("New SUB-URL added to urlList", abslink)
            print("Lenght of urlList increased to {}" .format(len(urlList)))
            #else:
             #   print("DUPLICATE SUB-URL FOUND", abslink)
        elif not(baseDomain in abslink) and (abslink.endswith(tuple(fileExtension))):
            print("Either Base url not in absolute url or It ends with a file extension", abslink)

    return


def urlFetch(mainUrl):
    urlList.append(mainUrl)
    for url in urlList:
        print("========================New Sub Url========================")
        print(url)
        urlCrawler(url)
        #print("Length of urlList {}" .format(len(urlList)))
    print("Total", len(urlList), "SUB-URL explored")


def fileWriter(imgurl, ul, src, alt, ht, wd):
    fileName = "dataset" + ".csv"
    if os.access(fileName, os.F_OK):
        fileMode = 'a+'
    else:
        fileMode = 'w'

    with open(fileName, fileMode) as csvFile:
        csvWriter = csv.DictWriter(csvFile, fieldnames=colHeader)
        if fileMode == 'w':
            csvWriter.writerow(colField)
        
     # Writing Column Header

    #if alt == " ":
     #   alt = "Alt text not defined"

    # writing each row with data
        csvWriter.writerow({'imageurl': imgurl, 'url': ul, 'src': src, 'alttext': alt, 'imgheight': ht,
                        'imgwidth': wd})
    return
