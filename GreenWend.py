import tkinter as tk
from tkinter import *
from tkinter import filedialog, messagebox
import os
from github import Github, UnknownObjectException
from github import Github
import firebase_admin
from firebase_admin import credentials, db
import time
from PIL import Image, ImageTk
import requests
from io import BytesIO
import pandas as pd
import socket
import threading

Key = {
  # Your json KEY
}

license_text = "Software License Agreement\n\n\
This Software License Agreement (\"Agreement\") \nis between GreenWend\n (\"SU2923-234\") and the individual or entity (\"Licensee\") who\n is agreeing to the terms of this Agreement.\n\n\
1. License Grant: Subject to the terms and \nconditions of this Agreement, Licensor grants Licensee\n a  license to use the software (\"Software\")\n provided by Licensor.\n\n\
2. Restrictions: Licensee shall not (a)\n sublicense, sell, lease, or otherwise \ndistribute the Software to any third\n party; (b) modify, adapt, translate, reverse engineer,\n decompile, or disassemble the Software; (c)\n remove or alter any copyright, trademark, or other \nproprietary notices; (d) use the Software in any manner\n that violates applicable laws or regulations.\n\n\
3. Ownership: Licensor retains all right, title,\n and interest in and to the Software, including all intellectual\n property rights.\n\n\
4. Warranty Disclaimer: The Software\n is provided \"as is\" without warranty\n of any kind. Licensor disclaims all\n warranties, express or implied, including but not limited to\n the implied warranties of merchantability, fitness\n for a particular purpose, and non-infringement.\n\n\
5. Limitation of Liability: In no event shall\n Licensor be liable for any direct, indirect, incidental, special,\n or consequential damages arising out of or in any way connected \nmwith the use or performance of the Software.\n\n\
6. Governing Law: This Agreement shall be\n governed by and construed in accordance with the\n laws of [Your Jurisdiction].\n\n\
7. Termination: This Agreement is effective until terminated\n by either party. Upon termination, Licensee \nshall cease all use of the Software and destroy all copies\n of the Software in its possession or control.\n\n\
8. Entire Agreement: This Agreement constitutes\n the entire understanding between the parties concerning the subject\n matter hereof and supersedes all prior agreements and understandings, whether\n oral or written.\n\n\
By using the Software, Licensee agrees to be\n bound by the terms and conditions of this Agreement.\n\n\
Copyright: ©greenwendenergy.com 2024 by Younas Khan\nAll rights reserved\
2/29/2024"


cred = credentials.Certificate(Key)
firebase_admin.initialize_app(cred, {'databaseURL': 'https://greenwend-1d975-default-rtdb.asia-southeast1.firebasedatabase.app/'})
ref = db.reference()

def get_github_token():
    token = db.reference("Firmware_Version/Update_Status/Github_ID")
    token_id = token.get()
    return str(token_id)

def update_github_token(token):
    db.reference("Firmware_Version/Update_Status/Github_ID").set(token)

github_token = get_github_token()

prev_rep = db.reference("Firmware_Version/Update_Status/Git_rep_user").get()

def Update_Rep(user,rep):
    db.reference("Firmware_Version/Update_Status/Git_rep_user").set(user)
    db.reference("Firmware_Version/Update_Status/Git_rep").set(rep)

def login():
    username = username_entry.get()
    password = password_entry.get()

    # Dummy authentication
    if username == "admin" and password == "password":
        clear_login_screen()
        create_menu()
    else:
        messagebox.showerror("Login Failed", "Invalid username or password")

def clear_login_screen():
    login_frame.place_forget()

# Function to update GitHub token
def update_github():
    token = tk.simpledialog.askstring("Update GitHub Token", "Enter new GitHub token:")
    update_github_token(token)
    

# Function to show GitHub token
def show_github_token():
    messagebox.showinfo("GitHub Token", f"The current GitHub token is: {github_token}")
    root.after(10000, lambda: root.clipboard_clear())

# Function to provide information about GitHub token
def info_github_token():
    messagebox.showinfo("GitHub Token Info", "The GitHub token is used for authentication with the GitHub API.")


def create_menu():
    menu = tk.Menu(root)
    root.config(menu=menu)

    file_menu = tk.Menu(menu)

    def User():
        clear_login_screen()
        user_uid_label = tk.Label(root, text="Enter User UID:", bg="#BDDFE0")
        user_uid_label.grid(row=10, column=0, padx=5, pady=10, sticky="w",)

        user_uid_entry = tk.Entry(root)
        user_uid_entry.grid(row=10, column=1, padx=5, pady=10)

        yearl = tk.Label(root, text="Enter Year:", bg="#BDDFE0")
        yearl.grid(row=11, column=0, padx=5, pady=10, sticky="w",)

        year = tk.Entry(root)
        year.grid(row=11, column=1, padx=5, pady=10)
    

        def get_entry_content():
            entry_content = user_uid_entry.get()
            year_ = year.get()
            # Now you have the content of the entry as a string
            # You can use entry_content wherever needed
            print("Entry Content:", entry_content)
            Export(entry_content,year_)

        retrieve_button = tk.Button(root, text="Export Data", command=get_entry_content,bg="#FFD167")
        retrieve_button.grid(row=12, column=0, columnspan=2, padx=5, pady=10)


    menu.add_cascade(label="File", menu=file_menu)
    file_menu.add_command(label="Upload Bin File", command=upload_bin_file)
    file_menu.add_command(label="Update Device", command=update_device)
    file_menu.add_separator()
    file_menu.add_command(label="Exit", command=root.destroy)

    data_menu = tk.Menu(menu)
    menu.add_cascade(label="Data log", menu=data_menu)
    data_menu.add_command(label="Export User Data", command=User)
    data_menu.add_command(label="Notification")

    # New GitHub Token submenu
    github_menu = tk.Menu(menu)
    menu.add_cascade(label="GitHub Token", menu=github_menu)
    github_menu.add_command(label="Update Token", command=update_github)
    github_menu.add_command(label="Show Token", command=show_github_token)
    github_menu.add_command(label="Update Rep",command=update_rep)
    github_menu.add_command(label="Info Token", command=info_github_token)

    menu.config(bg = "#F0C517")
    file_menu.config(bg = "#E1FBF6")
    data_menu.config(bg = "#E1FBF6")
    github_menu.config(bg = "#E1FBF6")
    def about():
        about_frame = tk.Frame(root, bg="#BDDFE0")
        about_frame.grid(row=0, column=0, sticky="nsew")

        # Create a Text widget
        about_text = tk.Text(about_frame, wrap="word", bg="#BDDFE0")
        about_text.grid(row=0, column=0, sticky="nsew")

        # Insert license text into the Text widget
        about_text.insert("1.0", license_text)

        # Create a Scrollbar
        scrollbar = tk.Scrollbar(about_frame, command=about_text.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")

        # Configure Text widget to use the scrollbar
        about_text.config(yscrollcommand=scrollbar.set)

        # Configure grid weights to make the Text widget and Scrollbar resizable
        about_frame.columnconfigure(0, weight=1)
        about_frame.rowconfigure(0, weight=1)

        # Create a back button
        back_button = tk.Button(about_frame, text="Back", command=about_frame.destroy,bg="#FFD167")
        back_button.grid(row=1, column=0, columnspan=2, pady=10)

    help_menu = tk.Menu(menu)
    menu.add_cascade(label="Help", menu=help_menu)
    help_menu.add_command(label="Download Instruction", command=instruct)
    help_menu.add_command(label="About", command=about)

    help_menu.config(bg = "#E1FBF6")

def upload_bin_file():
    file_path = filedialog.askopenfilename(title="Select Bin File", filetypes=[("Bin files", "*.bin")])
    if file_path:
        file_name = os.path.basename(file_path)
        if file_name.endswith(".bin"):
            try:
                # GitHub authentication
                g = Github(github_token)
                repo_owner = db.reference("Firmware_Version/Update_Status/Git_rep_user").get().__str__
                repo_name = db.reference("Firmware_Version/Update_Status/Git_rep").get().__str__
                branch_name = "main"  # Change this to the appropriate branch

                user = g.get_user(repo_owner)
                repo = user.get_repo(repo_name)
                
                # Initialize contents variable
                contents = None
                
                try:
                    # Check if the file already exists in the repository
                    contents = repo.get_contents(file_name, ref=branch_name)
                    if contents:
                        # File exists, delete it
                        repo.delete_file(contents.path, "Replacing existing file", contents.sha, branch=branch_name)
                except UnknownObjectException:
                    # File doesn't exist, handle accordingly (e.g., create the file)
                    pass
                    
                # Upload the new file
                repo.create_file(file_name, "Uploaded file", open(file_path, "rb").read(), branch=branch_name)
                messagebox.showinfo("Upload Success", f"{file_name} uploaded successfully.")
                
            except Exception as e:
                messagebox.showerror("Upload Error", f"An error occurred: {str(e)}")
        else:
            messagebox.showerror("Invalid File Type", "Please select a .bin file.")
def instruct():
    instruction_guide = """
    GreenWend Energy Pvt Ltd
    Think Solar to Live Better
    GreenWend Energy App Instruction
    Created By Younas Khan
    Date: 3/2/2024
    1: Open GreenWend.exe Application in Window
    2: Type User Name and Password
    3: When You login You will see Different Tab menus

    File: Upload Bin File>Update Device >Exit
                                    
    Data Log: Export User Data  >Notification 
                                        
    Github Token: Update Token> Show Token >Update Rep >Info Token
        
    Help: Download Manual>About

    File::
    1. The File contain three dropdown menus
    Upload Bin File use to Upload binary file that was created from Arduino IDE, Whenever new Firmware developed or modified You will first generate the bin file and upload that file to Github repository to update to all Devices
    2. When the first step get completed Now You are able to update the device that you want
    3. Click on Update Device to update a particular device or in simple words to upload new firmware to Energy Meter Device
    4. A new window will appear which requires User UID when You want to enable firmware for that device then Enter UID in input field and Press Start Update The Update will start in few seconds wait for a moments to get Update response back when update completes the response window will pop up Once completed the process then Click On Update device again And enter "0" or "enable" clcik on button to disable the update.
    5. Make Sure that the UID you enter is correct and Match the User UID Info
    6. Exit Tab exit the application

    Data Log
    1. In data log There are two Dropdown menus one is Export User Data and second one is Notification,
    2. The Export Data, Exports the User data Yearly
    3. When you Click Export User data then A new Input Fields will appears
    4. Enter the User UID and Year for which year you want to export data for analysis
    5. The Notification Menu will comming soon for now it is not connected with App root

    Github Token: 
    1. Github token Is generated for bin file upload authentication The Token normaly created for 90 days, When It get expires then You need to generate it again and then copy new token and Enter in the Token Field to Get update for new Authentication process. This is need because when token expires the token will rise error message during uploading bin file.
    2. Show Token Displays current token ID
    3. Token Info Displays Token Information
    5. Update Rep: If you want to change your github repository or Changed account then this menu will change the rep and user name.
        Make sure that to change your account or repository you must have to change access Token for it.
    4. For new Token generation refer to this link https://www.youtube.com/watch?v=mZbJtN4CJwg

    Help:
    Download manual: This tab will download User manual for Application
    About: This Tabe show App License and Agreement
    """

    with open("GreenWend_Instruction_Guide.txt", "w") as file:
        file.write(instruction_guide)
    messagebox.showinfo("Success", "*txt Instruction File created successfully\n See your current directory")

def update_firebase(status, user):
    if status == "disable":
        ref.update({
            "Firmware_Version/Update_Status/Update": False
        })
        ref.update({
            "Firmware_Version/Update_Status/User": "None"
        })
    elif status == "enable":
        ref.update({
            "Firmware_Version/Update_Status/Update": True
        })
        ref.update({
            "Firmware_Version/Update_Status/User": user
        })


def check_internet_connection():
    remote_server = "www.google.com"
    port = 80
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(5)
    try:
        sock.connect((remote_server, port))
        return True
    except socket.error:
        return False
    finally:
        sock.close()

def load_online_image(url):
    if check_internet_connection():
        try:
            response = requests.get(url)
            image_data = response.content
            image = Image.open(BytesIO(image_data))
            return ImageTk.PhotoImage(image)
        except ConnectionError:
            messagebox.showerror("Connection","Error")
    else:
        messagebox.showerror("Error","Internet Connection\nPlease Connect to Internet")

def get_update_status():
    status_ref = db.reference("Firmware_Version/Update_Status/status")
    status = status_ref.get()
    return status

def update_rep():
    frame_git = tk.Toplevel(root)
    frame_git.title("Update Rep")
    frame_git.geometry("300x150")
    frame_git.configure(bg="#BDDFE0")

    rep_label = tk.Label(frame_git, text="Enter User Name:", bg="#BDDFE0")
    rep_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

    rep_entry = tk.Entry(frame_git)
    rep_entry.grid(row=0, column=1, padx=5, pady=5)

    rep = tk.Label(frame_git,text="Enter Rep Name:", bg= "#BDDFE0")
    rep.grid(row=1,column=0,padx=5,pady=5,sticky="w")

    rep_n = tk.Entry(frame_git)
    rep_n.grid(row=1,column=1,padx=5,pady=5)

    def change_rep():
        rep_name = rep_entry.get()
        rep_user = rep_n.get()
        if rep_name != None:
            Update_Rep(str(rep_name),str(rep_user))
        frame_git.destroy()
        check = True
        time.sleep(5)
        while check:
            if  rep_name != prev_rep:
                messagebox.showinfo("Success","Github Rep/name Updated Successfully" )
                check = False
    update_but = tk.Button(frame_git, text="Send Command", command=change_rep, bg="#FFD167")
    update_but.grid(row=2, columnspan=2, pady=10)

def update_device():
    update_frame = tk.Toplevel(root)
    update_frame.title("Update Device")
    update_frame.geometry("300x150")
    update_frame.configure(bg="#BDDFE0")

    user_uid_label = tk.Label(update_frame, text="User UID:", bg="#BDDFE0")
    user_uid_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

    user_uid_entry = tk.Entry(update_frame)
    user_uid_entry.grid(row=0, column=1, padx=5, pady=5)

    instruct = tk.Label(update_frame, text="Disable: For disable update Enter 0 or None\n"
                                                    "Enable: For Enable Update Enter User UID",bg="#BDDFE0")
    instruct.grid(row=2,columnspan=3,padx=5, pady=5)

    def start_update():
        user_uid = user_uid_entry.get()
        if user_uid.lower() in ["none", "0"]:
            update_firebase("disable", user_uid)
            messagebox.showinfo("Update Device", "Update Disabled successfully.")
        else:
            update_firebase("enable", user_uid)
            messagebox.showinfo("Update Device", "Update started successfully\nWait for a while")
            update_frame.destroy()
            threading.Thread(target=update_progress, args=(user_uid,)).start()

    def update_progress(user_uid):
        check = True
        while check:
            if get_update_status() == True:
                messagebox.showinfo("Completed 100%", "Device Update Completed 100%")
                check = False
            time.sleep(1)  # Adjust the interval as needed
                

        

    update_button = tk.Button(update_frame, text="Send Command", command=start_update, bg="#FFD167")
    update_button.grid(row=1, columnspan=2, pady=10)

root = tk.Tk()
root.title("GreenWend 1.2")
root.geometry("720x500")
root.configure(bg="#BDDFE0")

image_url = "https://sunsaviour.com/wp-content/uploads/2024/01/cropped-sunsaviour-logo-final-01-4.png"

# Download and load the image
render = load_online_image(image_url)
root.iconphoto(False, render)

login_frame = tk.Frame(root, bg="#BDDFE0")
login_frame.place(relx=0.5, rely=0.5, anchor="center")

username_label = tk.Label(login_frame, text="Username:", bg="#BDDFE0")
username_label.grid(row=0, column=0, sticky="w")
username_entry = tk.Entry(login_frame)
username_entry.grid(row=0, column=1)

password_label = tk.Label(login_frame, text="Password:", bg="#BDDFE0")
password_label.grid(row=1, column=0, sticky="w")
password_entry = tk.Entry(login_frame, show="*")
password_entry.grid(row=1, column=1)

login_button = tk.Button(login_frame, text="Login", command=login, bg="#FFD167")
login_button.grid(row=2, columnspan=2, pady=10)
l = Label(root, text="GreenWend Energy", width=40,
            height=0, font=('Times New Roman', 20, 'bold'), bg="#BDDFE0")
l.grid(row=0,column=5,padx=45)

logo_image = tk.PhotoImage(file="re.png")
logo_image = logo_image.subsample(logo_image.width() // 100, logo_image.height() // 100)

# Display the logo image
logo_label = tk.Label(root, image=logo_image, bg="#BDDFE0")
logo_label.grid(row=1, column=5)

copyright_ = tk.Label(root, text="Copyright ©greenwendenergy.com 2024 by Younas Khan\nAll rights reserved", bg="#BDDFE0")
copyright_.place(relx = 0.3, rely = 1.0, anchor ='sw')

def Export(user,year):
  
  ref_path = f"/UsersData/{user}/analytics/{year}"
  ref = db.reference(ref_path)
  dic = ref.get()

  if dic is not None:
      pass
  else:
    messagebox.showinfo("Error Occure","No Data Found")


  Yearly = {"Total Export Units Per Year": 0,"Total Home Consumption Per Year": 0,"Total Import Units Per Year": 0,"Total Units Generated Per Year": 0}
  Jan = {}
  Feb = {}
  Mar = {}
  Apr = {}
  May = {}
  Jun = {}
  Jul = {}
  Aug = {}
  Sep = {}
  Oct = {}
  Nov = {}
  Dec = {}

  Jan_Days = []
  Feb_Days = []
  Mar_Days = []
  Apr_Days = []
  May_Days = []
  Jun_Days = []
  Jul_Days = []
  Aug_Days = []
  Sep_Days = []
  Oct_Days = []
  Nov_Days = []
  Dec_Days = []

  Jan_Total = []
  Feb_Total = []
  Mar_Total = []
  Apr_Total = []
  May_Total = []
  Jun_Total = []
  Jul_Total = []
  Aug_Total = []
  Sep_Total = []
  Oct_Total = []
  Nov_Total = []
  Dec_Total = []

  Sep_Days_value = []

  for data in dic:
      if data == "totalExportUnitsPerYear":
          Yearly["Total Export Units Per Year"] = dic[data]
      elif data == "totalHomeConsumptionPerYear":
          Yearly["Total Home Consumption Per Year"] = dic[data]
      elif data == "totalImportUnitsPerYear":
          Yearly["Total Import Units Per Year"] = dic[data]
      elif data == "totalUnitsGeneratedPerYear":
          Yearly["Total Units Generated Per Year"] = dic[data]
      else:
          if data == "01":
              Jan = dic[data]
          elif data == "02":
              Feb = dic[data]
          elif data == "03":
              Mar = dic[data]
          elif data == "04":
              Apr = dic[data]
          elif data == "05":
              May = dic[data]
          elif data == "06":
              Jun = dic[data]
          elif data == "07":
              Jul = dic[data]
          elif data == "08":
              Aug = dic[data]
          elif data == "09":
              Sep = dic[data]
          elif data == "10":
              Oct = dic[data]
          elif data == "11":
              Nov = dic[data]
          elif data == "12":
              Dec = dic[data]
  months = [Jan, Feb, Mar, Apr, May, Jun, Jul, Aug, Sep, Oct, Nov, Dec]

  Jan_Total_Data = {}
  Feb_Total_Data = {}
  Mar_Total_Data = {}
  Apr_Total_Data = {}
  May_Total_Data = {}
  Jun_Total_Data = {}
  Jul_Total_Data = {}
  Aug_Total_Data = {}
  Sep_Total_Data = {}
  Oct_Total_Data = {}
  Nov_Total_Data = {}
  Dec_Total_Data = {}

  PermonthList = ["totalExportUnitsPerMonth", "totalHomeConsumptionPerMonth", "totalImportUnitsPerMonth", "totalUnitsGeneratedPerMonth"]
  for month, total_list, days_list in zip(months, [Jan_Total, Feb_Total, Mar_Total, Apr_Total, May_Total, Jun_Total, Jul_Total, Aug_Total, Sep_Total, Oct_Total, Nov_Total, Dec_Total], [Jan_Days, Feb_Days, Mar_Days, Apr_Days, May_Days, Jun_Days, Jul_Days, Aug_Days, Sep_Days, Oct_Days, Nov_Days, Dec_Days]):
      for val in month:
          if val in PermonthList: 
              total_list.append(val)
              for d in PermonthList:
                if d in Jan:
                  Jan_Total_Data[d] = Jan[d]
                if d in Feb:
                  Feb_Total_Data[d] = Feb[d]
                if d in Mar:
                  Mar_Total_Data[d] = Mar[d]
                if d in Apr:
                  Apr_Total_Data[d] = Apr[d]
                if d in May:
                  May_Total_Data[d] = May[d]
                if d in Jun:
                  Jun_Total_Data[d] = Jun[d]
                if d in Jul:
                  Jul_Total_Data[d] = Jul[d]
                if d in Aug:
                  Aug_Total_Data[d] = Aug[d]
                if d in Sep:
                  Sep_Total_Data[d] = Sep[d]
                if d in Oct:
                  Oct_Total_Data[d] = Oct[d]
                if d in Nov:
                  Nov_Total_Data[d] = Nov[d]
                if d in Dec:
                  Dec_Total_Data[d] = Dec[d]
          else:
              days_list.append(val)

  # January
  days_Jan = [[] for _ in range(31)]

  # February (Assuming non-leap year for simplicity)
  days_Feb = [[] for _ in range(28)]

  # March
  days_Mar = [[] for _ in range(31)]

  # April
  days_Apr = [[] for _ in range(30)]

  # May
  days_May = [[] for _ in range(31)]

  # June
  days_Jun = [[] for _ in range(30)]

  # July
  days_Jul = [[] for _ in range(31)]

  # August
  days_Aug = [[] for _ in range(31)]

  # September
  days_Sep = [[] for _ in range(30)]

  # October
  days_Oct = [[] for _ in range(31)]

  # November
  days_Nov = [[] for _ in range(30)]

  # December
  days_Dec = [[] for _ in range(31)]

  # January
  for i in range(31):
      try:
          if Jan_Days[i] in Jan:
              days_Jan[i] = Jan[Jan_Days[i]]
      except IndexError:
          pass

  # February
  for i in range(28):
      try:
          if Feb_Days[i] in Feb:
              days_Feb[i] = Feb[Feb_Days[i]]
      except IndexError:
          pass

  # March
  for i in range(31):
      try:
          if Mar_Days[i] in Mar:
              days_Mar[i] = Mar[Mar_Days[i]]
      except IndexError:
          pass

  # April
  for i in range(30):
      try:
          if Apr_Days[i] in Apr:
              days_Apr[i] = Apr[Apr_Days[i]]
      except IndexError:
          pass

  # May
  for i in range(31):
      try:
          if May_Days[i] in May:
              days_May[i] = May[May_Days[i]]
      except IndexError:
          pass

  # June
  for i in range(30):
      try:
          if Jun_Days[i] in Jun:
              days_Jun[i] = Jun[Jun_Days[i]]
      except IndexError:
          pass

  # July
  for i in range(31):
      try:
          if Jul_Days[i] in Jul:
              days_Jul[i] = Jul[Jul_Days[i]]
      except IndexError:
          pass

  # August
  for i in range(31):
      try:
          if Aug_Days[i] in Aug:
              days_Aug[i] = Aug[Aug_Days[i]]
      except IndexError:
          pass

  # September
  for i in range(30):
      try:
          if Sep_Days[i] in Sep:
              days_Sep[i] = Sep[Sep_Days[i]]
      except IndexError:
          pass

  # October
  for i in range(31):
      try:
          if Oct_Days[i] in Oct:
              days_Oct[i] = Oct[Oct_Days[i]]
      except IndexError:
          pass

  # November
  for i in range(30):
      try:
          if Nov_Days[i] in Nov:
              days_Nov[i] = Nov[Nov_Days[i]]
      except IndexError:
          pass

  # December
  for i in range(31):
      try:
          if Dec_Days[i] in Dec:
              days_Dec[i] = Dec[Dec_Days[i]]
      except IndexError:
          pass




  # Create an empty DataFrame with the desired columns
  # Create an empty list to store individual DataFrames for each day
  df_jan = []
  df_feb = []
  df_mar = []
  df_apr = []
  df_may = []
  df_jun = []
  df_jul = []
  df_aug = []
  df_sep = []
  df_oct = []
  df_nov = []
  df_dec = []

  # Iterate through each day's data and convert it to a DataFrame
  for day_data in days_Jan:
      df = pd.DataFrame([day_data])
      df_jan.append(df)
  for day_data in days_Feb:
      df = pd.DataFrame([day_data])
      df_feb.append(df)
  for day_data in days_Mar:
      df = pd.DataFrame([day_data])
      df_mar.append(df)
  for day_data in days_Apr:
      df = pd.DataFrame([day_data])
      df_apr.append(df)
  for day_data in days_May:
      df = pd.DataFrame([day_data])
      df_may.append(df)
  for day_data in days_Jun:
      df = pd.DataFrame([day_data])
      df_jun.append(df)
  for day_data in days_Jul:
      df = pd.DataFrame([day_data])
      df_jul.append(df)
  for day_data in days_Aug:
      df = pd.DataFrame([day_data])
      df_aug.append(df)
  for day_data in days_Sep:
      df = pd.DataFrame([day_data])
      df_sep.append(df)
  for day_data in days_Oct:
      df = pd.DataFrame([day_data])
      df_oct.append(df)
  for day_data in days_Nov:
      df = pd.DataFrame([day_data])
      df_nov.append(df)
  for day_data in days_Dec:
      df = pd.DataFrame([day_data])
      df_dec.append(df)

  # Concatenate all DataFrames into a single DataFrame
  days_Jan_df = pd.concat(df_jan, ignore_index=True)
  days_Feb_df = pd.concat(df_feb, ignore_index=True)
  days_Mar_df = pd.concat(df_mar, ignore_index=True)
  days_Apr_df = pd.concat(df_apr, ignore_index=True)
  days_May_df = pd.concat(df_may, ignore_index=True)
  days_Jun_df = pd.concat(df_jun, ignore_index=True)
  days_Jul_df = pd.concat(df_jul, ignore_index=True)
  days_Aug_df = pd.concat(df_aug, ignore_index=True)
  days_Sep_df = pd.concat(df_sep, ignore_index=True)
  days_Oct_df = pd.concat(df_oct, ignore_index=True)
  days_Nov_df = pd.concat(df_nov, ignore_index=True)
  days_Dec_df = pd.concat(df_dec, ignore_index=True)

  Jan_Total_Data_df = pd.DataFrame([Jan_Total_Data])
  Feb_Total_Data_df = pd.DataFrame([Feb_Total_Data])
  Mar_Total_Data_df = pd.DataFrame([Mar_Total_Data])
  Apr_Total_Data_df = pd.DataFrame([Apr_Total_Data])
  May_Total_Data_df = pd.DataFrame([May_Total_Data])
  Jun_Total_Data_df = pd.DataFrame([Jun_Total_Data])
  Jul_Total_Data_df = pd.DataFrame([Jul_Total_Data])
  Aug_Total_Data_df = pd.DataFrame([Aug_Total_Data])
  Sep_Total_Data_df = pd.DataFrame([Sep_Total_Data])
  Oct_Total_Data_df = pd.DataFrame([Oct_Total_Data])
  Nov_Total_Data_df = pd.DataFrame([Nov_Total_Data])
  Dec_Total_Data_df = pd.DataFrame([Dec_Total_Data])

  Yearly_df = pd.DataFrame([Yearly])

  # Write each DataFrame to an Excel file
  with pd.ExcelWriter('data.xlsx') as writer:
      days_Jan_df.to_excel(writer, sheet_name='Jan', index=False)
      days_Feb_df.to_excel(writer, sheet_name='Feb', index=False)
      days_Mar_df.to_excel(writer, sheet_name='Mar', index=False)
      days_Apr_df.to_excel(writer, sheet_name='Apr', index=False)
      days_May_df.to_excel(writer, sheet_name='May', index=False)
      days_Jun_df.to_excel(writer, sheet_name='Jun', index=False)
      days_Jul_df.to_excel(writer, sheet_name='Jul', index=False)
      days_Aug_df.to_excel(writer, sheet_name='Aug', index=False)
      days_Sep_df.to_excel(writer, sheet_name='Sep', index=False)
      days_Oct_df.to_excel(writer, sheet_name='Oct', index=False)
      days_Sep_df.to_excel(writer, sheet_name='Nov', index=False)
      days_Nov_df.to_excel(writer, sheet_name='Dec', index=False)

      Jan_Total_Data_df.to_excel(writer, sheet_name='Jan_Total', index=False)
      Feb_Total_Data_df.to_excel(writer, sheet_name='Feb_Total', index=False)
      Mar_Total_Data_df.to_excel(writer, sheet_name='Mar_Total', index=False)
      Apr_Total_Data_df.to_excel(writer, sheet_name='Apr_Total', index=False)
      May_Total_Data_df.to_excel(writer, sheet_name='May_Total', index=False)
      Jun_Total_Data_df.to_excel(writer, sheet_name='Jun_Total', index=False)
      Jul_Total_Data_df.to_excel(writer, sheet_name='Jul_Total', index=False)
      Aug_Total_Data_df.to_excel(writer, sheet_name='Aug_Total', index=False)
      Sep_Total_Data_df.to_excel(writer, sheet_name='Sep_Total', index=False)
      Oct_Total_Data_df.to_excel(writer, sheet_name='Oct_Total', index=False)
      Nov_Total_Data_df.to_excel(writer, sheet_name='Nov_Total', index=False)
      Dec_Total_Data_df.to_excel(writer, sheet_name='Dec_Total', index=False)

      Yearly_df.to_excel(writer, sheet_name='Yearly', index=False)

root.mainloop()
