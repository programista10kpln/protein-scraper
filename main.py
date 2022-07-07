import re

import requests
from bs4 import BeautifulSoup


def calc_profitability(name, price):
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
        price_for_100g = round((price_numeric / quantity_numeric) * 100, 2)
    else:
        price_for_100g = 0
    return {'quantity': quantity, 'price_for_100g': price_for_100g}


def get_proteins_from_kfd():
    url = "https://sklep.kfd.pl/bialko-c-50.html"

    querystring = {"q": "Waga-kg-0.7-16/Dostępność-Dostępne", "page": "1"}
    payload = ""
    headers = {}

    site = requests.request("GET", url, data=payload, headers=headers, params=querystring)

    if site.status_code == 200:
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
                profitability = calc_profitability(name, price)
                link = tile.find('a')['href']

                products.append({
                    'name': name,
                    'price': price,
                    'quantity': profitability['quantity'],
                    'zł/100g': profitability['price_for_100g'],
                    'link': link
                })

        return products

    else:
        return f'Error: {site.status_code}'


def get_proteins_from_sfd():
    url = "https://sklep.sfd.pl/aspx/produkty.aspx"

    querystring = {"katid": "119", "page": "1"}
    payload = ""
    headers = {}

    site = requests.request("GET", url, data=payload, headers=headers, params=querystring)

    if site.status_code == 200:
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
                profitability = calc_profitability(name, price)
                link = f'https:{tile.find("a")["href"]}'

                products.append({
                    'name': name,
                    'price': price,
                    'quantity': profitability['quantity'],
                    'zł/100g': profitability['price_for_100g'],
                    'link': link
                })

        return products

    else:
        return f'Error: {site.status_code}'


def get_proteins_from_my_protein():
    url = "https://www.myprotein.pl/nutrition/protein.list"

    querystring = {"pageNumber": "1"}
    payload = ""
    headers = {}

    site = requests.request("GET", url, data=payload, headers=headers, params=querystring)

    if site.status_code == 200:
        soup = BeautifulSoup(site.content, 'html.parser')
        page_list_block = soup.find('ul', class_='responsivePageSelectors')
        page_list = page_list_block.findAll('li')
        numbers = [i.text.strip() for i in page_list if i.text.strip()]

        products = []

        for number in numbers:
            querystring = {"pageNumber": number}
            payload = ""
            headers = {}

            current_site = requests.request("GET", url, data=payload, headers=headers, params=querystring)
            current_soup = BeautifulSoup(current_site.content, 'html.parser')
            product_tiles = current_soup.findAll('li', class_='productListProducts_product')
            for tile in product_tiles:
                name = tile.find('div', class_='athenaProductBlock_title').text.strip()
                price = \
                    tile.find('div', class_='athenaProductBlock_priceBlock').text.strip().replace('\n', ' ').split('ł')[
                        0] + 'ł'
                profitability = calc_profitability(name, price)
                link = f'https://www.myprotein.pl{tile.find("a")["href"]}'

                products.append({
                    'name': name,
                    'price': price,
                    'quantity': profitability['quantity'],
                    'zł/100g': profitability['price_for_100g'],
                    'link': link
                })

        return products

    else:
        return f'Error: {site.status_code}'


def get_proteins_from_body_house():
    url = "https://bodyhouse.pl/settings.php"

    querystring = {
        "sort_order": "price-a",
        "portions": "1000"}
    payload = ""
    headers = {
        "Referer": "https://bodyhouse.pl/pol_m_Suplementy_Odzywki-bialkowe-307.html"
    }
    site = requests.request("GET", url, data=payload, headers=headers, params=querystring)

    if site.status_code == 200:
        soup = BeautifulSoup(site.content, 'html.parser')

        products = []

        product_tiles = soup.findAll('div', class_='product_wrapper')
        for tile in product_tiles:
            name = tile.find('a', class_='product-name').text.strip()
            price = tile.find('span', class_='price').text.strip().replace(',', '.')
            profitability = calc_profitability(name, price)
            link = f"https://bodyhouse.pl/{tile.find('a', class_='product-name')['href']}"

            products.append({
                'name': name,
                'price': price,
                'quantity': profitability['quantity'],
                'zł/100g': profitability['price_for_100g'],
                'link': link
            })

        return products

    else:
        return f'Error: {site.status_code}'


def cheap_proteins():
    proteins_from_kfd = get_proteins_from_kfd()
    proteins_from_sfd = get_proteins_from_sfd()
    proteins_from_my_protein = get_proteins_from_my_protein()
    proteins_from_body_house = get_proteins_from_body_house()
    all_proteins = proteins_from_kfd + proteins_from_sfd + proteins_from_my_protein + proteins_from_body_house
    sorted_proteins = sorted(all_proteins, key=lambda i: i['zł/100g'])
    return sorted_proteins


# print(get_proteins_from_kfd())
# print(get_proteins_from_sfd())
# print(get_proteins_from_my_protein())
# print(get_proteins_from_body_house())
print(cheap_proteins())
