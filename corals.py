from helpers import simple_get, split_string
from bs4 import BeautifulSoup
import re

def get_urls():
    url = 'https://reefs.com/coral/'
    response = simple_get(url)

    if response is not None:
        html = BeautifulSoup(response, 'html.parser')
        script = [s.extract() for s in html('script')][30]
        list = re.findall(r'coral/[\w\.-]+', script.text)
        return list


def get_data(url):
    response = simple_get(url)

    if response is not None:
        data = {}
        html = BeautifulSoup(response, 'html.parser')
        content = html.find('div', class_='dbEntryContent')
        
        strong_content = content.find_all('strong')
        data['full_genus'] = strong_content[0].text.strip()
        data['name'] = strong_content[1].next_sibling.strip()
        data['genus'] = strong_content[2].next_sibling.strip()
        data['coral_type'] = strong_content[3].next_sibling.strip()
        data['image'] = content.find('img')['src']

        color = content.find(string=re.compile('Color')).strip()
        all_colors = split_string(color)
        data['color'] = all_colors.split(', ')

        feeding = content.find(string=re.compile('Feeding')).strip()
        data['feeding'] = split_string(feeding)

        flow = content.find(string=re.compile('Flow')).strip()
        data['flow'] = split_string(flow)

        lighting = content.find(string=re.compile('Lighting')).strip()
        data['lighting'] = split_string(lighting)
        return data
