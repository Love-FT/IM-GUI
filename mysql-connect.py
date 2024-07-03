import mysql.connector
from tkinter import *

from tkinter import messagebox


# Create/Insert new Book Record
# Update a Book Record
# Delete a Book Record
# Print Book Records (Inventory?) List
# Print Registered Customer List
# Print Customer Transaction History

# Login Menu
def loginMenu():
    mycursor.execute('SELECT * FROM staff WHERE username = %s AND passw = %s', (username.get(), password.get()))
    result = mycursor.fetchone()
    if result:
        messagebox.showinfo("Message", "Login Success!")
        clear_window()
        startMenu()
    else:
        messagebox.showwarning("Access Denied", "Invalid Credentials!")


# Main Menu
def startMenu():
    clear_window()
    appWidth = 240
    appHeight = 200
    x = (root.winfo_screenwidth() / 2) - (appWidth / 2)
    y = (root.winfo_screenheight() / 2) - (appHeight / 2)
    root.geometry(f'{appWidth}x{appHeight}+{int(x)}+{int(y)}')
    title = Label(root, text="Bookshop Database")
    showb = Button(root, text="Show Book Records", command=showBooksMenu)
    showc = Button(root, text="Show Registered Customers")  #
    showt = Button(root, text="Show Customer Transaction History", command=showCustomerMenu)
    title.grid(row=0, column=0, columnspan=2, sticky='news')
    showb.grid(row=1, column=0, columnspan=2, pady=5, padx=5)
    showc.grid(row=2, column=0, columnspan=2, pady=5, padx=5)
    showt.grid(row=3, column=0, columnspan=2, pady=5, padx=5)


# Book Records Menu
def showBooksMenu():
    clear_window()
    root.geometry("1000x500")
    root.columnconfigure(0, weight=1)
    root.columnconfigure(1, weight=1)
    root.columnconfigure(2, weight=1)
    mycursor.execute('SELECT * from book')
    global books
    books = mycursor.fetchall()
    global bookrecords
    # Format headers
    headers = ["ID", "Title", "Genre", "Price", "Stock", "AuthorID", "GroupID"]
    formatted_headers = "{:<5} {:<45} {:<20} {:<10} {:<10} {:<10} {:<10}".format(*headers)

    bookrecords = Listbox(root, height=20, width=120, bg="white", font=("Courier New", 10))
    bookrecords.insert(0, formatted_headers)
    bookrecords.insert(1, "-" * 120)

    for book in books:
        # Replace None values with empty strings
        book = [str(item) if item is not None else '' for item in book]
        formatted_book = "{:<5} {:<45} {:<20} {:<10} {:<10} {:<10} {:<10}".format(
            book[0], book[1], book[2], book[3], book[4], book[5], book[6])
        bookrecords.insert(END, formatted_book)

    bookrecords.grid(row=0, column=0, columnspan=3)

    insert = Button(root, text="Create New Book Record", command=createWindow)
    update = Button(root, text="Update Book Record")  #
    delete = Button(root, text="Delete Book Record", command=deleteRec)

    insert.grid(row=1, column=0, pady=5, padx=5, sticky='s')
    update.grid(row=1, column=1, pady=5, padx=5, sticky='s')
    delete.grid(row=1, column=2, pady=5, padx=5, sticky='s')


# Show Registered Customers Menu
def showCustomerMenu():
    clear_window()
    appWidth = 1080
    appHeight = 480
    x = (root.winfo_screenwidth() / 2) - (appWidth / 2)
    y = (root.winfo_screenheight() / 2) - (appHeight / 2)
    root.geometry(f'{appWidth}x{appHeight}+{int(x)}+{int(y)}')
    mycursor.execute("SELECT * from customer")
    global customers
    customers = mycursor.fetchall()
    global customer_records

    customerTitle = Label(root,
                          text="REGISTERED CUSTOMER LIST:",
                          font=("Helvetica", 12, "normal"))
    customerTitle.pack(pady=12)

    # Format headers
    headers = ["ID", "Last Name", "First Name", "M.I.", "Email", "Phone"]
    formatted_headers = "{:<5} {:<25} {:<25} {:<5} {:<30} {:<15}".format(*headers)

    customer_records = Listbox(root,
                               height=20,
                               width=110,
                               bg="white",
                               font=("Courier New", 10))
    customer_records.insert(0, formatted_headers)
    customer_records.insert(1, "-" * 110)

    for c in customers:
        # Replace None values with empty strings
        c = [str(item) if item is not None else '' for item in c]
        formatted_book = "{:<5} {:<25} {:<25} {:<5} {:<30} {:<15}".format(
            c[0], c[1], c[2], c[3], c[4], c[5])
        customer_records.insert(END, formatted_book)
    customer_records.pack()

    btnBack = Button(root,
                     text="GO BACK TO MAIN MENU",
                     justify=CENTER,
                     width=42,
                     anchor="center",
                     command=startMenu)
    btnBack.pack(pady=24)


root = Tk()
root.title("Bookshop Database")
appWidth = 240
appHeight = 120
x = (root.winfo_screenwidth() / 2) - (appWidth / 2)
y = (root.winfo_screenheight() / 2) - (appHeight / 2)
root.geometry(f'{appWidth}x{appHeight}+{int(x)}+{int(y)}')
mydb = mysql.connector.connect(
    host='localhost',
    user='root',
    password='reindf_010604',
    port='3306',
    database='imdb'
)

root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=3)
mycursor = mydb.cursor()


# Window for creation of new book record
def createWindow():
    new = Toplevel()
    new.geometry("400x400")
    new.resizable(False, False)
    new.grab_set()
    global book_id
    global book_title
    global genre
    global price
    global stock
    global author_id
    global group_id

    l = Label(new, text="Book ID:")
    l1 = Label(new, text="Book Title:")
    l2 = Label(new, text="Genre:")
    l3 = Label(new, text="Price:")
    l4 = Label(new, text="Stock:")
    l5 = Label(new, text="Author ID:")
    l6 = Label(new, text="Group ID:")

    book_id = Entry(new)
    book_title = Entry(new)
    genre = Entry(new)
    price = Entry(new)
    stock = Entry(new)
    author_id = Entry(new)
    group_id = Entry(new)
    create_btn = Button(new, text="Insert Book Record", command=create)

    l.grid(row=0, column=0, pady=5, padx=5)
    l1.grid(row=1, column=0, pady=5, padx=5)
    l2.grid(row=2, column=0, pady=5, padx=5)
    l3.grid(row=3, column=0, pady=5, padx=5)
    l4.grid(row=4, column=0, pady=5, padx=5)
    l5.grid(row=5, column=0, pady=5, padx=5)
    l6.grid(row=6, column=0, pady=5, padx=5)

    book_id.grid(row=0, column=1, pady=5, padx=5)
    book_title.grid(row=1, column=1, pady=5, padx=5)
    genre.grid(row=2, column=1, pady=5, padx=5)
    price.grid(row=3, column=1, pady=5, padx=5)
    stock.grid(row=4, column=1, pady=5, padx=5)
    author_id.grid(row=5, column=1, pady=5, padx=5)
    group_id.grid(row=6, column=1, pady=5, padx=5)

    create_btn.grid(row=7, column=0, columnspan=2, padx=5, pady=5)


# Creating/Inserting new book records to list and database
def create():
    id = book_id.get()
    title = book_title.get()
    b_genre = genre.get()
    b_price = price.get()
    b_stock = stock.get()

    if not title or not b_genre or not b_price or not b_stock:
        messagebox.showwarning("Input Error", "All fields are required.")
        return

    try:
        mycursor.execute('INSERT INTO Book (BookID, Title, Genre, Price, Stock) VALUES (%s, %s, %s, %s, %s)',
                         (id, title, b_genre, b_price, b_stock))
        mydb.commit()
        messagebox.showinfo("Success", "Record inserted successfully.")
        clear_entries()
        showBooksMenu()
    except Exception as e:
        messagebox.showerror("Error", str(e))
        mydb.rollback()


# Deleting book records from list and database
def deleteRec():
    try:
        selected_index = bookrecords.curselection()

        for index in selected_index:
            selected_item = bookrecords.get(index)
            book_to_delete = selected_item.split()[0]
            mycursor.execute('DELETE FROM book WHERE BookID = %s', (book_to_delete,))
            mydb.commit()
            bookrecords.delete(index)

        messagebox.showinfo("Success", "Record(s) deleted successfully.")

    except Exception as e:
        messagebox.showerror("Error", str(e))
        mydb.rollback()


# For clearing entries in createWindow
def clear_entries():
    book_id.delete(0, END)
    book_title.delete(0, END)
    genre.delete(0, END)
    price.delete(0, END)
    stock.delete(0, END)
    author_id.delete(0, END)
    group_id.delete(0, END)


# def showcustomers():

# def showtrans():


def clear_window():
    for widget in root.winfo_children():
        widget.destroy()


title = Label(root, text="Bookshop Database Application")
title.config(font=("Helvetica", 10, "bold"))
l1 = Label(root, text="Username:")
l2 = Label(root, text="Password:")

username = Entry(root)
password = Entry(root, show="*")

log = Button(root, text="Login", command=loginMenu)

title.grid(row=0, column=0, columnspan=3, sticky='news')
l1.grid(row=1, column=0, sticky=W, padx=16, pady=5)
username.grid(row=1, column=1, columnspan=2, sticky=W, padx=5, pady=5)
l2.grid(row=2, column=0, sticky=W, padx=16, pady=5)
password.grid(row=2, column=1, columnspan=2, sticky=W, padx=5, pady=5)
log.grid(row=3, column=1, sticky=E, padx=16, pady=5)

root.resizable(False, False)

root.mainloop()
