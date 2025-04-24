import customtkinter as ctk
from PIL import Image
import json
from cryptography.fernet import Fernet
import os

# Global Vars
app_info_window = None
alert_info_window = None
settings_data = None
accounts_data = None

# Account Frame Object
class AccountFrame(ctk.CTkFrame):
    def __init__(self, master, username, password, site, notes, email, **kwargs):
        super().__init__(master, **kwargs)

        self.username_string = ctk.StringVar(value=username)
        self.password_string = ctk.StringVar(value=password)
        self.notes_string = ctk.StringVar(value=notes)
        self.email_string = ctk.StringVar(value=email)

        self.site = ctk.CTkLabel(self, text=site, font=('Aptos', 20), width=675)
        self.username = ctk.CTkEntry(self, textvariable=self.username_string, width=300)
        self.password = ctk.CTkEntry(self, textvariable=self.password_string, width=300)
        self.notes = ctk.CTkEntry(self, textvariable=self.notes_string, width=300)
        self.email = ctk.CTkEntry(self, textvariable=self.email_string, width=300)
        
        self.site.pack(pady=10)
        self.email.pack(pady=5)
        self.username.pack(pady=5)
        self.password.pack(pady=5)
        self.notes.pack(pady=5)


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
        app_info_text2 = ctk.CTkLabel(app_info_window, text="Version: b.1.7", font=('Aptos',15))
        app_info_text.pack(anchor="w")
        app_info_text2.pack(anchor="w")
    else:
        app_info_window.destroy()

def generate_key():
    global alert_info_window
    global settings_data
    key = Fernet.generate_key()
    key_location = ctk.filedialog.asksaveasfilename(title="Save Key File", defaultextension=".key", filetypes=[("Key Files", "*.key")])
    if os.path.isdir(os.path.dirname(key_location)):
        with open(key_location, 'wb') as filekey:
            filekey.write(key)
        settings_data["keyFileLocation"] = key_location
    else:
        if alert_info_window is None or not alert_info_window.winfo_exists():
            alert_info_window = ctk.CTkToplevel()
            alert_info_window.title("Alert")
            alert_info_window.geometry("300x100")
            alert_info_text = ctk.CTkLabel(alert_info_window, text="Not a valid file location", font=('Aptos', 15))
            alert_info_text.pack()

def load_data():
    for widget in main_frame.winfo_children():
        widget.destroy()
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
        settings_data_text.set(new_location)

def change_key_location(settings_key_text : ctk.StringVar):
    global settings_data
    new_location = ctk.filedialog.askopenfilename(title="Select Key File", defaultextension=".key", filetypes=[("Key Files", "*key")])
    if os.path.isfile(new_location):
        settings_data["keyFileLocation"] = new_location
        with open("Settings.json", 'w') as file:
            json.dump(settings_data, file, indent=4)
        settings_key_text.set(new_location)

def display_accounts():
    global settings_data
    global accounts_data
    for widget in main_frame.winfo_children():
        widget.destroy()
    account_frames = []

    if os.path.isfile(settings_data["accountsFileLocation"]):
        with open(settings_data["accountsFileLocation"], 'r') as file:
            accounts_data = json.load(file)
        accounts = accounts_data["accounts"]
        row_num = 0
        col_num = 0
        for account in accounts:
            account_frames.append(AccountFrame(master=main_frame, site=account["site"], username=account["username"], password=account["password"], email=account["email"], notes=account["notes"], fg_color="#808080"))
        for frame in account_frames:
            frame.grid(row=row_num, column=col_num, padx=5, pady=5)
            if col_num == 1:
                row_num += 1
                col_num = 0
            else:
                col_num += 1

def export_accounts():
    global settings_data
    global accounts_data
    global alert_info_window
    key_bytes = None
    if accounts_data == None:
        alert_info_window = ctk.CTkToplevel()
        alert_info_window.title("Alert")
        alert_info_window.geometry("300x100")
        alert_info_text = ctk.CTkLabel(alert_info_window, text="No data to save or export", font=('Aptos', 15))
        alert_info_text.pack()
    else:
        with open(settings_data["keyFileLocation"], 'rb') as filekey:
            key_bytes = filekey.read()


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