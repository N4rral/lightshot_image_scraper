import random
import cloudscraper

repeat = True
amount = 0
while repeat:
    try:
        amount = int(input("Enter a number: "))
        repeat = False
    except:
        print("invalid input")
        repeat = True

url_template = "https://prnt.sc/"
add = True
while add:
    for i in range(0, amount):
        scraper = cloudscraper.create_scraper()
        url_scrape = scraper.get(url_template + str(random.randint(0, 999999))).text
        index = 0
        img_url = ""
        for j in url_scrape:
            index += 1
            if index > url_scrape.find('<img class="no-click screenshot-image" src="') + 44 and j != '"':
                img_url += j
            elif index <= url_scrape.find('<img class="no-click screenshot-image" src="') + 44:
                pass
            else:
                break
        index = 0
        url_check = ""
        passes = 0
        for j in img_url:
            index += 1
            if index <= 16:
                url_check += j
            else:
                pass
        if url_check == "//st.prntscr.com" or "imageshack" in img_url:
            passes += 1
        else:
            print(img_url)
        if passes > 0:
            add = True
            amount = passes
        else:
            add = False
