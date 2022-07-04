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

    products = []

    for number in range(1, int(numbers[-1]) + 1):
        current_url = url + f'&page={number}'
        current_site = requests.get(current_url)
        current_soup = BeautifulSoup(current_site.content, 'html.parser')
        product_tiles = current_soup.findAll('div', class_='product-description')
        for tile in product_tiles:
            name = tile.find('a')
            price = tile.find('span', class_='price')
            link = tile.find('a')

            products.append({
                'name': name.text.strip(),
                'price': price.text.strip().replace('\xa0', ' '),
                'link': link['href']
            })

    return products


def get_protein_from_sfd():
    url = 'https://sklep.sfd.pl/aspx/produkty.aspx?katid=119'
    site = requests.get(url)
    soup = BeautifulSoup(site.content, 'html.parser')
    page_list_block = soup.find('span', class_='pagination')
    page_list = page_list_block.findAll()
    numbers = [i.text.strip() for i in page_list if i.text.isdigit()]

    products = []

    for number in range(1, int(numbers[-1]) + 1):
        current_url = url + f'&page={number}'
        current_site = requests.get(current_url)
        current_soup = BeautifulSoup(current_site.content, 'html.parser')
        product_tiles = current_soup.findAll('div', class_='product-tile__info-box')
        for tile in product_tiles:
            name = tile.find('h3')
            name_formatted = ' '.join(name.text.split())
            price = tile.find('span', class_='cena')
            link = tile.find('a')

            products.append({
                'name': name_formatted,
                'price': price.text.strip(),
                'link': f'https:{link["href"]}'
            })

    return products


def get_protein_from_my_protein():
    url = 'https://www.myprotein.pl/nutrition/protein.list'
    site = requests.get(url)
    soup = BeautifulSoup(site.content, 'html.parser')
    page_list_block = soup.find('ul', class_='responsivePageSelectors')
    page_list = page_list_block.findAll('li')
    numbers = [i.text.strip() for i in page_list if i.text.strip()]

    products = []

    for number in range(1, int(numbers[-1]) + 1):
        current_url = url + f'?pageNumber={number}'
        current_site = requests.get(current_url)
        current_soup = BeautifulSoup(current_site.content, 'html.parser')
        product_tiles = current_soup.findAll('li', class_='productListProducts_product')
        for tile in product_tiles:
            name = tile.find('div', class_='athenaProductBlock_title')
            price = tile.find('div', class_='athenaProductBlock_priceBlock')
            link = tile.find('a')

            products.append({
                'name': name.text.strip(),
                'price': price.text.strip().replace('\n', ' ').split('ł')[0] + 'ł',
                'link': f'https://www.myprotein.pl{link["href"]}'
            })

    return products


def get_protein_from_body_house():  # doesnt work
    url = 'https://bodyhouse.pl/pol_m_Suplementy_Odzywki-bialkowe-307.html#1000'
    site = requests.get(url)
    soup = BeautifulSoup(site.content, 'html.parser')

    products = []

    product_tiles = soup.findAll('div', class_='product_wrapper')
    # for tile in product_tiles:
    #     name = tile.find('div', class_='athenaProductBlock_title')
    #     price = tile.find('div', class_='athenaProductBlock_priceBlock')
    #     link = tile.find('a')
    #
    #     products.append({
    #         'name': name.text.strip(),
    #         'price': price.text.strip().replace('\n', ' ').split('ł')[0] + 'ł',
    #         'link': f'https://www.myprotein.pl{link["href"]}'
    #     })

    return soup

# print(get_protein_from_kfd())
# print(get_protein_from_sfd())
# print(get_protein_from_my_protein())
# print(get_protein_from_body_house())
