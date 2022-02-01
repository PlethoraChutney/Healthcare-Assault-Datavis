from bs4 import BeautifulSoup
import requests
import pandas as pd

base_url = 'https://www.bls.gov'
r = requests.get(base_url + '/iif/oshstate.htm')

soup = BeautifulSoup(r.content)

table = soup.findChildren('table')[0]
rows = table.findChildren('tr')

for row in rows:
    csv_link = None
    cells = row.findChildren('td')
    try:
        cell = cells[2]
    except IndexError:
        continue

    links = cell.findChildren('a')
    for link in links:
        if link.text == 'XLSX':
            csv_link = link['href']
            break

    if csv_link is not None:
        print(base_url + csv_link)
        data = pd.read_excel(base_url + csv_link, header=1)
        data.columns = [x.rstrip() for x in data.columns]
        print(data)
        try:
            print(data[data['NAICS Code3'] == 62])
        except KeyError:
            continue