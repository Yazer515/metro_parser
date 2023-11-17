import datetime
import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import pandas as pd 

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

def strip_and_make_digits(_input):
    if _input is not None:
        _input = _input.text
        _input = "".join(_input.split())
        _input = int(''.join(filter(str.isdigit, _input)))
        return _input
    else:
        return None
        
    #print(len(pet_food))

if __name__ == '__main__':
    #collect(16)
    
    output = []
        
    time = datetime.datetime.now().strftime('%d_%m_%Y_%H_%M')
    agent = UserAgent()

    headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'User-Agent' : agent.random
    }

    cookies = {
        'metroStoreId' : f'{16}'
    }

        # with open('index2.html', 'r') as file:
        #     scr = file.read()
       
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

    #print(pages_count)

    for page in range(pages_count):
        new_url = 'https://online.metro-cc.ru/category/alkogolnaya-produkciya/krepkiy-alkogol/viski?page=' + str(int(page) + 1)
        print(new_url)
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
                
                output.append({
                    'id' : id,
                    'title' : title,
                    'link' : link,
                    'promo_price' : promo_price,
                    'price' : price,
                    'product_brand' : product_brand,
                })
                        


                # print(f'ID товара: {id}')
                # print(f'Наименование: {title}')
                # print(f'Ссылка на товар: {link}')
                # print(f'Промо цена: {promo_price}')
                # print(f'Цена: {price}')
                # print(f'Бренд: {product_brand}')
                # print()
            else:
                continue
        #break
df = pd.DataFrame.from_records(output, index = 'id')
print(df)

# Saving a Pandas DataFrame to an Excel File
# With a Sheet Name
df.to_excel('output.xlsx')

