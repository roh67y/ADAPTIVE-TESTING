import tkinter as tk
from tkinter import messagebox
import mysql.connector as mys

# Placeholder functions so the code doesn't crash when called
def teacher_home(username, password, role):
    root=tk.Tk()
    root.title("Wlecome to teeacher homepage")
    root.geometry("400x300")
    
    # Using lambda to destroy the current window before opening the next
    login_button = tk.Button(root, text="create new test", command=lambda: [root.destroy(), create_new_test()], bg="#4CAF50", fg="white", width=15)
    login_button.pack(pady=15)
    
    signup_button = tk.Button(root, text="Veiw student performance", command=lambda: [root.destroy(), review_stdent()], bg="#4CAF50", fg="white", width=15)
    signup_button.pack(pady=15)
    
    root.mainloop()

def student_home(username, password, role):
    root=tk.Tk()
    root.title("Wlecome to student homepage")
    root.geometry("400x300")
    
    # Using lambda to destroy the current window before opening the next
    login_button = tk.Button(root, text="Take A test", command=lambda: [root.destroy(), Take_a_test(username)], bg="#4CAF50", fg="white", width=15)
    login_button.pack(pady=15)
    
    #signup_button = tk.Button(root, text="Veiw previous performance performance", command=lambda: [root.destroy(), review_stdent()], bg="#4CAF50", fg="white", width=15)
    #signup_button.pack(pady=15)
    
    root.mainloop()

def firstpage():
    root = tk.Tk()
    root.title("Main Menu")
    root.geometry("400x300")
    
    # Using lambda to destroy the current window before opening the next
    login_button = tk.Button(root, text="Login", command=lambda: [root.destroy(), login()], bg="#4CAF50", fg="white", width=15)
    login_button.pack(pady=15)
    
    signup_button = tk.Button(root, text="Signup", command=lambda: [root.destroy(), signup()], bg="#4CAF50", fg="white", width=15)
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
        con = mys.connect(host='localhost', user='root', passwd='password', autocommit=True, database="project1") 
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
                    teacher_home(username, password, role)
                elif role == "STUDENT":
                    student_home(username, password, role)
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
        con = mys.connect(host='localhost', user='root', passwd='password', autocommit=True, database="project1") 
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
##def Take_a_test():
##    root = tk.Tk()
##    root.title("Enter test id")
##    root.geometry("400x300")
##    
##
##
##    tk.Label(form_frame, text="test id:").grid(row=0, column=0, sticky="e", pady=5)
##    testid_entry = tk.Entry(form_frame, width=30)
##    testid_entry.grid(row=0, column=1, pady=5)
##
##
##    # Pass the specific string values to the check_data function
##    submit_btn = tk.Button(root, text="submit", 
##                           command=lambda: write_test(testid_entry.get()), 
##                           bg="#4CAF50", fg="white")
##    submit_btn.pack(pady=15)
##    root.mainloop()
##def write_test():
##    root = tk.Tk()
##    root.title("Enter test id")
##    root.geometry("400x300")
##    form_frame = tk.Frame(root)
##    form_frame.pack(pady=10)
##    
##
##    
##
##    tk.Label(form_frame, text="Option:").grid(row=3, column=0, sticky="e", pady=5)
##    option_var = tk.StringVar(value="A")
##    option_menu = tk.OptionMenu(form_frame, option_var, "A", "B","C","D")
##    option_menu.grid(row=3, column=1, sticky="w", pady=5)
##
##
##
##
##
##    # Pass the specific string values to the check_data function
##    submit_btn = tk.Button(root, text="submit",command=lambda: save_option(),bg="#4CAF50", fg="white")
##    submit_btn.pack(pady=15)
##    root.mainloop()
def save_option():
    con = None
    cur = None
    try:
        con = mys.connect(host='localhost', user='root', passwd='password', autocommit=True, database="project1") 
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
#Take test functon
def Take_a_test(username=None):
    root = tk.Tk()
    root.title("Enter test id")
    root.geometry("400x300")

    form_frame = tk.Frame(root)
    form_frame.pack(pady=10)

    tk.Label(form_frame, text="test id:").grid(row=0, column=0, sticky="e", pady=5)
    testid_entry = tk.Entry(form_frame, width=30)
    testid_entry.grid(row=0, column=1, pady=5)

    def start_test():
        tid = testid_entry.get().strip()
        if not tid:
            messagebox.showwarning("Missing Data", "Please enter a test id.")
            return
        try:
            test_id_int = int(tid)
        except ValueError:
            messagebox.showwarning("Invalid Input", "Test ID must be a number.")
            return
        root.destroy()
        write_test(test_id_int, username)

    submit_btn = tk.Button(root, text="submit", command=start_test, bg="#4CAF50", fg="white", width=15)
    submit_btn.pack(pady=15)
    root.mainloop()


def write_test(test_id, username=None):
    con = None
    cur = None
    attempt_id = None
    try:
        con = mys.connect(host="localhost", user="root", passwd="password", autocommit=True, database="project1")
        cur = con.cursor()

        cur.execute(
            """
            SELECT id, QUESTION_TEXT, OPTION_A, OPTION_B, OPTION_C, OPTION_D, CORRECT_OPTION, DIFFICULTY
            FROM questions
            WHERE test_id = %s
            """,
            (test_id,),
        )
        rows = cur.fetchall()

        if not rows:
            messagebox.showinfo("No Questions", "No questions found for this test ID.")
            return

        cur.execute(
            """
            INSERT INTO TEST_ATTEMPTS (username, test_id, score)
            VALUES (%s, %s, %s)
            """,
            (username, test_id, 0),
        )
        attempt_id = cur.lastrowid

    except Exception as e:
        messagebox.showerror("Database Error", f"Failed to start test: {e}")
        return
    finally:
        if cur:
            cur.close()
        if con and con.is_connected():
            con.close()

    # Group questions by difficulty level
    bank = {
        "EASY": [r for r in rows if r[7] == "EASY"],
        "MEDIUM": [r for r in rows if r[7] == "MEDIUM"],
        "HARD": [r for r in rows if r[7] == "HARD"],
    }
    asked_ids = set()
    state = {"level": "EASY", "score": 0, "asked": 0}

    def save_answer_to_db(question_id, selected_option, is_correct):
        db_con = None
        db_cur = None
        try:
            db_con = mys.connect(host="localhost", user="root", passwd="password", autocommit=True, database="project1")
            db_cur = db_con.cursor()
            db_cur.execute(
                """
                INSERT INTO attempt_answers (attempt_id, question_id, selected_option, is_correct)
                VALUES (%s, %s, %s, %s)
                """,
                (attempt_id, question_id, selected_option, int(bool(is_correct))),
            )
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to save answer: {e}")
        finally:
            if db_cur:
                db_cur.close()
            if db_con and db_con.is_connected():
                db_con.close()

    def finalize_attempt_score():
        db_con = None
        db_cur = None
        try:
            db_con = mys.connect(host="localhost", user="root", passwd="password", autocommit=True, database="project1")
            db_cur = db_con.cursor()
            db_cur.execute(
                """
                UPDATE TEST_ATTEMPTS
                SET score = %s
                WHERE id = %s
                """,
                (state["score"], attempt_id),
            )
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to update attempt score: {e}")
        finally:
            if db_cur:
                db_cur.close()
            if db_con and db_con.is_connected():
                db_con.close()

    def next_question(preferred_level):
        order = [preferred_level, "EASY", "MEDIUM", "HARD"]
        seen_order = []
        for lvl in order:
            if lvl not in seen_order:
                seen_order.append(lvl)

        for lvl in seen_order:
            for q in bank[lvl]:
                if q[0] not in asked_ids:
                    return q, lvl
        return None, None

    def show_question_window():
        q, actual_level = next_question(state["level"])
        if q is None:
            finalize_attempt_score()
            messagebox.showinfo(
                "Test Completed",
                f"Test finished!\nAttempt ID: {attempt_id}\nQuestions answered: {state['asked']}\nCorrect answers: {state['score']}",
            )
            return

        asked_ids.add(q[0])
        state["level"] = actual_level
        q_id, q_text, opt_a, opt_b, opt_c, opt_d, correct_opt, diff = q

        root = tk.Tk()
        root.title(f"Test {test_id} - {diff}")
        root.geometry("400x300")

        form_frame = tk.Frame(root)
        form_frame.pack(pady=10, padx=10)

        tk.Label(form_frame, text=f"Difficulty: {diff}", font=("Arial", 10, "bold")).grid(row=0, column=0, columnspan=2, pady=3)
        tk.Label(form_frame, text=q_text, wraplength=350, justify="left").grid(row=1, column=0, columnspan=2, pady=8)

        choice_var = tk.StringVar(value="A")
        options = [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d)]
        for idx, (letter, text) in enumerate(options, start=2):
            tk.Radiobutton(
                form_frame,
                text=f"{letter}: {text}",
                variable=choice_var,
                value=letter,
                wraplength=330,
                justify="left",
            ).grid(row=idx, column=0, columnspan=2, sticky="w", pady=2)

        def submit_answer():
            selected = choice_var.get().strip().upper()
            state["asked"] += 1
            is_correct = selected == str(correct_opt).strip().upper()

            if is_correct:
                state["score"] += 1
                save_answer_to_db(q_id, selected, True)
                if diff == "EASY":
                    state["level"] = "MEDIUM"
                elif diff == "MEDIUM":
                    state["level"] = "HARD"
                else:
                    state["level"] = "HARD"
                messagebox.showinfo("Correct", "Correct answer!")
            else:
                save_answer_to_db(q_id, selected, False)
                if diff == "MEDIUM":
                    state["level"] = "EASY"
                elif diff == "HARD":
                    state["level"] = "MEDIUM"
                else:
                    state["level"] = "EASY"
                messagebox.showwarning("Incorrect", f"Wrong answer! Correct option: {correct_opt}")

            root.destroy()
            show_question_window()

        tk.Button(
            root,
            text="submit",
            command=submit_answer,
            bg="#4CAF50",
            fg="white",
            width=15,
        ).pack(pady=12)

        root.mainloop()

    show_question_window()
# Create new teat function
def create_new_test():
    root = tk.Tk()
    root.title("Enter test id")
    root.geometry("400x300")

    form_frame = tk.Frame(root)
    form_frame.pack(pady=10)
    tk.Label(form_frame, text="test id:").grid(row=0, column=0, sticky="e", pady=5)
    testid_entry = tk.Entry(form_frame, width=30)
    testid_entry.grid(row=0, column=1, pady=5)

    tk.Label(form_frame, text="test Title:").grid(row=0, column=0, sticky="e", pady=5)
    testtitle_entry = tk.Entry(form_frame, width=30)
    testtitle_entry.grid(row=0, column=1, pady=5)

    tk.Label(form_frame, text="test Description:").grid(row=0, column=0, sticky="e", pady=5)
    testdescription_entry = tk.Entry(form_frame, width=30)
    testdescription_entry.grid(row=0, column=1, pady=5)

    def checkdata_testid():
        tid = testid_entry.get().strip()
        t_title= testtitle_entry.get().strip()
        t_description= testdescription_entry.get().strip()
        if not tid:
            messagebox.showwarning("Missing Data", "Please enter a test id.")
            return
        try:
            test_id_int = int(tid)
        except ValueError:
            messagebox.showwarning("Invalid Input", "Test ID must be a number.")
            return
        root.destroy()
        save_testid(test_id_int,t_title,t_description)

    submit_btn = tk.Button(root, text="submit", command=checkdata_testid(), bg="#4CAF50", fg="white", width=15)
    submit_btn.pack(pady=15)
    root.mainloop()


def save_testid(test_id,test_title,test_description):
    con = None
    cur = None
    attempt_id = None
    try:
        con = mys.connect(host="localhost", user="root", passwd="password", autocommit=True, database="project1")
        cur = con.cursor()

        cur.execute(
            """INSERT INTO tests (test_id,TITLE,DESCRIPTION) VALUES (%s, %s, %s)       
            """,
            (test_id,test_title,test_description),
        )
        add_questions(test_id)
        
def add_questions(test_id):
    root = tk.Tk()
    root.title(f"Add Questions - Test {test_id}")
    root.geometry("400x300")

    form_frame = tk.Frame(root)
    form_frame.pack(pady=5)

    tk.Label(form_frame, text="Question:").grid(row=0, column=0, sticky="e", pady=2)
    q_entry = tk.Entry(form_frame, width=30)
    q_entry.grid(row=0, column=1, pady=2)

    tk.Label(form_frame, text="Option A:").grid(row=1, column=0, sticky="e", pady=2)
    a_entry = tk.Entry(form_frame, width=30)
    a_entry.grid(row=1, column=1, pady=2)

    tk.Label(form_frame, text="Option B:").grid(row=2, column=0, sticky="e", pady=2)
    b_entry = tk.Entry(form_frame, width=30)
    b_entry.grid(row=2, column=1, pady=2)

    tk.Label(form_frame, text="Option C:").grid(row=3, column=0, sticky="e", pady=2)
    c_entry = tk.Entry(form_frame, width=30)
    c_entry.grid(row=3, column=1, pady=2)

    tk.Label(form_frame, text="Option D:").grid(row=4, column=0, sticky="e", pady=2)
    d_entry = tk.Entry(form_frame, width=30)
    d_entry.grid(row=4, column=1, pady=2)

    tk.Label(form_frame, text="Correct:").grid(row=5, column=0, sticky="e", pady=2)
    correct_var = tk.StringVar(value="A")
    correct_menu = tk.OptionMenu(form_frame, correct_var, "A", "B", "C", "D")
    correct_menu.grid(row=5, column=1, sticky="w", pady=2)

    tk.Label(form_frame, text="Difficulty:").grid(row=6, column=0, sticky="e", pady=2)
    diff_var = tk.StringVar(value="EASY")
    diff_menu = tk.OptionMenu(form_frame, diff_var, "EASY", "MEDIUM", "HARD")
    diff_menu.grid(row=6, column=1, sticky="w", pady=2)

    def save_question():
        q = q_entry.get().strip()
        a = a_entry.get().strip()
        b = b_entry.get().strip()
        c = c_entry.get().strip()
        d = d_entry.get().strip()
        correct = correct_var.get().strip().upper()
        difficulty = diff_var.get().strip().upper()

        if not q or not a or not b or not c or not d:
            messagebox.showwarning("Missing Data", "Please fill out all fields.")
            return

        con = None
        cur = None
        try:
            con = mys.connect(
                host="localhost",
                user="root",
                passwd="password",
                autocommit=True,
                database="project1",
            )
            cur = con.cursor()
            cur.execute(
                """
                INSERT INTO questions (
                    test_id, QUESTION_TEXT, OPTION_A, OPTION_B, OPTION_C, OPTION_D, CORRECT_OPTION, DIFFICULTY
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (test_id, q, a, b, c, d, correct, difficulty),
            )
            messagebox.showinfo("Success", "Question added successfully!")

            q_entry.delete(0, tk.END)
            a_entry.delete(0, tk.END)
            b_entry.delete(0, tk.END)
            c_entry.delete(0, tk.END)
            d_entry.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to add question: {e}")
        finally:
            if cur:
                cur.close()
            if con and con.is_connected():
                con.close()

    btn_frame = tk.Frame(root)
    btn_frame.pack(pady=8)

    tk.Button(
        btn_frame,
        text="Save Question",
        command=save_question,
        bg="#4CAF50",
        fg="white",
        width=14,
    ).grid(row=0, column=0, padx=5)

    tk.Button(
        btn_frame,
        text="Done",
        command=lambda: [root.destroy(), teacher_home()],
        bg="#4CAF50",
        fg="white",
        width=10,
    ).grid(row=0, column=1, padx=5)

    root.mainloop()
        
    
##        if not rows:
##            messagebox.showinfo("", "No questions found for this test ID.")
##            return
##
##        cur.execute(
##            """
##            INSERT INTO TEST_ATTEMPTS (username, test_id, score)
##            VALUES (%s, %s, %s)
##            """,
##            (username, test_id, 0),
##        )
##        attempt_id = cur.lastrowid

    except Exception as e:
        messagebox.showerror("Database Error", f"Failed to start test: {e}")
        return
    finally:
        if cur:
            cur.close()
        if con and con.is_connected():
            con.close()

if __name__ == "__main__":
    firstpage()
    





    #shfjfks dkjg

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
