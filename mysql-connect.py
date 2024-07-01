import mysql.connector
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
# Create/Insert new Book Record
# Update a Book Record
# Delete a Book Record
# Print Book Records (Inventory?) List
# Print Registered Customer List
# Print Customer Transaction History


root = Tk()
root.title("Try")
root.geometry("240x120")
mydb = mysql.connector.connect(
    host='localhost',
    user='root',
    password='l0v3tt3LAFT!!',
    port='3306',
    database='imdb'
)

root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=3)
mycursor = mydb.cursor()

def showbooks():
    clear_window()
    root.geometry("300x300")
    mycursor.execute('SELECT * from book')
    books = mycursor.fetchall()
    book_id = [book[0] for book in books]
    titles = [book[1] for book in books]
    genres = [book[2] for book in books]
    prices = [book[3] for book in books]
    stocks = [book[4] for book in books]
    author_id = [book[5] for book in books]
    group_id = [book[6] for book in books]

    bookrecords = Listbox(root, height=20, width=100, bg="white")
    for i in range(len(books)):
        bookrecords.insert(i, str(book_id[i])+ "    " +str(titles[i]) + "   " + str(genres[i]) + "   " + str(prices[i]) + "   " + str(stocks[i]))

    bookrecords.grid(row=0)
#def showcustomers():

#def showtrans():


def start():
    root.geometry("240x200")
    title = Label(root, text="Bookshop Database")
    showb = Button(root, text="Show Book Records", command=showbooks)
    showc = Button(root, text="Show Registered Customers" )#
    showt = Button(root, text="Show Customer Transaction History")#, command=showtrans
    title.grid(row=0, column=0, columnspan=2, sticky='news')
    showb.grid(row=1, column=0, columnspan=2, pady=5, padx=5)
    showc.grid(row=2, column=0, columnspan=2, pady=5, padx=5)
    showt.grid(row=3, column=0, columnspan=2, pady=5, padx=5)

def clear_window():
    for widget in root.winfo_children():
        widget.destroy()
    start()

def login():
    mycursor.execute('SELECT * FROM staff WHERE username = %s AND passw = %s', (username.get(),password.get()))
    result = mycursor.fetchone()
    if result:
        messagebox.showinfo("Message", "Login Success!")
        clear_window()
    else:
        messagebox.showwarning("Access Denied", "Invalid Credentials!")

title=Label(root, text="Bookshop Database")
l1 = Label(root, text="Username:")
l2 = Label(root, text="Password:")

username = Entry(root)
password = Entry(root, show="*")

log = Button(root, text="Login", command=login)

title.grid(row=0, column=0, columnspan=2, sticky='news')
l1.grid(row=1, column=0, sticky=W, padx=5, pady=5)
username.grid(row=1, column=1, sticky=E, padx=5, pady=5)
l2.grid(row=2, column=0, sticky=W, padx=5, pady=5)
password.grid(row=2, column=1, sticky=E, padx=5, pady=5)
log.grid(row=3, column=1, sticky=E, padx=5, pady=5)

mainloop()