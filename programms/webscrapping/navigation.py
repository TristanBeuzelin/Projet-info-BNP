import requests
import bs4 as BeautifulSoup
def get_year_older_data(soup):
    form = soup.find_all('input', attrs={'type': 'hidden'})
    espece = None
    last_date = None
    for line in form:
        if line.get('name') == "ESPECE":
            espece = line.get('value')
        if line.get('name') == "LASTDATE":
            last_date = line.get('value')
            year = int(last_date[-2:])
            year = year-1
            new_last_date = last_date[:-2] + str(year)
        if espece != None and last_date != None:
            headers = {'User-Agent': 'Mozilla/5.0'}
            link    = 'https://rnm.franceagrimer.fr/prix'
            payload = {'MENSUEL': '1', 'ESPECE': espece, 'DATE': new_last_date}
            session = requests.Session()
            resp    = session.get(link,headers=headers)
            cookies = requests.utils.cookiejar_from_dict(requests.utils.dict_from_cookiejar(session.cookies))
            resp    = session.post(link, headers = headers, data = payload, cookies = cookies)
            return BeautifulSoup(resp.text, 'html.parser')