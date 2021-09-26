import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import sys



url = "https://www.dia.es/compra-online/despensa/cf"

def get_data(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    return soup

def parse(soup):
    productlist = []
    results = soup.find_all("div",{ "class": "product-list__item"})
    for item in results:
        products = {
            "title": item.find("span", {"class": "details" }).text,
            "soldprice": (item.find("p", {"class": "price"}).text.replace("$","").strip().split()[0]),
            #"shipping": item.find("span", { "class": "s-item__shipping s-item__logisticsCost"}).text.replace("shipping",""),
        }

        productlist.append(products)
    return productlist

def output(productlist) :
    productsdf = pd.DataFrame(productlist)
    productsdf.to_csv("prices.csv", mode='a', header=False)

    return

n = 0
p = 0
try:
    while n == 0:
        soup = get_data(url)
        productlist = parse(soup)
        output(productlist)
        url = soup.find(rel="next").get("href")
        p += 1
        print("Page number: ",p )

except:
    print("importing CSV data to Excel Data...")
    time.sleep(3)

    read_file = pd.read_csv(r"D:\PYTHON\PROGRAMAS PYCHARM\prices.csv")
    read_file.to_excel(r"D:\PYTHON\PROGRAMAS PYCHARM\prices.xlsx", index=None, header=["1","title","Soldprice"] )
    print("Acomplished")
