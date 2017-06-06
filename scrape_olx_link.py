
import re
import urllib.request

url = 'https://www.olx.ua/if/q-macbook/' #main page

# get html
def get_response(url):
    response = urllib.request.urlopen(url)
    return (str(response.read().decode("utf-8")))

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
        file.write(link + '\n')
    file.close()

# get the last page
def get_max_page(html):
    max_page = re.search(r'(?<="page_count":").*?(?=")', html)
    return str(max_page.group(0))


def main():
    count_page = 1 # start page
    url_page = url + '?page=' + str(count_page)
    max_page = int(get_max_page(get_response(url)))

    #print (max_page)

    while max_page >= count_page:
        url_page = url + '?page=' + str(count_page)
        print('PAGE - [' + str(count_page) + ']')
        html = get_response(url_page)
        list_product = scrab_product(html)
        write_to_file('product.txt', list_product)
        count_page += 1

    print('OK!')


if __name__ == '__main__':
    main()

