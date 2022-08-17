from tkinter.filedialog import askdirectory
import os
try:
    cfg_file = open("variables.json", "x")
    cfg_file.flush()
    os.fsync(cfg_file.fileno())
except FileExistsError:
    pass
folder_path = askdirectory()
with open("variables.json", "w") as variables:
    variables.write(folder_path)
