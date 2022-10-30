import requests
from bs4 import BeautifulSoup
import re
import csv

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.124 YaBrowser/22.9.3.886 Yowser/2.5 Safari/537.36'}


def f_price(soup):
    product_price = soup.find('span', class_='ProductCardMainPrices_OnePrice')
    if product_price == None:
        return 'No price'
    else:
        regex = re.compile("(\d+)")
        product_price = regex.findall(product_price.text)[0]
        return product_price


def f_name(soup):
    product_name = soup.find('h1').text.replace('в Москве', '')
    return (product_name.replace('Шины', '')).strip()


def properties(soup):
    product_properties = soup.findAll('span', class_='ProductCardProperties_PropertyTextBackground')
    regex = re.compile('(\w+)')
    season = regex.findall(product_properties[7].text)[0]
    thorns = regex.findall(product_properties[9].text)[0]
    return int(product_properties[1].text), int(product_properties[3].text), int(
        product_properties[5].text), season, thorns


def product(soup):
    name = f_name(soup)
    price = f_price(soup)
    if price == 'No price':
        return name, price
    else:
        width, height, diameter, season, thorns = properties(soup)
        return name, price, width, height, diameter, season, thorns


def f_photo(soup):
    product_photo = soup.find_all('a', class_='popup_link fancy')
    photos = []
    for i in range(0, len(product_photo)):
        photos.append('https://koleso.ru' + product_photo[i]['href'])
    return photos


def csv_writing(name, price, width, height, diameter, season, thorns):
    fieldnames = ['Название товара', 'Цена товара', 'Ширина', 'Высота', 'Диаметр', 'Сезонность', 'Наличие шипов']
    with open('data.csv', 'w', encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writerow(
            {'Название товара': name, 'Цена товара': price, 'Ширина': width, 'Высота': height, 'Диаметр': diameter,
             'Сезонность': season, 'Наличие шипов': thorns})


page = 12
while page != 4464:
    data = requests.get('https://koleso.ru/catalog/tyres/zima/?per_page=' + str(page), headers=headers)
    soup_products = BeautifulSoup(data.text, 'html.parser')
    allproducts = soup_products.findAll('a', class_="dark_link js-ECommerce_ProductClick")
    for i in range(0, len(allproducts)):
        r_pr = requests.get(('https://koleso.ru' + allproducts[i]['href']), headers=headers)
        product_soup = BeautifulSoup(r_pr.text, 'html.parser')
        print(product(product_soup))
    page += 12
    print('Открываю следующую страницу.')
