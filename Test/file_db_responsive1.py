import time
import smtplib
from datetime import datetime
import tkinter as tk
from tkinter import Frame, filedialog, ttk, messagebox, font
import mysql.connector
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from tkinter import ttk


# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'file_app_user',
    'password': 'Hell0W0Rld',
    'database': 'file_register_db'
}

class ResponsiveApp:
     def __init__(self, root):
        self.root = root
        
        self.call_main_window()
        self.create_login_widgets() 
        self.test_db_connection()
        


     def call_main_window(self):
        self.root.title("File Movement Register")
        
        # Make the window fullscreen
        self.root.state('zoomed')  # For Windows
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
        self.password_entry = ttk.Entry(self.input_frame, width=40, font=self.label_font)
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
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            return conn
        except mysql.connector.Error as err:
            messagebox.showerror("Database Connection Error", f"Failed to connect to database: {err}")
            return None
     

     #login
     
  
     def login(self):
    
        username = self.username_entry.get()
        password = self.password_entry.get()

          # Validate inputs
        if not all([username, password]):
                messagebox.showerror("Invalid Input", "Please fill in all rrrrrequired fields.")
                return
        if username=='admin' and password=='123':
         print('LOgin success')
         messagebox.showinfo("login", "LOGIN success")

         self.open_treeview_window()
        else:
            messagebox.showerror("Invalid Input", "Incorrect password/username.")  


       #signup
     def signup(self):
        print('sign up')
        new_signup_window = tk.Toplevel(self.root)

        new_signup_window.title("Sign Up Form")
        
        # Make the new window fullscreen as well
        new_signup_window.state('zoomed')

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
        
        username_one = tk.Label(input_frame_one,text="Username")
        username_one.pack()

         
       
        self.username_entry = ttk.Entry(input_frame_one, width=40, font=self.label_font)
        self.username_entry.pack()
        # username_entry.grid(row=row, column=1, sticky="w", padx=10, pady=10)

        password_one = tk.Label(input_frame_one,text="password")
        password_one.pack()
        self.password_entry = ttk.Entry(input_frame_one, width=40, font=self.label_font)
        self.password_entry.pack()

        email_one = tk.Label(input_frame_one,text="email")
        email_one.pack()
        self.email_entry = ttk.Entry(input_frame_one, width=40, font=self.label_font)
        self.email_entry.pack()

        department_one = tk.Label(input_frame_one,text="department")
        department_one.pack()
        self.department_entry = ttk.Entry(input_frame_one, width=40, font=self.label_font)
        self.department_entry.pack()


        view_button = tk.Button(input_frame_one, text="SIGN UP", command=self.register,
                             bg='#2196F3', fg='white', width=20, height=2,
                             font=self.button_font, relief=tk.RAISED,
                             activebackground='#0b7dda', cursor="hand2")
        view_button.pack()


        back_to_login = tk.Button(input_frame_one, text="BACK TO LOGIN", command=self.back_to_login,
                             bg='#2196E3', fg='white', width=20, height=2,
                             font=self.button_font, relief=tk.RAISED,
                             activebackground='#0b7dda', cursor="hand2")
        back_to_login.pack()  


      #register
     def register(self):
        print("register")
        username = self.username_entry.get()
        print(username)
        password = self.password_entry.get()
        print(password)
        email = self.email_entry.get()
        print(email)
        department = self.department_entry.get()
        print(department)
       
        if not all([username, password,email,department]):
                messagebox.showerror("Invalid Input", "Please fill in all required fieldddddddddds.")
                return
        
            # Connect to database
        conn = self.connect_to_db()
        if not conn:
                return
                
        try:
                cursor = conn.cursor()
                
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
                messagebox.showerror("Database Error", f"Failed to add file to database:\n{err}")
        finally:
                if conn.is_connected():
                    cursor.close()
                    conn.close()   

       
     def back_to_login(self):
        print('back to login')
        self.login()             
# Main application execution
if __name__ == "__main__":
    root = tk.Tk()
    app = ResponsiveApp(root)
    root.mainloop()