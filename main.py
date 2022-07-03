import requests
from bs4 import BeautifulSoup


def get_protein_from_kfd():
    url = 'https://sklep.kfd.pl/bialko-c-50.html?q=Waga-kg-0.7-16/Dostępność-Dostępne'
    site = requests.get(url)
    soup = BeautifulSoup(site.content, 'html.parser')
    page_list_block = soup.find('ul', class_='page-list clearfix text-sm-center')
    page_list = page_list_block.findAll('li')
    numbers = [i.find('a', attrs={'rel': 'nofollow'}).text.strip() for i in page_list if
               i.find('a', attrs={'rel': 'nofollow'})]

    products_name_price = {}

    for number in range(1, int(numbers[-1]) + 1):
        current_url = url + f'&page={number}'
        current_site = requests.get(current_url)
        current_soup = BeautifulSoup(current_site.content, 'html.parser')
        product_tiles = current_soup.findAll('div', class_='product-description')
        for tile in product_tiles:
            name = tile.find('a')
            price = tile.find('span', class_='price')
            products_name_price[name.text.strip()] = price.text.strip()

    return products_name_price


def get_protein_from_sfd():
    url = 'https://sklep.sfd.pl/aspx/produkty.aspx?katid=119'
    site = requests.get(url)
    soup = BeautifulSoup(site.content, 'html.parser')
    page_list_block = soup.find('span', class_='pagination')
    numeric_strings = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    numbers = [i for i in list(page_list_block.text.strip()) if i in numeric_strings]

    products_name_price = {}

    for number in range(1, int(numbers[-1]) + 1):
        current_url = url + f'&page={number}'
        current_site = requests.get(current_url)
        current_soup = BeautifulSoup(current_site.content, 'html.parser')
        product_tiles = current_soup.findAll('div', class_='product-tile__info-box')
        for tile in product_tiles:
            name = tile.find('h3')
            price = tile.find('span', class_='cena')
            name_formatted = ' '.join(name.text.split())
            products_name_price[name_formatted] = price.text.strip()

    return products_name_price


print(get_protein_from_kfd())
print(get_protein_from_sfd())
