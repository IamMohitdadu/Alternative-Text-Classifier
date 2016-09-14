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

for urllist in columns['URL']:
    print("$" * 80)
    print(urllist)
    secscrap.urlFetch(urllist)
