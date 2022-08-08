import cloudscraper
scraper = cloudscraper.create_scraper()
file = open("url.txt","w",encoding="utf-8")
url = scraper.get("https://prnt.sc/123457").text
index = 0
switch = False
img_url = ""
for i in url:
    index += 1
    if index > url.find('<img class="no-click screenshot-image" src="') + 44 and i != '"':
        img_url += i
    elif index <= url.find('<img class="no-click screenshot-image" src="') + 44:
        pass
    else:
        break
print(img_url)
file.write(scraper.get("https://prnt.sc/123457").text)