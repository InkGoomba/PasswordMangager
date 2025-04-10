import customtkinter as ctk
from PIL import Image
import json
from cryptography.fernet import Fernet
import os

# Global Vars
app_info_window = None
settings_data = None

# Methods
def start():
    global settings_data
    with open('Settings.json', 'r') as file:
        settings_data = json.load(file)

def open_app_info():    
    global app_info_window
    if app_info_window is None or not app_info_window.winfo_exists():
        app_info_window = ctk.CTkToplevel()
        app_info_window.title("About Window")
        app_info_window.geometry("300x300")
        app_info_text = ctk.CTkLabel(app_info_window, text="Created by: James Meyers", font=('Aptos',15))
        app_info_text2 = ctk.CTkLabel(app_info_window, text="Version: b.1.4", font=('Aptos',15))
        app_info_text.pack(anchor="w")
        app_info_text2.pack(anchor="w")
    else:
        app_info_window.destroy()

def generate_key():
    key = Fernet.generate_key()
    key_location = ctk.filedialog.asksaveasfilename(title="Save Key File", defaultextension=".key", filetypes=[("Key Files", "*.key")])
    if key_location == os.path.isdir:
        with open(key_location, 'wb') as filekey:
            filekey.write(key)

def load_data():
    main_frame.grid_forget()
    main_frame.place_forget()
    global settings_data
    settings_data_accounts_text = ctk.StringVar(value=settings_data["accountsFileLocation"])
    settings_data_key_text = ctk.StringVar(value=settings_data["keyFileLocation"])
    accounts_file_location = ctk.CTkEntry(main_frame, width=500, textvariable=settings_data_accounts_text)
    key_file_location = ctk.CTkEntry(main_frame, width=500, textvariable=settings_data_key_text)
    change_accounts_location_button = ctk.CTkButton(main_frame ,text="Change File", command=lambda: change_data_location(settings_data_accounts_text))
    change_key_location_button = ctk.CTkButton(main_frame, text="Change File")
    accounts_desc_label = ctk.CTkLabel(main_frame, text="Accounts Location:")
    key_desc_label = ctk.CTkLabel(main_frame, text="Key Location:")
    accounts_desc_label.grid(row=0, column=0, padx=10, pady=10)
    accounts_file_location.grid(row=0, column=1, padx=10, pady=10)
    change_accounts_location_button.grid(row=0, column=2, padx=10, pady=10)
    key_desc_label.grid(row=1, column=0, padx=10, pady=10)
    key_file_location.grid(row=1, column=1, padx=10, pady=10)
    change_key_location_button.grid(row=1, column=2, padx=10, pady=10)

def change_data_location(settings_data_text : ctk.StringVar):
    global settings_data
    new_location = ctk.filedialog.askopenfilename(title="Select Account JSON File", defaultextension=".json", filetypes=[("JSON Files", "*json")])
    settings_data["accountsFileLocation"] = new_location
    with open("Settings.json", 'w') as file:
        json.dump(settings_data, file, indent=4)
    settings_data_text.set(new_location)

# Initialization
app = ctk.CTk()
app.title("Password Manager")
app.geometry("1600x900")

# Side Bar
sidebar_frame = ctk.CTkFrame(app, width=200, fg_color="#808080")
sidebar_frame.pack(side="left", fill="y")

image = Image.open("icon.png") 
logo_image_c = ctk.CTkImage(dark_image=image, size=(150,150))
logo_image = ctk.CTkLabel(sidebar_frame, image=logo_image_c, text="")
logo_image.pack(padx=10, pady=10)

load_frame = ctk.CTkFrame(sidebar_frame, fg_color="#6b6b6b")
load_frame.pack(pady=10)
load_frame_title = ctk.CTkLabel(load_frame, text="Load Options",text_color="#ffffff")
load_frame_title.pack()

selection_frame = ctk.CTkFrame(sidebar_frame, fg_color="#6b6b6b")
selection_frame.pack(pady=10)
selection_frame_title = ctk.CTkLabel(selection_frame, text="Selection Options", text_color="#ffffff")
selection_frame_title.pack()

info_frame = ctk.CTkFrame(sidebar_frame, fg_color="#6b6b6b")
info_frame.pack(pady=10)
info_frame_title = ctk.CTkLabel(info_frame, text="Data Managment", text_color="#ffffff")
info_frame_title.pack()

# Side Bar Buttons
load_acc_button = ctk.CTkButton(load_frame, text="Load Data", bg_color="#6b6b6b", command=load_data)
load_acc_button.pack(padx=10, pady=10)

export_accounts_button = ctk.CTkButton(load_frame, text="Export Accounts")
export_accounts_button.pack(padx=10, pady=10)

browse_button = ctk.CTkButton(selection_frame, text="Browse all Accounts")
browse_button.pack(padx=10, pady=10)

search_button = ctk.CTkButton(selection_frame, text="Search for Account")
search_button.pack(padx=10, pady=10)

add_account_button = ctk.CTkButton(info_frame, text="Add Account")
add_account_button.pack(padx=10, pady=10)

db_info = ctk.CTkButton(info_frame, text="DB Info")
db_info.pack(padx=10, pady=10)

app_info = ctk.CTkButton(info_frame, text="About", command=open_app_info)
app_info.pack(padx=10, pady=10)

generate_key_button = ctk.CTkButton(info_frame, text="Generate New Key", command=generate_key)
generate_key_button.pack(padx=10, pady=10)

# Main Frame
main_frame = ctk.CTkScrollableFrame(app)
main_frame.pack(side="right", fill="both", expand=True)


# Run the application
start()
app.mainloop()