# -*- coding: utf-8 -*-
import get_seller_number
import re
import urllib.request
import logging
import time
logging.basicConfig(level = logging.DEBUG)


url = 'https://www.olx.ua/if/q-macbook/' #main page

# get html
def get_response(url):
    response = urllib.request.urlopen(url)
    return response

# get list of products on page
def scrab_product(html):
    products = re.findall(r'(?<=<h3\ class="x-large)[\w\W]*?<div\ class="rel\ observelinkinfo', html)
    return products

# get product link
def scrab_product_link(product):
    link = re.search(r'(?<=a\ href=")[\w\W]*?\.html', product)
    return str(link.group(0))

# write product links in .txt file
def write_to_file(path_file, list_products):
    file = open(path_file,"a")

    for pr in list_products:
        link = scrab_product_link(pr)
        response = get_response(link)
        logging.debug('Work with page - ' + "[" + link + "]")
        str_response = str(response.read().decode("utf-8"))
        token = get_seller_number.parse_token(str_response)
        id_post = get_seller_number.parse_id_product(str_response)
        cookie = get_seller_number.get_cookie(response)
       # print(token + " " + id_post + " " + cookie)
       # print("link - " + link)

        #time.sleep(2)
        try:
            phone_response = get_seller_number.get_response_phone(id_post, cookie, token)
            phone = get_seller_number.scrab_number(phone_response)
            logging.debug('Parse phone - ' + "[" + phone + "]")
            file.write(link + '|' + phone + '\n')
        except:
            logging.warning("Product don't have number phone - " + "[" + link + "]")


    file.close()

# get the last page
def get_max_page(html):
    max_page = re.search(r'(?<="page_count":").*?(?=")', html)
    return str(max_page.group(0))



def main():
    path_file = 'product.txt' # file for result
    count_page = 1 # start page

    response = get_response(url)
    max_page = int(get_max_page(str(response.read().decode("utf-8"))))

    #print (max_page)

    while max_page >= count_page:
        url_page = url + '?page=' + str(count_page)
        logging.info('PAGE - [' + str(count_page) + ']')
        html = get_response(url_page)
        list_product = scrab_product(str(html.read().decode("utf-8")))
        logging.debug('Scrape list of products on page')
        write_to_file(path_file, list_product)
        count_page += 1

    logging.info('OK!')


if __name__ == '__main__':
    main()

