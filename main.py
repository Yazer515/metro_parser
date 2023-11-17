import datetime
import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup

time = datetime.datetime.now().strftime('%d_%m_%Y_%H_%M')
agent = UserAgent()

headers = {
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
'User-Agent' : agent.random
}

cookies = {
    'metroStoreId' : f'{16}'
}

response = requests.get(url='https://online.metro-cc.ru/category/alkogolnaya-produkciya/krepkiy-alkogol/viski', headers=headers, cookies=cookies)


def collect(store_code):
    time = datetime.datetime.now().strftime('%d_%m_%Y_%H_%M')
    agent = UserAgent()
    
    headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'User-Agent' : agent.random
    }
    
    cookies = {
        'metroStoreId' : f'{store_code}'
    }
    
    response = requests.get(url='https://online.metro-cc.ru/category/alkogolnaya-produkciya/krepkiy-alkogol/viski', headers=headers, cookies=cookies)
    
    
    with open('index2.html', 'w') as file:
        file.write(response.text)

def strip_and_make_digits(_input_str):
    _input_str = "".join(_input_str.split())
    _input_str = int(''.join(filter(str.isdigit, _input_str)))
    return _input_str
        
    #print(len(pet_food))

if __name__ == '__main__':
    #collect(16)


    with open('index2.html', 'r') as file:
        scr = file.read()
       
    response = requests.get(url='https://online.metro-cc.ru/category/alkogolnaya-produkciya/krepkiy-alkogol/viski', headers=headers, cookies=cookies)
    bs = BeautifulSoup(response.text, 'lxml')

    adress = bs.find(class_ = 'header-address__receive-address').text.strip()
    
    products = bs.find_all(class_ = 'catalog-2-level-product-card')
    
    brand_list = []
    
    brands_string = bs.find(class_ = 'catalog-checkbox-group')
    
    pages_count = bs.find_all(class_ = 'v-pagination__item catalog-paginate__item')[-1].text
    print(pages_count)

    brands = brands_string.text.strip().split('\n')
    for brand in brands:
        brand = brand.strip()
        if brand != '':
            brand_list.append(brand)
    #print(brand_list)

    for page in pages_count:
        response = requests.get(url='https://online.metro-cc.ru/category/alkogolnaya-produkciya/krepkiy-alkogol/viski?page=' + str(page + 1), headers=headers, cookies=cookies)
        bs = BeautifulSoup(response.text, 'lxml')
        
        for element in products:
            id = element.attrs['data-sku']
            link = 'https://online.metro-cc.ru' + element.find(class_ = 'product-card-photo__link').get('href')
            title = element.find(class_ = 'product-card-name__text').text.strip()
            product_brand = None
            
            try:
                discount = strip_and_make_digits(element.find(class_ = 'product-discount nowrap catalog-2-level-product-card__icon-discount style--catalog-2-level-product-card').text.strip())
            except:
                ArithmeticError
                discount = 0
                
            if discount != 0:
                price = strip_and_make_digits(element.find(class_ = 'product-unit-prices__old-wrapper').text.strip())
                try:
                    promo_price = strip_and_make_digits(element.find(class_ = 'product-price nowrap product-unit-prices__actual style--catalog-2-level-product-card-major-actual color--red').text.strip())
                except:
                    AttributeError
                    promo_price = price
            else:
                price = strip_and_make_digits(element.find(class_ = 'product-price__sum').text.strip())
                try:
                    promo_price = strip_and_make_digits(element.find(class_ = 'product-price nowrap product-unit-prices__actual style--catalog-2-level-product-card-major-actual color--red').text.strip())
                except:
                    AttributeError
                    promo_price = price
                
            for brand in brand_list:
                if brand in title.upper():
                    product_brand = brand
                    


            print(f'ID товара: {id}')
            print(f'Наименование: {title}')
            print(f'Ссылка на товар: {link}')
            print(f'Промо цена: {promo_price}')
            print(f'Цена: {price}')
            print(f'Бренд: {product_brand}')
            print()