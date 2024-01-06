def linkedin(keyword,country,location): 
    print(f"GETTING QUERIES FOR : {keyword} --- {country} --- {location} ")
    url = f'https://www.google.com/search?q={location} web development -inurl: dir/ email "@gmail.com" site:{country}.linkedin.com/in/ OR site:{country}.linkedin.com/pub/'
    options = Options()
    options.add_argument("--headless=new")
    chrome = webdriver.Chrome(options=options)
    chrome.get(url)
    time.sleep(5)

    exist = chrome.find_elements(By.CSS_SELECTOR, "a[aria-label='Plus de résultats']")
    more = 0 ;i = 0
    print("-------------------------//////////////////////////////////")
    if len(exist) > 0  : more = 1
    while more == 1 :
        chrome.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        i+=1
        time.sleep(2)
        exist = chrome.find_elements(By.CSS_SELECTOR, "a[aria-label='Plus de résultats']")
        if len(exist)==0 or i==5 : more = 0

    spans = chrome.find_elements(By.CSS_SELECTOR, "div[style='-webkit-line-clamp:2']") 
    queries = []
    for span in spans :
        global emails
        query = unicodedata.normalize('NFKD', span.text).encode('ascii', 'ignore').decode('utf-8')
        emails = re.search(r'[\w.+-]+@[\w-]+\.[\w.-]+', query)
        if emails != None :
            queries.append(query)

    with open("queries.json","r+") as f :
        data = json.loads(f.read())
        data.extend(queries)
        f.seek(0)
        json.dump(data,f)
    print("COLLECTED QUERIES FROM GOOGLE")
    for query in queries :
        scrape_linkedin_query(query, keyword, country)

def scrape_linkedin_query(query, keyword, country) : 
    print('SCRAPING QUERY')
    options = Options()
    options.add_argument("--headless=new")
    chrome = webdriver.Chrome(options=options)
    i = 0
    emails = re.search(r'[\w.+-]+@[\w-]+\.[\w.-]+', query)
    with open("data.json", 'r') as f :
        data = json.loads(f.read())
        for record in data :
            if record["email"] == emails[0]:
                i = 1
    if i == 0 :
        print("TRYING TO SCRAPE LINK")
        try :
            chrome.get(f"https://www.google.com?q={query}")
            time.sleep(2)
            chrome.find_element(By.TAG_NAME, "form").submit()
            time.sleep(3)
            hrefs = chrome.find_element(By.CSS_SELECTOR, "h3:first-of-type").click()
            time.sleep(7)
            link = chrome.current_url
            name = unicodedata.normalize('NFKD', chrome.find_element(By.TAG_NAME, "h1").text).encode('ascii', 'ignore').decode('utf-8')
            title = unicodedata.normalize('NFKD', chrome.find_elements(By.CSS_SELECTOR, "h2")[0].text).encode('ascii', 'ignore').decode('utf-8')
            location= ""
            l = chrome.find_element(By.CSS_SELECTOR, "h3:nth-of-type(1) div div span")
            location = unicodedata.normalize('NFKD', l.text).encode('ascii', 'ignore').decode('utf-8') 
            emails = re.search(r'[\w.+-]+@[\w-]+\.[\w.-]+', query)
            phone = re.findall(r'[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]', query)
            if len(phone) > 0 : ph = phone[0]  
            else : ph = ""
            new_data = {
                "fullName" : name,
                "job title" : title,
                "country" : country,
                "location" : location,
                "email" : emails[0],
                "phone" : ph,
                "keyword" : keyword,
                "source" : link
            }

            with open("data.json","r") as f :
                data = json.loads(f.read()) 
                data.append(new_data)
                with open("data.json", "w") as w :
                    json.dump(data,w)
            
            with open("queries.json", "r") as f :
                data = json.loads(f.read())
                data.remove(query)
                with open("queries.json", "w") as w :
                    json.dump(data,w)
            print("SCRAPED LINK SUCCESSFULLY")
        except NoSuchElementException:
            print("FAILED TO SCRAPE")
            pass
'''
//////////////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////////
'''
countries = ["UK","IT","ES","CA","SE","DE","FR","BZ"]
random.shuffle(countries)
jobs = ["affiliate","management" ,"web developer", "ceo", "seo", "finance", "accountant","banker","insurance"]
random.shuffle(jobs)
for job in jobs :
    for country in countries :
        cities = []
        with open("geo.json", 'r',encoding="utf-8") as f :
            data = json.loads(f.read())
            for c in data :
                if country in c["code"] :
                    cities.append(c["name"])
        cities.reverse()
        for city in cities :
            print(f"------ {country} + ||| {city} --------")
            linkedin(job,country,city)
            time.sleep(random.randint(30,40))
            random.shuffle(jobs)