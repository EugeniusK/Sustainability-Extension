import requests
from bs4 import BeautifulSoup
import json
import time

# Web scraping performed on climatiq.io
ID_SCRAPED = True
if ID_SCRAPED == False:
    final_json = []
    URL = 'https://www.climatiq.io/explorer?page='
    for page_no in range(1,295+1):
        page = requests.get(URL + str(page_no))
        soup = BeautifulSoup(page.content, 'html5lib')
        data = soup.select_one('#__NEXT_DATA__').string
        json_data = json.loads(data)
        final_json += [activity['activity_id'] for activity in json_data['props']['pageProps']['activities']]
    with open('climatiq_data/activity_id.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(final_json))

# Accessing API for each activity id

DATA_SCRAPED = True
if DATA_SCRAPED == False:
    URL = 'https://www.climatiq.io/explorer/api/factors?activity_id='
    final_json = []
    with open('climatiq_data/activity_id.json', 'r', encoding='utf-8') as j:
        json_data = json.load(j)
        for id in json_data:
            id_data = requests.get(URL + id)
            final_json += json.loads((id_data.content))['results']
            print(id)
    with open('climatiq_data/data.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(final_json))

with open('climatiq_data/data.json', 'r', encoding='utf-8') as f:
    data_keys = []
    json_data = json.load(f)

    for key in json_data[0].keys():
        print('max length', key, max([len(str(d[key])) if type(d[key]) == str else 1 for d in json_data]))

    print(max([len(activity) for activity in json_data]))


FILTERED = True
if FILTERED == False:
    with open('climatiq_data/data.json', 'r', encoding='utf-8') as f:
        json_data = json.load(f)
        final_data = []
        for data in json_data:
            if data['access_type'] == 'public' and 'Cloud Computing' not in data['category']and data['sector'] not in [
                'Transport', 'Waste', 'Insurance and Financial Services',"Buildings and Infrastructure", "Education", 'Energy', 'Organizational Activities', "Restaurants and Accommodation", 'Water'
            ]:
                if data['unit_type'][0] not in ['Weight', 'Money']:
                    print(data['unit_type'])
                tmp_json = {
                    'uuid': data['uuid'].replace('-', ''),
                    'name': data['name'],
                    'category': data['category'],
                    'sector': data['sector'],
                    'year': data['year'],
                    'region': data['region'],
                    'description': data['description'],
                    'unit_type': data['unit_type'][0],
                    'unit': data['unit'],
                    'co2e_factor': round(data['factor'], 3),   
                }
                if data['constituent_gases']['co2'] != None:
                    tmp_json['co2'] = round(data['constituent_gases']['co2'], 3)
                else:
                    tmp_json['co2'] = -1
                if data['constituent_gases']['ch4'] != None:
                    tmp_json['ch4'] = round(data['constituent_gases']['ch4'], 3)
                else:
                    tmp_json['ch4'] = -1
                if data['constituent_gases']['n2o'] != None:
                    tmp_json['n2o'] = round(data['constituent_gases']['n2o'], 3)
                else:
                    tmp_json['n2o'] = -1
                final_data.append(tmp_json)
        copy_final_data = [x for x in final_data]
        removed_data = []
        while True:
            removed = 0

           
            for data in final_data:
                for other_data in final_data:
                    if other_data['name'] == data['name'] and other_data['category'] == data['category'] and other_data['sector'] == data['sector'] and other_data['region'] == data['region']:
                        #print(data)
                        if data['year'] < other_data['year'] and data not in removed_data:
                            copy_final_data.remove(data)
                            
                            removed_data.append(data)
                            removed += 1
                        elif data['year'] > other_data['year'] and other_data not in removed_data:
                            copy_final_data.remove(other_data)
                            removed_data.append(other_data)
                            removed += 1
            if removed == 0:
                break

        combined_final_data = []
        for data in final_data:
            combined_final_data.append(
                {
                    'name_category_sector_description': " ".join([data['name'], data['category'], data['sector'], data['description']]),
                    'region': data['region'],
                    'unit_type': data['unit_type'][0],
                    'unit': data['unit'],
                    'co2e_factor': data['co2e_factor'],
                    'co2': data['co2'],
                    'ch4': data['ch4'],
                    'n2o': data['n2o']
                }
            )


    with open('climatiq_data/final.json', 'w', encoding='utf-8') as f:
        json_data = json.dumps(combined_final_data)
        f.write(json_data)

POSTED = False
if POSTED == False:
    with open('climatiq_data/final.json', 'r', encoding='utf-8') as f:
        json_data = json.load(f)
        for data in json_data:
            error = True
            while error == True:
                r = requests.post('http://127.0.0.1:8000/api/activities/', json=data)
                if r.status_code == 201:
                    error = False
                else:
                    time.sleep(0.5)
                    print(data)
            
