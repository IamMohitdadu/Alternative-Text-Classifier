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
global extension
extension = ('.pdf', '.doc', '.docx', '.txt', '.xls', '.xlsx','.css')

colHeader = ['imageurl', 'url', 'src', 'alttext', 'imgheight', 'imgwidth']
colField = {'imageurl':'IMAGE URL','url': 'URL', 'src': 'SRC',
            'alttext': 'ALT Text', 'imgheight': 'IMG Height',
            'imgwidth': 'IMG Width'}

global errorcode
errorcode = (404, 500, 502, 503)

urlNonEdu=['facebook.com','youtube.com','onlinesbi.com','gaberic.org','jssor.com','2glux.com',\
    'freehitcountercodes.com','ugc.ac.in','hit-counts.com','twitter.com','wowslider.com',\
    'google.com','bih.nic.in','gov.in','clat.ac.in','sphererays.com','mysy.guj.nic.in',\
    'gujaratinformatics.com','agri.ikhedut.aau.in','icar.org.in','in.linkedin.com','icar.org.in'\
    'logicopedia.in','gujaratindia.com','gsauca.in','dare.nic.in','faq.ikhedut.aau.in',\
    'indiaveterinarycommunity.com','iasri.res.in','vibrantgujarat.com','vidyalakshmi.co.in',\
    'gmail.com','escortigdir.xyz', 'escortgaziantep.xyz', 'sedo.com', 'web-stat.com', 'gstatic.com',\
    'maruticomputers', 'supercounters.com','gate-2016.in', 'easycounter.com', 'eands.dacnet.ac',\
    'jgateplus.com', 'openid.net', 'delcon.gov', 'asapglobe.com','life-global.org','edcastcloud.com']


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
    #if imgurl.startswith('https'):
    req = requests.get(imgurl, verify=True,
                       headers=hdrs, allow_redirects=True)
    #else:
    #    req = requests.get(imgurl, verify=False,
    #                       headers=hdrs, allow_redirects=True)

    if imgurl == req.url:
        urlbytedata = BytesIO(req.content)
        try:
            im = Image.open(urlbytedata)
            return im.size
        except IOError as err:
            print("IOError :", str(err))
            return (None, None)
    else:
        print("URL %s gets redirected...." %imgurl)
        return(None, None)


def images(urlk,):
    print("\n", urlk)
        # Reading URL and storing <img> tag
    if any(domain in urlk for domain in urlNonEdu):
        print("Non-edu url found....skipping to next url")
        return
    else:
        try:
            r = requests.get(urlk, headers=hdrs, verify=True, timeout=30)
            statusCode = r.status_code
        except requests.exceptions.Timeout as e:
            print("Timeout Error :", str(e))
            print("Moving to next url in urldict")
            return

    if statusCode == 503:
        print("Internal Server Error..! Error Code: %d!" % statusCode)
        return

    #imgtag=souping(r)
    bsobj = BeautifulSoup(r.content)
    imgtag = bsobj.find_all('img')  # Finding all <img> tag

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
            print("xxxxx [%s] SRC tag doesn't end with a valid image extention xxxxx" % srclink)
            continue

        print(srclink)
        imgurl = urlparse.urljoin(urlk, srclink)
        imgurl = imgurl.replace(' ', '%20')
        time.sleep(5)
        try:
            statusCode = requests.get(
                imgurl, headers=hdrs, verify=True, timeout=30).status_code
        except requests.exceptions.Timeout:
            print
            continue

        print(statusCode)
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

        if height and width:
            filewriter(imgurl, link, link.get('src'), link.get('alt'), height, width)


def souping(url):
    thepage=requests.get(url)
    soupdata = BeautifulSoup(thepage.content)
    return soupdata


def urlFetch(url):
    urldict = []
    tmp = []
    print("-------------------------------------------------------------------------")
    images(url)
    print("-------------------------------------------------------------------------")
    # Fetching all sub-url from root domain
    thepage = requests.get(url, verify=True, headers=hdrs)
    pageStatus = thepage.status_code

    if pageStatus in errorcode:
        return

    soup=souping(url)
    
    print('a')
    for ur in soup.findAll('a'):
        temp = ur.get('href')
        temp=str(temp)
        print(temp)
        '''
        if (temp.startswith('http') and (not(temp.endswith(tuple(extension))))):
            print(temp)
            tmp.append(temp)
        '''
        if (not(temp.endswith(tuple(extension)))):
            if (temp.startswith('http')):
                tmp.append(temp)
            else:
                temp=urlparse.urljoin(url, temp)
                tmp.append(temp)

    print("link")
    for ur in soup.findAll('link'):
        temp = ur.get('href')
        #print(temp)
        '''
        if (temp.startswith('http') and (not(temp.endswith(tuple(extension))))):
            print(temp)
            tmp.append(temp)
        '''
        if (not(temp.endswith(tuple(extension)))):
            if (temp.startswith('http')):
                tmp.append(temp)
            else:
                temp=urlparse.urljoin(url, temp)
                tmp.append(temp)
        
    urldict=list(set(tmp))
    print("Total", len(urldict), "link printed")

    for key in (x for x in urldict):
        print(key, "++++ suburl ++++")
        if (key.startswith('mailto')):
            continue
        try:
            statusCd = requests.get(key, headers=hdrs, verify=True, timeout=30).status_code
        except requests.exceptions.Timeout:
            print("timeout")
            continue
        images(key)


def filewriter(imgul, ul, src, alt, ht, wd):
    fileName = "pondiuni" + ".csv"
    if os.access(fileName, os.F_OK):
        fileMode = 'a+'
    else:
        fileMode = 'w'

    csvWriter = csv.DictWriter(open(fileName, fileMode), fieldnames=colHeader)

    if fileMode == 'w':
        csvWriter.writerow(colField)  # Writing Column Header

    if alt==" ":
        alt = "Alt text not defined"

    # writing each row with data
    csvWriter.writerow({'imageurl':imgul, 'url': ul, 'src': src, 'alttext': alt, 'imgheight': ht,
                        'imgwidth': wd})
    return