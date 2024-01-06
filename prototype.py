from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver
import unicodedata
import random
import json
import time
import re

def getProxy() :
    with open("proxies.txt") as f :
        proxies = f.readlines()
        proxy = proxies[random.randint(0,len(proxies))]
    px = ""
    for x in proxy :
        if x.isalpha() == False :
            px += x
        else : break
    proxy = px[:-1]
    return proxy

def linkedin(country, location, job) :
    proxy = getProxy()
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument(f"--proxy-server={proxy}")
    chrome = webdriver.Chrome(options=options)
    chrome.get(f'https://www.google.com/search?q={location} AND {job} -inurl: dir/ email "@gmail.com" site:{country}.linkedin.com/in/ OR site:{country}.linkedin.com/pub/')
    time.sleep(10)
    
    # SCROLL DOWN
    for i in range(5):
        chrome.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        i+=1
        time.sleep(3)

    links = chrome.find_elements(By.TAG_NAME, "h3")
    for i in range(len(links)-1) :
        link = chrome.find_elements(By.TAG_NAME, "h3")[i]
        ActionChains(chrome) \
            .key_down(Keys.CONTROL) \
            .click(link) \
            .key_up(Keys.CONTROL) \
            .perform()
        chrome.switch_to.window(chrome.window_handles[1])
        time.sleep(5)
        print("success")
    


jobs = ["affiliate","management" ,"web developer", "ceo", "seo", "finance", "accountant","banker","insurance"]
countries = ["UK","IT","ES","CA","SE","DE","FR","BZ"]

while True :
    job = random.choice(jobs)
    country = random.choice(countries)
    for job in jobs :
        for country in countries :
            cities = []
            with open("geo.json", 'r',encoding="utf-8") as f :
                data = json.loads(f.read())
                for c in data :
                    if country in c["code"] :
                        cities.append(c["name"])
            for city in cities :
                linkedin(country, city, job)
                random.shuffle(jobs)
                time.sleep(random.randint(30,40))