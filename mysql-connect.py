import mysql.connector
from tkinter import *

from tkinter import messagebox

# Login Menu
def loginMenu():
    startMenu()
    """mycursor.execute('SELECT * FROM staff WHERE username = %s AND passw = %s', (username.get(), password.get()))
    result = mycursor.fetchone()
    if result:
        messagebox.showinfo("Message", "Login Success!")
        clear_window()
        startMenu()
    else:
        messagebox.showwarning("Access Denied", "Invalid Credentials!")"""


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
    showc = Button(root, text="Show Registered Customers", command=showCustomerMenu)
    showt = Button(root, text="Show Customer Transaction History", command=showTransaction)  # Insert command
    title.grid(row=0, column=0, columnspan=2, sticky='news')
    showb.grid(row=1, column=0, columnspan=2, pady=5, padx=5)
    showc.grid(row=2, column=0, columnspan=2, pady=5, padx=5)
    showt.grid(row=3, column=0, columnspan=2, pady=5, padx=5)


# Function to truncate text
def truncate_text(text, length):
    if len(text) > length:
        return text[:length - 3] + "..."
    return text


# Book Records Menu ----------------------------------------------------------------------------------------------------
def showBooksMenu():
    clear_window()
    appWidth = 1080
    appHeight = 480
    x = (root.winfo_screenwidth() / 2) - (appWidth / 2)
    y = (root.winfo_screenheight() / 2) - (appHeight / 2)
    root.geometry(f'{appWidth}x{appHeight}+{int(x)}+{int(y)}')
    mycursor.execute('SELECT * from book')
    global books
    books = mycursor.fetchall()
    global book_records

    # List Box Frame
    panelList = LabelFrame(root, text="BOOK INFORMATION LIST", font=('Inter', 12, 'bold'),
                           padx=20, pady=12)
    panelList.pack(padx=80, pady=(12, 0), fill='both', expand=True)

    # Format headers
    headers = ["ID", "Title", "Genre", "Price", "Stock", "AuthorID", "GroupID"]
    max_lengths = [5, 40, 15, 10, 10, 10, 10]
    formatted_headers = "{:<5} {:<40} {:<15} {:<10} {:<10} {:<10} {:<10}".format(*headers)

    # Book Listbox
    book_records = Listbox(panelList, bg="white", font=("Courier New", 10))
    book_records.insert(0, formatted_headers)
    book_records.insert(1, "-" * 120)

    for b in books:
        # Replace None values with empty strings
        b = [truncate_text(str(item), max_lengths[i]) if item is not None else '' for i, item in enumerate(b)]
        formatted_book = "{:<5} {:<40} {:<15} {:<10} {:<10} {:<10} {:<10}".format(
            b[0], b[1], b[2], b[3], b[4], b[5], b[6])
        book_records.insert(END, formatted_book)

    book_records.pack(side='left', fill='both', expand=True)

    # Vertical Scrollbar
    vtScrollBar = Scrollbar(panelList, orient="vertical", command=book_records.yview)
    vtScrollBar.pack(side="right", fill="y")
    book_records.configure(yscrollcommand=vtScrollBar.set)

    # Buttons Frame
    panelButton = Frame(root)
    panelButton.pack(fill='x', padx=100, pady=24)

    # Buttons
    btnInsert = Button(panelButton, text="Create New Book Record", justify=CENTER, width=24,
                       command=createBookWindow)
    btnUpdate = Button(panelButton, text="Update Book Record", justify=CENTER, width=24,
                       command=lambda: updateBookWindow(getSelectedBook()))
    btnDelete = Button(panelButton, text="Delete Book Record", justify=CENTER, width=24, command=deleteRec)
    btnBack = Button(panelButton, text="Go back to Main Menu >", justify=CENTER, width=24, command=startMenu)

    btnInsert.pack(side=LEFT)
    btnUpdate.pack(side=LEFT, padx=12)
    btnDelete.pack(side=LEFT, padx=12)
    btnBack.pack(side=RIGHT)


# Method for Author Radiobuttons
def authorChoice(authorType):
    selection = authorType.get()
    if selection == 1:
        create_authid.config(state=NORMAL)
        create_groupid.config(state=DISABLED)
    else:
        create_authid.config(state=DISABLED)
        create_groupid.config(state=NORMAL)


# Window for creation of new book record
def createBookWindow():
    global create_bookid
    global create_title
    global create_genre
    global create_price
    global create_stock
    global create_authid
    global create_groupid
    global authorType
    global rbSingle
    global rbMultip

    insertWindow = Toplevel()
    insertWindow.geometry("400x400")
    insertWindow.resizable(False, False)
    insertWindow.grab_set()

    # Insert Entry Frame
    entryPanel = LabelFrame(insertWindow, text="CREATE BOOK RECORD", font=('Inter', 12, 'bold'),
                            padx=20, pady=12)
    entryPanel.pack(pady=(12, 0))

    l1 = Label(entryPanel, text="Book Title:", justify="left")
    l2 = Label(entryPanel, text="Genre:", justify="left")
    l3 = Label(entryPanel, text="Price:", justify="left")
    l4 = Label(entryPanel, text="Stock:", justify="left")
    l5 = Label(entryPanel, text="Author Type:", justify="left")
    l6 = Label(entryPanel, text="Author Name:", justify="left")
    l7 = Label(entryPanel, text="Group Name:", justify="left")

    create_title = Entry(entryPanel, width=24)
    create_genre = Entry(entryPanel, width=24)
    create_price = Entry(entryPanel, width=24)
    create_stock = Entry(entryPanel, width=24)
    create_authid = Entry(entryPanel, width=24)
    create_groupid = Entry(entryPanel, width=24)
    create_authid.config(state=DISABLED)
    create_groupid.config(state=DISABLED)

    authorType = IntVar()
    rbSingle = Radiobutton(entryPanel, text="Single", variable=authorType, value=1,
                           command=lambda: authorChoice(authorType))
    rbMultip = Radiobutton(entryPanel, text="Multi", variable=authorType, value=2,
                           command=lambda: authorChoice(authorType))

    l1.grid(row=1, column=0, pady=4, padx=(0, 16), sticky='w')
    l2.grid(row=2, column=0, pady=4, padx=(0, 16), sticky='w')
    l3.grid(row=3, column=0, pady=4, padx=(0, 16), sticky='w')
    l4.grid(row=4, column=0, pady=4, padx=(0, 16), sticky='w')
    l5.grid(row=5, column=0, columnspan=2, pady=4, padx=(0, 16), sticky='nesw')
    l6.grid(row=7, column=0, pady=4, padx=(0, 16), sticky='w')
    l7.grid(row=8, column=0, pady=4, padx=(0, 16), sticky='w')

    create_title.grid(row=1, column=1, pady=4, sticky='e')
    create_genre.grid(row=2, column=1, pady=4,  sticky='e')
    create_price.grid(row=3, column=1, pady=4, sticky='e')
    create_stock.grid(row=4, column=1, pady=4, sticky='e')
    rbSingle.grid(row=6, column=0, pady=4)
    rbMultip.grid(row=6, column=1, pady=4)
    create_authid.grid(row=7, column=1, pady=4, sticky='e')
    create_groupid.grid(row=8, column=1, pady=4, sticky='e')

    # Create Button Frame
    buttonPanel = Frame(insertWindow)
    buttonPanel.pack(expand=True)

    createButton = Button(buttonPanel, text="Create", width=16, command=bookCreateBtn)
    createButton.grid(row=0, column=0, sticky='nesw', padx=(0, 6), pady=4)
    clearButton = Button(buttonPanel, text="Clear",  width=16, command=clear_entries)
    clearButton.grid(row=0, column=1, sticky='nesw', padx=(6, 0), pady=4)
    cancelButton = Button(buttonPanel, text="Cancel", command=lambda: insertWindow.destroy())
    cancelButton.grid(row=1, column=0, columnspan=2, sticky='nesw', pady=4)


# Creating/Inserting new book records to list and database
def get_author_single_id(cursor, single_name):
    cursor.execute("SELECT AuthorID FROM Author_Single WHERE Single_Name = %s", (single_name,))
    result = cursor.fetchone()
    return result[0] if result else None


def get_author_multi_id(cursor, group_name):
    cursor.execute("SELECT GroupID FROM Author_Multi WHERE Group_Name = %s", (group_name,))
    result = cursor.fetchone()
    return result[0] if result else None


def insert_author_single(cursor, single_name):
    cursor.execute("INSERT INTO Author_Single (Single_Name) VALUES (%s)", (single_name,))
    return cursor.lastrowid


def insert_author_multi(cursor, group_name):
    cursor.execute("INSERT INTO Author_Multi (Group_Name) VALUES (%s)", (group_name,))
    return cursor.lastrowid


def insert_book(cursor, title, genre, price, stock, author_id=None, group_id=None):
    cursor.execute("""
        INSERT INTO Book (Title, Genre, Price, Stock, AuthorID, GroupID)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (title, genre, price, stock, author_id, group_id))
    return cursor.lastrowid


def bookCreateBtn():
    title = create_title.get()
    b_genre = create_genre.get()
    b_price = create_price.get()
    b_stock = create_stock.get()
    b_auth = create_authid.get()
    b_group = create_groupid.get()

    # Check for required fields
    if not title or not b_genre or not b_price or not b_stock or (not b_auth and not b_group):
        messagebox.showwarning("Input Error", "All fields are required.")
        return

    try:
        if authorType.get() == 1:
            author_id = get_author_single_id(mycursor, b_auth)
            if author_id is None:
                author_id = insert_author_single(mycursor, b_auth)
            insert_book(mycursor, title, b_genre, b_price, b_stock, author_id=author_id)
        elif authorType.get() == 2:
            group_id = get_author_multi_id(mycursor, b_group)
            if group_id is None:
                group_id = insert_author_multi(mycursor, b_group)
            insert_book(mycursor, title, b_genre, b_price, b_stock, group_id=group_id)
        else:
            raise ValueError("author_type must be either 'single' or 'multi'")

        messagebox.showinfo("Success", "Record inserted successfully.")
        mydb.commit()
    except Exception as e:
        messagebox.showerror("Error", str(e))
        mydb.rollback()

    clear_entries()
    showBooksMenu()


# For clearing entries in createWindow
def clear_entries():
    create_title.delete(0, END)
    create_genre.delete(0, END)
    create_price.delete(0, END)
    create_stock.delete(0, END)
    create_authid.delete(0, END)
    create_groupid.delete(0, END)
    authorType.set(None)
    create_authid.config(state=DISABLED)
    create_groupid.config(state=DISABLED)


# Updating book records from list and database
def getSelectedBook():
    selected_index = book_records.curselection()
    if selected_index and selected_index[0] > 1:
        selected_book = books[selected_index[0] - 2]  # Adjust for header and separator
        return selected_book
    return None


# Update Book Record Window
def updateBookWindow(book):
    if book is None:
        return

    global updateWindow
    global label_bookid
    global entry_title
    global entry_genre
    global entry_price
    global entry_stock
    global entry_authorid
    global entry_groupid

    updateWindow = Toplevel()
    updateWindow.title("Update Book Record:")
    updateWindow.geometry("400x320")
    updateWindow.resizable(False, False)
    updateWindow.grab_set()

    # Update Entry Frame
    entryPanel = LabelFrame(updateWindow, text="UPDATE BOOK INFORMATION", font=('Inter', 12, 'bold'),
                            padx=20, pady=12)
    entryPanel.pack(pady=(12, 0))

    print(book)
    book_id, title, genre, price, stock, author_id, group_id = book
    l1 = Label(entryPanel, text="Book ID:", justify="left")
    l2 = Label(entryPanel, text="Title:", justify="left")
    l3 = Label(entryPanel, text="Genre:", justify="left")
    l4 = Label(entryPanel, text="Price:", justify="left")
    l5 = Label(entryPanel, text="Stock:", justify="left")
    l6 = Label(entryPanel, text="Author ID:", justify="left")
    l7 = Label(entryPanel, text="Group ID:", justify="left")

    label_bookid = Label(entryPanel, text=book_id)
    entry_title = Entry(entryPanel, width=24)
    entry_title.insert(0, title)
    entry_genre = Entry(entryPanel, width=24)
    entry_genre.insert(0, genre)
    entry_price = Entry(entryPanel, width=24)
    entry_price.insert(0, price)
    entry_stock = Entry(entryPanel, width=24)
    entry_stock.insert(0, stock)
    entry_authorid = Entry(entryPanel, width=24)
    entry_groupid = Entry(entryPanel, width=24)

    l1.grid(row=1, column=0, sticky="w", pady=4, padx=(0, 16))
    l2.grid(row=2, column=0, sticky="w", pady=4, padx=(0, 16))
    l3.grid(row=3, column=0, sticky="w", pady=4, padx=(0, 16))
    l4.grid(row=4, column=0, sticky="w", pady=4, padx=(0, 16))
    l5.grid(row=5, column=0, sticky="w", pady=4, padx=(0, 16))

    label_bookid.grid(row=1, column=1, pady=4)
    entry_title.grid(row=2, column=1, sticky="e", pady=4)
    entry_genre.grid(row=3, column=1, sticky="e", pady=4)
    entry_price.grid(row=4, column=1, sticky="e", pady=4)
    entry_stock.grid(row=5, column=1, sticky="e", pady=4)

    # For Author ID and Group ID
    if author_id is None:
        entry_groupid.insert(0, group_id)
        l7.grid(row=6, column=0, sticky="w", pady=4, padx=(0, 16))
        entry_groupid.grid(row=6, column=1, sticky="e", pady=4)
    elif group_id is None:
        entry_authorid.insert(0, author_id)
        l6.grid(row=6, column=0, sticky="w", pady=4, padx=(0, 16))
        entry_authorid.grid(row=6, column=1, sticky="e", pady=4)

    # Update Button Frame
    buttonPanel = Frame(updateWindow)
    buttonPanel.pack(fill='x', expand=True, padx=50)

    updateButton = Button(buttonPanel, text="Update", width=16, command=bookUpdateBtn)
    updateButton.pack(side='left')
    cancelButton = Button(buttonPanel, text="Cancel", width=16, command=lambda: updateWindow.destroy())
    cancelButton.pack(side='right')


#   Update Book Record Function
def bookUpdateBtn():
    global updateWindow
    global label_bookid
    global entry_title
    global entry_genre
    global entry_price
    global entry_stock
    global entry_authorid
    global entry_groupid

    bookid = label_bookid.cget("text")
    title = entry_title.get()
    genre = entry_genre.get()
    price = entry_price.get()
    stock = entry_stock.get()
    authid = entry_authorid.get()
    groupid = entry_groupid.get()

    # Checks whether an entry box is left empty or not
    if not title or not genre or not price or not stock or (not authid and not groupid):
        messagebox.showwarning("Input Error", "All fields are required.")
        return

    try:
        # For Author ID and Group ID
        if not authid:
            query = ("UPDATE book "
                     "SET Title = %s, Genre = %s, Price = %s, Stock = %s, GroupID = %s "
                     "WHERE BookID = %s;")
            mycursor.execute(query, (title, genre, price, stock, groupid, bookid))
        else:
            query = ("UPDATE book "
                     "SET Title = %s, Genre = %s, Price = %s, Stock = %s, AuthorID = %s "
                     "WHERE BookID = %s;")
            mycursor.execute(query, (title, genre, price, stock, authid, bookid))

        mydb.commit()

        # Log update success
        print(f"Updated book: {bookid} - {title}, {genre}, {price}, {stock}, {groupid if groupid else authid}")

        messagebox.showinfo("Success", "Record updated successfully.")

        updateWindow.destroy()
        showBooksMenu()

    except Exception as e:
        messagebox.showerror("Error", str(e))
        mydb.rollback()


# Deleting book records from list and database
def deleteRec():
    try:
        selected_index = book_records.curselection()

        for index in selected_index:
            selected_item = book_records.get(index)
            book_to_delete = selected_item.split()[0]
            mycursor.execute('DELETE FROM book WHERE BookID = %s', (book_to_delete,))
            mydb.commit()
            book_records.delete(index)

        messagebox.showinfo("Success", "Record(s) deleted successfully.")

    except Exception as e:
        messagebox.showerror("Error", str(e))
        mydb.rollback()


# Show Registered Customers Menu ---------------------------------------------------------------------------------------
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

    # List Box Frame
    panelList = LabelFrame(root, text="REGISTERED CUSTOMER LIST", font=('Inter', 12, 'bold'),
                           padx=20, pady=12)
    panelList.pack(padx=80, pady=(12, 0), fill='both', expand=True)

    # Format Headers
    headers = ["ID", "Last Name", "First Name", "M.I.", "Email", "Phone"]
    max_lengths = [5, 25, 25, 5, 30, 15]
    formatted_headers = "{:<5} {:<25} {:<25} {:<5} {:<30} {:<15}".format(*headers)

    # Customer Listbox
    customer_records = Listbox(panelList, bg="white", font=("Courier New", 10))
    customer_records.insert(0, formatted_headers)
    customer_records.insert(1, "-" * 110)

    for c in customers:
        # Replace None values with empty strings
        c = [truncate_text(str(item), max_lengths[i]) if item is not None else '' for i, item in enumerate(c)]
        formatted_book = "{:<5} {:<25} {:<25} {:<5} {:<30} {:<15}".format(*c)
        customer_records.insert(END, formatted_book)

    customer_records.pack(side='left', fill='both', expand=True)

    # Vertical Scrollbar
    vtScrollBar = Scrollbar(panelList, orient="vertical", command=customer_records.yview)
    vtScrollBar.pack(side="right", fill="y")
    customer_records.configure(yscrollcommand=vtScrollBar.set)

    # Buttons Frame
    panelButton = Frame(root)
    panelButton.pack(fill='x', padx=100, pady=24)

    # Buttons
    btnUpdate = Button(panelButton, text="Update Customer Record", justify=CENTER, width=24,
                       command=lambda: updateCustomerWindow(getSelectedCustomer()))
    btnDelete = Button(panelButton, text="Delete Customer Record", justify=CENTER, width=24,
                       command=lambda: deleteCustomerWindow(getSelectedCustomer()))
    btnBack = Button(panelButton, text="Go back to Main Menu >", justify=CENTER, width=24, command=startMenu)
    btnUpdate.pack(side=LEFT)
    btnDelete.pack(side=LEFT, padx=56)
    btnBack.pack(side=RIGHT)


def getSelectedCustomer():
    selected_index = customer_records.curselection()
    if selected_index and selected_index[0] > 1:
        selected_customer = customers[selected_index[0] - 2]  # Adjust for header and separator
        return selected_customer
    return None


# Update Customer Record Window
def updateCustomerWindow(customer):
    if customer is None:
        return

    global updateWindow
    global label_custid
    global entry_lastname
    global entry_firstname
    global entry_middlein
    global entry_email
    global entry_phone

    updateWindow = Toplevel()
    updateWindow.title("Update Customer Record:")
    updateWindow.geometry("400x320")
    updateWindow.resizable(False, False)
    updateWindow.grab_set()

    # Update Entry Frame
    entryPanel = LabelFrame(updateWindow, text="UPDATE CUSTOMER INFORMATION", font=('Inter', 12, 'bold'),
                            padx=20, pady=12)
    entryPanel.pack(pady=(12, 0))

    customer_id, last_name, first_name, middle_in, email, phone = customer
    l1 = Label(entryPanel, text="Customer ID:", justify="left")
    l2 = Label(entryPanel, text="Last Name:", justify="left")
    l3 = Label(entryPanel, text="First Name:", justify="left")
    l4 = Label(entryPanel, text="Middle Initial:", justify="left")
    l5 = Label(entryPanel, text="E-mail:", justify="left")
    l6 = Label(entryPanel, text="Phone No:", justify="left")

    label_custid = Label(entryPanel, text=customer_id)
    entry_lastname = Entry(entryPanel, width=24)
    entry_lastname.insert(0, last_name)
    entry_firstname = Entry(entryPanel, width=24)
    entry_firstname.insert(0, first_name)
    entry_middlein = Entry(entryPanel, width=24)
    entry_middlein.insert(0, middle_in)
    entry_email = Entry(entryPanel, width=24)
    entry_email.insert(0, email)
    entry_phone = Entry(entryPanel, width=24)
    entry_phone.insert(0, phone)

    l1.grid(row=1, column=0, sticky="w", pady=4, padx=(0, 16))
    l2.grid(row=2, column=0, sticky="w", pady=4, padx=(0, 16))
    l3.grid(row=3, column=0, sticky="w", pady=4, padx=(0, 16))
    l4.grid(row=4, column=0, sticky="w", pady=4, padx=(0, 16))
    l5.grid(row=5, column=0, sticky="w", pady=4, padx=(0, 16))
    l6.grid(row=6, column=0, sticky="w", pady=4, padx=(0, 16))

    label_custid.grid(row=1, column=1, pady=4)
    entry_lastname.grid(row=2, column=1, sticky="e", pady=4)
    entry_firstname.grid(row=3, column=1, sticky="e", pady=4)
    entry_middlein.grid(row=4, column=1, sticky="e", pady=4)
    entry_email.grid(row=5, column=1, sticky="e", pady=4)
    entry_phone.grid(row=6, column=1, sticky="e", pady=4)

    # Update Button Frame
    buttonPanel = Frame(updateWindow)
    buttonPanel.pack(fill='x', expand=True, padx=50)

    updateButton = Button(buttonPanel, text="Update", width=16, command=custUpdateBtn)
    updateButton.pack(side='left')
    cancelButton = Button(buttonPanel, text="Cancel", width=16, command=lambda: updateWindow.destroy())
    cancelButton.pack(side='right')


#   Update Customer Record Function
def custUpdateBtn():
    global updateWindow
    global label_custid
    global entry_lastname
    global entry_firstname
    global entry_middlein
    global entry_email
    global entry_phone

    cusid = label_custid.cget("text")
    fname = entry_lastname.get()
    lname = entry_firstname.get()
    mname = entry_middlein.get()
    email = entry_email.get()
    phone = entry_phone.get()

    # Checks whether an entry box is left empty or not
    if not fname or not lname or not mname or not email or not phone:
        messagebox.showwarning("Input Error", "All fields are required.")
        return

    try:
        query = ("UPDATE customer "
                 "SET Last_name = %s, First_name = %s, Middle_in = %s, Email = %s, Phone = %s "
                 "WHERE CustomerID = %s;")
        mycursor.execute(query, (lname, fname, mname, email, phone, cusid))
        mydb.commit()

        print(cusid, lname, mname, email, phone, cusid)
        messagebox.showinfo("Success", "Record updated successfully.")
    except Exception as e:
        messagebox.showerror("Error", str(e))
        mydb.rollback()

    updateWindow.destroy()
    showCustomerMenu()


#   Delete Customer Record Window
def deleteCustomerWindow(customer):
    if customer is None:
        return

    global deleteWindow
    global label_custid

    deleteWindow = Toplevel()
    deleteWindow.title("Delete Customer Record:")
    deleteWindow.geometry("400x352")
    deleteWindow.resizable(False, False)
    deleteWindow.grab_set()

    # Update Entry Frame
    entryPanel = LabelFrame(deleteWindow, text="DELETE CUSTOMER INFORMATION", font=('Inter', 12, 'bold'),
                            padx=20, pady=12)
    entryPanel.pack(pady=(12, 0))

    confirmMessage1 = Message(entryPanel,
                              text="You are about to delete the following customer information from the database "
                                   "and all of their Transaction History:",
                              justify=LEFT,
                              width=290)
    confirmMessage2 = Message(entryPanel,
                              text="Would you like to continue this Deletion of the customer information?",
                              justify=LEFT,
                              width=290)

    customer_id, last_name, first_name, middle_in, email, phone = customer
    l1a = Label(entryPanel, text="Customer ID:", justify="left")
    l2a = Label(entryPanel, text="Last Name:", justify="left")
    l3a = Label(entryPanel, text="First Name:", justify="left")
    l4a = Label(entryPanel, text="Middle I.:", justify="left")
    l5a = Label(entryPanel, text="E-mail:", justify="left")
    l6a = Label(entryPanel, text="Phone No:", justify="left")

    label_custid = Label(entryPanel, text=customer_id, justify="left")
    l2b = Label(entryPanel, text=last_name, justify="left")
    l3b = Label(entryPanel, text=first_name, justify="left")
    l4b = Label(entryPanel, text=middle_in, justify="left")
    l5b = Label(entryPanel, text=email, justify="left")
    l6b = Label(entryPanel, text=phone, justify="left")

    confirmMessage1.grid(row=0, column=0, rowspan=2, columnspan=3, pady=(0, 8), sticky='w')
    l1a.grid(row=2, column=0, sticky='w')
    l2a.grid(row=3, column=0, sticky='w')
    l3a.grid(row=4, column=0, sticky='w')
    l4a.grid(row=5, column=0, sticky='w')
    l5a.grid(row=6, column=0, sticky='w')
    l6a.grid(row=7, column=0, sticky='w')
    label_custid.grid(row=2, column=1, sticky='w')
    l2b.grid(row=3, column=1, sticky='w')
    l3b.grid(row=4, column=1, sticky='w')
    l4b.grid(row=5, column=1, sticky='w')
    l5b.grid(row=6, column=1, sticky='w')
    l6b.grid(row=7, column=1, sticky='w')
    confirmMessage2.grid(row=8, column=0, rowspan=2, columnspan=3, pady=(8, 0), sticky='w')

    # Delete Button Frame
    buttonPanel = Frame(deleteWindow)
    buttonPanel.pack(fill='x', expand=True, padx=50)

    deleteButton = Button(buttonPanel, text="Delete", width=16, command=custDeleteBtn)
    deleteButton.pack(side='left')
    cancelButton = Button(buttonPanel, text="Cancel", width=16, command=lambda: deleteWindow.destroy())
    cancelButton.pack(side='right')


#   Delete Customer Record Function
def custDeleteBtn():
    global deleteWindow
    global label_custid

    cusid = label_custid.cget("text")
    print(f"Attempting to delete CustomerID: {cusid}")  # Debugging print

    try:
        query = ("ALTER TABLE orders "
                 "DROP FOREIGN KEY orders_ibfk_1;"
                 "ALTER TABLE orders "
                 "ADD CONSTRAINT orders_ibfk_1 FOREIGN KEY (CustomerID) "
                 "REFERENCES customer(CustomerID) ON DELETE CASCADE;")
        mycursor.execute(query, (cusid,))
        mydb.commit()
        messagebox.showinfo("Success", "Record deleted successfully.")
        print(f"CustomerID {cusid} deleted successfully.")  # Debugging print
    except Exception as e:
        messagebox.showerror("Error", str(e))
        mydb.rollback()
        print(f"Error deleting CustomerID {cusid}: {e}")  # Debugging print

    deleteWindow.destroy()
    showCustomerMenu()


# Show Transaction History Menu ----------------------------------------------------------------------------------------
def showTransaction():
    clear_window()
    appWidth = 1080
    appHeight = 480
    x = (root.winfo_screenwidth() / 2) - (appWidth / 2)
    y = (root.winfo_screenheight() / 2) - (appHeight / 2)
    root.geometry(f'{appWidth}x{appHeight}+{int(x)}+{int(y)}')

    root.pack_propagate(False)  # Prevent resizing based on content

    # List Box Frame
    panelList = LabelFrame(root, text="CUSTOMER'S TRANSACTION HISTORY", font=('Inter', 12, 'bold'),
                           padx=20, pady=12)
    panelList.pack(padx=80, pady=(12, 0), fill='both', expand=True)

    # CustomerID entry and Show buttons frame
    show = Frame(panelList)
    show.pack(pady=10, anchor='n')

    customer_label = Label(show, text="Customer ID:")
    customer_label.pack(side=LEFT)

    customer_entry = Entry(show)
    customer_entry.pack(side=LEFT, padx=10)

    show_specific = Button(show, text="Show", command=lambda: show_customer_history(customer_entry.get()),
                           width=13, height=1)
    show_specific.pack(side=LEFT)

    show_all = Button(show, text="Show All", command=show_all_history, width=13, height=1)
    show_all.pack(side=LEFT, padx=10)

    global history_listbox
    history_listbox = Listbox(panelList, bg="white", font=("Courier New", 10))
    history_listbox.pack(side=LEFT, fill='both', expand=True)

    # Vertical Scrollbar
    vtScrollBar = Scrollbar(panelList, orient="vertical", command=history_listbox.yview)
    vtScrollBar.pack(side=RIGHT, fill="y")
    history_listbox.configure(yscrollcommand=vtScrollBar.set)

    # Back to Main Menu and Refund button frame
    panelButton = Frame(root)
    panelButton.pack(side=BOTTOM, fill='x', padx=100, pady=24)

    btnBack = Button(panelButton, text="Go back to Main Menu >", justify=CENTER, width=24, command=startMenu)
    btnBack.pack(side=RIGHT)


# Function to get specific customer transaction history
def show_customer_history(customer_id):
    query = '''
        SELECT c.Last_name, c.First_name, c.Middle_in, o.OrderID, b.Title, od.Quantity, p.Amount, o.OrderDate
        FROM customer c
        JOIN orders o ON c.CustomerID = o.CustomerID
        JOIN orderdetail od ON o.OrderID = od.OrderID
        JOIN book b ON od.BookID = b.BookID
        JOIN payment p ON o.OrderID = p.OrderID
        WHERE c.CustomerID = %s
        ORDER BY o.OrderDate DESC
        '''
    mycursor.execute(query, (customer_id,))

    transactions = mycursor.fetchall()

    # Clear the listbox before inserting new data
    history_listbox.delete(0, END)

    # Add headers to the listbox
    headers = ["Last Name", "First Name", "MI", "Order ID", "Book Title", "Qty", "Amount", "Order Date"]
    max_lengths = [15, 15, 3, 10, 30, 5, 10, 15]
    formatted_headers = "{:<15} {:<15} {:<3} {:<10} {:<30} {:<5} {:<10} {:<15}".format(*headers)
    history_listbox.insert(0, formatted_headers)
    history_listbox.insert(1, "-" * 120)

    # Insert transaction data into the listbox
    for t in transactions:
        t = [truncate_text(str(item), max_lengths[i]) if item is not None else '' for i, item in enumerate(t)]
        formatted_transaction = "{:<15} {:<15} {:<3} {:<10} {:<30} {:<5} {:<10} {:<15}".format(
            t[0], t[1], t[2], t[3], t[4], t[5], t[6], str(t[7]))
        history_listbox.insert(END, formatted_transaction)


# Function to fetch all transaction history
def show_all_history():
    query = '''
        SELECT c.Last_name, c.First_name, c.Middle_in, o.OrderID, b.Title, od.Quantity, p.Amount, o.OrderDate
        FROM customer c
        JOIN orders o ON c.CustomerID = o.CustomerID
        JOIN orderdetail od ON o.OrderID = od.OrderID
        JOIN book b ON od.BookID = b.BookID
        JOIN payment p ON o.OrderID = p.OrderID
        ORDER BY o.OrderDate DESC
        '''
    mycursor.execute(query)

    transactions = mycursor.fetchall()

    # Clear the listbox before inserting new data
    history_listbox.delete(0, END)

    # Add headers to the listbox
    headers = ["Last Name", "First Name", "MI", "Order ID", "Book Title", "Qty", "Amount", "Order Date"]
    max_lengths = [15, 15, 3, 10, 30, 5, 10, 15]
    formatted_headers = "{:<15} {:<15} {:<3} {:<10} {:<30} {:<5} {:<10} {:<15}".format(*headers)
    history_listbox.insert(0, formatted_headers)
    history_listbox.insert(1, "-" * 120)

    # Insert transaction data into the listbox
    for t in transactions:
        t = [truncate_text(str(item), max_lengths[i]) if item is not None else '' for i, item in enumerate(t)]
        formatted_transaction = "{:<15} {:<15} {:<3} {:<10} {:<30} {:<5} {:<10} {:<15}".format(
            t[0], t[1], t[2], t[3], t[4], t[5], t[6], str(t[7]))
        history_listbox.insert(END, formatted_transaction)


# Main Configuration of the System -------------------------------------------------------------------------------------
root = Tk()
root.title("Bookshop Database")
appWidth = 240
appHeight = 120
x = (root.winfo_screenwidth() / 2) - (appWidth / 2)
y = (root.winfo_screenheight() / 2) - (appHeight / 2)
root.geometry(f'{appWidth}x{appHeight}+{int(x)}+{int(y)}')
root.columnconfigure(0, weight=1)

mydb = mysql.connector.connect(
    host='localhost',
    user='root',
    password='reindf_010604',
    port='3306',
    database='imdb'
)
root.columnconfigure(1, weight=3)
mycursor = mydb.cursor()


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
