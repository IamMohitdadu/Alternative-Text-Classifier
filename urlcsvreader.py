import csv
import secscrap
from collections import defaultdict

columns = defaultdict(list)  # each value in each column is appended to a list

with open('urls.csv') as f:
    reader = csv.DictReader(f)  # read rows into a dictionary format
    for row in reader:  # read a row as {column1: value1, column2: value2,...}
        for (k, v) in row.items():
            columns[k].append(v)  # append the value into the appropriate list
            # based on column name k
#print(columns['University Name'])
print(columns['URL'])
global i
i=0

#secscrap.url_fetch("http://www.pondiuni.edu.in")

for url in columns['URL']:
    if not(url):
    	continue
    
    i=i+1
    print("$" * 80)
    print("url {} fetching from csv file".format(i))
    print(url)
    #secscrap.urlFetch(urllist)
    secscrap.url_fetch(url)
    secscrap.url_list=[]