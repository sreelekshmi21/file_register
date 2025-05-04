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

         
       
        self.username_one_entry = ttk.Entry(input_frame_one, width=40, font=self.label_font)
        self.username_one_entry.pack()
        # username_entry.grid(row=row, column=1, sticky="w", padx=10, pady=10)

        password_one = tk.Label(input_frame_one,text="password")
        password_one.pack()
        self.password_one_entry = ttk.Entry(input_frame_one, width=40, font=self.label_font)
        self.password_one_entry.pack()

        email_one = tk.Label(input_frame_one,text="email")
        email_one.pack()
        self.email_one_entry = ttk.Entry(input_frame_one, width=40, font=self.label_font)
        self.email_one_entry.pack()

        department_one = tk.Label(input_frame_one,text="department")
        department_one.pack()
        self.department_one_entry = ttk.Entry(input_frame_one, width=40, font=self.label_font)
        self.department_one_entry.pack()


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
        username = self.username_one_entry.get()
        print(username)
        password = self.password_one_entry.get()
        print(password)
        email = self.email_one_entry.get()
        print(email)
        department = self.department_one_entry.get()
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


     def open_treeview_window(self):
        """Open a new window with treeview to display database data"""
        new_window = tk.Toplevel(self.root)
        new_window.title("File Register Data")
        
        # Make the new window fullscreen as well
        new_window.state('zoomed')  # For Windows
        # For Linux/Mac: new_window.attributes('-zoomed', True)
        
        # Get screen dimensions
        screen_width = new_window.winfo_screenwidth()
        screen_height = new_window.winfo_screenheight()
        
        # Configure the grid
        new_window.grid_columnconfigure(0, weight=1)
        new_window.grid_rowconfigure(1, weight=1)  # Give the treeview area most of the space
        
        new_window.configure(bg='#e6f2ff')
        
        # Title frame
        title_frame = tk.Frame(new_window, bg='#003366', pady=10)
        title_frame.grid(row=0, column=0, sticky="ew")
        
        title_label = tk.Label(title_frame, text="File Register Data", 
                             font=self.title_font, bg='#003366', fg='white')
        title_label.pack()
        
        # Main content area with Treeview
        content_frame = tk.Frame(new_window, bg='#e6f2ff', padx=20, pady=10)
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
            self.load_data_from_db(tree, status_label)
        
        search_button = tk.Button(search_frame, text="Search", 
                                command=lambda: search_treeview(search_entry.get()),
                                bg='#2196F3', fg='white', font=self.button_font, padx=10)
        search_button.pack(side=tk.LEFT, padx=10)
        
        refresh_button = tk.Button(search_frame, text="Refresh", command=refresh_data,
                                 bg='#4CAF50', fg='white', font=self.button_font, padx=10)
        refresh_button.pack(side=tk.LEFT, padx=10)
        
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
        
        # Action buttons frame
        action_frame = tk.Frame(content_frame, bg='#e6f2ff', pady=10)
        action_frame.grid(row=3, column=0, sticky="ew")
        
        edit_btn = tk.Button(action_frame, text="Select Record to Edit",
                          bg='#ff9800', fg='white', font=self.button_font, padx=10)
        edit_btn.pack(side=tk.LEFT, padx=10)
        
        delete_btn = tk.Button(action_frame, text="Delete Selected Records",
                            bg='#f44336', fg='white', font=self.button_font, padx=10)
        delete_btn.pack(side=tk.LEFT, padx=10)
        
        update_btn = tk.Button(action_frame, text="UPDATE RECORD",
                            bg='#4CAF50', fg='white', font=self.button_font, padx=10)
        update_btn.pack(side=tk.LEFT, padx=10)
        
        back_btn = tk.Button(action_frame, text="BACK TO HOME",
                            bg='#4CAF50', fg='white', font=self.button_font, padx=10)  #back btn
        back_btn.pack(side=tk.LEFT, padx=10)

        add_btn = tk.Button(action_frame, text="ADD FILE",
                            bg='#4CAF50', fg='white', font=self.button_font, padx=10)  #add
        add_btn.pack(side=tk.LEFT, padx=10)
        # Form frame for editing
        form_frame = tk.Frame(content_frame, bg='#e6f2ff', padx=10, pady=10)
        form_frame.grid(row=4, column=0, sticky="ew")
        
        # Create a 3-column layout for the form
        form_frame.grid_columnconfigure(0, weight=1)
        form_frame.grid_columnconfigure(1, weight=1)
        form_frame.grid_columnconfigure(2, weight=1)
        
        # File ID
        file_id_label = tk.Label(form_frame, text="File ID:", bg='#e6f2ff', font=self.label_font)
        file_id_label.grid(row=0, column=0, sticky="e", padx=5, pady=5)
        file_id_box = ttk.Entry(form_frame, width=25)
        file_id_box.grid(row=0, column=1, sticky="w", padx=5, pady=5)
        
        # File Name
        name_label = tk.Label(form_frame, text="File Name:", bg='#e6f2ff', font=self.label_font)
        name_label.grid(row=1, column=0, sticky="e", padx=5, pady=5)
        name_box = ttk.Entry(form_frame, width=25)
        name_box.grid(row=1, column=1, sticky="w", padx=5, pady=5)
        
        # Sender
        sender_label = tk.Label(form_frame, text="Sender:", bg='#e6f2ff', font=self.label_font)
        sender_label.grid(row=0, column=2, sticky="e", padx=5, pady=5)
        sender_box = ttk.Entry(form_frame, width=25)
        sender_box.grid(row=0, column=3, sticky="w", padx=5, pady=5)
        
        # Receiver
        receiver_label = tk.Label(form_frame, text="Receiver:", bg='#e6f2ff', font=self.label_font)
        receiver_label.grid(row=1, column=2, sticky="e", padx=5, pady=5)
        receiver_box = ttk.Entry(form_frame, width=25)
        receiver_box.grid(row=1, column=3, sticky="w", padx=5, pady=5)
        
        # Despatched To
        despatched_label = tk.Label(form_frame, text="Despatched To:", bg='#e6f2ff', font=self.label_font)
        despatched_label.grid(row=0, column=4, sticky="e", padx=5, pady=5)
        despatched_box = ttk.Entry(form_frame, width=25)
        despatched_box.grid(row=0, column=5, sticky="w", padx=5, pady=5)
        
        # Remarks
        remarks_label = tk.Label(form_frame, text="Remarks:", bg='#e6f2ff', font=self.label_font)
        remarks_label.grid(row=1, column=4, sticky="e", padx=5, pady=5)
        remarks_box = ttk.Entry(form_frame, width=25)
        remarks_box.grid(row=1, column=5, sticky="w", padx=5, pady=5)
        
        # Status label
        status_label = tk.Label(new_window, text="", pady=10, bg='#e6f2ff', font=self.label_font)
        status_label.grid(row=2, column=0, sticky="ew")
        
        ##########################################
        # frame=tk.Frame(root,bg='lightblue')
        # frame.place(relx=0.2,rely=0.2,relheight=0.6,relwidth=0.6)
        # def page1():
        #        label=tk.Label(frame,text='this is the page1')
        #        label.place(relx=0.3,rely=0.4)

        # bt=tk.Button(root,text='page1',command=page1)
        # bt.grid(column=0,row=0)

        ########################################
        # Define the edit_data function for the edit button
        def edit_data():
            name_box.delete(0, tk.END)
            file_id_box.delete(0, tk.END)
            sender_box.delete(0, tk.END)
            receiver_box.delete(0, tk.END)
            despatched_box.delete(0, tk.END)
            remarks_box.delete(0, tk.END)
            
            print('edit')
            # Check if multiple items are selected
            selected_items = tree.selection()
            if not selected_items:
                print('not selected')
                messagebox.showinfo("Edit Data", "Select a record to edit")
                # self.deiconify()s
                root.withdraw()
                return
            
            # For editing, only allow one record at a time
            if len(selected_items) > 1:
                messagebox.showinfo("Edit Data", "Please select only one record to edit")
                return
                
            selected = selected_items[0]
            print('Selected item:', selected)
            
            print(tree.item(selected), tree.item(selected)["values"], tree.item(selected)["values"][0])
            values = tree.item(selected, 'values')
            print(values)
            
            file_id_box.insert(0, values[1])
            name_box.insert(0, values[2])
            sender_box.insert(0, values[3])
            receiver_box.insert(0, values[4])
            despatched_box.insert(0, values[5])
            remarks_box.insert(0, values[7])
        
        # Define the update_data function for the update button
        def update_data():
            selected_items = tree.selection()
            
            if not selected_items:
                messagebox.showinfo("Update Data", "Select a record to update!")
                return
                
            # For updating, only allow one record at a time
            if len(selected_items) > 1:
                messagebox.showinfo("Update Data", "Please select only one record to update")
                return
                
            selected = selected_items[0]
            id = tree.item(selected)["values"][0]
            
            tree.item(selected, text='', values=(name_box.get(), file_id_box.get(), 
                                              sender_box.get(), receiver_box.get(), 
                                              despatched_box.get(), remarks_box.get()))
            
            
            
            name = name_box.get()
            file_id = file_id_box.get()

            print('NAME====',name,file_id,name == '')
            sender = sender_box.get()
            receiver = receiver_box.get()
            despatched = despatched_box.get()
            remarks = remarks_box.get()

            if file_id == '':
                messagebox.showinfo("Warning", "Click the Record to Edit button to proceed!")
                return
            
            name_box.delete(0, tk.END)
            file_id_box.delete(0, tk.END)
            sender_box.delete(0, tk.END)
            receiver_box.delete(0, tk.END)
            despatched_box.delete(0, tk.END)
            remarks_box.delete(0, tk.END)
            
            date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            update_query = "UPDATE files SET file_id=%s,file_name=%s,sender=%s,receiver=%s,despatched_to=%s,date_added=%s,remarks=%s WHERE id =%s "
            data = [file_id, name, sender, receiver, despatched, date, remarks, id]
            
            conn = self.connect_to_db()
            if not conn:
                return
                
            try:
                cursor = conn.cursor()
                cursor.execute(update_query, data)
                conn.commit()
                
                messagebox.showinfo("Success", "Data updated successfully!")
                refresh_data()
                
            except mysql.connector.Error as err:
                status_label.config(text=f"Database Error: {err}")
            finally:
                if conn.is_connected():
                    cursor.close()
                    conn.close()
        
        # Define the delete_from_db function for multiple record deletion
        def delete_from_db(ids):
            if not ids:
                return
                
            # Connect to database
            conn = self.connect_to_db()
            if not conn:
                return
                
            try:
                cursor = conn.cursor()
                
                # Create placeholder string for SQL IN clause
                placeholders = ','.join(['%s'] * len(ids))
                delete_query = f"DELETE FROM files WHERE id IN ({placeholders})"
                
                cursor.execute(delete_query, ids)
                conn.commit()
                
                print(f"{len(ids)} files deleted successfully from database.")

                messagebox.showinfo("Success", f"{len(ids)} files deleted successfully from database.")
                refresh_data()
                
                # Update selection label
                selection_label.config(text="Selected: 0 records")
                
            except mysql.connector.Error as err:
                status_label.config(text=f"Database Error: {err}")
            finally:
                if conn.is_connected():
                    cursor.close()
                    conn.close()
        
        # Define the delete_data function for the delete button (supports multiple selection)
        def delete_data():
            print('Delete Data')
            selected_items = tree.selection()
            if not selected_items:
                print('not selected')
                messagebox.showinfo("Delete Data", "Select records to delete")
                return
            
            # Get all the IDs of the selected records
            ids_to_delete = []
            for item in selected_items:
                ids_to_delete.append(tree.item(item)["values"][0])
            
            result = messagebox.askquestion("Confirmation", f"Are you sure you want to delete {len(ids_to_delete)} selected file(s)?")
            if result == 'yes':
                # Perform the deletion
                delete_from_db(ids_to_delete)
                print(f"{len(ids_to_delete)} files deleted.")
            else:
                print("Deletion canceled.")
                return
            
        def open_main_page():
            print('open main page')
            new_window.destroy()  # Close the new window
            root.deiconify()  # Show the home window again

        def open_add_page(self):
           print('open add page')
           add_window = tk.Toplevel(self.root)
           add_window.title("Add FILE")
        #    self.call_main_window()
        #    self.create_widgets()
        
        # Make the new window fullscreen as well
        #    add_window.state('zoomed')  # For Windows
        # For Linux/Mac: new_window.attributes('-zoomed', True)


        # Connect the functions to the buttons
        edit_btn.config(command=edit_data)
        update_btn.config(command=update_data)
        delete_btn.config(command=delete_data)

        back_btn.config(command=open_main_page)

        add_btn.config(command=open_add_page(self))
        
        # Load data from database
        self.load_data_from_db(tree, status_label)
        
        return new_window
        
     def load_data_from_db(self, tree, status_label):
        """Load data from database into treeview"""
        conn = self.connect_to_db()
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
   

     def create_widgets(self):
        """Create all UI elements"""
        # Create a title label
        title_label = tk.Label(self.root, text="File Movement Register", 
                              font=self.title_font, bg='#e6f2ff', fg='#003366')
        title_label.grid(row=0, column=0, columnspan=3, pady=20)
        
        # Create main frames
        self.input_frame = tk.Frame(self.root, bg='#e6f2ff', padx=20, pady=20,
                                  highlightbackground='#99ccff', highlightthickness=1)
        self.input_frame.grid(row=1, column=0, columnspan=3, sticky="nsew", padx=40, pady=10)
        self.input_frame.grid_columnconfigure(0, weight=1)
        self.input_frame.grid_columnconfigure(1, weight=2)
        
        # Create a form using grid for better alignment
        # File ID
        row = 0
        id_label = tk.Label(self.input_frame, text="File ID:", bg='#e6f2ff', 
                           font=self.label_font, anchor="e")
        id_label.grid(row=row, column=0, sticky="e", padx=10, pady=10)
        self.id_entry = ttk.Entry(self.input_frame, width=40, font=self.label_font)
        self.id_entry.grid(row=row, column=1, sticky="w", padx=10, pady=10)
        
        # File Name
        row += 1
        name_label = tk.Label(self.input_frame, text="File Name:", bg='#e6f2ff', 
                             font=self.label_font, anchor="e")
        name_label.grid(row=row, column=0, sticky="e", padx=10, pady=10)
        self.name_entry = ttk.Entry(self.input_frame, width=40, font=self.label_font)
        self.name_entry.grid(row=row, column=1, sticky="w", padx=10, pady=10)
        
        # Sender
        row += 1
        sender_label = tk.Label(self.input_frame, text="From (Sender):", bg='#e6f2ff', 
                               font=self.label_font, anchor="e")
        sender_label.grid(row=row, column=0, sticky="e", padx=10, pady=10)
        self.sender_entry = ttk.Entry(self.input_frame, width=40, font=self.label_font)
        self.sender_entry.grid(row=row, column=1, sticky="w", padx=10, pady=10)
        
        # Receiver
        row += 1
        receiver_label = tk.Label(self.input_frame, text="To (Receiver):", bg='#e6f2ff', 
                                 font=self.label_font, anchor="e")
        receiver_label.grid(row=row, column=0, sticky="e", padx=10, pady=10)
        self.receiver_entry = ttk.Entry(self.input_frame, width=40, font=self.label_font)
        self.receiver_entry.grid(row=row, column=1, sticky="w", padx=10, pady=10)
        
        # Despatched To
        row += 1
        despatch_label = tk.Label(self.input_frame, text="Despatched To:", bg='#e6f2ff', 
                                 font=self.label_font, anchor="e")
        despatch_label.grid(row=row, column=0, sticky="e", padx=10, pady=10)
        self.despatch_entry = ttk.Entry(self.input_frame, width=40, font=self.label_font)
        self.despatch_entry.grid(row=row, column=1, sticky="w", padx=10, pady=10)
        
        # Remarks
        row += 1
        remarks_label = tk.Label(self.input_frame, text="Remarks:", bg='#e6f2ff', 
                                font=self.label_font, anchor="e")
        remarks_label.grid(row=row, column=0, sticky="e", padx=10, pady=10)
        self.remarks_entry = ttk.Entry(self.input_frame, width=40, font=self.label_font)
        self.remarks_entry.grid(row=row, column=1, sticky="w", padx=10, pady=10)
        
        # Create buttons frame
        button_frame = tk.Frame(self.root, bg='#e6f2ff', pady=20)
        button_frame.grid(row=2, column=0, columnspan=3, sticky="ew")
        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(1, weight=1)
        
        # Submit button with improved styling
        self.submit_button = tk.Button(button_frame, text="Submit", command=self.add_file,
                              bg='#4CAF50', fg='white', width=20, height=2,
                              font=self.button_font, relief=tk.RAISED,
                              activebackground='#45a049', cursor="hand2")
        self.submit_button.grid(row=0, column=0, padx=20, pady=20)
        
        # View Register button with improved styling
        self.view_button = tk.Button(button_frame, text="View Register", command=self.open_treeview_window,
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









# # Function to validate the login
# def validate_login():
#     userid = username_entry.get()
#     password = password_entry.get()

#     # You can add your own validation logic here
#     if userid == "admin" and password == "password":
#         messagebox.showinfo("Login Successful", "Welcome, Admin!")
#     else:
#         messagebox.showerror("Login Failed", "Invalid username or password")


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


# root.mainloop()

  ###################################################################33










# Main application execution
if __name__ == "__main__":
    root = tk.Tk()
    app = ResponsiveApp(root)
    root.mainloop()