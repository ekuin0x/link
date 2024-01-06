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


options = Options()
options.add_argument("--headless=new")

chrome = webdriver.Chrome(options=options)
chrome.get('https://www.google.com/search?q=Hamburg AND web development -inurl: dir/ email "@gmail.com" site:de.linkedin.com/in/ OR site:de.linkedin.com/pub/')
time.sleep(10)

""" ////////////////////////////////////////////////////////////////////////////"""
exist = chrome.find_elements(By.CSS_SELECTOR, "a[aria-label='Plus de résultats']")
more = 0 ;i = 0
if len(exist) > 0  : more = 1
while more == 1 :
    chrome.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    i+=1
    time.sleep(2)
    exist = chrome.find_elements(By.CSS_SELECTOR, "a[aria-label='Plus de résultats']")
    if len(exist)==0 or i==5 : more = 0
""" ////////////////////////////////////////////////////////////////////////////"""

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

    # -------------- SCRAPE PAGE DATA ---------------------

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

    # -----------------END OF SCRAPING ---------------------
    chrome.close()
    chrome.switch_to.window(chrome.window_handles[0])
    time.sleep(random.randint(40,60))
