from bs4 import BeautifulSoup
import requests
import pandas as pd

base_url = 'https://www.bls.gov'
r = requests.get(base_url + '/iif/oshstate.htm')

soup = BeautifulSoup(r.content, features = 'html.parser')

table = soup.findChildren('table')[0]
rows = table.findChildren('tr')

states = []

for row in rows:
    csv_link = None
    cells = row.findChildren('td')
    try:
        state = cells[0].text.strip().replace('SOII', '').replace('/CFOI', '')
        cell = cells[2]
    except IndexError:
        continue

    links = cell.findChildren('a')
    for link in links:
        if link.text == 'XLSX':
            csv_link = link['href']
            break

    if csv_link is not None:
        data = pd.read_excel(base_url + csv_link, header=1)
        data.columns = [x.rstrip() for x in data.columns]
        # NAICS Code has a 3 on it because of the footnote.
        if 'NAICS Code3' not in data.columns:
            continue
        try:
            all_healthcare = data[data['NAICS Code3'] == '62']
            all_healthcare = float(all_healthcare.iloc[0]['Total recordable cases'])
        # have to except a ValueError too, all because Montana has a (-10-) in its data for some reason
        except (IndexError, ValueError):
            all_healthcare = None
        try:
            hospitals = data[data['NAICS Code3'] == '622']
            hospitals = float(hospitals.iloc[0]['Total recordable cases'])
        except (IndexError, ValueError):
            hospitals = None
        try:
            nursing_and_res_care = data[data['NAICS Code3'] == '623']
            nursing_and_res_care = float(nursing_and_res_care.iloc[0]['Total recordable cases'])
        except (IndexError, ValueError):
            nursing_and_res_care = None
        state_dict = {
            'state': state,
            'all_healthcare': all_healthcare,
            'hospitals': hospitals,
            'nursing_and_res_care': nursing_and_res_care
            }

        if not all([x is None for x in state_dict.values()]):
            states.append(state_dict)

final_data = pd.DataFrame(states)
final_data.to_csv('all_state_data.csv', index = False)
