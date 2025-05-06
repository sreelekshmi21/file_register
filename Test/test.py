import time
import smtplib
import csv
from datetime import datetime
import tkinter as tk
from tkinter import Frame, filedialog, ttk, messagebox
import os

FILENAME = 'file_register.csv'

def view_register():
    with open(FILENAME, 'r') as file:
        reader = csv.reader(file)
        headers = next(reader)
        print("Column names:", headers)
        for row in reader:
            print(row)
    
    # Open with default application (Excel, if associated)
    file_path = 'file_register.csv'
    os.startfile(file_path)  

def open_treeview_window():
    """Open a new window with treeview to display CSV data"""
    new_window = tk.Toplevel()
    new_window.title("File Register Data")
    new_window.geometry("1000x600")  
    new_window.configure(bg='lightblue')
    
    # Create Treeview in the new window
    tree = ttk.Treeview(new_window, show="headings")
    tree.pack(padx=20, pady=20, fill="both", expand=True)
    
    # Add a scrollbar
    scrollbar = ttk.Scrollbar(new_window, orient="vertical", command=tree.yview)
    scrollbar.pack(side="right", fill="y")
    tree.configure(yscrollcommand=scrollbar.set)
    
    # Status label
    status_label = tk.Label(new_window, text="", padx=20, pady=10)
    status_label.pack()
    
    # Function to search in Treeview
    def search_treeview(query):
        items = tree.get_children()
        for item in items:
            if query.lower() in str(tree.item(item)['values']).lower():
                tree.selection_set(item)
                tree.focus(item)
                tree.see(item)  # Ensure the found item is visible
                return
        messagebox.showinfo("Search", f"No results found for '{query}'.")
    
    # Search frame
    search_frame = tk.Frame(new_window, bg='lightblue')
    search_frame.pack(fill="x", padx=10, pady=5)
    
    # Search Entry
    search_label = tk.Label(search_frame, text="Search:", bg='lightblue')
    search_label.pack(side=tk.LEFT, padx=5)
    search_entry = ttk.Entry(search_frame, width=30)
    search_entry.pack(side=tk.LEFT, padx=5)
    
    # Search Button
    search_button = ttk.Button(search_frame, text="Search", 
                              command=lambda: search_treeview(search_entry.get()))
    search_button.pack(side=tk.LEFT, padx=5)
    
    # Load the CSV data into the treeview
    try:
        with open(FILENAME, 'r', newline='') as file:
            csv_reader = csv.reader(file)
            header = next(csv_reader)  # Read the header row
            
            tree["columns"] = header
            for col in header:
                tree.heading(col, text=col)
                tree.column(col, width=100)
            
            for row in csv_reader:
                tree.insert("", "end", values=row)
            
            status_label.config(text=f"CSV file loaded: {FILENAME}")
    
    except Exception as e:
        status_label.config(text=f"Error: {str(e)}")
    
    return new_window

def send_email(name):
    try: 
        print(name)
    except ValueError:
        print('Invalid input')
        messagebox.showerror("Invalid Input", "Please enter a valid number.")
        return
    
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    sender_email = 'ssreelekshmi09@gmail.com'
    receiver_email = ["sreelek24@gmail.com","ganeshsree2010@gmail.com","vsreeprakash@gmail.com"]
    password = 'xskv nmom wbyh eyyg'  # Use an app password, not your main password
    sample_string = ''.join(receiver_email)
    sample_bytes = sample_string.encode()
    
    # Create message
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = ", ".join(receiver_email)
    message['Subject'] = 'File Received'

    # Email body         
    body = name+' updated!'
    message.attach(MIMEText(body, 'plain'))

    # Send email
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Secure the connection
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())
        print("Email sent successfully!")
        messagebox.showinfo("Success", "Email sent successfully!")

        # Instead of view_register(), open the new window with treeview
        open_treeview_window()

    except Exception as e:
        print("Failed to send email:", e)
        messagebox.showerror("Error", f"Failed to send email:\n{e}")
    finally:
        server.quit()

def add_file():
    try: 
        fileid = id_entry.get()
        name = name_entry.get()
        sender = sender_entry.get()
        receiver = receiver_entry.get()
        despatch = despatch_entry.get()
        remarks = remarks_entry.get()
        
        # Validate inputs
        if not all([fileid, name, sender, receiver]):
            messagebox.showerror("Invalid Input", "Please fill in all required fields.")
            return
            
        print(name)
        print(sender)     
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Create the CSV file if it doesn't exist
        file_exists = os.path.isfile(FILENAME)
        
        with open(FILENAME, 'a', newline='') as file:
            writer = csv.writer(file)
            
            # If the file is new, write the header first
            if not file_exists:
                writer.writerow(['File ID', 'File Name', 'Sender', 'Receiver', 'Despatched To', 'Date', 'Remarks'])
                
            writer.writerow([fileid, name, sender, receiver, despatch, date, remarks])
            
        print("File added successfully.")
        print('Sending email...')
        
        # Send email and open treeview window
        send_email(name)
        
        # Clear entries after successful submission
        id_entry.delete(0, tk.END)
        name_entry.delete(0, tk.END)
        sender_entry.delete(0, tk.END)
        receiver_entry.delete(0, tk.END)
        despatch_entry.delete(0, tk.END)
        remarks_entry.delete(0, tk.END)
      
    except ValueError:
        print('Invalid input')
        messagebox.showerror("Invalid Input", "Please enter a valid input.")
        return

def open_csv_file():
    file_path = filedialog.askopenfilename(title="Open CSV File", filetypes=[("CSV files", "*.csv")])
    if file_path:
        # Open new window with treeview to display CSV data
        new_window = tk.Toplevel()
        new_window.title("CSV Data")
        new_window.geometry("800x600")
        
        # Create a treeview in the new window
        tree = ttk.Treeview(new_window, show="headings")
        tree.pack(padx=20, pady=20, fill="both", expand=True)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(new_window, orient="vertical", command=tree.yview)
        scrollbar.pack(side="right", fill="y")
        tree.configure(yscrollcommand=scrollbar.set)
        
        # Status label
        status_label = tk.Label(new_window, text="", padx=20, pady=10)
        status_label.pack()
        
        # Display CSV data
        display_csv_data(file_path, tree, status_label)

def display_csv_data(file_path, tree, status_label):
    try:
        with open(file_path, 'r', newline='') as file:
            csv_reader = csv.reader(file)
            header = next(csv_reader)  # Read the header row
            tree.delete(*tree.get_children())  # Clear the current data

            tree["columns"] = header
            for col in header:
                tree.heading(col, text=col)
                tree.column(col, width=100)

            for row in csv_reader:
                tree.insert("", "end", values=row)

            status_label.config(text=f"CSV file loaded: {file_path}")

    except Exception as e:
        status_label.config(text=f"Error: {str(e)}")

# Main application window
root = tk.Tk()
root.title("File Movement Register")
root.geometry("400x700")  
root.configure(bg='lightblue')

# File ID
id_label = tk.Label(root, text="Enter the File ID:", bg='lightblue')
id_label.pack(pady=10)
id_entry = tk.Entry(root, width=30)
id_entry.pack(pady=5)

# File Name
name_label = tk.Label(root, text="Enter File Name:", bg='lightblue')
name_label.pack(pady=10)
name_entry = tk.Entry(root, width=30)
name_entry.pack(pady=5)

# Sender
sender_label = tk.Label(root, text="Enter From (Sender):", bg='lightblue')
sender_label.pack(pady=10)
sender_entry = tk.Entry(root, width=30)
sender_entry.pack(pady=5)

# Receiver
receiver_label = tk.Label(root, text="Enter To (Receiver):", bg='lightblue')
receiver_label.pack(pady=10)
receiver_entry = tk.Entry(root, width=30)
receiver_entry.pack(pady=5)

# Despatched To
despatch_label = tk.Label(root, text="Despatched To:", bg='lightblue')
despatch_label.pack(pady=10)
despatch_entry = tk.Entry(root, width=30)
despatch_entry.pack(pady=5)

# Remarks
remarks_label = tk.Label(root, text="Enter Remarks:", bg='lightblue')
remarks_label.pack(pady=10)
remarks_entry = tk.Entry(root, width=30)
remarks_entry.pack(pady=5)

# Submit button
submit_button = tk.Button(root, text="Submit", command=add_file, bg='#4CAF50', fg='white', width=15)
submit_button.pack(pady=20)

# View Register button - opens directly in new window
view_button = tk.Button(root, text="View Register", command=open_treeview_window, 
                        bg='#2196F3', fg='white', width=15)
view_button.pack(pady=10)

# Add import for MIMEText and MIMEMultipart that was not included at the beginning
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Start the application
root.mainloop()