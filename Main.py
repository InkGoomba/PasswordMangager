import customtkinter as ctk
from PIL import Image
import json
from cryptography.fernet import Fernet
import os
from datetime import datetime

# Global Vars
app_info_window = None
alert_info_window = None
settings_data = None
accounts_data = None
key_data_fernet = None

# Account Frame Object
class AccountFrame(ctk.CTkFrame):
    def __init__(self, master, username, password, site, notes, email, **kwargs):
        super().__init__(master, **kwargs)

        self.username_string = ctk.StringVar(value=username)
        self.password_string = ctk.StringVar(value=password)
        self.notes_string = ctk.StringVar(value=notes)
        self.email_string = ctk.StringVar(value=email)

        self.site = ctk.CTkLabel(self, text=site, font=('Aptos', 20))
        self.username = ctk.CTkEntry(self, textvariable=self.username_string, width=300)
        self.password = ctk.CTkEntry(self, textvariable=self.password_string, width=300)
        self.notes = ctk.CTkEntry(self, textvariable=self.notes_string, width=300)
        self.email = ctk.CTkEntry(self, textvariable=self.email_string, width=300)
        self.username_label = ctk.CTkLabel(self, text="Username")
        self.password_label = ctk.CTkLabel(self, text="Password")
        self.notes_label = ctk.CTkLabel(self, text="Notes")
        self.email_label = ctk.CTkLabel(self, text="Email")
        
        self.site.grid(row=0, column=0, columnspan=2, padx=5, pady=10)
        self.username_label.grid(row=1, column=0, padx=(175,10), pady=5)
        self.password_label.grid(row=2, column=0, padx=(175,10), pady=5)
        self.email_label.grid(row=3, column=0, padx=(175,10), pady=5)
        self.notes_label.grid(row=4, column=0, padx=(175,10), pady=5)
        self.username.grid(row=1, column=1, padx=5, pady=5)
        self.password.grid(row=2, column=1, padx=5, pady=5)
        self.email.grid(row=3, column=1, padx=5, pady=5)
        self.notes.grid(row=4, column=1, padx=5, pady=5)
        
# Methods
def start():
    global accounts_data
    global settings_data
    global key_data_fernet
    with open('Settings.json', 'r') as file:
        settings_data = json.load(file)
    if os.path.isfile(settings_data["keyFileLocation"]):
        with open(settings_data["keyFileLocation"], 'rb') as filekey:
            key_bytes = filekey.read()
        key_data_fernet = Fernet(key_bytes)
    if os.path.isfile(settings_data["accountsFileLocation"]) and key_data_fernet != None:
        with open(settings_data["accountsFileLocation"], 'rb') as enc_file:
            encrypted_bytes = enc_file.read()
        try:
            decrypted_bytes = key_data_fernet.decrypt(encrypted_bytes)
            accounts_data = json.loads(decrypted_bytes.decode('utf-8'))
        except:
            info_popup("Invalid Key. Must use the same key used to encrypt file", "Error")

def open_app_info():    
    global app_info_window
    global settings_data
    global accounts_data

    if app_info_window is None or not app_info_window.winfo_exists():
        total_num_accounts = len(accounts_data["accounts"])
        last_key_save_date = datetime.fromtimestamp(os.path.getmtime(settings_data["keyFileLocation"])).strftime("%m-%d-%Y")
        last_accounts_save_date = datetime.fromtimestamp(os.path.getmtime(settings_data["accountsFileLocation"])).strftime("%m-%d-%Y")

        app_info_window = ctk.CTkToplevel()
        app_info_window.title("About Window")
        app_info_window.geometry("300x300")
        app_info_text = ctk.CTkLabel(app_info_window, text="Created by: James Meyers", font=('Aptos',15))
        app_info_text2 = ctk.CTkLabel(app_info_window, text="Version: 1.01", font=('Aptos',15))
        app_info_text.pack(anchor="w")
        app_info_text2.pack(anchor="w")
        total_num_accounts_text = ctk.CTkLabel(app_info_window, text=f'Total Accounts in File: {total_num_accounts}', font=('Aptos',15))
        accounts_last_save_text = ctk.CTkLabel(app_info_window, text=f'Account File Last Save: {last_accounts_save_date}', font=('Aptos',15))
        key_last_save_text = ctk.CTkLabel(app_info_window, text=f'Key File Last Save: {last_key_save_date}', font=('Aptos',15))
        total_num_accounts_text.pack(anchor="w")
        accounts_last_save_text.pack(anchor="w")
        key_last_save_text.pack(anchor="w")

    else:
        app_info_window.destroy()

def generate_key():
    global alert_info_window
    global settings_data
    global key_data_fernet
    key = Fernet.generate_key()
    key_location = ctk.filedialog.asksaveasfilename(title="Save Key File", defaultextension=".key", filetypes=[("Key Files", "*.key")])
    if os.path.isdir(os.path.dirname(key_location)):
        with open(key_location, 'wb') as filekey:
            filekey.write(key)
        settings_data["keyFileLocation"] = key_location
        key_data_fernet = Fernet(key)
    else:
        info_popup("Not a valid file location", "Error")

def load_data():
    for widget in main_frame.winfo_children():
        widget.destroy()
    main_frame.grid_columnconfigure(0,weight=0)
    main_frame.grid_columnconfigure(1,weight=0)
    global settings_data
    settings_data_accounts_text = ctk.StringVar(value=settings_data["accountsFileLocation"])
    settings_data_key_text = ctk.StringVar(value=settings_data["keyFileLocation"])
    accounts_file_location = ctk.CTkEntry(main_frame, width=500, textvariable=settings_data_accounts_text, state=ctk.DISABLED)
    key_file_location = ctk.CTkEntry(main_frame, width=500, textvariable=settings_data_key_text, state=ctk.DISABLED)
    change_accounts_location_button = ctk.CTkButton(main_frame ,text="Change File", command=lambda: change_account_location(settings_data_accounts_text))
    change_key_location_button = ctk.CTkButton(main_frame, text="Change File", command=lambda: change_key_location(settings_data_key_text))
    accounts_desc_label = ctk.CTkLabel(main_frame, text="Accounts Location:")
    key_desc_label = ctk.CTkLabel(main_frame, text="Key Location:")
    accounts_desc_label.grid(row=0, column=0, padx=10, pady=10)
    accounts_file_location.grid(row=0, column=1, padx=10, pady=10)
    change_accounts_location_button.grid(row=0, column=2, padx=10, pady=10)
    key_desc_label.grid(row=1, column=0, padx=10, pady=10)
    key_file_location.grid(row=1, column=1, padx=10, pady=10)
    change_key_location_button.grid(row=1, column=2, padx=10, pady=10)

def change_account_location(settings_data_text : ctk.StringVar):
    global settings_data
    new_location = ctk.filedialog.askopenfilename(title="Select Account JSON File", defaultextension=".json", filetypes=[("JSON Files", "*json")])
    if os.path.isfile(new_location):
        settings_data["accountsFileLocation"] = new_location
        with open("Settings.json", 'w') as file:
            json.dump(settings_data, file, indent=4)
        start()
        settings_data_text.set(new_location)

def change_key_location(settings_key_text : ctk.StringVar):
    global settings_data
    new_location = ctk.filedialog.askopenfilename(title="Select Key File", defaultextension=".key", filetypes=[("Key Files", "*key")])
    if os.path.isfile(new_location):
        settings_data["keyFileLocation"] = new_location
        with open("Settings.json", 'w') as file:
            json.dump(settings_data, file, indent=4)
        start()
        settings_key_text.set(new_location)

def display_accounts():
    global accounts_data
    for widget in main_frame.winfo_children():
        widget.destroy()
    account_frames = []

    main_frame.grid_columnconfigure(0,weight=1)
    main_frame.grid_columnconfigure(1,weight=1)

    if accounts_data != None:
        accounts = accounts_data["accounts"]
        row_num = 0
        col_num = 0
        for account in accounts:
            account_frames.append(AccountFrame(master=main_frame, site=account["site"], username=account["username"], password=account["password"], email=account["email"], notes=account["notes"], fg_color="#808080"))
        for frame in account_frames:
            frame.grid(row=row_num, column=col_num, padx=5, pady=5, sticky="nsew")
            if col_num == 1:
                row_num += 1
                col_num = 0
            else:
                col_num += 1
    else:
        info_popup("Account data is missing or invalid", "Error")

def export_accounts():
    global settings_data
    global accounts_data
    global key_data_fernet

    if accounts_data == None or key_data_fernet == None:
        info_popup("Invalid key or account data to save or export", "Error")
    else:
        accounts_json = json.dumps(accounts_data, indent=4)
        accounts_bytes = accounts_json.encode('utf-8')
        encrypted_accounts = key_data_fernet.encrypt(accounts_bytes)

        if os.path.isfile(settings_data["accountsFileLocation"]):
            with open(settings_data["accountsFileLocation"],'wb') as encrypted_file:
                encrypted_file.write(encrypted_accounts)
            info_popup(f"Accounts exported to {settings_data['accountsFileLocation']}", "Success")
        else:
            encrypted_file_location = ctk.filedialog.asksaveasfilename(title="Save Encrypted Account File", defaultextension=".json", filetypes=[("JSON Files", "*.json")])
            if os.path.isdir(os.path.dirname(encrypted_file_location)):
                with open(encrypted_file_location, 'wb') as encrypted_file:
                    encrypted_file.write(encrypted_accounts)
                settings_data["accountsFileLocation"] = encrypted_file_location
            else:
                info_popup("Not a valid file location", "Error")

def info_popup(info_message, info_title):
    global alert_info_window
    alert_info_window = ctk.CTkToplevel()
    alert_info_window.title(info_title)
    alert_info_window.geometry("300x100")
    alert_info_text = ctk.CTkLabel(master=alert_info_window, text=info_message, font=('Aptos', 15))
    alert_info_text.pack()

def add_account():
    global accounts_data

    for widget in main_frame.winfo_children():
        widget.destroy()
    main_frame.grid_columnconfigure(0,weight=0)
    main_frame.grid_columnconfigure(1,weight=0)

    site_name = ctk.CTkEntry(main_frame)
    username = ctk.CTkEntry(main_frame)
    password = ctk.CTkEntry(main_frame)
    email = ctk.CTkEntry(main_frame)
    notes = ctk.CTkEntry(main_frame)
    site_name_label = ctk.CTkLabel(main_frame, text="Site Name:")
    username_label = ctk.CTkLabel(main_frame, text="Username:")
    password_label = ctk.CTkLabel(main_frame, text="Password:")
    email_label = ctk.CTkLabel(main_frame, text="Email:")
    notes_label = ctk.CTkLabel(main_frame, text="Notes:")
    submit_button = ctk.CTkButton(main_frame, text="Add Account", command=lambda: submit_account_data(site_name.get(), username.get(), password.get(), email.get(), notes.get()))
    site_name_label.grid(row=0, column=0, padx=10, pady=10)
    username_label.grid(row=1, column=0, padx=10, pady=10)
    password_label.grid(row=2, column=0, padx=10, pady=10)
    email_label.grid(row=3, column=0, padx=10, pady=10)
    notes_label.grid(row=4, column=0, padx=10, pady=10)
    site_name.grid(row=0, column=1, padx=10, pady=10)
    username.grid(row=1, column=1, padx=10, pady=10)
    password.grid(row=2, column=1, padx=10, pady=10)
    email.grid(row=3, column=1, padx=10, pady=10)
    notes.grid(row=4, column=1, padx=10, pady=10)
    submit_button.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

def submit_account_data(site_name, username, password, email, notes):
    global accounts_data
    new_account = {
        "site": site_name,
        "username": username,
        "password": password,
        "email": email,
        "notes": notes
    }
    if accounts_data == None:
        accounts_data = {"accounts":[]}
        accounts_data["accounts"].append(new_account)
    elif "accounts" in accounts_data and isinstance(accounts_data["accounts"], list):
        accounts_data["accounts"].append(new_account)
    else:
        accounts_data["accounts"] = [new_account]

def search_account_page():
    for widget in main_frame.winfo_children():
        widget.destroy()

    main_frame.grid_columnconfigure(0,weight=1)
    main_frame.grid_columnconfigure(1,weight=1)
    main_frame.grid_columnconfigure(2,weight=2)

    search_bar = ctk.CTkEntry(main_frame, width=300)
    search_text = ctk.CTkLabel(main_frame, text="Search", font=('Aptos', 20))
    search_button = ctk.CTkButton(main_frame, text="Search Accounts", command= lambda:search_accounts(search_bar.get())) 
    search_bar.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
    search_text.grid(row=0, column=0, padx=10, pady=10)
    search_button.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

def search_accounts(query_string:str):
    global accounts_data
    account_frames=[]

    search_account_page()

    if accounts_data != None:
        for account in accounts_data["accounts"]:
            if query_string.lower() in account["site"].lower():
                account_frames.append(AccountFrame(master=main_frame, site=account["site"], username=account["username"], password=account["password"], email=account["email"], notes=account["notes"], fg_color="#808080"))
        
        row_count = 3

        for frame in account_frames:
            frame.grid(row=row_count, column=3, padx=5, pady=5, sticky="nsew")
            row_count = row_count + 1

    else:
        info_popup("Account data is missing or invalid", "Error")

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

export_accounts_button = ctk.CTkButton(load_frame, text="Save/Export Accounts", command=export_accounts)
export_accounts_button.pack(padx=10, pady=10)

browse_button = ctk.CTkButton(selection_frame, text="Browse all Accounts", command=display_accounts)
browse_button.pack(padx=10, pady=10)

search_button = ctk.CTkButton(selection_frame, text="Search for Account", command=search_account_page)
search_button.pack(padx=10, pady=10)

add_account_button = ctk.CTkButton(info_frame, text="Add Account", command=add_account)
add_account_button.pack(padx=10, pady=10)

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