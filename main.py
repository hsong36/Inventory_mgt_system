# Haena Song, CIS 345, TTH 10:30, Final_Project
from tkinter import *
from tkinter import ttk
import tkinter.messagebox
import json
from products_customer_classes import Product, Attachment, Customer
import order_logger
import time

transactions = [['DateTime', 'Name', 'Product Description', 'Qty', 'Total']]
products = list()
new_products = list()
customers = list()
edit_mode = False
expression = ""
total = 0.00
total_list = list()
edit_index = 0
acct_index = 0


# *********************************FUNCTIONS*************************************************
with open('products.json', 'r') as file:
    product_list = json.load(file)


def save_data():
    with open('products.json', 'w') as filePointer:
        json.dump(product_list, filePointer)


def check_pin():
    global pin, customers, edit_mode, acct_index
    acct_index = acct_listbox.curselection()[0]
    edit_acct = customers[acct_index]
    if int(edit_acct.pin) == int(pin.get()):
        tkinter.messagebox.showinfo(title='Welcome', message=f'Hello {edit_acct.name}.')
        order_but.config(state=NORMAL)
        if int(edit_acct.pin) == 9999:
            edit_mode = True
            add_but.config(state=NORMAL)
        else:
            edit_mode = False
            add_but.config(state=DISABLED)
            # order_but.config(state=DISABLED)
            # tkinter.messagebox.showinfo(title='Hi Customer', message='You are not an employee!')
    else:
        tkinter.messagebox.showinfo(title='Incorrect', message='Wrong pin.')
        edit_mode = False
        add_but.config(state=DISABLED)
        order_but.config(state=DISABLED)
    clear_form()


def load_products():
    global product_listbox, product_list, pid, desc, qty, price, material, products
    for p in product_list:
        pid.set(p)
        desc.set(product_list[p]['desc'])
        qty.set(product_list[p]['qty'])
        price.set(product_list[p]['price'])
        prod = Product(pid.get(), desc.get(), qty.get(), price.get())
        products.append(prod)
        product_listbox.insert(END, prod)
    clear_form()


def load_customers():
    global acct, name, pin, balance, accounts, customers, acct_listbox
    for a in accounts:
        acct.set(a[0])
        name.set(a[1])
        balance.set(a[2])
        pin.set(a[3])
        cust = Customer(acct.get(), name.get(), balance.get(), pin.get())
        customers.append(cust)
        acct_listbox.insert(END, cust)
    clear_form()


def toggle_edit():
    global add_but, edit_mode
    if edit_mode:
        add_but.config(state=NORMAL)
    else:
        add_but.config(state=DISABLED)


def toggle_material(prod_type):
    global product_type, material_tbx
    if prod_type == 'A':
        material_tbx['state'] = NORMAL
    if prod_type == 'P':
        material_tbx['state'] = DISABLED


def order_product():
    global pid, desc, qty, price, material, product_type, transactions, order_listbox, \
        quantity_order, products, product_listbox, order_price, expression, \
        total_price, total, product_list, mode_type, pin, acct, customers, edit_index, acct_index, edit_mode
    edit_index = product_listbox.curselection()[0]
    edit_prod = products[edit_index]
    if edit_mode == False:
        edit_prod.qty = int(edit_prod.qty) - int(quantity_order.get())
    if edit_mode == True:
        edit_prod.qty = int(edit_prod.qty) + int(quantity_order.get())
    product_listbox.delete(edit_index)
    product_listbox.insert(edit_index, edit_prod)
    prod = f'{edit_prod.desc}: {quantity_order.get()}'
    order_listbox.insert(END, prod)
    if edit_mode == False:
        ord_price = round(float(edit_prod.price)*int(quantity_order.get()), 2)
        order_price.set(f'{edit_prod.desc}: ${ord_price}')
        total = round((total + ord_price), 2)
        total_price.set(f'Total Transaction: ${total}')
        product_list[edit_prod.pid]['qty'] = edit_prod.qty
    if edit_mode == True:
        order_price.set(f'{edit_prod.desc}: $0.00')
        total_price.set(f'Total Transaction: $0.00')


def submit_order():
    global total, customers, acct_index, balance, edit_index, quantity_order, edit_mode
    edit_acct = customers[acct_index]
    edit_prod = products[edit_index]
    # tkinter.messagebox.showinfo(title='Hi Customer', message=f'{order_prod.price}, {edit_acct.balance}, {total}')
    if edit_mode == False:
        if float(edit_acct.balance) <= total:
            tkinter.messagebox.showinfo(title='Low Balance', message='Not enough money in your account.')
        if float(edit_acct.balance) >= total:
            edit_acct.balance = float(edit_acct.balance) - total
    transactions.append(([time.ctime(), edit_acct.name, edit_prod.desc, quantity_order.get(),
                                 order_logger.format_money(total)]))
    order_logger.log_transaction(transactions)
    tkinter.messagebox.showinfo(title='Success', message='Order Completed.')
    clear_form()


def add_product():
    """function to add new product"""
    global pid, desc, qty, price, material, product_listbox, products, product_list, new_products, product_type, \
        edit_mode
    if edit_mode == False:
        tkinter.messagebox.showinfo(title='Hi Customer', message='You are not an employee!')
    if edit_mode == True:
        if product_type.get() == 'A':
            prod = Attachment(material.get(), pid.get(), desc.get(), qty.get(), price.get())
        else:
            prod = Product(pid.get(), desc.get(), qty.get(), price.get())
        products.append(prod)
        product_listbox.insert(END, prod)
        save_data()
    clear_form()


def clear_form():
    global pid, desc, qty, price, material, quantity_order, acct, name, pin, balance, mode_type, order_listbox
    pid.set('')
    desc.set('')
    qty.set('')
    price.set('')
    material.set('')
    quantity_order.set('')
    pin.set('')
    balance.set('')
    mode_type.set('C')
    order_listbox.delete(END, 0)


# ***********************************************************************************
# ===========================DESIGN==================================================
# mode = {'Employee': 'E', 'Customer': 'C'}
product_types = {'Product': 'P', 'Attachment': 'A'}
accounts = [[1, 'Robert Downey Jr', 0.00, 9999],
            [2, 'Chris Evans', 999999.99, 1234], [3, 'Mark Ruffalo', 2.50, 1111],
            [4, 'Scarlett Johansson', 234.77, 2222], [5, 'Jeremy Renner', 77765.50, 3333]]
bg_color = 'light blue'
order_logger.log_customer(accounts)

win = Tk()
win.config(background=bg_color)
win.geometry('1000x1000')
win.title('Kitchen Supply Management System')
win.iconbitmap('truck.ico')

pid = StringVar()
desc = StringVar()
qty = StringVar()
price = StringVar()
material = StringVar()
product_type = StringVar()
acct_selected = StringVar()
acct = StringVar()
name = StringVar()
pin = StringVar()
balance = StringVar()
mode_type = StringVar()
quantity_order = StringVar()
order_price = StringVar()
total_price = StringVar()


menu_bar = Menu(win)
win.config(menu=menu_bar)


file_menu = Menu(menu_bar, tearoff=False)
menu_bar.add_cascade(label='File', menu=file_menu)
file_menu.add_command(label='Quit', command=win.quit)
file_menu.add_command(label='Save', command=save_data)

acct_label = Label(win, text='Select Account:', background=bg_color, justify=LEFT)
acct_label.grid(row=0, column=0, padx=10)
acct_listbox = Listbox(win, width=40)
acct_listbox.grid(row=1, column=0)
pin_lbl = Label(win, text='Enter Pin:', background=bg_color)
pin_lbl.grid(row=0, column=1)
pin_tbx = Entry(win, textvariable=pin, width=10)
pin_tbx.grid(row=0, column=2)
pin_button = Button(win, text='OK', command=check_pin)
pin_button.grid(row=0, column=3)

product_label = Label(win, text='Available Inventory\n(id, description, qty, price, material)',
                      background=bg_color, justify=LEFT)
product_label.grid(row=1, column=1, padx=5)
product_listbox = Listbox(win, width=40)
product_listbox.grid(row=2, column=1, padx=5, pady=5)
prod_rad_btn = Radiobutton(win, text='Product', variable=product_type, value=product_type,
                           command=lambda: toggle_material('P'))
prod_rad_btn.grid(row=3, column=0)
att_rad_btn = Radiobutton(win, text='Attachment', variable=product_type, value=product_type,
                           command=lambda: toggle_material('A'))
att_rad_btn.grid(row=3, column=1)
id_lbl = Label(win, text='ProductID:', background=bg_color, justify=LEFT)
id_lbl.grid(row=4, column=0, pady=5)
id_tbx = Entry(win, textvariable=pid, width=10)
id_tbx.grid(row=4, column=1, padx=5)
desc_lbl = Label(win, text='Description:', background=bg_color, justify=LEFT)
desc_lbl.grid(row=5, column=0, pady=5)
desc_tbx = Entry(win, textvariable=desc, width=20)
desc_tbx.grid(row=5, column=1, padx=5)
qty_lbl = Label(win, text='Quantity:', background=bg_color, justify=LEFT)
qty_lbl.grid(row=6, column=0, pady=5)
qty_tbx = Entry(win, textvariable=qty, width=10)
qty_tbx.grid(row=6, column=1, padx=5)
price_lbl = Label(win, text='Price: $', background=bg_color, justify=LEFT)
price_lbl.grid(row=7, column=0, pady=5)
price_tbx = Entry(win, textvariable=price, width=10)
price_tbx.grid(row=7, column=1, padx=5)
material_lbl = Label(win, text='Material:', background=bg_color, justify=LEFT)
material_lbl.grid(row=8, column=0, pady=5)
material_tbx = Entry(win, textvariable=material, width=20)
material_tbx.grid(row=8, column=1, pady=5)
add_but = Button(win, bg=bg_color, text='Add', command=add_product, state=DISABLED)
# save_but.bind('<Double-Button-1>', double_click_product())
add_but.grid(row=9, column=1)

order_qty_lbl = Label(win, text='Qty (Enter the quantity you want to order)', background=bg_color)
order_qty_lbl.grid(row=4, column=3)
order_qty_tbx = Entry(win, textvariable=quantity_order, width=10)
order_qty_tbx.grid(row=5, column=3)

order_lbl = Label(win, text='List of Orders', background=bg_color)
order_lbl.grid(row=1, column=3)
order_listbox = Listbox(win, width=30)
order_listbox.grid(row=2, column=3, columnspan=3)
order_but = Button(win, bg=bg_color, text='Add to Order List', command=order_product)
order_but.grid(row=6, column=3, padx=10)

order_price_lbl = Label(win, textvariable=order_price, background=bg_color)
order_price_lbl.grid(row=7, column=3)
total_price_lbl = Label(win, textvariable=total_price, background=bg_color)
total_price_lbl.grid(row=8, column=3)

submit_order_but = Button(win, text='Submit Order', command=submit_order)
submit_order_but.grid(row=8, column=4)

load_products()
load_customers()

win.mainloop()


