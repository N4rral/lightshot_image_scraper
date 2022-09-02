import random
import cloudscraper
import os
import requests
import time
from urllib import request
import json
from types import SimpleNamespace
from subprocess import call
import shutil
import subprocess

full_repeat = True
amount = 0
default_cfg = {
    "cooldown_time": 5,
    "open_folder_end": "True",
    "images_folder_location": "images",
    "image_management_mode": "replace"
}
cfg = {}
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
        images_folder_location = n.images_folder_location
        image_management_mode = n.image_management_mode
        if images_folder_location != "images":
            try:
                os.mkdir(images_folder_location)
            except FileExistsError:
                pass
        else:
            try:
                os.mkdir("images")
            except FileExistsError:
                pass
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
            with open("settings.json", "r") as cfg_file:
                cfg = json.load(cfg_file)
            settings_repeat = True
            while settings_repeat:
                option = input("1 Change cooldown time = " + str(cfg["cooldown_time"]) +
                               "\n2 Open images folder after downloading is done = " + str(cfg["open_folder_end"]) +
                               "\n3 Set a new directory for the images which is currently: "
                               + str(cfg["images_folder_location"]) +
                               "\n4 Image management mode = " + str(cfg["image_management_mode"]) +
                               "\n5 Restore to default settings\n6 Back to main menu\nchoice: ")
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
                    print("Choose whether you want to open images folder after downloading is done.")
                    with open("settings.json", "r") as cfg_file:
                        cfg = json.load(cfg_file)
                    print("open_folder_end = " + cfg["open_folder_end"])
                    choice = input("1 True\n2 False\nChoice: ")
                    if choice == "1":
                        cfg["open_folder_end"] = "True"
                        with open("settings.json", "w") as cfg_file:
                            json.dump(cfg, cfg_file)
                    if choice == "2":
                        cfg["open_folder_end"] = "False"
                        with open("settings.json", "w") as cfg_file:
                            json.dump(cfg, cfg_file)
                    else:
                        print("\nInvalid input. No changes were made.")
                    print("")
                # Choose a new directory for the images to be downloaded to
                elif option == "3":
                    option = input("1 Choose a new path\n2 Set default remove folder and delete images"
                                   "\n3 Set default remove folder and migrate images"
                                   " (replaces images in default folder if names are duplicate)"
                                   "\n4 Back to settings\nchoice: ")
                    if option == "1":
                        with open("settings.json", "r") as cfg_file:
                            cfg = json.load(cfg_file)
                        print("Choose a directory where you want to create a new folder.")
                        s = subprocess.check_output(r"subprocess\folder.exe", shell=True)
                        with open("variables.json", "r") as variables:
                            cfg["images_folder_location"] = variables.read() + "/images"
                        os.remove("variables.json")
                        with open("settings.json", "w") as cfg_file:
                            json.dump(cfg, cfg_file)
                        with open("settings.json", "r") as cfg_file:
                            cfg = json.load(cfg_file)
                            try:
                                os.mkdir(cfg["images_folder_location"])
                            except FileExistsError:
                                pass
                            else:
                                try:
                                    os.mkdir("images")
                                except FileExistsError:
                                    pass
                        print("\nFolder has been set to your desired location.")
                    elif option == "2":
                        with open("settings.json", "r") as cfg_file:
                            cfg = json.load(cfg_file)
                            if cfg["images_folder_location"] != "images":
                                try:
                                    for path in os.listdir(images_folder_location + "/"):
                                        os.remove(images_folder_location + "/" + path)
                                    os.rmdir(cfg["images_folder_location"])
                                except FileNotFoundError:
                                    pass
                                cfg["images_folder_location"] = default_cfg["images_folder_location"]
                                print("\nYour folder has been successfully removed along with all the images.")
                            else:
                                print("\nFolder is set to default. Deleting that folder is not permitted.")
                        with open("settings.json", "w") as cfg_file:
                            json.dump(cfg, cfg_file)
                    elif option == "3":
                        with open("settings.json", "r") as cfg_file:
                            cfg = json.load(cfg_file)
                            if cfg["images_folder_location"] != "images":
                                try:
                                    for path in os.listdir(images_folder_location + "/"):
                                        try:
                                            shutil.move(images_folder_location + "/" + path, "images")
                                        except shutil.Error:
                                            os.replace(images_folder_location + "/" + path, "images/" + path)
                                    os.rmdir(cfg["images_folder_location"])
                                except FileNotFoundError:
                                    pass
                                cfg["images_folder_location"] = default_cfg["images_folder_location"]
                                print("\nYour folder has been successfully removed along with all the images.")
                            else:
                                print("\nFolder is set to default. Deleting that folder is not permitted.")
                        with open("settings.json", "w") as cfg_file:
                            json.dump(cfg, cfg_file)
                    elif option == "4":
                        pass
                    else:
                        print("\nInvalid input. Choose option.")
                    print("")
                elif option == "4":
                    with open("settings.json", "r") as cfg_file:
                        cfg = json.load(cfg_file)
                    print("image_management_mode = " + cfg["image_management_mode"])
                    choice = input("1 Replace (replaces old images when new are being downloaded)"
                                   "\n2 Append (old images will be kept when downloading new ones)"
                                   "\n3 Back to settings \nchoice:")
                    if choice == "1":
                        cfg["image_management_mode"] = "replace"
                        with open("settings.json", "w") as cfg_file:
                            json.dump(cfg, cfg_file)
                        print("\nChanges were saved successfully.")
                    elif choice == "2":
                        cfg["image_management_mode"] = "append"
                        with open("settings.json", "w") as cfg_file:
                            json.dump(cfg, cfg_file)
                        print("\nChanges were saved successfully.")
                    elif choice == "3":
                        pass
                    else:
                        print("\nInvalid input.")
                    print("")
                # Return to defaults
                elif option == "5":
                    with open("settings.json", "w") as cfg_file:
                        json.dump(default_cfg, cfg_file)
                    print("Settings were restored to default values.\n")
                # Go back to main menu
                elif option == "6":
                    settings_repeat = False
                # Invalid input
                else:
                    print("Invalid value\n")
                    settings_repeat = True
        # Remove old images
        elif option == "3":
            try:
                for path in os.listdir(images_folder_location + "/"):
                    os.remove(images_folder_location + "/" + path)
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
    alt_i = 0
    if image_management_mode == "replace":
        pass
    else:
        for path in os.listdir(images_folder_location + "/"):
            alt_i += 1
    partial_repeat = True
    # Generate basic urls that will later be used to get images from
    while partial_repeat:
        while i < amount:
            st = time.time()
            i += 1
            alt_i += 1
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
                alt_i -= 1
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
                    alt_i -= 1
                else:
                    # So the printed urls are in a column
                    if i < 10:
                        print(str(alt_i) + ":   " + img_url)
                    elif 10 <= alt_i < 100:
                        print(str(alt_i) + ":  " + img_url)
                    elif 100 <= alt_i < 1000:
                        print(str(alt_i) + ": " + img_url)
                    else:
                        print(str(alt_i) + ":" + img_url)
                    # Saving image from the url
                    img_data = requests.get(img_url).content
                    with open(os.path.join(images_folder_location, str(alt_i) + ".jpg"), "wb") as handler:
                        handler.write(img_data)
                    et = time.time()
                    # Get process runtime and set time.sleep() for the process to be 5sec or longer if necessary
                    ft = et - st
                    if i < amount:
                        if ft >= cooldown_time or cooldown_time == 0:
                            time.sleep(0)
                        else:
                            time.sleep(cooldown_time - ft)
                    else:
                        print("Process finished\n")
                        if open_folder_end == "True":
                            os.startfile(images_folder_location)
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
