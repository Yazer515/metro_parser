import datetime
import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import pandas as pd 

def parse(k, v, writer):
    time = datetime.datetime.now().strftime('%d_%m_%Y_%H_%M')
    agent = UserAgent()
    
    headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'User-Agent' : agent.random
    }
    
    cookies = {
        'metroStoreId' : f'{k}'
    }
    
    output = []
              
    response = requests.get(url='https://online.metro-cc.ru/category/alkogolnaya-produkciya/krepkiy-alkogol/viski', headers=headers, cookies=cookies)
    bs = BeautifulSoup(response.text, 'lxml')

    adress = bs.find(class_ = 'header-address__receive-address').text.strip()
    
    products = bs.find_all(class_ = 'catalog-2-level-product-card')
    
    brand_list = []
    
    brands_string = bs.find(class_ = 'catalog-checkbox-group')
    
    pages_count = int(bs.find_all(class_ = 'v-pagination__item catalog-paginate__item')[-1].text)

    brands = brands_string.text.strip().split('\n')
    for brand in brands:
        brand = brand.strip()
        if brand != '':
            brand_list.append(brand)

    for page in range(pages_count):
        new_url = 'https://online.metro-cc.ru/category/alkogolnaya-produkciya/krepkiy-alkogol/viski?page=' + str(int(page) + 1)
        response = requests.get(url=new_url, headers=headers, cookies=cookies)
        bs = BeautifulSoup(response.text, 'lxml')
        products = bs.find_all(class_ = 'catalog-2-level-product-card')
        
        for element in products:
            sold_status = element.find(class_ = 'product-title catalog-2-level-product-card__title style--catalog-2-level-product-card')
            if sold_status == None:
                id = element.attrs['data-sku']
                link = 'https://online.metro-cc.ru' + element.find(class_ = 'product-card-photo__link').get('href')
                title = element.find(class_ = 'product-card-name__text').text.strip()
                product_brand = None
                
                discount = strip_and_make_digits(element.find(class_ = 'product-discount nowrap catalog-2-level-product-card__icon-discount style--catalog-2-level-product-card'))
                   
                if discount != None:
                    price = strip_and_make_digits(element.find(class_ = 'product-unit-prices__old-wrapper'))
                    promo_price = strip_and_make_digits(element.find(class_ = 'product-price nowrap product-unit-prices__actual style--catalog-2-level-product-card-major-actual color--red'))
                else:
                    price = strip_and_make_digits(element.find(class_ = 'product-price__sum'))
                    promo_price = price

                pb = list(filter(lambda x: x in title.upper(), brand_list))
                if pb == []:
                        pass
                else:
                    product_brand = pb[0]
                    
                if product_brand == None:
                    continue
                
                output.append({
                    'id' : id,
                    'title' : title,
                    'link' : link,
                    'promo_price' : promo_price,
                    'price' : price,
                    'product_brand' : product_brand,
                })
            else:
                continue
    df = pd.DataFrame.from_records(output, index = 'id')
    df.to_excel(writer, sheet_name = str(v))

def strip_and_make_digits(_input):
    if _input is not None:
        _input = _input.text
        _input = "".join(_input.split())
        _input = int(''.join(filter(str.isdigit, _input)))
        return _input
    else:
        return None
        
if __name__ == '__main__':
    cities = [(356,'Москва'), (16, 'Санкт_петербург')]
    writer = pd.ExcelWriter('output.xlsx', engine = 'xlsxwriter')
    for k,v in cities:
        parse(k,v, writer)
    writer.close()