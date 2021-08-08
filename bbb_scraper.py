import requests
from bs4 import BeautifulSoup
import pandas as pd
from time import sleep

results = []

def get_details(soup):
    global search, cityy, state, total
    items = soup.select('div.result-item')
    for item in items:
        if item.select_one('a.AdDisclosure-sc-1vrwuf3-0') :  pass
        else:
            data = {}
            data['Name'] = item.select_one('a.duvGnB').text
            data['Link'] = item.select_one('a.duvGnB')['href']

            if item.select_one('.result-item__categories'):
                data['Category'] = item.select_one('.result-item__categories').text
            else : data['Category'] = '-'

            if item.select_one('a[title="Call this BBB"]'):
                data['Phone'] = item.select_one('a[title="Call this BBB"]')['href'].replace('tel:','')
            else : data['Phone'] = '-'

            if item.select_one('.result-item__address'):
                data['Address'] = item.select_one('.result-item__address').text
            else : data['Address'] = '-'

            if item.select_one('.result-item__rating .ccWqHZ'):
                data['rating'] = item.select_one('.result-item__rating .ccWqHZ').text
            else : data['rating'] = '-'
            
            results.append(data)
            print(len(results), ' of ', total, data)
    df = pd.DataFrame(results)
    df.to_excel(f'BBB {cityy}, {state} {search}.xlsx',index=False)
    sleep(3)

headers = {
    'sec-ch-ua': '"Chromium";v="88", "Google Chrome";v="88", ";Not A Brand";v="99',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36',
    'content-type': 'text/plain',
    'accept': '*/*',
    'origin': 'https://www.bbb.org',
    'referer': 'https://www.bbb.org/',
    'accept-language': 'en-US,en;q=0.9',
}

cityy = 'Los Angeles'
state = 'CA'
search = 'General Contractor'

city = cityy.replace(' ','%20')
search_word = search.replace(' ','%20')
url = f'https://www.bbb.org/search?city={city}&find_country=USA&find_loc={city}%2C%20{state}&find_text={search_word}'
response = requests.get(url, headers=headers)

if response.status_code in range(200,300):
    soup = BeautifulSoup(response.content, 'html.parser')
    total = soup.select_one('h2.search-heading__subtitle > strong').text
    get_details(soup)
    next_page = soup.select_one('a:contains("Next")')
    while next_page:
        url = next_page['href']
        response = requests.get(url, headers=headers)
        if response.status_code in range(200,300):
            soup = BeautifulSoup(response.content, 'html.parser')
            get_details(soup)
            next_page = soup.select_one('a:contains("Next")')
        else :
            print(f'Error with response {response.status_code}')
            pass
else :
    print(f'Error with response {response.status_code}')
    pass
