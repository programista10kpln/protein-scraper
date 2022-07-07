import re

import requests
from bs4 import BeautifulSoup


def get_protein_from_kfd():
    url = "https://sklep.kfd.pl/bialko-c-50.html"

    querystring = {"q": "Waga-kg-0.7-16/Dostępność-Dostępne", "page": "1"}
    payload = ""
    headers = {}

    site = requests.request("GET", url, data=payload, headers=headers, params=querystring)
    soup = BeautifulSoup(site.content, 'html.parser')
    page_list_block = soup.find('ul', class_='page-list clearfix text-sm-center')
    page_list = page_list_block.findAll('li')
    numbers = [i.text.strip() for i in page_list if i.text.strip().isdigit()]

    products = []

    for number in numbers:
        querystring = {"q": "Waga-kg-0.7-16/Dostępność-Dostępne", "page": number}
        payload = ""
        headers = {}

        current_site = requests.request("GET", url, data=payload, headers=headers, params=querystring)
        current_soup = BeautifulSoup(current_site.content, 'html.parser')
        product_tiles = current_soup.findAll('div', class_='product-description')
        for tile in product_tiles:
            name = tile.find('a').text.strip()
            price = tile.find('span', class_='price').text.strip().replace('\xa0', ' ').replace(',', '.')
            try:
                quantity = re.findall(r'\d*,*\d+ *k* *g+', name, re.IGNORECASE)[0]
            except IndexError:
                quantity = None
            if quantity:
                price_numeric = float(re.findall(r'\d*,*\d+', price, re.IGNORECASE)[0])
                quantity_numeric = float(re.findall(r'\d*,*\d+', quantity, re.IGNORECASE)[0].replace(',', '.'))
                if 'k' in quantity.lower():
                    quantity_numeric = int(quantity_numeric * 1000)
                    quantity = f'{quantity_numeric} g'
                else:
                    quantity_numeric = int(quantity_numeric)
                price_for_100g = f'{round((price_numeric / quantity_numeric) * 100, 2)} zł/100g'
            else:
                price_for_100g = None
            link = tile.find('a')['href']

            products.append({
                'name': name,
                'price': price,
                'quantity': quantity,
                'price for 100g': price_for_100g,
                'link': link
            })

    return products


def get_protein_from_sfd():
    url = "https://sklep.sfd.pl/aspx/produkty.aspx"

    querystring = {"katid": "119", "page": "1"}
    payload = ""
    headers = {}

    site = requests.request("GET", url, data=payload, headers=headers, params=querystring)

    soup = BeautifulSoup(site.content, 'html.parser')
    page_list_block = soup.find('span', class_='pagination')
    page_list = page_list_block.findAll()
    numbers = [i.text.strip() for i in page_list if i.text.strip().isdigit()]

    products = []

    for number in numbers:
        querystring = {"katid": "119", "page": number}
        payload = ""
        headers = {}

        current_site = requests.request("GET", url, data=payload, headers=headers, params=querystring)
        current_soup = BeautifulSoup(current_site.content, 'html.parser')
        product_tiles = current_soup.findAll('div', class_='product-tile__info-box')
        for tile in product_tiles:
            name = ' '.join(tile.find('h3').text.split())
            price = tile.find('span', class_='cena').text.strip().replace(',', '.')
            try:
                quantity = re.findall(r'\d*,*\d+ *k* *g+', name, re.IGNORECASE)[0]
            except IndexError:
                quantity = None
            if quantity:
                price_numeric = float(re.findall(r'\d*,*\d+', price, re.IGNORECASE)[0])
                quantity_numeric = float(re.findall(r'\d*,*\d+', quantity, re.IGNORECASE)[0].replace(',', '.'))
                if 'k' in quantity.lower():
                    quantity_numeric = int(quantity_numeric * 1000)
                    quantity = f'{quantity_numeric} g'
                else:
                    quantity_numeric = int(quantity_numeric)
                price_for_100g = f'{round((price_numeric / quantity_numeric) * 100, 2)} zł/100g'
            else:
                price_for_100g = None
            link = f'https:{tile.find("a")["href"]}'

            products.append({
                'name': name,
                'price': price,
                'quantity': quantity,
                'price for 100g': price_for_100g,
                'link': link
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


def get_protein_from_body_house():
    url = "https://bodyhouse.pl/settings.php"
    querystring = {"sort_order": "price-a", "portions": "1000"}
    headers = {
        "Referer": "https://bodyhouse.pl/pol_m_Suplementy_Odzywki-bialkowe-307.html"
    }
    site = requests.get(url, headers=headers, params=querystring)
    soup = BeautifulSoup(site.content, 'html.parser')

    products = []

    product_tiles = soup.findAll('div', class_='product_wrapper')
    for tile in product_tiles:
        name = tile.find('a', class_='product-name')
        price = tile.find('span', class_='price')
        link = tile.find('a', class_='product-name')

        products.append({
            'name': name.text.strip(),
            'price': price.text.strip(),
            'link': f'https://bodyhouse.pl/{link["href"]}'
        })

    return products


# print(get_protein_from_kfd())
print(get_protein_from_sfd())
# print(get_protein_from_my_protein())
# print(get_protein_from_body_house())
