import random
import cloudscraper
import os
import requests
import time
from urllib import request

repeat = True
amount = 0
while repeat:
    try:
        amount = int(input("Input the amount of images you want to download: : "))
        if 0 < amount < 9999:
            repeat = False
        else:
            print("Input value in range 0-9999")
            repeat = True
    except:
        print("Input a numerical value in range 0-9999")
        repeat = True

url_template = "https://prnt.sc/"
i = 0
while i < amount:
    st = time.time()
    i += 1
    scraper = cloudscraper.create_scraper()
    url_scrape = scraper.get(url_template + str(random.randint(0, 999999))).text
    img_url = ""
    index = 0
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
    for j in img_url:
        index += 1
        if index <= 16:
            url_check += j
        else:
            pass
    if url_check == "//st.prntscr.com" or "imageshack" in img_url\
            or "//image.prntscr.com" in img_url:
        i -= 1
    else:
        if "https://i.imgur.com" in img_url:
            response = request.urlopen(img_url)
            new_url = response.geturl()
        else:
            new_url = ""
        if new_url == "https://i.imgur.com/removed.png":
            i -= 1
        else:
            if i < 10:
                print(str(i) + ":   " + img_url)
            elif 10 <= i < 100:
                print(str(i) + ":  " + img_url)
            elif 100 <= i < 1000:
                print(str(i) + ": " + img_url)
            else:
                print(str(i) + ":" + img_url)
            img_data = requests.get(img_url).content
            with open(os.path.join("images", str(i) + ".jpg"), "wb") as handler:
                handler.write(img_data)
            et = time.time()
            ft = et - st
            if i < amount:
                if ft >= 5:
                    time.sleep(0)
                else:
                    time.sleep(5 - ft)
            else:
                print("process finished")
