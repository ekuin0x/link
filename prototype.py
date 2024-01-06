from selenium.webdriver.common.action_chains import ActionChains
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
    options.add_argument("--headless")
    options.add_argument(f"--proxy-server={proxy}")
    chrome = webdriver.Chrome(options=options)
    chrome.get(f'https://www.google.com/search?q={location} AND {job} -inurl: dir/ email "@gmail.com" site:{country}.linkedin.com/in/ OR site:{country}.linkedin.com/pub/')
    time.sleep(5)
    # SCROLL DOWN
    for i in range(4):
        chrome.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        i+=1
        time.sleep(2)

    links = chrome.find_elements(By.TAG_NAME, "h3")
    for i in range(len(links)-1) :
        link = chrome.find_elements(By.TAG_NAME, "h3")[i]
        ActionChains(chrome) \
            .key_down(Keys.CONTROL) \
            .click(link) \
            .key_up(Keys.CONTROL) \
            .perform()
        chrome.switch_to.window(chrome.window_handles[1])
        link = chrome.current_url
        name = unicodedata.normalize('NFKD', chrome.find_element(By.TAG_NAME, "h1").text).encode('ascii', 'ignore').decode('utf-8')
        title = unicodedata.normalize('NFKD', chrome.find_elements(By.CSS_SELECTOR, "h2")[0].text).encode('ascii', 'ignore').decode('utf-8')
        location= ""
        l = chrome.find_element(By.CSS_SELECTOR, "h3:nth-of-type(1) div div span")
        location = unicodedata.normalize('NFKD', l.text).encode('ascii', 'ignore').decode('utf-8') 
        txt = chrome.find_elements(By.CSS_SELECTOR, "section")[0].text
        emails = re.search(r'[\w.+-]+@[\w-]+\.[\w.-]+', txt)
        phone = re.findall(r'[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]', txt)
        if len(phone) > 0 : ph = phone[0]  
        else : ph = ""
        
        if emails != None or ph != "" :
            new_data = {
                "fullName" : name,
                "job title" : title,
                "country" : "DE",
                "location" : location,
                "email" : emails[0],
                "phone" : ph,
                "keyword" : "MODIFY LATER",
                "source" : link
            }

            with open("data.json","r") as f :
                data = json.loads(f.read()) 
                data.append(new_data)
                with open("data.json", "w") as w :
                    json.dump(data,w)
            time.sleep(2)

    
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
                try :
                    linkedin(country, city, job)
                    random.shuffle(jobs)
                    time.sleep(2)
                except : 
                    pass   