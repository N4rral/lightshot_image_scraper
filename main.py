import random
import cloudscraper
import os
import requests
import time
from urllib import request
import configparser

full_repeat = True
amount = 0
try:
    os.mkdir("images")
except FileExistsError:
    pass
# Create config file if it doesn't exist already and assign default settings
config = configparser.ConfigParser()
try:
    config.add_section("settings")
    with open("settings.ini", "w") as file:
        config.write(file)
        file.flush()
        os.fsync(file.fileno())
except configparser.DuplicateSectionError:
    pass
try:
    config.add_section("default")
    config.set("default", "cooldown_time", str(5))
    with open("settings.ini", "w") as file:
        config.write(file)
        file.flush()
        os.fsync(file.fileno())
except configparser.DuplicateSectionError:
    pass
file.close()
while full_repeat:
    # Get config data and assign them to variables
    config.read(open("settings.ini", "r"))
    keys = ["cooldown_time"]
    settings_dictionary = {}
    for key in keys:
        try:
            settings_dictionary[key] = config.get("settings", key)
        except configparser.NoOptionError:
            settings_dictionary[key] = config.get("default", key)
    cooldown_time = int(settings_dictionary["cooldown_time"])
    # User inputs
    repeat = True
    while repeat:
        # Main menu
        option = input("1 Download new images\n2 Edit settings\n3 Remove old images\n4 End program\nchoice: ")
        print("")
        # Download new images
        if option == "1":
            amount_repeat = True
            while amount_repeat:
                try:
                    amount = int(input("Input the amount of images you want to download: "))
                    if 0 < amount < 9999:
                        amount_repeat = False
                        repeat = False
                        amount_default = amount
                    else:
                        print("Input value in range 0-9999")
                        amount_repeat = True
                except:
                    print("Invalid input")
                    amount_repeat = True
        # Edit settings
        elif option == "2":
            settings_repeat = True
            while settings_repeat:
                option = input("1 Change cooldown time\n2 Back to main menu\nchoice: ")
                print("")
                if option == "1":
                    print("change cooldown time (Should be 5-10, but you can disable it by typing 0.)")
                    try:
                        print("cooldown_time = " + str(config.get("settings", "cooldown_time")))
                    except configparser.NoOptionError:
                        print("cooldown_time = " + str(config.get("default", "cooldown_time")))
                    try:
                        cooldown_time = int(input("Enter value: "))
                        if cooldown_time >= 0:
                            config.set("settings", "cooldown_time", str(cooldown_time))
                            config.write(open("settings.ini", "w"))
                            print("")
                            print("Value saved successfully.")
                        else:
                            print("")
                            print("Invalid input. cooldown time has been set to default value.")
                            cooldown_time = 5
                        settings_repeat = False
                    except:
                        print("")
                        print("Invalid input. cooldown time has been set to default value.")
                        cooldown_time = 5
                    print("")
                elif option == "2":
                    settings_repeat = False
                else:
                    print("Invalid value\n")
                    settings_repeat = True
        # Remove old images
        elif option == "3":
            print("work in progress\n")
        # Terminate program
        elif option == "4":
            exit()
        else:
            print("\nInvalid value\n")
            repeat = True

    url_template = "https://prnt.sc/"
    i = 0
    partial_repeat = True
    # Generate basic urls that will later be used to get images from
    while partial_repeat:
        while i < amount:
            st = time.time()
            i += 1
            scraper = cloudscraper.create_scraper()
            url_scrape = scraper.get(url_template + str(random.randint(0, 999999))).text
            img_url = ""
            index = 0
        # Get image url from url_scrape html code
            for j in url_scrape:
                index += 1
                if index > url_scrape.find('<img class="no-click screenshot-image" src="') + 44 and j != '"':
                    img_url += j
                elif index <= url_scrape.find('<img class="no-click screenshot-image" src="') + 44:
                    pass
                else:
                    break
            index = 0
        # Check whether the url is blacklisted or not
            if "//st.prntscr.com" in img_url or "imageshack" in img_url\
                    or "//image.prntscr.com" in img_url:
                i -= 1
            else:
                # Check if the url is i.imgur.com and get a redirection url in case the image has been removed
                if "https://i.imgur.com" in img_url:
                    response = request.urlopen(img_url)
                    new_url = response.geturl()
                else:
                    new_url = ""
                # Check if the image has been removed and issue a replacement url if it has been removed
                if new_url == "https://i.imgur.com/removed.png":
                    i -= 1
                else:
                    # So the printed urls are in a column
                    if i < 10:
                        print(str(i) + ":   " + img_url)
                    elif 10 <= i < 100:
                        print(str(i) + ":  " + img_url)
                    elif 100 <= i < 1000:
                        print(str(i) + ": " + img_url)
                    else:
                        print(str(i) + ":" + img_url)
                    # Saving image from the url
                    img_data = requests.get(img_url).content
                    with open(os.path.join("images", str(i) + ".jpg"), "wb") as handler:
                        handler.write(img_data)
                    et = time.time()
                    # Get process runtime and set time.sleep() for the process to be 5 s or longer if necessary
                    ft = et - st
                    if i < amount:
                        if ft >= cooldown_time or cooldown_time == 0:
                            time.sleep(0)
                        else:
                            time.sleep(cooldown_time - ft)
                    else:
                        print("Process finished\n")
                        end_repeat = True
                        while end_repeat:
                            end_choice = input("1 Generate another " + str(amount_default) + " images"
                                               "\n2 Restart the program\n3 End the program\nchoice: ")
                            if end_choice == "1":
                                partial_repeat = True
                                end_repeat = False
                                amount += amount_default
                            elif end_choice == "2":
                                partial_repeat = False
                                full_repeat = True
                                end_repeat = False
                                print("")
                            elif end_choice == "3":
                                partial_repeat = False
                                full_repeat = False
                                end_repeat = False
                            else:
                                print("\nInvalid value\n")
                                end_repeat = True
