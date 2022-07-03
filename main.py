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

    products = {}

    for number in range(1, int(numbers[-1]) + 1):
        current_url = url + f'&page={number}'
        current_site = requests.get(current_url)
        current_soup = BeautifulSoup(current_site.content, 'html.parser')
        descriptions = current_soup.findAll('div', class_='product-description')
        for description in descriptions:
            # name = description.find('h2', class_='h3 product-title')
            name = description.find('a')
            price = description.find('span', class_='price')
            products[name.text.strip()] = price.text.strip()

    # for i in products:
    #     yield i.text

    return products

    # numbers = []
    # for i in page_list:
    #     number = i.find('a', attrs={'rel': 'nofollow'})
    #     if number:
    #         numbers.append(number.text.strip())
    # return numbers


print(get_protein_from_kfd())

# for i in get_protein_from_kfd():
#     print(i)
