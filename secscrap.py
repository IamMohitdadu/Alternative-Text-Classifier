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
extension = ('.pdf', '.doc', '.docx', '.txt', '.xls', '.xlsx', '.css', '.zip')

colHeader = ['imageurl', 'url', 'src', 'alttext', 'imgheight', 'imgwidth']
colField = {'imageurl': 'IMAGE URL', 'url': 'URL', 'src': 'SRC',
            'alttext': 'ALT Text', 'imgheight': 'IMG Height',
            'imgwidth': 'IMG Width'}

global errorcode
errorcode = (404, 500, 502, 503)

global url_list
url_list=[]
'''
global urlNonEdu
urlNonEdu = ['facebook.com', 'youtube.com', 'onlinesbi.com', 'gaberic.org', 'jssor.com', '2glux.com',
             'freehitcountercodes.com', 'ugc.ac.in', 'hit-counts.com', 'twitter.com', 'wowslider.com',
             'google.com', 'bih.nic.in', 'gov.in', 'clat.ac.in', 'sphererays.com', 'mysy.guj.nic.in',
             'gujaratinformatics.com', 'agri.ikhedut.aau.in', 'icar.org.in', 'linkedin.com', 'icar.org.in'
             'logicopedia.in', 'gujaratindia.com', 'gsauca.in', 'dare.nic.in', 'faq.ikhedut.aau.in',
             'indiaveterinarycommunity.com', 'iasri.res.in', 'vibrantgujarat.com', 'vidyalakshmi.co.in',
             'gmail.com', 'escortigdir.xyz', 'escortgaziantep.xyz', 'sedo.com', 'web-stat.com', 'gstatic.com',
             'maruticomputers', 'supercounters.com', 'gate-2016.in', 'easycounter.com', 'eands.dacnet.ac',
             'jgateplus.com', 'openid.net', 'delcon.gov', 'asapglobe.com', 'life-global.org', 'edcastcloud.com',
             'nssanu.org', 'goo.gl', 'webinfinium.com', 'gujaratinformatics.com', 'aiu.ac.in', 'apmedco.com',
             'nityahosting.com', 'rcsindia.co.in', 'aiuweb.org', 'appgecet.org', 'solventindia.com', 'javascript']
'''

def get_image_size(imgurl):
    #    Find the image size(height and  width)
    
    # data = requests.get(imgurl).content
    # im = Image.open(BytesIO(data))
    urlbytedata = None
    try:
        responseObject = requests.get(imgurl, verify=certpath,
                                      headers=hdrs, timeout=30, allow_redirects=True)
    except requests.exceptions.SSLError:
        responseObject = requests.get(imgurl, verify=True, headers=hdrs,
                                       timeout=30, allow_redirects=True)
    except requests.exceptions.Timeout as e:
        print("Time out Error while fetching image-size", str(e))
        return(None, None)

    if imgurl == responseObject.url:
        urlbytedata = BytesIO(responseObject.content)
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
    '''
    if any(domain in urlk for domain in urlNonEdu):
        print("Non-edu url found....skipping to next url")
        return
    else:
        try:
            r = requests.get(urlk, verify=certpath, headers=hdrs, timeout=30)
            statusCode = r.status_code
        except requests.exceptions.Timeout as e:
            print("Timeout Error :", str(e))
            print("Moving to next url in urldict")
            return
    '''
    try:
        responseObject = requests.get(urlk, verify=certpath, headers=hdrs, timeout=30)
        statusCode = responseObject.status_code
    except requests.exceptions.SSLError:
        responseObject = requests.get(urlk, verify=True, headers=hdrs, timeout=30)
        statusCode = responseObject.status_code
    except requests.exceptions.Timeout as e:
        print("Timeout Error :", str(e))
        print("Moving to next url in urldict")
        return

    if statusCode == 503:
        print("Internal Server Error..! Error Code: %d!" % statusCode)
        return

    # soupdata = souping(r)
    soupdata = BeautifulSoup(responseObject.content)
    imgtag = soupdata.find_all('img')  # Finding all <img> tag

    print(len(imgtag), "+++imglinks+++")
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

        print(srclink)
        imgurl = urlparse.urljoin(urlk, srclink)
        imgurl = imgurl.replace(' ', '%20')
        time.sleep(5)
        try:
            statusCode = requests.get(
                imgurl, verify=certpath, headers=hdrs, timeout=30).status_code
        except requests.exceptions.SSLError:
            statusCode = requests.get(
                imgurl, verify=True, headers=hdrs, timeout=30).status_code
        except requests.exceptions.Timeout as e:
            print("Timeout Error!", str(e))
            continue

        print(statusCode)
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
            width, height = get_image_size(imgurl)
            print(height, width)
        else:
            width, height = imgwidth, imgheight
            print(height, width)
        if (height == None or width == None):
            continue
        
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
    
    print("-------------------------------------------------------------------------")
    images(url)
    print("-------------------------------------------------------------------------")

    try:
        responseObject = requests.get(url, verify=certpath, headers=hdrs, timeout=30)
    except requests.exceptions.SSLError:
        responseObject = requests.get(url, verify=True, headers=hdrs)
    statusCode=responseObject.status_code
    if statusCode in errorcode:
        return
    '''
    except requests.exceptions.Timeout as e:
        print("Timeout error!", str(e))
        return
    '''
    
    # Fetching all sub-url from root domain
    #responseObject = requests.get(url, verify=certpath, headers=hdrs, timeout=30)
    #statusCode = responseObject.status_code

    #if statusCode in errorcode:
    #    return

    # soupdata = souping(url)
    soupdata = BeautifulSoup(responseObject.content)

    for tags in soupdata.findAll('a'):
        linktag = str(tags.get('href'))
        #print(temp)
        if (linktag.startswith('/') and (not(linktag.endswith(tuple(extension))))):
            if ('=' not in linktag):
                abslink=urlparse.urljoin(url, linktag)
                if (abslink not in url_list):
                    url_list.append(abslink)
                    print(abslink)
        else: 
            continue
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


def url_fetch(urs):
    url_list.append(urlparse.urljoin(urs,"/"))
    for ur in url_list:
        print("+++++++++++++++++++++++++++++++++")
        print(ur)
        print("+++++++++++++++++++++++++++++++++")
        url_crawler(ur)
    print("Total", len(url_list), "link printed")


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
    fileName = "pondiuni" + ".csv"
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