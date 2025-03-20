import customtkinter as ctk

# Initialization
app = ctk.CTk()
app.title("Password Manager")
app.geometry("1600x900")

# Side Bar
sidebar_frame = ctk.CTkFrame(app, width=200, fg_color="#808080")
sidebar_frame.pack(side="left", fill="y")

testlbl = ctk.CTkLabel(sidebar_frame, text="lol")
testlbl.pack()

# Main Frame
main_frame = ctk.CTkScrollableFrame(app, )
main_frame.pack(side="right", fill="both", expand=True)


# Run the application
app.mainloop()