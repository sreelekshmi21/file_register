import time
import smtplib
from datetime import datetime
import tkinter as tk
from tkinter import Frame, filedialog, ttk, messagebox
import os
import mysql.connector
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'file_app_user',
    'password': 'Hell0W0Rld',
    'database': 'file_register_db'
}

def connect_to_db():
    """Create and return a database connection"""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except mysql.connector.Error as err:
        messagebox.showerror("Database Connection Error", f"Failed to connect to database: {err}")
        return None

def view_register():
    """Open database viewing window"""
    open_treeview_window()

def open_treeview_window():
    """Open a new window with treeview to display database data"""
    new_window = tk.Toplevel()
    new_window.title("File Register Data")
    new_window.geometry("900x600")  
    new_window.configure(bg='lightblue')
    

 


    # Create Treeview in the new window
    tree = ttk.Treeview(new_window, show="headings")
    tree.pack(padx=20, pady=20, fill="both", expand=True)


def delete_from_db(id):
    conn = connect_to_db()
    if not conn:
        status_label.config(text="Error: Could not connect to database")
        return

    try:
       cursor = conn.cursor()
       cursor.execute("DELETE FROM files WHERE id = "+id)
    except mysql.connector.Error as err:
        status_label.config(text=f"Database Error: {err}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()





    def delete():
   # Get selected item to Delete
      selected_item = tree.selection()[0]
      print(selected_item)

      curItem = tree.focus()
      print(tree.item(curItem),tree.item(curItem)["values"],tree.item(curItem)["values"][0])

      delete_from_db(tree.item(curItem)["values"][0])
    #   tree.delete(selected_item)
    #   loc_value = tree.set(a, column="file_id")
    #   print(loc_value)

    
    # Add a scrollbar
    scrollbar = ttk.Scrollbar(new_window, orient="vertical", command=tree.yview)
    scrollbar.pack(side="right", fill="y")
    tree.configure(yscrollcommand=scrollbar.set)
    
    # Status label
    status_label = tk.Label(new_window, text="", padx=20, pady=10, bg='lightblue')
    status_label.pack()

    
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
    
    # Function to refresh treeview data
    def refresh_data():
        # Clear current data
        tree.delete(*tree.get_children())
        # Load data from database
        load_data_from_db(tree, status_label)
    
    # Search frame
    search_frame = tk.Frame(new_window, bg='lightblue')
    search_frame.pack(fill="x", padx=10, pady=5)

    del_btn = tk.Button(new_window, text="Delete", command=delete)
    del_btn.pack(side='right',pady=20,padx=20)
    
    # Search Entry
    search_label = tk.Label(search_frame, text="Search:", bg='lightblue')
    search_label.pack(side=tk.LEFT, padx=5)
    search_entry = ttk.Entry(search_frame, width=30)
    search_entry.pack(side=tk.LEFT, padx=5)
    
    # Search Button
    search_button = ttk.Button(search_frame, text="Search", 
                              command=lambda: search_treeview(search_entry.get()))
    search_button.pack(side=tk.LEFT, padx=5)
    
    # Refresh Button
    refresh_button = ttk.Button(search_frame, text="Refresh", command=refresh_data)
    refresh_button.pack(side=tk.LEFT, padx=20)
    
    # Load the database data into the treeview
    load_data_from_db(tree, status_label)
    
    return new_window

def load_data_from_db(tree, status_label):
    """Load data from database into treeview"""
    conn = connect_to_db()
    if not conn:
        status_label.config(text="Error: Could not connect to database")
        return
        
    try:
        cursor = conn.cursor()
        
        # Get column names
        cursor.execute("SHOW COLUMNS FROM files")
        headers = [column[0] for column in cursor.fetchall()]
        
        # Configure treeview columns
        tree["columns"] = headers
        for col in headers:
            tree.heading(col, text=col.replace('_', ' ').title())
            # Adjust column width based on content
            if col in ('file_name', 'sender', 'receiver', 'despatched_to', 'remarks'):
                tree.column(col, width=150)
            elif col == 'date_added':
                tree.column(col, width=130)
            else:
                tree.column(col, width=80)
        
        # Get data from database
        cursor.execute("SELECT * FROM files ORDER BY date_added DESC")
        rows = cursor.fetchall()
        
        # Insert data into treeview
        for row in rows:
            tree.insert("", "end", values=row)
            
        status_label.config(text=f"Database loaded successfully. {len(rows)} records found.")
        
    except mysql.connector.Error as err:
        status_label.config(text=f"Database Error: {err}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

def send_email(name):
    try: 
        print(f"Sending email about file: {name}")
    except ValueError:
        print('Invalid input')
        messagebox.showerror("Invalid Input", "Please enter a valid name.")
        return
    
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    sender_email = 'ssreelekshmi09@gmail.com'
    receiver_email = ["sreelek24@gmail.com","ganeshsree2010@gmail.com","vsreeprakash@gmail.com"]
    password = 'xskv nmom wbyh eyyg'  # Use an app password, not your main password
    
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

        # Open the treeview window
        open_treeview_window()

    except Exception as e:
        print("Failed to send email:", e)
        messagebox.showerror("Error", f"Failed to send email:\n{e}")
    finally:
        if 'server' in locals():
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
            
        print(f"Adding file: {name} from {sender} to {receiver}")    
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Connect to database
        conn = connect_to_db()
        if not conn:
            return
            
        try:
            cursor = conn.cursor()
            
            # Insert data into database
            query = """
            INSERT INTO files (file_id, file_name, sender, receiver, despatched_to, date_added, remarks)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            values = (fileid, name, sender, receiver, despatch, date, remarks)
            
            cursor.execute(query, values)
            conn.commit()
            
            print("File added successfully to database.")
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
            
        except mysql.connector.Error as err:
            print(f"Database error: {err}")
            messagebox.showerror("Database Error", f"Failed to add file to database:\n{err}")
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()
      
    except ValueError as e:
        print(f'Invalid input: {e}')
        messagebox.showerror("Invalid Input", "Please enter valid input values.")
        return

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

# Database connection status
db_status_label = tk.Label(root, text="", bg='lightblue', fg='green')
db_status_label.pack(pady=5)

# Test database connection on startup
def test_db_connection():
    conn = connect_to_db()
    if conn:
        db_status_label.config(text="✓ Database connected", fg='green')
        conn.close()
    else:
        db_status_label.config(text="✗ Database not connected", fg='red')
    
    # Schedule next check
    root.after(60000, test_db_connection)  # Check every minute

# Submit button
submit_button = tk.Button(root, text="Submit", command=add_file, bg='#4CAF50', fg='white', width=15)
submit_button.pack(pady=20)

# View Register button - opens directly in new window
# view_button = tk.Button(root, text="View Register", command=open_treeview_window, 
#                         bg='#2196F3', fg='white', width=15)
view_button = tk.Button(root, text="View Register", command=open_treeview_window, 
                        bg='blue', fg='white', width=15)
view_button.pack(pady=10)




# Check database connection when application starts
test_db_connection()





# Start the application
root.mainloop()