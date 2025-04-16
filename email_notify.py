import time
import smtplib;

# s = smtplib.SMTP('smtp.gmail.com', 587)
# s.starttls()
# s.login("ssreelekshmi09@gmail.com", "BalaSundari9876@")

# message = "Hello"

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import tkinter as tk
from tkinter import messagebox

# Email configuration
def send_email(file_name):
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
    body = file_name+' updated!'

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