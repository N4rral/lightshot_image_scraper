import random
import cloudscraper
import os
import requests
import time
from urllib import request
import json
from types import SimpleNamespace

full_repeat = True
amount = 0
default_cfg = {
    "cooldown_time": 5,
    "open_folder_end": "True"
}
cfg = {}
try:
    os.mkdir("images")
except FileExistsError:
    pass
# Create settings.json if it doesn't exist and assign default values provided by default_cfg
try:
    cfg_file = open("settings.json", "x")
    cfg_file.flush()
    os.fsync(cfg_file.fileno())
    cfg_file.close()
    cfg_file = open("settings.json", "w")
    json.dump(default_cfg, cfg_file)
    cfg_file.close()
except FileExistsError:
    pass
while full_repeat:
    # User inputs
    repeat = True
    while repeat:
        cfg_file = open("settings.json", "r")
        cfg = json.load(cfg_file)
        n = SimpleNamespace(**cfg)
        # Assign values to variables using namespace
        cooldown_time = n.cooldown_time
        open_folder_end = n.open_folder_end
        # Close the cfg_file
        cfg_file.close()
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
                except ValueError:
                    print("Invalid input")
                    amount_repeat = True
        # Edit settings
        elif option == "2":
            settings_repeat = True
            while settings_repeat:
                option = input("1 Change cooldown time\n2 Open images folder after downloading is done"
                               "\n3 Restore to default settings\n4 Back to main menu\nchoice: ")
                print("")
                # Cooldown_time
                if option == "1":
                    print("Should be 5 - 10 seconds, but can be turned off by using 0.")
                    with open("settings.json", "r") as cfg_file:
                        cfg = json.load(cfg_file)
                    print("cooldown_time = " + str(cfg["cooldown_time"]))
                    try:
                        cfg["cooldown_time"] = int(input("Input value: "))
                        if 0 <= cfg["cooldown_time"] <= 10000:
                            with open("settings.json", "w") as cfg_file:
                                json.dump(cfg, cfg_file)
                            print("\nChanges were saved successfully.")
                        else:
                            print("\nInvalid input. Choose a value between 0-10000 No changes were made.")
                    except ValueError:
                        print("\nInvalid input. No changes were made.")
                    print("")
                # Open_folder_end
                elif option == "2":
                    template_true = "True"
                    template_false = "False"
                    print("Choose whether you want to open images folder after downloading is done.")
                    with open("settings.json", "r") as cfg_file:
                        cfg = json.load(cfg_file)
                    print("open_folder_end = " + cfg["open_folder_end"])
                    cfg["open_folder_end"] = input("Input value: ")
                    if not cfg["open_folder_end"].isdigit():
                        if cfg["open_folder_end"].lower() == template_true.lower():
                            cfg["open_folder_end"] = "True"
                        elif cfg["open_folder_end"].lower() == template_false.lower():
                            cfg["open_folder_end"] = "False"
                        with open("settings.json", "w") as cfg_file:
                            json.dump(cfg, cfg_file)
                        print("\nChanges were saved successfully.")
                    else:
                        print("\nInvalid input. Enter True or False.")
                    print("")
                # Return to defaults
                elif option == "3":
                    with open("settings.json", "w") as cfg_file:
                        json.dump(default_cfg, cfg_file)
                    print("Settings were restored to default values.\n")
                # Go back to main menu
                elif option == "4":
                    settings_repeat = False
                # Invalid input
                else:
                    print("Invalid value\n")
                    settings_repeat = True
        # Remove old images
        elif option == "3":
            try:
                for path in os.listdir("images"):
                    os.remove("images/" + path)
                print("Previously downloaded files have been cleared successfully.\n")
            except FileNotFoundError:
                print("There are no files to be deleted.\n")
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
                        if open_folder_end == "True":
                            os.startfile("images")
                        else:
                            pass
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
