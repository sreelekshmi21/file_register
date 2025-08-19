import time
import smtplib
from datetime import datetime
import tkinter as tk
from tkinter import Frame, filedialog, ttk, messagebox, font
import mysql.connector
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
# import app_password
from app_password import *
from tkcalendar import DateEntry
from datetime import date



from tkinter import ttk
import re
import pymysql

import os
from pathlib import Path
from dotenv import load_dotenv
import sys
# import pandas as pd

# Database configuration
# DB_CONFIG = {
#     'host': 'localhost',
#     'user': 'root',
#     'password': '',
#     'database': 'file_register_db'
# load_dotenv()
# }
if getattr(sys, 'frozen', False):
    base_path = Path(sys.executable).parent
else:
    base_path = Path(__file__).parent

# ✅ Load .env from the same directory as the .exe
env_path = base_path / ".env"
load_dotenv(dotenv_path=env_path)

# ✅ Debug print
print("Loaded MYSQL_HOST =", os.getenv("MYSQL_HOST"))

class ResponsiveApp:
     def __init__(self, root):
        self.root = root
        
        self.call_main_window()
        self.create_login_widgets() 
        self.test_db_connection()
        


     def call_main_window(self):
        self.root.title("File Movement Register")
        
        # Make the window fullscreen
        # self.root.state('zoomed')  # For Windows
        if sys.platform.startswith('win'):
             self.root.state('zoomed')
        elif sys.platform.startswith('linux'):    
             self.root.state('normal')  # For linux

         # Get screen dimensions
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # Set default size (will expand to fullscreen)
        self.root.geometry(f"{int(screen_width*0.8)}x{int(screen_height*0.8)}")
        
        # Configure the grid to be responsive
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_columnconfigure(2, weight=1)
        
        # Set background and style
        self.root.configure(bg='#e6f2ff')  # Light blue background
        
        # Create custom fonts
        self.title_font = font.Font(family="Helvetica", size=16, weight="bold")
        self.label_font = font.Font(family="Helvetica", size=12)
        self.button_font = font.Font(family="Helvetica", size=12, weight="bold")
        
        # Configure ttk styles
        self.style = ttk.Style()
        self.style.configure('TEntry', padding=5)
        self.style.configure('TButton', padding=10)


     def create_login_widgets(self):

        title_label = tk.Label(self.root, text="File Movement Register - LOGIN FORM", 
                              font=self.title_font, bg='#e6f2ff', fg='#003366')
        title_label.grid(row=0, column=0, columnspan=3, pady=20)  
        self.input_frame = tk.Frame(self.root, bg='#e6f2ff', padx=20, pady=20,
                                  highlightbackground='#99ccff', highlightthickness=1)
        self.input_frame.grid(row=1, column=0, columnspan=3, sticky="nsew", padx=40, pady=10)
        self.input_frame.grid_columnconfigure(0, weight=1)
        self.input_frame.grid_columnconfigure(1, weight=2)
        row = 0
        username_label = tk.Label(self.input_frame, text="Username", bg='#e6f2ff', 
                           font=self.label_font, anchor="e")
        username_label.grid(row=row, column=0, sticky="e", padx=10, pady=10)
        self.username_entry = ttk.Entry(self.input_frame, width=40, font=self.label_font)
        self.username_entry.grid(row=row, column=1, sticky="w", padx=10, pady=10)
        
        # File Name
        row += 1
        password_label = tk.Label(self.input_frame, text="Password:", bg='#e6f2ff', 
                             font=self.label_font, anchor="e")
        password_label.grid(row=row, column=0, sticky="e", padx=10, pady=10)
        self.password_entry = ttk.Entry(self.input_frame, width=40, font=self.label_font,show="*")
        self.password_entry.grid(row=row, column=1, sticky="w", padx=10, pady=10)
        
        # Create buttons frame
        button_frame = tk.Frame(self.root, bg='#e6f2ff', pady=20)
        button_frame.grid(row=2, column=0, columnspan=3, sticky="ew")
        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(1, weight=1)
        
        # Submit button with improved styling
        self.submit_button = tk.Button(button_frame, text="LOGIN", command=self.login,
                              bg='#4CAF50', fg='white', width=20, height=2,
                              font=self.button_font, relief=tk.RAISED,
                              activebackground='#45a049', cursor="hand2")
        self.submit_button.grid(row=0, column=0, padx=20, pady=20)
        
        # View Register button with improved styling
        self.view_button = tk.Button(button_frame, text="SIGN UP", command=self.signup,
                             bg='#2196F3', fg='white', width=20, height=2,
                             font=self.button_font, relief=tk.RAISED,
                             activebackground='#0b7dda', cursor="hand2")
        self.view_button.grid(row=0, column=1, padx=20, pady=20)


        # Status bar at the bottom
        self.status_frame = tk.Frame(self.root, bg='#003366', height=30)
        self.status_frame.grid(row=3, column=0, columnspan=3, sticky="ew")
        
        self.db_status_label = tk.Label(self.status_frame, text="Database Status: Checking...", 
                                      bg='#003366', fg='white', anchor="w", padx=10)
        self.db_status_label.pack(side=tk.LEFT, fill=tk.X)

     def test_db_connection(self):
        """Test database connection and update status"""
        conn = self.connect_to_db()
        if conn:
            self.db_status_label.config(text="✓ Database connected", fg='#8eff8e')
            conn.close()
        else:
            self.db_status_label.config(text="✗ Database not connected", fg='#ff8e8e')
        
        # Schedule next check
        self.root.after(60000, self.test_db_connection)  # Check every minute
        
     def connect_to_db(self):
        """Create and return a database connection"""
        MYSQL_HOST = os.getenv("MYSQL_HOST")
        MYSQL_USER = os.getenv("MYSQL_USER")
        MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
        MYSQL_DB = os.getenv("MYSQL_DB") 
        
        print(f"API Key: {MYSQL_HOST}")
        print(f"API Key: {MYSQL_USER}")
        print(f"API Key: {MYSQL_PASSWORD}")
        print(f"API Key: {MYSQL_DB}")
        try:
            conn = pymysql.connect(host = MYSQL_HOST,user = MYSQL_USER,password = MYSQL_PASSWORD,database = MYSQL_DB)
            return conn
        except pymysql.Error as err:
            messagebox.showerror("Database Connection Error", f"Failed to connect to database: {err}")
            return None
     


     
     def add_file(self):
        """Add a new file to the database"""
        try: 
            fileid = self.id_entry.get()
            name = self.name_entry.get()
            subject = self.subject_entry.get()
            sender = self.sender_entry.get()
            receiver = self.receiver_entry.get()
            # despatch = self.despatch_entry.get()
            
            inwardnum = self.inwardnum_entry.get()
            outwardnum = self.outwardnum_entry.get()
            current_status = self.current_status_entry.get()
            remarks = self.remarks_entry.get()
            # sender_sel = self.sender_dropdown.get()
            # print(sender_sel)
            # receiver_sel = self.receiver_dropdown.get()
            # print(sender_sel)
            
            # Validate inputs

            selected_date = self.bottom_entries["Despatched Date"].get_date()     # datetime.date
            selected_hour = self.bottom_entries["Despatched Hour"].get()          # string "HH"
            selected_minute = self.bottom_entries["Despatched Minute"].get()      # string "MM"

            # Combine into datetime object
            dt_obj = datetime.combine(selected_date, datetime.strptime(f"{selected_hour}:{selected_minute}", "%H:%M").time())

            # Format as string for storing in DB
            datetime_str = dt_obj.strftime("%Y-%m-%d %H:%M:%S")






            if not all([fileid, name, subject, sender, receiver,current_status]):
                messagebox.showerror("Invalid Input", "Please fill in all required fields.")
                return
            
            # if not sender_sel:
            #    messagebox.showerror("Error", "Please select a sender email")
            #    return
            # if not receiver_sel:
            #    messagebox.showerror("Error", "Please select a receiver email")
            #    return
                
            print(f"Adding file: {name} from {sender} to {receiver}")    
            date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Connect to database
            conn = self.connect_to_db()
            if not conn:
                return
                
            try:
                cursor = conn.cursor()


                query = "SELECT file_id FROM files WHERE file_id = %s"

                cursor.execute(query,(fileid,))

                if cursor.fetchone():
                 messagebox.showerror("File Error", "File already exists!")
                 return
                

                
                
                # Insert data into database 
                query = """
                INSERT INTO files (file_id, file_name, file_subject, sender, receiver, date_added, 
                inwardnum,outwardnum,current_status, remarks,department)
                VALUES (%s, %s, %s, %s, %s, %s, %s,%s, %s,%s, %s)
                """
                values = (fileid, name, subject, sender, receiver, datetime_str, inwardnum,outwardnum, current_status, remarks,
                          self.user_department)
                
                cursor.execute(query, values)  
                conn.commit()
                
                print("File added successfully to database.")
                # messagebox.showinfo("Success", "File added successfully to database.")
                messagebox.showinfo("Info", f"{fileid} received in {receiver} office.")
                self.open_treeview_window()
                # Send email notification
                # self.send_email(name,sender_sel,receiver_sel,inwardnum,outwardnum)
                
                # Clear entries after successful submission
                self.id_entry.delete(0, tk.END)
                self.name_entry.delete(0, tk.END)
                self.subject_entry.delete(0, tk.END)
                self.sender_entry.delete(0, tk.END)
                self.receiver_entry.delete(0, tk.END)
                # self.despatch_entry.delete(0, tk.END)
                
                self.inwardnum_entry.delete(0, tk.END)
                self.outwardnum_entry.delete(0, tk.END)
                self.current_status_entry.delete(0, tk.END)
                self.remarks_entry.delete(0, tk.END)
                
            except mysql.connector.Error as err:
                print(f"Database error: {err}")
                messagebox.showerror("Database Error", f"Failed to add file to database:\n{err}")
            finally:
                # if conn.is_connected():
                    cursor.close()
                    conn.close()
          
        except ValueError as e:
            print(f'Invalid input: {e}')
            messagebox.showerror("Invalid Input", "Please enter valid input values.")
            return

     def open_add_file_window(self):
        print('open_add-file')
        add_file_window = tk.Toplevel(self.root)
        add_file_window.title("Add File Information")

        self.bottom_entries = {}
        
        # Make the window fullscreen
        # add_file_window.state('zoomed')
        if sys.platform.startswith('win'):
              add_file_window.state('zoomed')
        elif sys.platform.startswith('linux'):    
              add_file_window.state('normal')  # For linux




        # Configure the grid
        add_file_window.grid_columnconfigure(0, weight=1)
        add_file_window.grid_rowconfigure(1, weight=1)
        
        add_file_window.configure(bg='#e6f2ff')
        
        # Title frame
        title_frame = tk.Frame(add_file_window, bg='#003366', pady=10)
        title_frame.grid(row=0, column=0, sticky="ew")
        
        title_label = tk.Label(title_frame, text="Add File Information", 
                             font=self.title_font, bg='#003366', fg='white')
        title_label.pack()
         # Main content frame
        content_frame = tk.Frame(add_file_window, bg='#e6f2ff', padx=20, pady=20,
                               highlightbackground='#99ccff', highlightthickness=1)
        content_frame.grid(row=1, column=0, sticky="nsew", padx=40, pady=10)
        content_frame.grid_columnconfigure(0, weight=1)
        content_frame.grid_columnconfigure(1, weight=1)
        
        # Create form fields
        # File ID
        row = 0
        file_id_label = tk.Label(content_frame, text="File ID:", bg='#e6f2ff', 
                               font=self.label_font, anchor="e")
        file_id_label.grid(row=row, column=0, sticky="e", padx=10, pady=10)
        self.id_entry = ttk.Entry(content_frame, width=40, font=self.label_font)
        self.id_entry.grid(row=row, column=1, sticky="w", padx=10, pady=10)
        
        # File Name
        row += 1
        name_label = tk.Label(content_frame, text="File Name:", bg='#e6f2ff', 
                            font=self.label_font, anchor="e")
        name_label.grid(row=row, column=0, sticky="e", padx=10, pady=10)
        self.name_entry = ttk.Entry(content_frame, width=40, font=self.label_font)
        self.name_entry.grid(row=row, column=1, sticky="w", padx=10, pady=10)
        
        row += 1
        subject_label = tk.Label(content_frame, text="File Subject:", bg='#e6f2ff', 
                            font=self.label_font, anchor="e")
        subject_label.grid(row=row, column=0, sticky="e", padx=10, pady=10)
        self.subject_entry = ttk.Entry(content_frame, width=40, font=self.label_font)
        self.subject_entry.grid(row=row, column=1, sticky="w", padx=10, pady=10)

        # Sender
        row += 1
        sender_label = tk.Label(content_frame, text="Originator:", bg='#e6f2ff', 
                              font=self.label_font, anchor="e")
        sender_label.grid(row=row, column=0, sticky="e", padx=10, pady=10)
        self.sender_entry = ttk.Entry(content_frame, width=40, font=self.label_font)
        self.sender_entry.grid(row=row, column=1, sticky="w", padx=10, pady=10)
        
        # Receiver
        # Receiver Entry
        row += 1
        receiver_label = tk.Label(content_frame, text="File Recipient:", bg='#e6f2ff',
                                font=self.label_font, anchor="e")
        receiver_label.grid(row=row, column=0, sticky="e", padx=10, pady=10)

        self.receiver_entry = ttk.Entry(content_frame, width=40, font=self.label_font)
        self.receiver_entry.grid(row=row, column=1, sticky="w", padx=10, pady=10)

        # Despatched To (Date + Time)
        row += 1
        datetime_label = tk.Label(content_frame, text="Date:", bg='#e6f2ff',
                                font=self.label_font, anchor="e")
        datetime_label.grid(row=row, column=0, sticky="e", padx=10, pady=10)

        # --- Date Entry ---
        date_entry = DateEntry(content_frame, width=12, date_pattern='yyyy-mm-dd')
        date_entry.grid(row=row, column=1, sticky="w", padx=(10, 0), pady=10)

        # --- Time Pickers ---
        now = datetime.now()
        hour_var = tk.StringVar(value=now.strftime("%H"))   # Define and set current hour
        minute_var = tk.StringVar(value=now.strftime("%M")) # Define and set current minute

        hours = [f"{h:02d}" for h in range(0, 24)]
        minutes = [f"{m:02d}" for m in range(0, 60)]

        # Hour Combobox
        hour_box = ttk.Combobox(content_frame, textvariable=hour_var, values=hours, width=3)
        hour_box.grid(row=row, column=1, padx=(130, 0), sticky="w")

        # Colon separator
        tk.Label(content_frame, text=":").grid(row=row, column=1, padx=(165, 0), sticky="w")

        # Minute Combobox
        minute_box = ttk.Combobox(content_frame, textvariable=minute_var, values=minutes, width=3)
        minute_box.grid(row=row, column=1, padx=(180, 0), sticky="w")

        # Optional: Store entries in a dictionary
        self.bottom_entries["Despatched Date"] = date_entry
        self.bottom_entries["Despatched Hour"] = hour_var
        self.bottom_entries["Despatched Minute"] = minute_var






      
        row += 1
        inwardnum_label = tk.Label(content_frame, text="Inward Num:", bg='#e6f2ff', 
                            font=self.label_font, anchor="e")
        inwardnum_label.grid(row=row, column=0, sticky="e", padx=10, pady=10)
        self.inwardnum_entry = ttk.Entry(content_frame, width=40, font=self.label_font)
        self.inwardnum_entry.grid(row=row, column=1, sticky="w", padx=10, pady=10)

        row += 1
        outwardnum_label = tk.Label(content_frame, text="Outward Num:", bg='#e6f2ff', 
                            font=self.label_font, anchor="e")
        outwardnum_label.grid(row=row, column=0, sticky="e", padx=10, pady=10)
        self.outwardnum_entry = ttk.Entry(content_frame, width=40, font=self.label_font)
        self.outwardnum_entry.grid(row=row, column=1, sticky="w", padx=10, pady=10)


        row += 1
        current_status = tk.Label(content_frame, text="Live File Location:", bg='#e6f2ff', 
                               font=self.label_font, anchor="e")
        current_status.grid(row=row, column=0, sticky="e", padx=10, pady=10)
        self.current_status_entry = ttk.Entry(content_frame, width=40, font=self.label_font)
        self.current_status_entry.grid(row=row, column=1, sticky="w", padx=10, pady=10)


        row += 1
        remarks_label = tk.Label(content_frame, text="Remarks:", bg='#e6f2ff', 
                               font=self.label_font, anchor="e")
        remarks_label.grid(row=row, column=0, sticky="e", padx=10, pady=10)
        self.remarks_entry = ttk.Entry(content_frame, width=40, font=self.label_font)
        self.remarks_entry.grid(row=row, column=1, sticky="w", padx=10, pady=10)

        # choices = ["ssreelekshmi09@gmail.com","sreelek24@gmail.com","vsreeprakash@gmail.com","ceo@santhigirifoundation.com","Info@santhigirifoundation.com"]

        # choices_one = ["ssreelekshmi09@gmail.com","sreelek24@gmail.com","vsreeprakash@gmail.com","gad@santhigiriashram.org",
        #                "hr@santhigiriashram.org","operations@santhigiriashram.org",
        #                "finance@santhigiriashram.org","comm@santhigiriashram.org","ind@santhigiriashram.org",
        #                "shro@santhigiriashram.org","mkt@santhigiriashram.org","Dept..agri@santhigiriashram.org",
        #                "edu@santhigiriashram.org","culture@santhigiriashram.org","mmd@santhigiriashram.org",
        #                   "energy@santhigiriashram.org","planning@santhigiriashram.org","legal@santhigiriashram.org",
        #                    "assets@santhigiriashram.org","research@santhigiriashram.org","safety@santhigiriashram.org",
        #                     "security@santhigiriashram.org","qc@santhigiriashram.org", "gsadmin@santhigiriashram.org" ]

        # row +=1 
        # title_label = tk.Label(content_frame, text="Select Sender email", bg='#e6f2ff', 
        #                     font=self.label_font, anchor="e")
        # title_label.grid(row=row, column=0, sticky="e", padx=10, pady=10)
        # self.sender_dropdown = ttk.Combobox(content_frame,values=choices)
        # self.sender_dropdown.grid(row=row, column=1, sticky='w', padx=10, pady=10)
    
        # def on_selection_change(event):
        #  sender_selection = self.sender_dropdown.get()
        #  print('SEL1===', sender_selection)
        
        
        # self.sender_dropdown.bind("<<ComboboxSelected>>", on_selection_change) 
        # self.sender_dropdown.set("Choose sender email...")

      
        # # choices_ = ["Option 6", "Option 7", "Option 8", "Option 9", "Option 10"]

        # def on_receiver_selection_change(event):
        #  receiver_selection = self.receiver_dropdown.get()
        #  print('SEL22222222===', receiver_selection) 
        
        

        # row +=1
        # title_label_one = tk.Label(content_frame, text="Select Receiver email", bg='#e6f2ff', 
        #                     font=self.label_font, anchor="e")
        # title_label_one.grid(row=row, column=0, sticky="e", padx=10, pady=10)
        # self.receiver_dropdown = ttk.Combobox(content_frame,values=choices_one)
        # self.receiver_dropdown.grid(row=row, column=1, sticky='w',padx=10, pady=10)
               
        # self.receiver_dropdown.bind("<<ComboboxSelected>>", on_receiver_selection_change)    
        # self.receiver_dropdown.set("Choose receiver email...")
       
        # def search(event):
        #   value = event.widget.get()
        #   if value == '':
        #        self.receiver_dropdown['value'] = choices_one
        #   else:
        #       data = []
        #       for item in choices_one:
        #           if value.lower() in item.lower():
        #              data.append(item)
        #       self.receiver_dropdown['values'] = data

        # self.receiver_dropdown.bind("<KeyRelease>", search)
        
      # Buttons frame
        buttons_frame = tk.Frame(add_file_window, bg='#e6f2ff', pady=20)
        buttons_frame.grid(row=2, column=0, sticky="ew")
        buttons_frame.grid_columnconfigure(0, weight=1)
        buttons_frame.grid_columnconfigure(1, weight=1)
        buttons_frame.grid_columnconfigure(2, weight=1)
        
        # Submit button
        submit_button = tk.Button(buttons_frame, text="SUBMIT", command=self.add_file,
                                bg='#4CAF50', fg='white', width=20, height=2,
                                font=self.button_font, relief=tk.RAISED,
                                activebackground='#45a049', cursor="hand2")
        submit_button.grid(row=0, column=0, padx=20, pady=20)
        
        view_button = tk.Button(buttons_frame, text="VIEW REGISTER", 
                              command=lambda: self.open_treeview_window(add_file_window),
                              bg='#2196F3', fg='white', width=20, height=2,
                              font=self.button_font, relief=tk.RAISED,
                              activebackground='#0b7dda', cursor="hand2")
        view_button.grid(row=0, column=1, padx=20, pady=20)
     #login
        logout_button = tk.Button(buttons_frame, text="LOGOUT", 
                              command=lambda: self.logout_and_close_window(add_file_window),
                              bg='#f44336', fg='white', width=20, height=2,
                              font=self.button_font, relief=tk.RAISED,
                              activebackground='#0b7dda', cursor="hand2")
        logout_button.grid(row=0, column=2, padx=20, pady=20)
     
  
     # Prevent closing the window from X button without proper logout
        add_file_window.protocol("WM_DELETE_WINDOW", lambda: self.logout_and_close_window(add_file_window))
        
        return add_file_window

     
     def logout_and_close_window(self, window):
       result = messagebox.askquestion("Logout", "Are you sure you want to logout?")
       if result == 'yes':
         window.destroy()
         self.logout()
         
         self.username_entry.delete(0, tk.END)
         self.password_entry.delete(0, tk.END)



     def edit_selected_file(self, tree):
        """Edit the selected file"""
        selected = tree.selection()
        
        if not selected:
            messagebox.showinfo("Selection", "Please select a file to edit")
            return
            
        # For simplicity, only edit the last selected item if multiple are selected
        item = selected[0]
        values = tree.item(item, 'values')

        print('VALUES',values,len(values), values[0],values[10])
        
        if not values:
            return
            
        #Create edit dialog
        edit_window = tk.Toplevel(self.root)
        edit_window.title("Edit File Information")
        edit_window.geometry("500x500")
        edit_window.configure(bg='#e6f2ff')

        if sys.platform.startswith('win'):
               edit_window.state('zoomed')
        elif sys.platform.startswith('linux'):    
               edit_window.state('normal')  # For linux

       
        
        # Create form
        form_frame = tk.Frame(edit_window, bg='#e6f2ff')
        form_frame.pack(fill=tk.BOTH, expand=True)

        inner_frame = tk.Frame(form_frame, bg='#e6f2ff')
        inner_frame.pack(anchor='center')
        
                # File ID
        tk.Label(inner_frame, text="File ID:", bg='#e6f2ff', font=self.label_font).grid(row=0, column=0, sticky="e", padx=10, pady=5)
        edit_file_id = ttk.Entry(inner_frame, width=30, font=self.label_font)
        edit_file_id.grid(row=0, column=1, sticky="w", padx=10, pady=5)
        edit_file_id.insert(0, values[1])  # Index 1 = file_id

        # File Name
        tk.Label(inner_frame, text="File Name:", bg='#e6f2ff', font=self.label_font).grid(row=1, column=0, sticky="e", padx=10, pady=5)
        edit_file_name = ttk.Entry(inner_frame, width=30, font=self.label_font)
        edit_file_name.grid(row=1, column=1, sticky="w", padx=10, pady=5)
        edit_file_name.insert(0, values[2])  # Index 2 = file_name

        # File Subject
        tk.Label(inner_frame, text="File Subject:", bg='#e6f2ff', font=self.label_font).grid(row=2, column=0, sticky="e", padx=10, pady=5)
        edit_file_subject = ttk.Entry(inner_frame, width=30, font=self.label_font)
        edit_file_subject.grid(row=2, column=1, sticky="w", padx=10, pady=5)
        edit_file_subject.insert(0, values[3])  # Index 3 = file_subject

        # Sender
        tk.Label(inner_frame, text="Originator:", bg='#e6f2ff', font=self.label_font).grid(row=3, column=0, sticky="e", padx=10, pady=5)
        edit_sender = ttk.Entry(inner_frame, width=30, font=self.label_font)
        edit_sender.grid(row=3, column=1, sticky="w", padx=10, pady=5)
        edit_sender.insert(0, values[4])  # Index 4 = sender

        tk.Label(inner_frame, text="File Recipient:", bg='#e6f2ff', font=self.label_font)\
        .grid(row=4, column=0, sticky="e", padx=10, pady=5)

        edit_receiver = ttk.Entry(inner_frame, width=30, font=self.label_font)
        edit_receiver.grid(row=4, column=1, columnspan=4, sticky="w", padx=10, pady=5)
        edit_receiver.insert(0, values[5])  # Index 5 = receiver

        # --- Date and Time ---
        tk.Label(inner_frame, text="Date & Time:", bg='#e6f2ff', font=self.label_font)\
        .grid(row=5, column=0, sticky="e", padx=10, pady=5)

        datetime_frame = tk.Frame(inner_frame, bg='#e6f2ff')
        datetime_frame.grid(row=5, column=1, columnspan=4, sticky="w", padx=10, pady=5)

        self.date_entry = DateEntry(datetime_frame, width=15, date_pattern='yyyy-mm-dd')
        self.date_entry.pack(side=tk.LEFT)

        self.hour_var = tk.StringVar()
        self.minute_var = tk.StringVar()

        ttk.Combobox(datetime_frame, textvariable=self.hour_var, values=[f"{h:02d}" for h in range(24)], width=3)\
            .pack(side=tk.LEFT, padx=(10, 2))

        tk.Label(datetime_frame, text=":", bg='#e6f2ff', font=self.label_font).pack(side=tk.LEFT)

        ttk.Combobox(datetime_frame, textvariable=self.minute_var, values=[f"{m:02d}" for m in range(60)], width=3)\
            .pack(side=tk.LEFT, padx=(2, 0))

        # --- Set Date and Time from values[6] ---
        dt = datetime.strptime(values[6], "%Y-%m-%d %H:%M:%S")
        self.date_entry.set_date(dt.date())
        self.hour_var.set(dt.strftime("%H"))
        self.minute_var.set(dt.strftime("%M"))

        # --- Inward Number ---
        tk.Label(inner_frame, text="Inward Num:", bg='#e6f2ff', font=self.label_font)\
            .grid(row=6, column=0, sticky="e", padx=10, pady=5)

        edit_inwardnum = ttk.Entry(inner_frame, width=30, font=self.label_font)
        edit_inwardnum.grid(row=6, column=1, columnspan=4, sticky="w", padx=10, pady=5)
        edit_inwardnum.insert(0, values[7])  # Index 7 = inwardnum

        # Outward Number
        tk.Label(inner_frame, text="Outward Num:", bg='#e6f2ff', font=self.label_font).grid(row=7, column=0, sticky="e", padx=10, pady=5)
        edit_outwardnum = ttk.Entry(inner_frame, width=30, font=self.label_font)
        edit_outwardnum.grid(row=7, column=1, sticky="w", padx=10, pady=5)
        edit_outwardnum.insert(0, values[8])  # Index 8 = outwardnum

        # Current Status
        tk.Label(inner_frame, text="Live File Location:", bg='#e6f2ff', font=self.label_font).grid(row=8, column=0, sticky="e", padx=10, pady=5)
        edit_current_status = ttk.Entry(inner_frame, width=30, font=self.label_font)
        edit_current_status.grid(row=8, column=1, sticky="w", padx=10, pady=5)
        edit_current_status.insert(0, values[9])  # Index 9 = current status

        # Remarks
        tk.Label(inner_frame, text="Remarks:", bg='#e6f2ff', font=self.label_font).grid(row=9, column=0, sticky="e", padx=10, pady=5)
        edit_remarks = ttk.Entry(inner_frame, width=30, font=self.label_font)
        edit_remarks.grid(row=9, column=1, sticky="w", padx=10, pady=5)
        edit_remarks.insert(0, values[10])  # Index 10 = remarks


        


        def update_file():
            # Get updated values
            file_id = edit_file_id.get()
            name = edit_file_name.get()
            subject = edit_file_subject.get()
            sender = edit_sender.get()
            receiver = edit_receiver.get()
            inwardnum = edit_inwardnum.get()
            outwardnum = edit_outwardnum.get()            
            current_status = edit_current_status.get()
            remarks = edit_remarks.get()
           
            selected_items = tree.selection()
            id = tree.item(selected_items[0])["values"][0]

            # Validate
            if not all([file_id, name,subject, sender, receiver,current_status]):
                messagebox.showerror("Invalid Input", "Please fill in all required fields.")
                return
                
            # Connect to database
            conn = self.connect_to_db()
            if not conn:
                return
                
            try:
                cursor = conn.cursor()
                date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


                selected_date = self.date_entry.get_date()              # returns a datetime.date
                selected_hour = self.hour_var.get()                     # string like '14'
                selected_minute = self.minute_var.get()                 # string like '45'

                # Step 2: Combine into full datetime
                datetime_str = f"{selected_date} {selected_hour}:{selected_minute}:00"  # '2025-07-17 14:45:00'
                selected_datetime = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")




                # Update data
                query = """
                UPDATE files 
                SET file_id = %s, file_name = %s, file_subject = %s, sender = %s, receiver = %s, 
                    date_added=%s, inwardnum = %s,outwardnum = %s,current_status = %s,remarks = %s
                WHERE id = %s
                """
                values = (file_id, name, subject, sender, receiver, selected_datetime, inwardnum,outwardnum, current_status, remarks,id)  # values[0] contains the ID
                
                cursor.execute(query, values)
                conn.commit()
                
                messagebox.showinfo("Success", "File information updated successfully.")
                
                # Refresh the treeview
                edit_window.destroy()
                # self.refresh_data()
                self.load_data_from_db(tree,edit_window)
                
                # Close the edit window
                # edit_window.destroy()
                
            except mysql.connector.Error as err:
                messagebox.showerror("Database Error", f"Failed to update file: {err}")
            finally:
                # if conn.is_connected():
                    cursor.close()
                    conn.close()
        

        buttons_frame = tk.Frame(edit_window, bg='#e6f2ff', pady=10)
        buttons_frame.pack(side=tk.BOTTOM,fill=tk.X)

        # Inner frame to center buttons and keep them close
        center_button_frame = tk.Frame(buttons_frame, bg='#e6f2ff')
        center_button_frame.pack()
        
        update_button = tk.Button(center_button_frame, text="UPDATE",command=update_file,
                                bg='#4CAF50', fg='white', width=15, height=1,
                                font=self.button_font, relief=tk.RAISED,
                                activebackground='#45a049', cursor="hand2")
        update_button.pack(side=tk.LEFT, padx=10)
        
        cancel_button = tk.Button(center_button_frame, text="CANCEL", command=edit_window.destroy,
                                bg='#f44336', fg='white', width=15, height=1,
                                font=self.button_font, relief=tk.RAISED,
                                activebackground='#d32f2f', cursor="hand2")
        cancel_button.pack(side=tk.LEFT, padx=10)

        # def update_file(self):
        #     print('update file')
            # Get updated values
           
    # Update function


     def login(self):
    
        username = self.username_entry.get()
        password = self.password_entry.get()

          # Validate inputs
        if not all([username, password]):
                messagebox.showerror("Invalid Input", "Please fill in all required fields.")
                return
        # if username=='admin' and password=='123':
        #  print('LOgin success')
        #  messagebox.showinfo("login", "LOGIN success")        
         
        #  self.open_treeview_window()
        # else:
        #     messagebox.showerror("Invalid Input", "Incorrect password/username.")  
        
     
        conn = self.connect_to_db()
        if not conn:
                return
                
        try:
                cursor = conn.cursor()

                # cursor.execute("SELECT * FROM signup WHERE passwd=123456")
                
                query = "SELECT username,passwd, department FROM signup WHERE username = %s AND passwd = %s"
                cursor.execute(query,(username, password))
                result = cursor.fetchone()

                print('RES==================',result)
                # cursor.execute()
                # conn.commit()
                if result:
                 self.user_department = result[2] 
                 messagebox.showinfo("Login", f"Login successful - Department: {self.user_department}")
                 self.root.withdraw()
                 self.open_add_file_window()
                else: 
                   messagebox.showerror("login failed", "login failed")
        except mysql.connector.Error as err:
                print(f"Database error: {err}")
                messagebox.showerror("Database Error", f"Failed to login:\n{err}")
        finally:
                # if conn.is_connected():
                    cursor.close()
                    conn.close()


       #signup
     def signup(self):
        print('sign up')
        new_signup_window = tk.Toplevel(self.root)

        new_signup_window.title("Sign Up Form")
        
        # Make the new window fullscreen as well
        # new_signup_window.state('zoomed')
        if sys.platform.startswith('win'):
              new_signup_window.state('zoomed')
        elif sys.platform.startswith('linux'):    
              new_signup_window.state('normal')  # For linux





        new_signup_window.grid_columnconfigure(0, weight=1)
        new_signup_window.grid_rowconfigure(1, weight=1)  # Give the treeview area most of the space
        
        new_signup_window.configure(bg='#e6f2ff')
        
        # Title frame
        title_frame = tk.Frame(new_signup_window, bg='#003366', pady=10)
        title_frame.grid(row=0, column=0, sticky="ew")
        
        title_label = tk.Label(title_frame, text="SIGN UP FORM", 
                             font=self.title_font, bg='#003366', fg='white')
        title_label.pack()


         # Create main frames
        input_frame_one = tk.Frame(new_signup_window, bg='#e6f2ff', padx=20, pady=20,
                                  highlightbackground='#99ccff', highlightthickness=1)
        input_frame_one.grid(row=1, column=0, columnspan=3, sticky="nsew", padx=40, pady=10)
        input_frame_one.grid_columnconfigure(0, weight=1)
        input_frame_one.grid_columnconfigure(1, weight=2)
        
        username_one = tk.Label(input_frame_one,text="Username", bg='#e6f2ff', font=self.label_font)
        username_one.pack(pady=(10,5))

         
       
        self.username_one_entry = ttk.Entry(input_frame_one, width=40, font=self.label_font)
        self.username_one_entry.pack(pady=(0,10))
        # username_entry.grid(row=row, column=1, sticky="w", padx=10, pady=10)

        password_one = tk.Label(input_frame_one,text="password", bg='#e6f2ff', font=self.label_font)
        password_one.pack(pady=(10, 5))
        self.password_one_entry = ttk.Entry(input_frame_one, width=40, font=self.label_font, show="*")
        self.password_one_entry.pack(pady=(0, 10))

        email_one = tk.Label(input_frame_one,text="email",bg='#e6f2ff', font=self.label_font)
        email_one.pack(pady=(10, 5))
        self.email_one_entry = ttk.Entry(input_frame_one, width=40, font=self.label_font)
        self.email_one_entry.pack(pady=(0, 10))

        department_one = tk.Label(input_frame_one,text="department",bg='#e6f2ff', font=self.label_font)
        department_one.pack(pady=(10, 5))
        self.department_one_entry = ttk.Entry(input_frame_one, width=40, font=self.label_font)
        self.department_one_entry.pack(pady=(0, 10))


        signup_button = tk.Button(input_frame_one, text="SIGN UP", command=self.register,
                             bg='#2196F3', fg='white', width=20, height=2,
                             font=self.button_font, relief=tk.RAISED,
                             activebackground='#0b7dda', cursor="hand2")
        signup_button.pack(pady=10)

        view_button = tk.Button(input_frame_one, text="BACK TO LOGIN", command=new_signup_window.destroy,
                             bg='#2196F3', fg='white', width=20, height=2,
                             font=self.button_font, relief=tk.RAISED,
                             activebackground='#0b7dda', cursor="hand2")
        view_button.pack(pady=10)

     def logout(self):
            self.root.deiconify() #back to login
        

      #register
     def register(self):
        username = self.username_one_entry.get()
        print(username)
        password = self.password_one_entry.get()
        print(password)
        email = self.email_one_entry.get()
        print(email)
        department = self.department_one_entry.get()
        print(department)
       
        if not all([username, password,email,department]):
                messagebox.showerror("Invalid Input", "Please fill in all required fields.")
                return
        
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

        if not (re.match(email_pattern,email)):        
            print('invalif')   
            messagebox.showerror("Invalid email", "Invalid email.")
            return  

            # Connect to database
        conn = self.connect_to_db()
        if not conn:
                return
                
        try:
                cursor = conn.cursor()
                #check if username already exists
                query = "SELECT username FROM signup WHERE username = %s"

                cursor.execute(query,(username,))

                if cursor.fetchone():
                 messagebox.showerror("Registration Error", "Username already exists!")
                 return

                # Insert data into database
                query = """
                INSERT INTO signup (username, passwd, email, department)
                VALUES (%s, %s, %s, %s)
                """
                values = (username, password, email, department)
                
                cursor.execute(query, values)
                conn.commit()

                messagebox.showinfo("signup", "Signed up successfullly")
                
        except mysql.connector.Error as err:
                print(f"Database error: {err}")
                messagebox.showerror("Database Error", f"Failed to register user:\n{err}")
        finally:
                # if conn.is_connected():
                    cursor.close()
                    conn.close()   

       
     def back_to_loginwindow(self):
        print('back to login')
        self.root.withdraw()
        self.open_add_file_window()

       


     def open_treeview_window(self, parent_window=None):
        """Open a new window with treeview to display database data"""
        treeview_window = tk.Toplevel(self.root)
        treeview_window.title("File Register Data")
        
        # Make the new window fullscreen as well
        # treeview_window.state('zoomed')
        if sys.platform.startswith('win'):
              treeview_window.state('zoomed')
        elif sys.platform.startswith('linux'):    
              treeview_window.state('normal')  # For linux

        
        # Configure the grid
        treeview_window.grid_columnconfigure(0, weight=1)
        treeview_window.grid_rowconfigure(1, weight=1)  # Give the treeview area most of the space
        
        treeview_window.configure(bg='#e6f2ff')
        
        # Title frame
        title_frame = tk.Frame(treeview_window, bg='#003366', pady=10)
        title_frame.grid(row=0, column=0, sticky="ew")
        
        title_label = tk.Label(title_frame, text="File Register Data", 
                             font=self.title_font, bg='#003366', fg='white')
        title_label.pack()
        
        # Main content area with Treeview
        content_frame = tk.Frame(treeview_window, bg='#e6f2ff', padx=20, pady=10)
        content_frame.grid(row=1, column=0, sticky="nsew")
        content_frame.grid_columnconfigure(0, weight=1)
        content_frame.grid_rowconfigure(0, weight=1)
        
        # Create Treeview with scrollbars
        tree_frame = tk.Frame(content_frame)
        tree_frame.grid(row=0, column=0, sticky="nsew")
        
        # Create Treeview with multiselect enabled
        tree = ttk.Treeview(tree_frame, selectmode='extended')  # 'extended' allows multiple selection
        
        # Add scrollbars
        vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
        hsb = ttk.Scrollbar(tree_frame, orient="horizontal", command=tree.xview)
        tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        # Grid layout for treeview with scrollbars
        tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")
        
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)
        
        # Create search frame
        search_frame = tk.Frame(content_frame, bg='#e6f2ff', pady=10)
        search_frame.grid(row=1, column=0, sticky="ew")
        
        search_label = tk.Label(search_frame, text="Search:", bg='#e6f2ff', font=self.label_font)
        search_label.pack(side=tk.LEFT, padx=5)
        
        search_entry = ttk.Entry(search_frame, width=30, font=self.label_font)
        search_entry.pack(side=tk.LEFT, padx=5)

            # Selection indicator frame
        selection_frame = tk.Frame(content_frame, bg='#e6f2ff', pady=5)
        selection_frame.grid(row=2, column=0, sticky="ew")
        
        selection_label = tk.Label(selection_frame, text="Selected: 0 records", bg='#e6f2ff', font=self.label_font)
        selection_label.pack(side=tk.LEFT, padx=10)
        
        # Update the selection counter when selection changes
        def on_tree_select(event):
            selected_items = len(tree.selection())
            selection_label.config(text=f"Selected: {selected_items} records")
        
        tree.bind('<<TreeviewSelect>>', on_tree_select)
        
        # Function to search in Treeview
        def search_treeview(query):
            # Clear current selection
            tree.selection_remove(tree.selection())
            
            if not query:
                return
                
            items = tree.get_children()
            found = False
            
            for item in items:
                values = tree.item(item)['values']
                # Convert all values to string and search
                for value in values:
                    if query.lower() in str(value).lower():
                        tree.selection_set(item)
                        tree.focus(item)
                        tree.see(item)  # Ensure the found item is visible
                        found = True
                        break
                if found:
                    break
                    
            if not found:
                messagebox.showinfo("Search", f"No results found for '{query}'.")   
       

        status_frame = tk.Frame(treeview_window, bg='#003366', height=30)
        status_frame.grid(row=2, column=0, sticky="ew")
        
        status_label = tk.Label(status_frame, text="Ready", bg='#003366', fg='white', anchor="w", padx=10)
        status_label.pack(side=tk.LEFT, fill=tk.X)
     

       # Define columns
        tree['columns'] = ('ID', 'file_id', 'file_name', 'file_subject', 'sender', 'receiver', 'date_added', 'inwardnum','outwardnum','current_status', 'remarks')
        
        # Format columns
        tree.column('#0', anchor='center', width=0, stretch=tk.NO)  # Hidden column
        tree.column('ID', width=50, anchor=tk.CENTER)
        tree.column('file_id', width=100, anchor=tk.CENTER)
        tree.column('file_name',width=150, anchor=tk.CENTER)
        tree.column('file_subject', width=100, anchor=tk.CENTER)
        tree.column('sender', width=150, anchor=tk.CENTER)
        tree.column('receiver', width=150, anchor=tk.CENTER)
        # tree.column('despatched_to', width=150, anchor=tk.W)
        tree.column('date_added', width=150, anchor=tk.CENTER)      
        tree.column('inwardnum', width=200, anchor=tk.CENTER)
        tree.column('outwardnum', width=200, anchor=tk.CENTER)
        tree.column('current_status',width=200, anchor=tk.CENTER)
        tree.column('remarks', width=200, anchor=tk.CENTER)
        
        # Create headings
        tree.heading('#0', text='', anchor=tk.CENTER)
        tree.heading('ID', text='ID', anchor=tk.CENTER)
        tree.heading('file_id', text='File ID', anchor=tk.CENTER)
        tree.heading('file_name', text='File Name', anchor=tk.CENTER)
        tree.heading('file_subject', text='File Subject', anchor=tk.CENTER)
        tree.heading('sender', text='Originator', anchor=tk.CENTER)
        tree.heading('receiver', text='File Recipient', anchor=tk.CENTER)
        # tree.heading('despatched_to', text='Despatched To', anchor=tk.CENTER)
        tree.heading('date_added', text='Date', anchor=tk.CENTER)
        tree.heading('inwardnum', text='InwardNum', anchor=tk.CENTER)
        tree.heading('outwardnum', text='OutwardNum', anchor=tk.CENTER)
        tree.heading('current_status', text='Live File Location', anchor=tk.CENTER)
        tree.heading('remarks', text='Remarks', anchor=tk.CENTER)
        
        self.load_data_from_db(tree, status_label)

        def refresh_data():
            # Clear current data
            tree.delete(*tree.get_children())
            # Load data from database
            self.load_data_from_db(tree, status_label)


        search_button = tk.Button(search_frame, text="Search", 
                                command=lambda: search_treeview(search_entry.get()),
                                bg='#2196F3', fg='white', font=self.button_font, padx=10)
        search_button.pack(side=tk.LEFT, padx=10)
        
        refresh_button = tk.Button(search_frame, text="Refresh", command=refresh_data,
                                 bg='#4CAF50', fg='white', font=self.button_font, padx=10)
        refresh_button.pack(side=tk.LEFT, padx=10)
        buttons_frame = tk.Frame(content_frame, bg='#e6f2ff', pady=10)
        buttons_frame.grid(row=4, column=0, sticky="ew")
        buttons_frame.grid_columnconfigure(0, weight=1)
        buttons_frame.grid_columnconfigure(1, weight=1)
        buttons_frame.grid_columnconfigure(2, weight=1) 
        buttons_frame.grid_columnconfigure(3, weight=1) 
        edit_button = tk.Button(buttons_frame, text="EDIT", command=lambda: self.edit_selected_file(tree),
                              bg='#FFA500', fg='white', width=15, height=1,
                              font=self.button_font, relief=tk.RAISED,
                              activebackground='#FF8C00', cursor="hand2")
        edit_button.grid(row=0, column=0, padx=10, pady=10)
        
        # Delete button
        delete_button = tk.Button(buttons_frame, text="DELETE", command=lambda: self.delete_selected_file(tree,self.db_status_label),
                                bg='#f44336', fg='white', width=15, height=1,
                                font=self.button_font, relief=tk.RAISED,
                                activebackground='#d32f2f', cursor="hand2")
        delete_button.grid(row=0, column=1, padx=10, pady=10)


        back_button = tk.Button(buttons_frame, text="back", 
                                # command=self.back_to_loginwindow,
                                command=treeview_window.destroy,
                                bg='#2196F3', fg='white', width=15, height=1,
                                font=self.button_font, relief=tk.RAISED,
                                activebackground='#0b7dda', cursor="hand2")
        back_button.grid(row=0, column=2, padx=10, pady=10)   

        # Export button
        # export_button = tk.Button(buttons_frame, text="EXPORT", command=lambda: self.export_to_csv(tree),
        #                         bg='#4CAF50', fg='white', width=15, height=1,
        #                         font=self.button_font, relief=tk.RAISED,
        #                         activebackground='#45a049', cursor="hand2")
        # export_button.grid(row=0, column=3, padx=10, pady=10)

#         def upload_excel_to_db():
#             file_path = filedialog.askopenfilename(
#                 filetypes=[
#                     ("Excel Files (.xlsx)", "*.xlsx"),
#                     ("Excel 97-2003 Files (.xls)", "*.xls"),
#                     ("All Files", "*.*")
#                 ]
#             )
#             if not file_path:
#                 return

#             try:
#                 df = pd.read_excel(file_path,header=3)
#                 print(df.columns)   
#                 # Drop any columns with missing headers
#                 df = df.loc[:, df.columns.notna()]

#                 # Normalize headers
#                 df.columns = df.columns.str.strip().str.lower()

#                 print("Excel Columns:", df.columns.tolist())

#                 required_columns = [
#                     'file_id', 'file_name', 'file_subject', 'sender', 'receiver',
#                     'date_added', 'inwardnum', 'outwardnum', 'current_status',
#                     'remarks', 'department'
#                 ]

#                 missing = [col for col in required_columns if col not in df.columns]
#                 if missing:
#                     messagebox.showerror("Error", f"Excel file missing required columns: {', '.join(missing)}")
#                     return

#                 # Keep only expected columns (prevents unexpected ones)
#                 df = df[required_columns]

#                 # conn = mysql.connector.connect(
#                 #     host="localhost",
#                 #     user="root",
#                 #     password="",
#                 #     database="file_register_db"
#                 # )
#                 conn = mysql.connector.connect(
#                     host="192.168.7.219",
#                     user="file_app_user",
#                     password="Hello",
#                     database="file_register_db"
#                 )
#                 cursor = conn.cursor()

               

#                 for index, row in df.iterrows():
#                     try:

#                          row = row.where(pd.notnull(row), None)

# # Format the date safely
#                          date_value = pd.to_datetime(row['date_added'], dayfirst=True).strftime('%Y-%m-%d') if row['date_added'] else None
#                          cursor.execute("""
#                             INSERT INTO files (
#                                 file_id, file_name, file_subject, sender, receiver,
#                                 date_added, inwardnum, outwardnum, current_status,
#                                 remarks, department
#                             ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
#                         """, (
#                             row['file_id'],
#                             row['file_name'],
#                             row['file_subject'],
#                             row['sender'],
#                             row['receiver'],
#                             date_value,
#                             row['inwardnum'],
#                             row['outwardnum'],
#                             row['current_status'],
#                             row['remarks'],
#                             row['department']
#                         ))
#                     except Exception as insert_err:
#                         print(f"Error inserting row {index + 2}: {insert_err}")

#                 conn.commit()
#                 cursor.close()
#                 conn.close()

#                 messagebox.showinfo("Success", "Excel data uploaded successfully.")

#             except Exception as e:
#                 print("Unexpected error:", e)
#                 messagebox.showerror("Upload Failed", str(e))


        # upload_btn = tk.Button(buttons_frame, text="Upload Excel to Register", command=upload_excel_to_db)
        # upload_btn.grid(row=0,column=4, padx=10, pady=10)

                










      
     def delete_selected_file(self, tree, status_label):
         """Delete selected file(s) from database"""
         selected = tree.selection()
        
         if not selected:
            messagebox.showinfo("Selection", "Please select file(s) to delete")
            return
            
        # Confirm deletion
         result = messagebox.askquestion("Delete Confirmation", 
                                     f"Are you sure you want to delete {len(selected)} file(s)?")
         if result != 'yes':
            return
            
        # Connect to database
         conn = self.connect_to_db()
         if not conn:
            return
            
         try:
            cursor = conn.cursor()
            
            # Delete each selected item
            for item in selected:
                values = tree.item(item, 'values')
                if values:
                    # Delete by ID
                    query = "DELETE FROM files WHERE id = %s"
                    cursor.execute(query, (values[0],))  # values[0] contains the ID
                    tree.delete(item)
                   

            conn.commit()
            
            messagebox.showinfo("Success", f"{len(selected)} file(s) deleted successfully.")
            
            # Refresh treeview
            self.load_data_from_db(tree, status_label)
            
         except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Failed to delete file(s): {err}")
         finally:
            # if conn.is_connected():
                cursor.close()
                conn.close()

     def load_data_from_db(self, tree, status_label):
        """Load data from database into treeview"""
        # Clear existing data
        for i in tree.get_children():
            tree.delete(i)
            
        # Update status
        if status_label.winfo_exists():
         status_label.config(text="Loading data...")
        
        # Connect to database
        conn = self.connect_to_db()
        if not conn:
            status_label.config(text="Error connecting to database")
            return
            
        try:
            cursor = conn.cursor()
            
            # Get all files
            # query = "SELECT * FROM files ORDER BY date_added DESC"
            # cursor.execute(query)
            # rows = cursor.fetchall()
            print('DEPT=========',self.user_department)

            if self.user_department == 'Santhigiri Foundation':
             query = "SELECT * FROM files ORDER BY date_added DESC"
             cursor.execute(query)
            else:
            #  query = "SELECT * FROM files WHERE department = %s ORDER BY date_added DESC"
            #  cursor.execute(query, (self.user_department,))

               query = "SELECT * FROM files WHERE sender = %s OR receiver = %s OR current_status = %s ORDER BY date_added DESC"
               cursor.execute(query, (self.user_department,self.user_department, self.user_department))

            rows = cursor.fetchall()

            
            # Insert data into treeview
            if not rows:
                values = [""] * len(tree["columns"])
                values[len(values) // 2] = "No records found"
                tree.insert('', 'end', values=values)
                if status_label.winfo_exists():     
                 status_label.config(text="No records found")
            else:
             for i, row in enumerate(rows):
                tree.insert('', 'end', values=row)
             if status_label.winfo_exists():     
                status_label.config(text=f"Loaded {len(rows)} records")
            
        except mysql.connector.Error as err:
            status_label.config(text=f"Database error: {err}")
            messagebox.showerror("Database Error", f"Failed to load data: {err}")
        finally:
            # if conn.is_connected():
                cursor.close()
                conn.close()


     def send_email(self, name,sender_sel,receiver_sel,inwardnum,outwardnum):
        """Send notification email about file update"""
        try: 
            print(f"Sending email about file: {name}")

            print(f"Sending email about file: {sender_sel}")
            

            messagebox.showinfo("Sending Email", f"Sending email about file: {name}")
        except ValueError:
            print('Invalid input')
            messagebox.showerror("Invalid Input", "Please enter a valid name.")
            return
        
       
        smtp_server = 'smtp.gmail.com'
        smtp_port = 587
        # sender_email = 'ssreelekshmi09@gmail.com'
        sender_email = sender_sel
        #  
        # receiver_email = ["sreelek24@gmail.com", "ganeshsree2010@gmail.com", "vsreeprakash@gmail.com"]
        # receiver_email = [receiver_sel]
        receiver_email = receiver_sel


        # password = 'xskv nmom wbyh eyyg'  # Use an app password, not your main password
        
        password = generate_app_password(sender_sel)   

        # Create message
        message = MIMEMultipart()
        message['From'] = sender_email
        # message['To'] = ", ".join(receiver_email)  
        message['To'] = receiver_email             
        #            
        # message['Subject'] = name
        username = receiver_email.split('@')[0]
        if inwardnum != '': 
            message['Subject'] = name+' File Received from '+username
        elif outwardnum != '' :   
            message['Subject'] = name+' File sent to '+username
        # Email body         
        body = name + ' updated!'
        message.attach(MIMEText(body, 'plain'))

        # Send email
        try:
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()  # Secure the connection
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())
            print("Email sent successfully!")
            messagebox.showinfo("Success", "Email sent successfully!")
            
        except Exception as e:
            print("Failed to send email:", e)
            messagebox.showerror("Error", f"Failed to send email:\n{e}")
        finally:
            if 'server' in locals():
                server.quit()
        
     def export_to_csv(self, tree):
        """Export treeview data to CSV file"""
        # Ask user for save location
        file_path = filedialog.asksaveasfilename(
            defaultextension='.csv',
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            title="Save CSV File"
        )
        
        if not file_path:
            return  # User canceled
            
        try:
            with open(file_path, 'w', newline='') as csvfile:
                # Get column headers
                headers = tree['columns']
                
                # Write headers
                csvfile.write(','.join(headers) + '\n')
                
                # Write data rows
                for item in tree.get_children():
                    values = tree.item(item, 'values')
                    # Convert all values to strings
                    row = [str(val) for val in values]
                    csvfile.write(','.join(row) + '\n')
                    
            messagebox.showinfo("Export Successful", f"Data exported to {file_path}")
            
        except Exception as e:
            messagebox.showerror("Export Failed", f"Error exporting data: {e}")    
    
    #  def open_treeview_window(self):
    #     """Open a new window with treeview to display database data"""
    #     new_window = tk.Toplevel(self.root)
    #     new_window.title("File Register Data")
        
    #     # Make the new window fullscreen as well
    #     new_window.state('zoomed')  # For Windows
    #     # For Linux/Mac: new_window.attributes('-zoomed', True)
        
    #     # Get screen dimensions
    #     screen_width = new_window.winfo_screenwidth()
    #     screen_height = new_window.winfo_screenheight()
        
    #     # Configure the grid
    #     new_window.grid_columnconfigure(0, weight=1)
    #     new_window.grid_rowconfigure(1, weight=1)  # Give the treeview area most of the space
        
    #     new_window.configure(bg='#e6f2ff')
        
    #     # Title frame
    #     title_frame = tk.Frame(new_window, bg='#003366', pady=10)
    #     title_frame.grid(row=0, column=0, sticky="ew")
        
    #     title_label = tk.Label(title_frame, text="File Register Data", 
    #                          font=self.title_font, bg='#003366', fg='white')
    #     title_label.pack()
        
    #     # Main content area with Treeview
    #     content_frame = tk.Frame(new_window, bg='#e6f2ff', padx=20, pady=10)
    #     content_frame.grid(row=1, column=0, sticky="nsew")
    #     content_frame.grid_columnconfigure(0, weight=1)
    #     content_frame.grid_rowconfigure(0, weight=1)
        
    #     # Create Treeview with scrollbars
    #     tree_frame = tk.Frame(content_frame)
    #     tree_frame.grid(row=0, column=0, sticky="nsew")
        
    #     # Create Treeview with multiselect enabled
    #     tree = ttk.Treeview(tree_frame, selectmode='extended')  # 'extended' allows multiple selection
        
    #     # Add scrollbars
    #     vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
    #     hsb = ttk.Scrollbar(tree_frame, orient="horizontal", command=tree.xview)
    #     tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
    #     # Grid layout for treeview with scrollbars
    #     tree.grid(row=0, column=0, sticky="nsew")
    #     vsb.grid(row=0, column=1, sticky="ns")
    #     hsb.grid(row=1, column=0, sticky="ew")
        
    #     tree_frame.grid_rowconfigure(0, weight=1)
    #     tree_frame.grid_columnconfigure(0, weight=1)
        
    #     # Create search frame
    #     search_frame = tk.Frame(content_frame, bg='#e6f2ff', pady=10)
    #     search_frame.grid(row=1, column=0, sticky="ew")
        
    #     search_label = tk.Label(search_frame, text="Search:", bg='#e6f2ff', font=self.label_font)
    #     search_label.pack(side=tk.LEFT, padx=5)
        
    #     search_entry = ttk.Entry(search_frame, width=30, font=self.label_font)
    #     search_entry.pack(side=tk.LEFT, padx=5)
        
    #     # Function to search in Treeview
    #     def search_treeview(query):
    #         # Clear current selection
    #         tree.selection_remove(tree.selection())
            
    #         if not query:
    #             return
                
    #         items = tree.get_children()
    #         found = False
            
    #         for item in items:
    #             values = tree.item(item)['values']
    #             # Convert all values to string and search
    #             for value in values:
    #                 if query.lower() in str(value).lower():
    #                     tree.selection_set(item)
    #                     tree.focus(item)
    #                     tree.see(item)  # Ensure the found item is visible
    #                     found = True
    #                     break
    #             if found:
    #                 break
                    
    #         if not found:
    #             messagebox.showinfo("Search", f"No results found for '{query}'.")
        
    #     # Function to refresh treeview data
    #     def refresh_data():
    #         # Clear current data
    #         tree.delete(*tree.get_children())
    #         # Load data from database
    #         self.load_data_from_db(tree, status_label)
        
    #     search_button = tk.Button(search_frame, text="Search", 
    #                             command=lambda: search_treeview(search_entry.get()),
    #                             bg='#2196F3', fg='white', font=self.button_font, padx=10)
    #     search_button.pack(side=tk.LEFT, padx=10)
        
    #     refresh_button = tk.Button(search_frame, text="Refresh", command=refresh_data,
    #                              bg='#4CAF50', fg='white', font=self.button_font, padx=10)
    #     refresh_button.pack(side=tk.LEFT, padx=10)
        
    #     # Selection indicator frame
    #     selection_frame = tk.Frame(content_frame, bg='#e6f2ff', pady=5)
    #     selection_frame.grid(row=2, column=0, sticky="ew")
        
    #     selection_label = tk.Label(selection_frame, text="Selected: 0 records", bg='#e6f2ff', font=self.label_font)
    #     selection_label.pack(side=tk.LEFT, padx=10)
        
    #     # Update the selection counter when selection changes
    #     def on_tree_select(event):
    #         selected_items = len(tree.selection())
    #         selection_label.config(text=f"Selected: {selected_items} records")
        
    #     tree.bind('<<TreeviewSelect>>', on_tree_select)
        
    #     # Action buttons frame
    #     action_frame = tk.Frame(content_frame, bg='#e6f2ff', pady=10)
    #     action_frame.grid(row=3, column=0, sticky="ew")
        
    #     edit_btn = tk.Button(action_frame, text="Select Record to Edit",
    #                       bg='#ff9800', fg='white', font=self.button_font, padx=10)
    #     edit_btn.pack(side=tk.LEFT, padx=10)
        
    #     delete_btn = tk.Button(action_frame, text="Delete Selected Records",
    #                         bg='#f44336', fg='white', font=self.button_font, padx=10)
    #     delete_btn.pack(side=tk.LEFT, padx=10)
        
    #     update_btn = tk.Button(action_frame, text="UPDATE RECORD",
    #                         bg='#4CAF50', fg='white', font=self.button_font, padx=10)
    #     update_btn.pack(side=tk.LEFT, padx=10)
        
    #     back_btn = tk.Button(action_frame, text="BACK TO HOME",
    #                         bg='#4CAF50', fg='white', font=self.button_font, padx=10)  #back btn
    #     back_btn.pack(side=tk.LEFT, padx=10)

    #     add_btn = tk.Button(action_frame, text="ADD FILE",
    #                         bg='#4CAF50', fg='white', font=self.button_font, padx=10)  #add
    #     add_btn.pack(side=tk.LEFT, padx=10)
    #     # Form frame for editing
    #     form_frame = tk.Frame(content_frame, bg='#e6f2ff', padx=10, pady=10)
    #     form_frame.grid(row=4, column=0, sticky="ew")
        
    #     # Create a 3-column layout for the form
    #     form_frame.grid_columnconfigure(0, weight=1)
    #     form_frame.grid_columnconfigure(1, weight=1)
    #     form_frame.grid_columnconfigure(2, weight=1)
        
    #     # File ID
    #     file_id_label = tk.Label(form_frame, text="File ID:", bg='#e6f2ff', font=self.label_font)
    #     file_id_label.grid(row=0, column=0, sticky="e", padx=5, pady=5)
    #     file_id_box = ttk.Entry(form_frame, width=25)
    #     file_id_box.grid(row=0, column=1, sticky="w", padx=5, pady=5)
        
    #     # File Name
    #     name_label = tk.Label(form_frame, text="File Name:", bg='#e6f2ff', font=self.label_font)
    #     name_label.grid(row=1, column=0, sticky="e", padx=5, pady=5)
    #     name_box = ttk.Entry(form_frame, width=25)
    #     name_box.grid(row=1, column=1, sticky="w", padx=5, pady=5)
        
    #     # Sender
    #     sender_label = tk.Label(form_frame, text="Sender:", bg='#e6f2ff', font=self.label_font)
    #     sender_label.grid(row=0, column=2, sticky="e", padx=5, pady=5)
    #     sender_box = ttk.Entry(form_frame, width=25)
    #     sender_box.grid(row=0, column=3, sticky="w", padx=5, pady=5)
        
    #     # Receiver
    #     receiver_label = tk.Label(form_frame, text="Receiver:", bg='#e6f2ff', font=self.label_font)
    #     receiver_label.grid(row=1, column=2, sticky="e", padx=5, pady=5)
    #     receiver_box = ttk.Entry(form_frame, width=25)
    #     receiver_box.grid(row=1, column=3, sticky="w", padx=5, pady=5)
        
    #     # Despatched To
    #     despatched_label = tk.Label(form_frame, text="Despatched To:", bg='#e6f2ff', font=self.label_font)
    #     despatched_label.grid(row=0, column=4, sticky="e", padx=5, pady=5)
    #     despatched_box = ttk.Entry(form_frame, width=25)
    #     despatched_box.grid(row=0, column=5, sticky="w", padx=5, pady=5)
        
    #     # Remarks
    #     remarks_label = tk.Label(form_frame, text="Remarks:", bg='#e6f2ff', font=self.label_font)
    #     remarks_label.grid(row=1, column=4, sticky="e", padx=5, pady=5)
    #     remarks_box = ttk.Entry(form_frame, width=25)
    #     remarks_box.grid(row=1, column=5, sticky="w", padx=5, pady=5)
        
    #     # Status label
    #     status_label = tk.Label(new_window, text="", pady=10, bg='#e6f2ff', font=self.label_font)
    #     status_label.grid(row=2, column=0, sticky="ew")
        
    #     ##########################################
    #     # frame=tk.Frame(root,bg='lightblue')
    #     # frame.place(relx=0.2,rely=0.2,relheight=0.6,relwidth=0.6)
    #     # def page1():
    #     #        label=tk.Label(frame,text='this is the page1')
    #     #        label.place(relx=0.3,rely=0.4)

    #     # bt=tk.Button(root,text='page1',command=page1)
    #     # bt.grid(column=0,row=0)

    #     ########################################
    #     # Define the edit_data function for the edit button
    #     def edit_data():
    #         name_box.delete(0, tk.END)
    #         file_id_box.delete(0, tk.END)
    #         sender_box.delete(0, tk.END)
    #         receiver_box.delete(0, tk.END)
    #         despatched_box.delete(0, tk.END)
    #         remarks_box.delete(0, tk.END)
            
    #         print('edit')
    #         # Check if multiple items are selected
    #         selected_items = tree.selection()
    #         if not selected_items:
    #             print('not selected')
    #             messagebox.showinfo("Edit Data", "Select a record to edit")
    #             # self.deiconify()s
    #             root.withdraw()
    #             return
            
    #         # For editing, only allow one record at a time
    #         if len(selected_items) > 1:
    #             messagebox.showinfo("Edit Data", "Please select only one record to edit")
    #             return
                
    #         selected = selected_items[0]
    #         print('Selected item:', selected)
            
    #         print(tree.item(selected), tree.item(selected)["values"], tree.item(selected)["values"][0])
    #         values = tree.item(selected, 'values')
    #         print(values)
            
    #         file_id_box.insert(0, values[1])
    #         name_box.insert(0, values[2])
    #         sender_box.insert(0, values[3])
    #         receiver_box.insert(0, values[4])
    #         despatched_box.insert(0, values[5])
    #         remarks_box.insert(0, values[7])
        
    #     # Define the update_data function for the update button
    #     def update_data():
    #         selected_items = tree.selection()
            
    #         if not selected_items:
    #             messagebox.showinfo("Update Data", "Select a record to update!")
    #             return
                
    #         # For updating, only allow one record at a time
    #         if len(selected_items) > 1:
    #             messagebox.showinfo("Update Data", "Please select only one record to update")
    #             return
                
    #         selected = selected_items[0]
    #         id = tree.item(selected)["values"][0]
            
    #         tree.item(selected, text='', values=(name_box.get(), file_id_box.get(), 
    #                                           sender_box.get(), receiver_box.get(), 
    #                                           despatched_box.get(), remarks_box.get()))
            
            
            
    #         name = name_box.get()
    #         file_id = file_id_box.get()

    #         print('NAME====',name,file_id,name == '')
    #         sender = sender_box.get()
    #         receiver = receiver_box.get()
    #         despatched = despatched_box.get()
    #         remarks = remarks_box.get()

    #         if file_id == '':
    #             messagebox.showinfo("Warning", "Click the Record to Edit button to proceed!")
    #             return
            
    #         name_box.delete(0, tk.END)
    #         file_id_box.delete(0, tk.END)
    #         sender_box.delete(0, tk.END)
    #         receiver_box.delete(0, tk.END)
    #         despatched_box.delete(0, tk.END)
    #         remarks_box.delete(0, tk.END)
            
    #         date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
    #         update_query = "UPDATE files SET file_id=%s,file_name=%s,sender=%s,receiver=%s,despatched_to=%s,date_added=%s,remarks=%s WHERE id =%s "
    #         data = [file_id, name, sender, receiver, despatched, date, remarks, id]
            
    #         conn = self.connect_to_db()
    #         if not conn:
    #             return
                
    #         try:
    #             cursor = conn.cursor()
    #             cursor.execute(update_query, data)
    #             conn.commit()
                
    #             messagebox.showinfo("Success", "Data updated successfully!")
    #             refresh_data()
                
    #         except mysql.connector.Error as err:
    #             status_label.config(text=f"Database Error: {err}")
    #         finally:
    #             if conn.is_connected():
    #                 cursor.close()
    #                 conn.close()
        
    #     # Define the delete_from_db function for multiple record deletion
    #     def delete_from_db(ids):
    #         if not ids:
    #             return
                
    #         # Connect to database
    #         conn = self.connect_to_db()
    #         if not conn:
    #             return
                
    #         try:
    #             cursor = conn.cursor()
                
    #             # Create placeholder string for SQL IN clause
    #             placeholders = ','.join(['%s'] * len(ids))
    #             delete_query = f"DELETE FROM files WHERE id IN ({placeholders})"
                
    #             cursor.execute(delete_query, ids)
    #             conn.commit()
                
    #             print(f"{len(ids)} files deleted successfully from database.")

    #             messagebox.showinfo("Success", f"{len(ids)} files deleted successfully from database.")
    #             refresh_data()
                
    #             # Update selection label
    #             selection_label.config(text="Selected: 0 records")
                
    #         except mysql.connector.Error as err:
    #             status_label.config(text=f"Database Error: {err}")
    #         finally:
    #             if conn.is_connected():
    #                 cursor.close()
    #                 conn.close()
        
    #     # Define the delete_data function for the delete button (supports multiple selection)
    #     def delete_data():
    #         print('Delete Data')
    #         selected_items = tree.selection()
    #         if not selected_items:
    #             print('not selected')
    #             messagebox.showinfo("Delete Data", "Select records to delete")
    #             return
            
    #         # Get all the IDs of the selected records
    #         ids_to_delete = []
    #         for item in selected_items:
    #             ids_to_delete.append(tree.item(item)["values"][0])
            
    #         result = messagebox.askquestion("Confirmation", f"Are you sure you want to delete {len(ids_to_delete)} selected file(s)?")
    #         if result == 'yes':
    #             # Perform the deletion
    #             delete_from_db(ids_to_delete)
    #             print(f"{len(ids_to_delete)} files deleted.")
    #         else:
    #             print("Deletion canceled.")
    #             return
            
    #     def open_main_page():
    #         print('open main page')
    #         new_window.destroy()  # Close the new window
    #         root.deiconify()  # Show the home window again

    #     def open_add_page(self):
    #        print('open add page')
    #        add_window = tk.Toplevel(self.root)
    #        add_window.title("Add FILE")
    #     #    self.call_main_window()
    #     #    self.create_widgets()
        
    #     # Make the new window fullscreen as well
    #     #    add_window.state('zoomed')  # For Windows
    #     # For Linux/Mac: new_window.attributes('-zoomed', True)


    #     # Connect the functions to the buttons
    #     edit_btn.config(command=edit_data)
    #     update_btn.config(command=update_data)
    #     delete_btn.config(command=delete_data)

    #     back_btn.config(command=open_main_page)

    #     add_btn.config(command=open_add_page(self))
        
    #     # Load data from database
    #     self.load_data_from_db(tree, status_label)
        
    #     return new_window
        
    #  def load_data_from_db(self, tree, status_label):
    #     """Load data from database into treeview"""
    #     conn = self.connect_to_db()
    #     if not conn:
    #         status_label.config(text="Error: Could not connect to database")
    #         return
            
    #     try:
    #         cursor = conn.cursor()
            
    #         # Get column names
    #         cursor.execute("SHOW COLUMNS FROM files")
    #         headers = [column[0] for column in cursor.fetchall()]
            
    #         # Configure treeview columns
    #         tree["columns"] = headers
    #         for col in headers:
    #             tree.heading(col, text=col.replace('_', ' ').title())
    #             # Adjust column width based on content
    #             if col in ('file_name', 'sender', 'receiver', 'despatched_to', 'remarks'):
    #                 tree.column(col, width=150)
    #             elif col == 'date_added':
    #                 tree.column(col, width=130)
    #             else:
    #                 tree.column(col, width=80)
            
    #         # Get data from database
    #         cursor.execute("SELECT * FROM files ORDER BY date_added DESC")
    #         rows = cursor.fetchall()
            
    #         # Insert data into treeview
    #         for row in rows:
    #             tree.insert("", "end", values=row)
                
    #         status_label.config(text=f"Database loaded successfully. {len(rows)} records found.")
            
    #     except mysql.connector.Error as err:
    #         status_label.config(text=f"Database Error: {err}")
    #     finally:
    #         if conn.is_connected():
    #             cursor.close()
    #             conn.close()
   

    #  def create_widgets(self):
    #     """Create all UI elements"""
    #     # Create a title label
    #     title_label = tk.Label(self.root, text="File Movement Register", 
    #                           font=self.title_font, bg='#e6f2ff', fg='#003366')
    #     title_label.grid(row=0, column=0, columnspan=3, pady=20)
        
    #     # Create main frames
    #     self.input_frame = tk.Frame(self.root, bg='#e6f2ff', padx=20, pady=20,
    #                               highlightbackground='#99ccff', highlightthickness=1)
    #     self.input_frame.grid(row=1, column=0, columnspan=3, sticky="nsew", padx=40, pady=10)
    #     self.input_frame.grid_columnconfigure(0, weight=1)
    #     self.input_frame.grid_columnconfigure(1, weight=2)
        
    #     # Create a form using grid for better alignment
    #     # File ID
    #     row = 0
    #     id_label = tk.Label(self.input_frame, text="File ID:", bg='#e6f2ff', 
    #                        font=self.label_font, anchor="e")
    #     id_label.grid(row=row, column=0, sticky="e", padx=10, pady=10)
    #     self.id_entry = ttk.Entry(self.input_frame, width=40, font=self.label_font)
    #     self.id_entry.grid(row=row, column=1, sticky="w", padx=10, pady=10)
        
    #     # File Name
    #     row += 1
    #     name_label = tk.Label(self.input_frame, text="File Name:", bg='#e6f2ff', 
    #                          font=self.label_font, anchor="e")
    #     name_label.grid(row=row, column=0, sticky="e", padx=10, pady=10)
    #     self.name_entry = ttk.Entry(self.input_frame, width=40, font=self.label_font)
    #     self.name_entry.grid(row=row, column=1, sticky="w", padx=10, pady=10)
        
    #     # Sender
    #     row += 1
    #     sender_label = tk.Label(self.input_frame, text="From (Sender):", bg='#e6f2ff', 
    #                            font=self.label_font, anchor="e")
    #     sender_label.grid(row=row, column=0, sticky="e", padx=10, pady=10)
    #     self.sender_entry = ttk.Entry(self.input_frame, width=40, font=self.label_font)
    #     self.sender_entry.grid(row=row, column=1, sticky="w", padx=10, pady=10)
        
    #     # Receiver
    #     row += 1
    #     receiver_label = tk.Label(self.input_frame, text="To (Receiver):", bg='#e6f2ff', 
    #                              font=self.label_font, anchor="e")
    #     receiver_label.grid(row=row, column=0, sticky="e", padx=10, pady=10)
    #     self.receiver_entry = ttk.Entry(self.input_frame, width=40, font=self.label_font)
    #     self.receiver_entry.grid(row=row, column=1, sticky="w", padx=10, pady=10)
        
    #     # Despatched To
    #     row += 1
    #     despatch_label = tk.Label(self.input_frame, text="Despatched To:", bg='#e6f2ff', 
    #                              font=self.label_font, anchor="e")
    #     despatch_label.grid(row=row, column=0, sticky="e", padx=10, pady=10)
    #     self.despatch_entry = ttk.Entry(self.input_frame, width=40, font=self.label_font)
    #     self.despatch_entry.grid(row=row, column=1, sticky="w", padx=10, pady=10)
        
    #     # Remarks
    #     row += 1
    #     remarks_label = tk.Label(self.input_frame, text="Remarks:", bg='#e6f2ff', 
    #                             font=self.label_font, anchor="e")
    #     remarks_label.grid(row=row, column=0, sticky="e", padx=10, pady=10)
    #     self.remarks_entry = ttk.Entry(self.input_frame, width=40, font=self.label_font)
    #     self.remarks_entry.grid(row=row, column=1, sticky="w", padx=10, pady=10)
        
    #     # Create buttons frame
    #     button_frame = tk.Frame(self.root, bg='#e6f2ff', pady=20)
    #     button_frame.grid(row=2, column=0, columnspan=3, sticky="ew")
    #     button_frame.grid_columnconfigure(0, weight=1)
    #     button_frame.grid_columnconfigure(1, weight=1)
        
    #     # Submit button with improved styling
    #     self.submit_button = tk.Button(button_frame, text="Submit", command=self.add_file,
    #                           bg='#4CAF50', fg='white', width=20, height=2,
    #                           font=self.button_font, relief=tk.RAISED,
    #                           activebackground='#45a049', cursor="hand2")
    #     self.submit_button.grid(row=0, column=0, padx=20, pady=20)
        
    #     # View Register button with improved styling
    #     self.view_button = tk.Button(button_frame, text="View Register", command=self.open_treeview_window,
    #                          bg='#2196F3', fg='white', width=20, height=2,
    #                          font=self.button_font, relief=tk.RAISED,
    #                          activebackground='#0b7dda', cursor="hand2")
    #     self.view_button.grid(row=0, column=1, padx=20, pady=20)
        
    #     # Status bar at the bottom
    #     self.status_frame = tk.Frame(self.root, bg='#003366', height=30)
    #     self.status_frame.grid(row=3, column=0, columnspan=3, sticky="ew")
        
    #     self.db_status_label = tk.Label(self.status_frame, text="Database Status: Checking...", 
    #                                   bg='#003366', fg='white', anchor="w", padx=10)
    #     self.db_status_label.pack(side=tk.LEFT, fill=tk.X)
  ######################################################################################
# class CircularProgress(tk.Canvas):
#     def __init__(self, master=None, **kwargs):
#         super().__init__(master, **kwargs)
#         self.width = self.winfo_reqwidth()
#         self.height = self.winfo_reqheight()
#         self.center_x = self.width // 2
#         self.center_y = self.height // 2
#         self.radius = min(self.center_x, self.center_y) - 5
#         self.angle = 0
#         self.speed = 1

#         self.configure(bg="white", highlightthickness=0)
#         self.create_oval(
#             self.center_x - self.radius, self.center_y - self.radius,
#             self.center_x + self.radius, self.center_y + self.radius,
#             outline="gray", width=2
#         )

#         self.arc = self.create_arc(
#             self.center_x - self.radius, self.center_y - self.radius,
#             self.center_x + self.radius, self.center_y + self.radius,
#             start=0, extent=0, outline="blue", width=3, style=tk.ARC
#         )
#         self.after(50, self.update)

#     def update(self):
#         self.angle += self.speed
#         if self.angle > 360:
#             self.angle = 0
#         self.draw_arc()
#         self.after(50, self.update)

#     def draw_arc(self):
#         self.itemconfig(
#             self.arc,
#             extent=self.angle,
#             outline="blue" if self.angle <= 180 else "red"
#         )


# from tkinter import ttk
# import tkinter as tk
# from tkinter.messagebox import showinfo


# # root window
# root = tk.Tk()
# root.geometry('300x120')
# root.title('Progressbar Demo')


# def update_progress_label():
#     return f"Current Progress: {pb['value']}%"


# def progress():
#     if pb['value'] < 100:
#         pb['value'] += 20
#         value_label['text'] = update_progress_label()
#     else:
#         showinfo(message='The progress completed!')


# def stop():
#     pb.stop()
#     value_label['text'] = update_progress_label()


# # progressbar
# pb = ttk.Progressbar(
#     root,
#     orient='horizontal',
#     mode='determinate',
#     length=280
# )
# # place the progressbar
# pb.grid(column=0, row=0, columnspan=2, padx=10, pady=20)

# # label
# value_label = ttk.Label(root, text=update_progress_label())
# value_label.grid(column=0, row=1, columnspan=2)

# # start button
# start_button = ttk.Button(
#     root,
#     text='Progress',
#     command=progress
# )
# start_button.grid(column=0, row=2, padx=10, pady=10, sticky=tk.E)

# stop_button = ttk.Button(
#     root,
#     text='Stop',
#     command=stop
# )
# stop_button.grid(column=1, row=2, padx=10, pady=10, sticky=tk.W)

  ###################################################################33

# Main application execution
if __name__ == "__main__":
    root = tk.Tk()
    app = ResponsiveApp(root)
    root.mainloop()