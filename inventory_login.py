import tkinter as tk
from tkinter import messagebox
import pymysql


def connect_database():
    try:
        connection = pymysql.connect(
            host='localhost',
            user='root',
            password='',
            charset='utf8mb4'
        )
        cursor = connection.cursor()
        return cursor, connection
    except Exception as e:
        messagebox.showerror('Database Error', f'Failed to connect: {e}')
        return None, None


def create_database_table():
    cursor, connection = connect_database()
    if not cursor or not connection:
        return
    try:
        cursor.execute('CREATE DATABASE IF NOT EXISTS inventory_system')
        cursor.execute('USE inventory_system')
        cursor.execute(
            'CREATE TABLE IF NOT EXISTS employee_data(empid INT PRIMARY KEY, name VARCHAR(100), email VARCHAR(100), '
            'gender VARCHAR(50), dob VARCHAR(30), contact VARCHAR(30), employment_type VARCHAR(50), education VARCHAR(50), '
            'work_shift VARCHAR(50), address VARCHAR(100), doj VARCHAR(30), salary VARCHAR(50), usertype VARCHAR(50), '
            'password VARCHAR(50))'
        )
        connection.commit()
    except Exception as e:
        messagebox.showerror('Error', f'Error creating table: {e}')
    finally:
        cursor.close()
        connection.close()


def verify_login(root, name_entry, password_entry):
    from dashboard import create_dashboard
    name = name_entry.get()
    password = password_entry.get()

    if not name or not password:
        messagebox.showerror('Error', 'Please enter both name and password')
        return

    cursor, connection = connect_database()
    if not cursor or not connection:
        return

    try:
        cursor.execute('USE inventory_system')
        cursor.execute('SELECT name, usertype FROM employee_data WHERE name = %s AND password = %s', (name, password))
        result = cursor.fetchone()

        if result:
            name, usertype = result
            messagebox.showinfo('Success', f'Welcome, {name}!')
            root.destroy()
            create_dashboard(usertype)
        else:
            messagebox.showerror('Error', 'Invalid name or password')

    except Exception as e:
        messagebox.showerror('Error', f'Error during login: {e}')

    finally:
        cursor.close()
        connection.close()


def create_login_window():
    root = tk.Tk()
    root.title("Inventory System Login")
    root.geometry('1270x668+0+0')
    root.configure(bg='#010c48')


    main_frame = tk.Frame(root, bg='white', bd=10, relief='flat')
    main_frame.place(relx=0.5, rely=0.5, anchor='center', width=500, height=580)


    header_frame = tk.Frame(main_frame, bg='#4d636d')
    header_frame.pack(fill='x')
    tk.Label(header_frame, text="VOKA Inventory", font=('Arial', 30, 'bold'), fg='white', bg='#4d636d').pack(pady=20)
    tk.Label(header_frame, text="Login to your account", font=('Arial', 16), fg='white', bg='#4d636d').pack(pady=5)


    form_frame = tk.Frame(main_frame, bg='white')
    form_frame.pack(pady=30)


    tk.Label(form_frame, text="Name", font=('Arial', 14, 'bold'), bg='white', fg='#010c48').pack(pady=(10, 5))
    name_entry = tk.Entry(form_frame, width=30, font=('Arial', 16), bg='#f0f0f0', bd=0, relief='flat')
    name_entry.pack(pady=10, ipady=8)
    tk.Frame(form_frame, bg='#010c48', height=2).pack(fill='x')


    tk.Label(form_frame, text="Password", font=('Arial', 14, 'bold'), bg='white', fg='#010c48').pack(pady=(20, 5))
    password_entry = tk.Entry(form_frame, width=30, font=('Arial', 16), show='*', bg='#f0f0f0', bd=0, relief='flat')
    password_entry.pack(pady=10, ipady=8)
    tk.Frame(form_frame, bg='#010c48', height=2).pack(fill='x')


    login_button = tk.Button(main_frame, text="Login", font=('Arial', 16, 'bold'), bg='#009688', fg='white',
                             bd=0, relief='flat', pady=15, padx=30,
                             command=lambda: verify_login(root, name_entry, password_entry))
    login_button.pack(pady=40)


    def on_enter(e):
        login_button.config(bg='#00796b')
    def on_leave(e):
        login_button.config(bg='#009688')
    login_button.bind('<Enter>', on_enter)
    login_button.bind('<Leave>', on_leave)


    create_database_table()

    return root


if __name__ == "__main__":
    root = create_login_window()
    root.mainloop()