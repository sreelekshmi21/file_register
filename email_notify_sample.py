import time
import smtplib;
import csv
from datetime import datetime
from tkinter import Frame

from tkinter import filedialog
from tkinter import ttk

FILENAME = 'file_register.csv'
import os

# s = smtplib.SMTP('smtp.gmail.com', 587)
# s.starttls()
# s.login("ssreelekshmi09@gmail.com", "BalaSundari9876@")

# message = "Hello"

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import tkinter as tk
from tkinter import messagebox

def view_register():
    with open(FILENAME, 'r') as file:
        reader = csv.reader(file)
        headers = next(reader)
        print("Column names:", headers)
        for row in reader:
            print(row)
        f = open('file_register.csv')  
        file_path = 'file_register.csv'

        # file_path = 'D:/2024 DOCS/work/file_register'

        # Open with default application (Excel, if associated)
        os.startfile(file_path)  

     

# Email configuration
def send_email(name):

    try: 
       
        # name = name_entry.get()
        print(name)
        # sender = entry_length_two.get()
        # print('file',name)
        # print('name: '+name)
        # print('sender name: '+sender)
      
    except ValueError:
        print('Invalid input')
        messagebox.showerror("Invalid Input", "Please enter a valid number.")
        return
    


    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    sender_email = 'ssreelekshmi09@gmail.com'
    # receiver_email = 'sreelek24@gmail.com'
    # receiver_email = "sreelek24@gmail.com"
    receiver_email = ["sreelek24@gmail.com","ganeshsree2010@gmail.com","vsreeprakash@gmail.com"]
    # bytes(receiver_email)
    password = 'xskv nmom wbyh eyyg'  # Use an app password, not your main password
    sample_string = ''.join(receiver_email)
    sample_bytes = sample_string.encode()

    # sample_list = ['WELCOME, ITSOURCECODERS']
    # sample_string = ''.join(sample_list)
    # sample_bytes = sample_string.encode()
    
    
    # Create message
    message = MIMEMultipart()
    message['From'] = sender_email
    # message['To'] = receiver_email
    message['To'] = ", ".join(receiver_email)


    # message['Subject'] = 'Test Email from Python'
    message['Subject'] = 'File Received'

    # Email body         
    # body = 'Hello, this is a test email sent from Python!'
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

        view_register()


    except Exception as e:
        print("Failed to send email:", e)
        messagebox.showerror("Error", f"Failed to send email:\n{e}")
    finally:
        server.quit()


# while True:
#         # print("\n--- Email sent ---")
#         print("1. send email")
#         print("3. Exit")
#         choice = input("Enter your choice: ")

#         if choice == '1':
#              send_email()
#         elif choice == '3':
#              break    



# from email.message import EmailMessage
# from watchdog.observers import Observer
# from watchdog.events import FileSystemEventHandler
# import os

# # --- Email Sending Function ---
# def send_email_with_attachment(file_path, recipient_email):
#     msg = EmailMessage()
#     msg['Subject'] = 'New File Received in File Movement Register'
#     msg['From'] = 'your_email@example.com'
#     msg['To'] = 'ssreelekshmi09@gmail.com'
#     msg.set_content(f'A new file has been received:\n\n{file_path}')

#     # Attach the file
#     with open(file_path, 'rb') as f:
#         file_data = f.read()
#         file_name = os.path.basename(file_path)
#     msg.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=file_name)

#     # Send the email
#     with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
#         smtp.login('ssreelekshmi09@gmail.com', 'sree123')  # Use App Password if using Gmail
#         smtp.send_message(msg)

#     print(f"Email sent with attachment: {file_name}")

# # --- Watchdog Handler ---
# class FileHandler(FileSystemEventHandler):
#     def on_created(self, event):
#         if not event.is_directory:
#             send_email_with_attachment(event.src_path, 'recipient@example.com')

# # --- Main Logic ---
# if __name__ == "__main__":
#     path_to_watch = '/path/to/file/movement/register'
#     observer = Observer()
#     handler = FileHandler()
#     observer.schedule(handler, path=path_to_watch, recursive=False)
#     observer.start()
#     print(f"Watching for new files in: {path_to_watch}")
#     try:
#         while True:
#             time.sleep(1)
#     except KeyboardInterrupt:
#         observer.stop()
#     observer.join()





def add_file():
    # print('file name'+file_name)
    # date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # with open(FILENAME, 'a', newline='') as file:
    #     writer = csv.writer(file)
    #     writer.writerow([file_id, file_name, sender, receiver, date, remarks])
    # print("File added successfully.")
    # print('Sending email...')
    # send_email(file_name) 
    try: 
        fileid = id_entry.get()
        name = name_entry.get()
        sender = sender_entry.get()
        receiver = receiver_entry.get()
        despatch = despatch_entry.get()
        remarks = remarks_entry.get()
        print(name)
        print(sender)     
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(FILENAME, 'a', newline='') as file:
            writer = csv.writer(file)


            

            writer.writerow([fileid, name, sender, receiver, despatch, date, remarks])
        print("File added successfully.")
        print('Sending email...')
    # send_email(file_name) 

        send_email(name)
        # sender = entry_length_two.get()
        # print('file',name)
        # print('name: '+name)
        # print('sender name: '+sender)
      
    except ValueError:
        print('Invalid input')
        messagebox.showerror("Invalid Input", "Please enter a valid input.")
        return
    


# def open_csv_file():
#     file_path = filedialog.askopenfilename(title="Open CSV File", filetypes=[("CSV files", "*.csv")])
#     if file_path:
#         display_csv_data(file_path)


# def display_csv_data(file_path):
#     try:
#         with open(file_path, 'r', newline='') as file:
#             csv_reader = csv.reader(file)
#             header = next(csv_reader)  # Read the header row
#             tree.delete(*tree.get_children())  # Clear the current data

#             tree["columns"] = header
#             for col in header:
#                 tree.heading(col, text=col)
#                 tree.column(col, width=100)

#             for row in csv_reader:
#                 tree.insert("", "end", values=row)

#             status_label.config(text=f"CSV file loaded: {file_path}")

#     except Exception as e:
#         status_label.config(text=f"Error: {str(e)}")   

root = tk.Tk()
root.title("File Movement Register")
root.geometry("400x700")  
root.configure(bg='lightblue')

label_length = tk.Label(root, text="Enter the File ID:")
label_length.pack(pady=10)
id_entry = tk.Entry(root)
id_entry.pack(pady=5)

name_label = tk.Label(root, text="Enter File Name:")
name_label.pack(pady=10)
name_entry = tk.Entry(root)
name_entry.pack(pady=5)

label_length = tk.Label(root, text="Enter From (Sender):")
label_length.pack(pady=10)
sender_entry = tk.Entry(root)
sender_entry.pack(pady=5)

label_length = tk.Label(root, text="Enter To (Receiver):")
label_length.pack(pady=10)
receiver_entry = tk.Entry(root)
receiver_entry.pack(pady=5)

label_length = tk.Label(root, text="Despatched To:")
label_length.pack(pady=10)
despatch_entry = tk.Entry(root)
despatch_entry.pack(pady=5)

label_length = tk.Label(root, text="Enter Remarks:")
label_length.pack(pady=10)
remarks_entry = tk.Entry(root)
remarks_entry.pack(pady=5)

send_button = tk.Button(root, text="Submit", command=add_file)
send_button.pack(pady=20)

# open_button = tk.Button(root, text="Open CSV File", command=open_csv_file)
# open_button.pack(padx=20, pady=10)

# tree = ttk.Treeview(root, show="headings")
# tree.pack(padx=20, pady=20, fill="both", expand=True)

# status_label = tk.Label(root, text="", padx=20, pady=10)
# status_label.pack()


# def open_new_window():
#     new_window = tk.Toplevel(root)
#     new_window.title("New Window")
#     new_window.geometry("300x200")
#     label = tk.Label(new_window, text="This is a new window!")
#     label.pack(pady=20)

# root = tk.Tk()
# root.title("Main Window")
# root.geometry("400x300")

# open_window_button = tk.Button(root, text="Open New Window", command=open_new_window)
# open_window_button.pack(pady=50)

# root.mainloop()