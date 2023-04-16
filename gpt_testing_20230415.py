import csv
from cgitb import text
from bs4 import BeautifulSoup 
import json
import re
import requests
import pyperclip
import pdb
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


f = open("output_testing.csv",'w')
writer = csv.writer(f)




# figure out what category it is from the brand's product title?
searchTerm="Black Miray ruffled floral-print silk-georgette blouse"
category_match = set(category_dict).intersection(searchTerm.lower().split())
if category_match:
    brand_category = category_match.pop()
    print(brand_category)


def scrape_info(url):
    if 'poshmark' in url: 
        for i in range(0,3):
            try:
                search_results_to_items_poshmark(url,scrape_raw_html(url))
            except: 
                print("hit an exception")
                print(url)
                if i == 2: 
                    writer.writerow(['error',url])
                continue
            break
    else:
        writer.writerow(['error',url])
        return 'ionno'


def scrape_raw_html(url):
    proxy = {}
    # get html response   resp = requests.get(url[:url.find('?')], headers={
    resp = requests.get(url
        ,headers={
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "accept-language": "en-US,en;q=0.9",
        "cache-control": "max-age=0",
        "sec-ch-prefers-color-scheme": "dark",
        "sec-ch-ua": "\" Not A;Brand\";v=\"99\", \"Chromium\";v=\"100\", \"Google Chrome\";v=\"100\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"macOS\"",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "viewport-width": "1728",
        },allow_redirects=False)#,proxies=proxy)
    return resp.text






# working on the grid-view version (not product-view) 12/15/22
def search_results_to_items_poshmark(url,raw_html):
    soup = BeautifulSoup(raw_html, features="html.parser")

    # Find the <script> tag that contains all the data we want 
    script_data_pattern = re.compile(r'"gridData":', re.MULTILINE | re.DOTALL)
    script_with_data = soup.find('script', text=script_data_pattern)

    # Use some brittle text splitting to get just the JSON text
    text_before_poshmark = ",\"$_search\":"
    text_after_poshmark = "};(function()"
    
    raw_search_results = script_with_data.get_text().split(text_before_poshmark)[1].split(text_after_poshmark)[0]
    
    # Turn it into a JSON object
    json_search_results = json.loads(raw_search_results)["gridData"]["data"]
    
    writer.writerow(["brand","title","product_url","price","description","size","category","colors","Poshmark"])

    output = []

    for item in json_search_results:
        try:
            title = item["title"]
        except:
            title = "ERROR PAY ATTENTION HERE"

        try:
            price = item["price_amount"]["currency_symbol"] + item["price_amount"]["val"]
        except:
            price = "ERROR PAY ATTENTION HERE"

        try:
            description = item["description"]
        except:
            desription = "ERROR PAY ATTENTION HERE"

        try:
            image = item["cover_shot"]["url"]
        except:
            image = "ERROR PAY ATTENTION HERE"

        try:
            location = "Ships for $7.67"
        except:
            location = "ERROR PAY ATTENTION HERE"

        try:
            size = item["size"] # TODO: iterate through inventory sizes and create a string for it instead of just this one
        except:
            size = "ERROR PAY ATTENTION HERE"

        try:
            original_price = item["original_price"]
        except:
            original_price = "ERROR PAY ATTENTION HERE"

        try:
            _id = item["id"]
        except:
            _id = "ERROR PAY ATTENTION HERE"

        try:
            product_url = "https://poshmark.com/listing/" + item["id"]
        except:
            product_url = "ERROR PAY ATTENTION HERE"

        try:
            brand = item["brand"]
        except:
            brand = "ERROR PAY ATTENTION HERE"

        try:
            #below is more for future backend-y stuff
            status = item["status"]
        except:
            status = "ERROR PAY ATTENTION HERE"

        try:
            style_tags = item["style_tags"]
        except:
            style_tags = "ERROR PAY ATTENTION HERE"

        try:
            brand_id_poshmark = item["brand_id"]
        except:
            brand_id_poshmark = "ERROR PAY ATTENTION HERE"

        try:
            department = item["catalog"]["department_obj"]["display"]
        except:
            department = "ERROR PAY ATTENTION HERE"

        try:
            category = item["category"]
        except:
            category = "ERROR PAY ATTENTION HERE"

        try:
            colors = item["colors"]
        except:
            colors = "ERROR PAY ATTENTION HERE"





        wr = [brand,title,product_url,price,description,size,category,colors,'Poshmark', brand_category.lower()==category.lower(), brand_category.lower() in title.lower()]
        writer.writerow(wr)


        output.append({
            "name": title
            ,"price": price 
            ,"description": description
            ,"image": image
            ,"original_price": original_price 
            ,"size": size 
            ,"location": location
            ,"_id": _id
            ,"status": status 
            ,"style_tags": style_tags
            ,"url": product_url
            ,"brand": brand
            ,"brand_id_poshmark": brand_id_poshmark
            ,"department": department
            ,"category": category
            ,"colors": colors
            ,"source": "Poshmark"
        })

    print(output)

    return output




with open("testing.csv",'r') as file:
    csvreader = csv.reader(file)
    for row in csvreader:
        scrape_info(row[0])


