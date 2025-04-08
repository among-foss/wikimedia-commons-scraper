import requests
from bs4 import BeautifulSoup

user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.3'
headers = {'User-Agent': user_agent}
search_term = input('Enter a search term: ')
items_number = input('Enter the number of images you want to download: ')

def scrape_images(input_url):
    
    x = 0
    response = requests.get(input_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    images = soup.find_all(class_= 'sdms-image-result' or 'sdms-image-result sdms-image-result--portrait')
    
    for image in images[:int(items_number)]:
        href = image.get('href')
        urls = []
        urls.append(href)

        for url in urls:

            if url.startswith('https'):

                response = requests.get(url, headers=headers)
                soup = BeautifulSoup(response.text, 'html.parser')
                images = soup.find_all('img')

                for image in images:

                    if image.get('alt') and image.get('alt').startswith('File:'):
                        
                        src = image.get('src')
                        upload_urls = []
                        upload_urls.append(src)
                        
                        for url in upload_urls:
                            response = requests.get(url, headers=headers)

                            if response.status_code == 200:

                                x += 1

                                with open(str(x) + '.jpg', 'wb') as file:
                                    file.write(response.content)

scrape_images(f'https://commons.wikimedia.org/w/index.php?search={search_term}&title=Special%3AMediaSearch')
