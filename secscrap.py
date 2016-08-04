from bs4 import BeautifulSoup
from urllib.request import urlopen
import os
import csv

def images(url):

    # Reading URL and storing <img> tag
    r = urlopen(url).read()
    bsobj = BeautifulSoup(r)
    imgtag = bsobj.find_all('img')

    # Printing all image tag
    i = 1
    for i in range(len(imgtag)):
        print(i, imgtag[i])

    # Printing only required tag and value
    print("*" * 80)
#     imgsrc = bsobj.find_all('src')
#     for item in imgsrc:
#         print (item)

    m = 1
    for link in imgtag:
        filewriter(m, link, link.get('alt'), link.get('height'), link.get('width'))
        m += 1

def urlParse(url):
    thepage = urlopen(url)
    soupdata = BeautifulSoup(thepage, "html.parser")
    return soupdata

soup = urlParse('http://www.pondiuni.edu.in')
print("#" * 80)
extension = ('.pdf', '.doc', '.docx', '.txt', 'xls', 'xlsx')
urldict = {}
temp = []

# Fetching all sub-url from root domain
for ur in soup.findAll('a'):
    temp = ur.get('href')
    if str(temp).startswith('http') and (str(temp).endswith(tuple(extension)) == False):
        urldict[temp] = 0

print('Printing URL List.....................................')
for key in urldict:
    print(key, urldict[key])

print("Total", len(urldict), "link printed")

colHeader = ['s.no', 'url', 'alttext', 'imgheight', 'imgwidth']
colField = {'s.no' : 'S. No.', 'url' :  'URL',
            'alttext' : 'ALT Text', 'imgheight' : 'IMG Height',
            'imgwidth' : 'IMG Width'}

def filewriter(x,y,z,a,b):
    fileName = "pondiuni" + ".csv"
    if os.access(fileName, os.F_OK):
        fileMode = 'a+'
    else:
        fileMode = 'wb'

    csvWriter = csv.DictWriter(open(fileName, fileMode), fieldnames = colHeader)

    if fileMode == 'wb':
        csvWriter.writerow(colField)
        # csvWriter.writeheader()
    csvWriter.writerow({'s.no' : x, 'url' : y, 'alttext' : z, 'imgheight' : a, 'imgwidth' : b})

for key in (x for x in urldict):
    images(key)
    # print(i,key)
    # i += 1

with open('pondiuni.csv') as myfile:
    reader = csv.DictWriter(myfile)
    for row in reader:
        print(row['S.No'], row['Link'])
