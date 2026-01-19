import tkinter
from tkinter import *
from employees import employee_form
from supplier import supplier_form
from category import category_form
from products import product_form

from employees import connect_database
import time
from inventory_login import create_login_window

def create_dashboard(usertype):
    window = Tk()
    window.geometry('1270x668+0+0')
    window.resizable(0, 0)
    window.config(bg='white')
    window.title('Dashboard')


    after_id = None


    def update():
        nonlocal after_id
        cursor, connection = connect_database()
        if not cursor or not connection:
            return
        cursor.execute('use inventory_system')
        cursor.execute('SELECT * from employee_data')
        emp_records = cursor.fetchall()
        total_emp_count_label.config(text=len(emp_records))

        cursor.execute('SELECT * from supplier_data')
        sup_records = cursor.fetchall()
        total_sup_count_label.config(text=len(sup_records))

        cursor.execute('SELECT * from category_data')
        cat_records = cursor.fetchall()
        total_cat_count_label.config(text=len(cat_records))

        cursor.execute('SELECT * from product_data')
        prod_records = cursor.fetchall()
        total_prod_count_label.config(text=len(prod_records))

        date_time = time.strftime('%I:%M:%S %p on %A, %B %d, %Y')
        subtitleLabel.config(text=f'Welcome {usertype.capitalize()}\t\t\t\t {date_time}')
        after_id = subtitleLabel.after(400, update)


    def exit_to_login():
        nonlocal after_id
        if after_id is not None:
            subtitleLabel.after_cancel(after_id)
        window.destroy()
        login_root = create_login_window()
        login_root.mainloop()

    current_frame = None
    def show_form(form_function):
        nonlocal current_frame
        if current_frame:
            current_frame.place_forget()
        current_frame = form_function(window)

    # UI Setup
    bg_Image = PhotoImage(file='inventory.png')
    titleLabel = Label(window, image=bg_Image, compound=LEFT,
                       text=' VOKA Inventory Management System',
                       font=('times new roman', 40, 'bold'),
                       bg='#010c48', fg='white', anchor='w', padx=20)
    titleLabel.place(x=0, y=0, relwidth=1)

    logoutButton = Button(window, text='LOGOUT', font=('times new roman', 20, 'bold'), fg='#010c48',
                          command=exit_to_login)
    logoutButton.place(x=1100, y=10)

    subtitleLabel = Label(window, text=f'Welcome {usertype.capitalize()}\t\t Date: 10-10-2024 \t\t Time:03:10 am',
                          font=('times new roman', 15), bg='#4d636d', fg='white')
    subtitleLabel.place(x=0, y=70, relwidth=1)

    leftFrame = Frame(window)
    leftFrame.place(x=0, y=102, width=200, height=566)

    logoImage = PhotoImage(file='supplier.png')
    imageLabel = Label(leftFrame, image=logoImage)
    imageLabel.pack()

    menuLabel = Label(leftFrame, text='Menu', font=('times new roman', 20), bg='#009688')
    menuLabel.pack(fill=X)

    if usertype.lower() == 'admin':
        employee_icon = PhotoImage(file='employee.png')
        employee_button = Button(leftFrame, image=employee_icon, compound=LEFT, text='Employees',
                                 font=('times new roman', 20, 'bold'), anchor='w',
                                 command=lambda: show_form(employee_form))
        employee_button.pack(fill=X)

    supplier_icon = PhotoImage(file='supplier (1).png')
    supplier_button = Button(leftFrame, image=supplier_icon, compound=LEFT, text='Supplier',
                             font=('times new roman', 20, 'bold'), anchor='w', padx=10,
                             command=lambda: show_form(supplier_form))
    supplier_button.pack(fill=X)

    category_icon = PhotoImage(file='category.png')
    category_button = Button(leftFrame, image=category_icon, compound=LEFT, text='Category',
                             font=('times new roman', 20, 'bold'), anchor='w', padx=10,
                             command=lambda: show_form(category_form))
    category_button.pack(fill=X)

    product_icon = PhotoImage(file='products.png')
    product_button = Button(leftFrame, image=product_icon, compound=LEFT, text='Product',
                            font=('times new roman', 20, 'bold'), anchor='w', padx=10,
                            command=lambda: show_form(product_form))
    product_button.pack(fill=X)



    exit_icon = PhotoImage(file='exit.png')
    exit_button = Button(leftFrame, image=exit_icon, compound=LEFT, text='Exit',
                         font=('times new roman', 20, 'bold'), command=exit_to_login)
    exit_button.pack(fill=X)


    emp_frame = Frame(window, bg='#2c3E50', bd=3, relief=RIDGE)
    emp_frame.place(x=400, y=125, height=170, width=200)
    total_emp_icon = PhotoImage(file='employee (64).png')
    total_emp_icon_label = Label(emp_frame, image=total_emp_icon, bg='#2c3E50')
    total_emp_icon_label.pack(pady=10)
    total_emp_label = Label(emp_frame, text='Total Employees', bg='#2c3E50', fg='white',
                            font=('times new roman', 15, 'bold'))
    total_emp_label.pack(pady=10)
    global total_emp_count_label
    total_emp_count_label = Label(emp_frame, text='0', bg='#2c3E50', fg='white',
                                  font=('times new roman', 30, 'bold'))
    total_emp_count_label.pack()

    sup_frame = Frame(window, bg='#2c3E50', bd=3, relief=RIDGE)
    sup_frame.place(x=800, y=125, height=170, width=200)
    total_sup_icon = PhotoImage(file='supplier (64).png')
    total_sup_icon_label = Label(sup_frame, image=total_sup_icon, bg='#2c3E50')
    total_sup_icon_label.pack(pady=10)
    total_sup_label = Label(sup_frame, text='Total Suppliers', bg='#2c3E50', fg='white',
                            font=('times new roman', 15, 'bold'))
    total_sup_label.pack(pady=10)
    global total_sup_count_label
    total_sup_count_label = Label(sup_frame, text='0', bg='#2c3E50', fg='white',
                                  font=('times new roman', 30, 'bold'))
    total_sup_count_label.pack()

    cat_frame = Frame(window, bg='#2c3E50', bd=3, relief=RIDGE)
    cat_frame.place(x=400, y=310, height=170, width=200)
    total_cat_icon = PhotoImage(file='categorization (64).png')
    total_cat_icon_label = Label(cat_frame, image=total_cat_icon, bg='#2c3E50')
    total_cat_icon_label.pack(pady=10)
    total_cat_label = Label(cat_frame, text='Total Categories', bg='#2c3E50', fg='white',
                            font=('times new roman', 15, 'bold'))
    total_cat_label.pack(pady=10)
    global total_cat_count_label
    total_cat_count_label = Label(cat_frame, text='0', bg='#2c3E50', fg='white',
                                  font=('times new roman', 30, 'bold'))
    total_cat_count_label.pack()

    prod_frame = Frame(window, bg='#2c3E50', bd=3, relief=RIDGE)
    prod_frame.place(x=800, y=310, height=170, width=200)
    total_prod_icon = PhotoImage(file='products (64).png')
    total_prod_icon_label = Label(prod_frame, image=total_prod_icon, bg='#2c3E50')
    total_prod_icon_label.pack(pady=10)
    total_prod_label = Label(prod_frame, text='Total Products', bg='#2c3E50', fg='white',
                             font=('times new roman', 15, 'bold'))
    total_prod_label.pack(pady=10)
    global total_prod_count_label
    total_prod_count_label = Label(prod_frame, text='0', bg='#2c3E50', fg='white',
                                   font=('times new roman', 30, 'bold'))
    total_prod_count_label.pack()



    update()
    window.mainloop()

if __name__ == "__main__":
    create_dashboard("admin")