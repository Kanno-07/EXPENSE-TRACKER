from tkinter import *
from tkinter import ttk
import datetime as dt
from database import Database
from tkinter import messagebox

# Initialize database connection
data = Database(db='myexpense.db')

count = 0
selected_rowid = 0

# Function to save record to the database
def saveRecord():
    global data
    data.insertRecord(item_name=item_name.get(), item_price=item_amt.get(), purchase_date=transaction_date.get())

# Function to set current date in the transaction_date entry
def setDate():
    date = dt.datetime.now()
    dopvar.set(f'{date:%d %B %Y}')

# Function to clear all input entries
def clearEntries():
    item_name.delete(0, 'end')
    item_amt.delete(0, 'end')
    transaction_date.delete(0, 'end')

# Function to fetch records from the database and display them in the treeview
def fetch_records():
    f = data.fetchRecord('SELECT rowid, * FROM expense_record')
    global count
    for rec in f:
        tv.insert(parent='', index='0', iid=count, values=(rec[0], rec[1], rec[2], rec[3]))
        count += 1
    tv.after(400, refreshData)

# Function to select a record from the treeview for editing
def select_record(event):
    global selected_rowid
    selected = tv.focus()
    val = tv.item(selected, 'values')

    try:
        selected_rowid = val[0]
        d = val[3]
        namevar.set(val[1])
        amtvar.set(val[2])
        dopvar.set(str(d))
    except Exception as ep:
        pass

# Function to update a record in the database and treeview
def update_record():
    global selected_rowid
    selected = tv.focus()

    try:
        data.updateRecord(namevar.get(), amtvar.get(), dopvar.get(), selected_rowid)
        tv.item(selected, text="", values=(namevar.get(), amtvar.get(), dopvar.get()))
    except Exception as ep:
        messagebox.showerror('Error', ep)

    # Clear entry boxes
    clearEntries()
    tv.after(400, refreshData)

# Function to calculate total balance
def totalBalance():
    f = data.fetchRecord(query="SELECT sum(item_price) FROM expense_record")
    for i in f:
        for j in i:
            messagebox.showinfo('Current Balance: ', f"Total Expense: {j} \nBalance Remaining: {5000 - j}")

# Function to refresh the treeview data
def refreshData():
    for item in tv.get_children():
        tv.delete(item)
    fetch_records()

# Function to delete a selected row from the database and refresh the treeview
def deleteRow():
    global selected_rowid
    data.removeRecord(selected_rowid)
    refreshData()

# Initialize the main window
ws = Tk()
ws.title('Office Expense')

# Define fonts and variables
f = ('Times New Roman', 14)
namevar = StringVar()
amtvar = IntVar()
dopvar = StringVar()

# Frame widgets
f2 = Frame(ws)
f2.pack()

f1 = Frame(ws, padx=10, pady=10)
f1.pack(expand=True, fill=BOTH)

# Label widgets
Label(f1, text='ITEM NAME', font=f).grid(row=0, column=0, sticky=W)
Label(f1, text='ITEM PRICE', font=f).grid(row=1, column=0, sticky=W)
Label(f1, text='PURCHASE DATE', font=f).grid(row=2, column=0, sticky=W)

# Entry widgets
item_name = Entry(f1, font=f, textvariable=namevar)
item_amt = Entry(f1, font=f, textvariable=amtvar)
transaction_date = Entry(f1, font=f, textvariable=dopvar)

# Entry grid placement
item_name.grid(row=0, column=1, sticky=EW, padx=(10, 0))
item_amt.grid(row=1, column=1, sticky=EW, padx=(10, 0))
transaction_date.grid(row=2, column=1, sticky=EW, padx=(10, 0))

# Action buttons
cur_date = Button(f1, text='Current Date', font=f, bg='#04C4D9', command=setDate, width=15)
submit_btn = Button(f1, text='Save Record', font=f, command=saveRecord, bg='#42602D', fg='white')
clr_btn = Button(f1, text='Clear Entry', font=f, command=clearEntries, bg='#D9B036', fg='white')
quit_btn = Button(f1, text='Exit', font=f, command=ws.quit, bg='#D33532', fg='white')
total_bal = Button(f1, text='Total Balance', font=f, bg='#486966', fg='white', command=totalBalance)
update_btn = Button(f1, text='Update', font=f, bg='#C2BB00', fg='white', command=update_record)
del_btn = Button(f1, text='Delete', font=f, bg='#BD2A2E', fg='white', command=deleteRow)

# Button grid placement
cur_date.grid(row=3, column=1, sticky=EW, padx=(10, 0))
submit_btn.grid(row=0, column=2, sticky=EW, padx=(10, 0))
clr_btn.grid(row=1, column=2, sticky=EW, padx=(10, 0))
quit_btn.grid(row=2, column=2, sticky=EW, padx=(10, 0))
total_bal.grid(row=0, column=3, sticky=EW, padx=(10, 0))
update_btn.grid(row=1, column=3, sticky=EW, padx=(10, 0))
del_btn.grid(row=2, column=3, sticky=EW, padx=(10, 0))

# Treeview to display the record
tv = ttk.Treeview(f2, selectmode='browse', columns=(1, 2, 3, 4), show='headings', height=8)
tv.pack(side="left")

tv.column(1, anchor=CENTER, stretch=NO, width=70)
tv.column(2, anchor=CENTER)
tv.column(3, anchor=CENTER)
tv.column(4, anchor=CENTER)
tv.heading(1, text="Serial no")
tv.heading(2, text="Item Name")
tv.heading(3, text="Item Price")
tv.heading(4, text="Purchase Date")

# Scrollbar widget
scrollbar = Scrollbar(f2, orient='vertical')
scrollbar.configure(command=tv.yview)
scrollbar.pack(side="right", fill="y")
tv.config(yscrollcommand=scrollbar.set)

# Bind the select_record function to treeview selection
tv.bind("<ButtonRelease-1>", select_record)

# Start the infinite loop
ws.mainloop()
