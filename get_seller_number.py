import re
import urllib.request

def get_response_phone(id_product, cookie, token):
    url = 'https://www.olx.ua/ajax/misc/contact/phone/' + id_product +'/?pt=' + token
    r = urllib.request.Request(url, headers={'Cookie': cookie})
    phone = urllib.request.urlopen(r)
    return str(phone.read().decode("utf-8"))

def parse_token(html):
    token = re.search(r"(?<=phoneToken\ =\ ')[\w\W]*?(?=';)", html)
    return str(token.group(0))

def parse_id_product(html):
    id_product = re.search(r'(?<=ID)[\w\W]*?(?=\.html)', html)
    return str(id_product.group(0))

def scrab_number(html):
    pass

# get cookie
def get_cookie(response):
    return response.getheader('Set-Cookie')