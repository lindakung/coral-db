from helpers import simple_get, split_string
from bs4 import BeautifulSoup
from pipeline import CoralPipeline
import re
import time

def load_them_all():
    urls = get_urls()
    last_ran = next(i + 2 for i, url in enumerate(urls) if url == 'coral/6')

    for i, value in enumerate(urls):
        if i <= last_ran:
            continue
        if i == last_ran:
            continue
        print(i, last_ran)
        full_url = 'https://reefs.com/{}'.format(value)
        print(full_url)
        coral_data = get_data(full_url)
        pipeline = CoralPipeline()

        pipeline.process_item(coral_data)

        time.sleep(1)

def get_urls():
    url = 'https://reefs.com/coral/'
    response = simple_get(url)

    if response is not None:
        html = BeautifulSoup(response, 'html.parser')
        script = [s.extract() for s in html('script')][30]
        list = re.findall(r'coral/[\w\.-]+', script.text)
        return list

    raise Exception('Error retrieving data from {}'.format(url))

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

        color = content.find(string=re.compile('Color:')).strip()
        all_colors = split_string(color)
        if 'and' in all_colors:
            all_colors = all_colors.replace('and ', '')

        data['color'] = all_colors.split(', ')

        feeding = content.find(string=re.compile('Feeding:')).strip()
        data['feeding'] = split_string(feeding)

        flow = content.find(string=re.compile('Flow:')).strip()
        data['flow'] = split_string(flow)

        lighting = content.find(string=re.compile('Lighting:')).strip()
        data['lighting'] = split_string(lighting)
        
        data['url'] = url
        return data

    raise Exception('Error getting data from {}'.format(url))


if __name__ == '__main__':
    load_them_all()
