import tkinter as tk
from tkinter import messagebox
import mysql.connector as mys

# Placeholder functions so the code doesn't crash when called
def teacher_home():
    messagebox.showinfo("Success", "Welcome Teacher!")

def student_home():
    messagebox.showinfo("Success", "Welcome Student!")

def firstpage():
    root = tk.Tk()
    root.title("Main Menu")
    root.geometry("400x300")
    
    # Using lambda(custom function) to close the current window before opening the next
    login_button = tk.Button(root, text="Login", command=lambda: [root.destroy(), login()], bg="#4CAF50", fg="red", width=15)
    login_button.pack(pady=15)
    
    signup_button = tk.Button(root, text="Signup", command=lambda: [root.destroy(), signup()], bg="#4CAF50", fg="red", width=15)
    signup_button.pack(pady=15)
    
    root.mainloop()

def login():
    root = tk.Tk()
    root.title("User Login")
    root.geometry("400x300")
    
    tk.Label(root, text="User Login", font=("Arial", 14, "bold")).pack(pady=10)
    form_frame = tk.Frame(root)
    form_frame.pack(pady=10)

    tk.Label(form_frame, text="Username:").grid(row=0, column=0, sticky="e", pady=5)
    username_entry = tk.Entry(form_frame, width=30)
    username_entry.grid(row=0, column=1, pady=5)

    tk.Label(form_frame, text="Password:").grid(row=1, column=0, sticky="e", pady=5)
    password_entry = tk.Entry(form_frame, width=30, show="*")
    password_entry.grid(row=1, column=1, pady=5)

    tk.Label(form_frame, text="Role:").grid(row=2, column=0, sticky="e", pady=5)
    role_var = tk.StringVar(value="STUDENT")
    role_menu = tk.OptionMenu(form_frame, role_var, "STUDENT", "TEACHER")
    role_menu.grid(row=2, column=1, sticky="w", pady=5)

    # Pass the specific string values to the check_data function
    submit_btn = tk.Button(root, text="Login", 
                           command=lambda: check_data(username_entry.get(), password_entry.get(), role_var.get()), 
                           bg="#4CAF50", fg="white")
    submit_btn.pack(pady=15)
    root.mainloop()

def check_data(username, password, role):
    username = username.strip()
    
    if not username or not password:
        messagebox.showwarning("Missing Data", "Please fill out all fields.")
        return

    con = None
    cur = None
    try:
        con = mys.connect(host='localhost', user='root', passwd='root', autocommit=True, database="project1") 
        cur = con.cursor()
        
        # Fixed syntax and used parameterized query (%s) for safety
        q = "SELECT username, password, role FROM users WHERE username = %s"
        cur.execute(q, (username,))
        result = cur.fetchone() # Fetchone is better when expecting a single user
        
        if result:
            db_username, db_password, db_role = result
            if db_password == password and db_role == role:
                print("Valid login")
                if role == "TEACHER":
                    teacher_home()
                elif role == "STUDENT":
                    student_home()
            else:
                messagebox.showerror("Error", "Invalid password or role.")
        else:
            messagebox.showerror("Error", "User not found.")
            
    except Exception as e:
        messagebox.showerror("Database Error", f"Failed to fetch data: {e}")
    finally:
        # Fixed the variable names in the cleanup block
        if cur:
            cur.close()
        if con and con.is_connected():
            con.close()

def signup():
    root = tk.Tk()
    root.title("User Registration")
    root.geometry("400x300")

    tk.Label(root, text="User Registration Form", font=("Arial", 14, "bold")).pack(pady=10)
    form_frame = tk.Frame(root)
    form_frame.pack(pady=10)

    tk.Label(form_frame, text="Name:").grid(row=0, column=0, sticky="e", pady=5)
    name_entry = tk.Entry(form_frame, width=30)
    name_entry.grid(row=0, column=1, pady=5)

    tk.Label(form_frame, text="Username:").grid(row=1, column=0, sticky="e", pady=5)
    username_entry = tk.Entry(form_frame, width=30)
    username_entry.grid(row=1, column=1, pady=5)

    tk.Label(form_frame, text="Password:").grid(row=2, column=0, sticky="e", pady=5)
    password_entry = tk.Entry(form_frame, width=30, show="*")
    password_entry.grid(row=2, column=1, pady=5)

    tk.Label(form_frame, text="Role:").grid(row=3, column=0, sticky="e", pady=5)
    role_var = tk.StringVar(value="STUDENT")
    role_menu = tk.OptionMenu(form_frame, role_var, "STUDENT", "TEACHER")
    role_menu.grid(row=3, column=1, sticky="w", pady=5)

    submit_btn = tk.Button(root, text="Save to Database", 
                           command=lambda: save_data(name_entry.get(), username_entry.get(), password_entry.get(), role_var.get()), 
                           bg="#4CAF50", fg="white")
    submit_btn.pack(pady=15)
    root.mainloop()

def save_data(name, username, password, role):
    username = username.strip()
    name = name.strip()

    if not username or not password or not name:
        messagebox.showwarning("Missing Data", "Please fill out all fields.")
        return

    con = None
    cur = None
    try:
        con = mys.connect(host='localhost', user='root', passwd='root', autocommit=True, database="project1") 
        cur = con.cursor()
        
        # Parameterized query for secure insertion
        q = "INSERT INTO users (name, username, password, role) VALUES (%s, %s, %s, %s)"
        cur.execute(q, (name, username, password, role))
        
        messagebox.showinfo("Success", "User registered successfully!")
        firstpage()
        
    except Exception as e:
        messagebox.showerror("Database Error", f"Failed to insert data: {e}")
    finally:
        if cur:
            cur.close()
        if con and con.is_connected():
            con.close()

if __name__ == "__main__":
    firstpage()


##import tkinter as tk
##from tkinter import messagebox
##import CONN
##import mysql.connector as mys
##def firstpage():
##    root = tk.Tk()
##    root.title("Data Capture GUI")
##    root.geometry("400x300")
##        # Submit Button
##    login_button = tk.Button(root, text="login", command=login, bg="#4CAF50", fg="white")
##    login_button.pack(pady=15)
##    signup_button = tk.Button(root, text="signup", command=signup, bg="#4CAF50", fg="white")
##    signup_button.pack(pady=15)
### --- GUI Setup ---
##def login():
##    root = tk.Tk()
##    root.title("Data Capture GUI")
##    root.geometry("400x300")
##    
##    tk.Label(root, text="User Login", font=("Arial", 14, "bold")).pack(pady=10)
##
##    form_frame = tk.Frame(root)
##    form_frame.pack(pady=10)
##
##    # Textfields
##    tk.Label(form_frame, text="Name:").grid(row=0, column=0, sticky="e", pady=5)
##    name_entry = tk.Entry(form_frame, width=30)
##    name_entry.grid(row=0, column=1, pady=5)
##
##    tk.Label(form_frame, text="Username:").grid(row=1, column=0, sticky="e", pady=5)
##    username_entry = tk.Entry(form_frame, width=30)
##    username_entry.grid(row=1, column=1, pady=5)
##
##    tk.Label(form_frame, text="Password:").grid(row=2, column=0, sticky="e", pady=5)
##    password_entry = tk.Entry(form_frame, width=30, show="*")
##    password_entry.grid(row=2, column=1, pady=5)
##
##    # Role Selector
##    tk.Label(form_frame, text="Role:").grid(row=3, column=0, sticky="e", pady=5)
##    role_var = tk.StringVar(value="STUDENT")
##    role_menu = tk.OptionMenu(form_frame, role_var, "STUDENT", "TEACHER")
##    role_menu.grid(row=3, column=1, sticky="w", pady=5)
##
##    # Submit Button
##    submit_btn = tk.Button(root, text="Login", command=check_data, bg="#4CAF50", fg="white")
##    submit_btn.pack(pady=15)
##
##    root.mainloop()
##def check_data():
##        # 1. Capture info from textfields
##    username = username_entry.get().strip()
##    password = password_entry.get()
##    name = name_entry.get().strip()
##    role = role_var.get()
##
##    # Basic validation
##    if not username or not password or not name:
##        messagebox.showwarning("Missing Data", "Please fill out all textfields.")
##        return
##
##    # 2. Connect to MySQL and insert efficiently
##    try:
##        # Assuming your CONN file has a function like get_connection()
##        con =mys.connect(host='localhost',user='root',passwd='root',autocommit=True,database="project1") 
##        cur = con.cursor()
##        q="select username password from users where username='{}';"
##        cur.execute(q.format(username))
##        t=cur.fetchall()
##        v= t[0]
##        if v[0]==str(username) and v[1]==str(password):
##            print("Valid login")
##            if role=="TEACHER":
##                teacher_home()
##            elif role=="STUDENT":
##                student_home()
##        else:
##            print("invalid login details")     
##        
##
##            
##    except Exception as e:
##        messagebox.showerror("Database Error", f"Failed to insert data: {e}")
##    finally:
##        if 'connection' in locals() and connection.is_connected():
##            cursor.close()
##            connection.close()
##    
##    
##def signup():
##    root = tk.Tk()
##    root.title("Data Capture GUI")
##    root.geometry("400x300")
##
##    tk.Label(root, text="User Registration Form", font=("Arial", 14, "bold")).pack(pady=10)
##
##    form_frame = tk.Frame(root)
##    form_frame.pack(pady=10)
##
##    # Textfields
##    tk.Label(form_frame, text="Name:").grid(row=0, column=0, sticky="e", pady=5)
##    name_entry = tk.Entry(form_frame, width=30)
##    name_entry.grid(row=0, column=1, pady=5)
##
##    tk.Label(form_frame, text="Username:").grid(row=1, column=0, sticky="e", pady=5)
##    username_entry = tk.Entry(form_frame, width=30)
##    username_entry.grid(row=1, column=1, pady=5)
##
##    tk.Label(form_frame, text="Password:").grid(row=2, column=0, sticky="e", pady=5)
##    password_entry = tk.Entry(form_frame, width=30, show="*")
##    password_entry.grid(row=2, column=1, pady=5)
##
##    # Role Selector
##    tk.Label(form_frame, text="Role:").grid(row=3, column=0, sticky="e", pady=5)
##    role_var = tk.StringVar(value="STUDENT")
##    role_menu = tk.OptionMenu(form_frame, role_var, "STUDENT", "TEACHER")
##    role_menu.grid(row=3, column=1, sticky="w", pady=5)
##
##    # Submit Button
##    submit_btn = tk.Button(root, text="Save to Database", command=save_data, bg="#4CAF50", fg="white")
##    submit_btn.pack(pady=15)
##
##    root.mainloop()
##def save_data():
##    # 1. Capture info from textfields
##    username = username_entry.get().strip()
##    password = password_entry.get()
##    name = name_entry.get().strip()
##    role = role_var.get()
##
##    # Basic validation
##    if not username or not password or not name:
##        messagebox.showwarning("Missing Data", "Please fill out all textfields.")
##        return
##
##    # 2. Connect to MySQL and insert efficiently
##    try:
##        # Assuming your CONN file has a function like get_connection()
##        con =mys.connect(host='localhost',user='root',passwd='root',autocommit=True,database="project1") 
##        cur = con.cursor()
##        q= "insert into users(name, username, password, role)  values('{}','{}','{}','{}')"
##        cur.execute(q.format(name,username,password,role))
## 
##
##            
##    except Exception as e:
##        messagebox.showerror("Database Error", f"Failed to insert data: {e}")
##    finally:
##        if 'connection' in locals() and connection.is_connected():
##            cursor.close()
##            connection.close()
##firstpage()
##
