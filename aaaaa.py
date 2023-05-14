import tkinter as tk
import sqlite3
from tkinter import ttk
from tkinter import * # type: ignore
from tkinter import messagebox
import requests
import math
from tkcalendar import DateEntry
import math
from tkinter.scrolledtext import ScrolledText
ltt = []
check, total, z = 0, 0, 0
list1 = []
listv = []
table_name = "expense_tracker"
conn = sqlite3.connect("Database\\ExpenseTracker.db")
cur = conn.cursor()

# Create the main window
tot = 0
cur.execute("SELECT Amount_Paid FROM " + table_name)
amt = cur.fetchall()
for amount in amt:
    tot += int(amount[0])
root = tk.Tk()
root.title("NBN FINANCE TRACKER")

# Set the size of the window
root.geometry("660x600")
root.configure(background="#191919")
root.resizable(False, False)

# Create a new style for the window background
style = ttk.Style(root)
style.configure("TFrame", background="#191919")

# Create a label for the title
title_label = ttk.Label(root, text="NBN FINANCE TRACKER", font=("TkDefaultFont", 40), background="#191919" , foreground="white")
title_label.pack()

# Create a label for the total expense
total_expense_label = ttk.Label(root, text="Total Expense: Rs."+ str(tot), font=("TkDefaultFont", 16), background="#191919" , foreground="white")
total_expense_label.pack(pady=20)

# Create a style for the buttons
style = ttk.Style()
style.configure("TButton", font=("TkDefaultFont", 12), padding=10 ,background="#191919")

# Create a style for the hover effect
style.map("TButton",
          foreground=[("active", "blue")],
          background=[("active", "!disabled", "light blue")])
# Create a frame to hold the buttons
button_frame = ttk.Frame(root)
button_frame.pack()

# Define a global variable to store the total expense
def submit(data_list):
    check = 0
    for i in data_list:
        if i.get() == "":
            pass
        else:
            check += 1
    try:
        if check == 4:
            global total
            conn = sqlite3.connect(r"Database\ExpenseTracker.db")
            cur = conn.cursor()
            cur.execute("INSERT INTO " + str(
                table_name) + " VALUES (:Date_Of_Payment,:Method_of_Payment,:Paid_To,:Description,:Amount_Paid)",
                        {'Date_Of_Payment': (data_list[0]).get(),'Method_of_Payment':Method_Of_Payment_Entry.get(),
                         'Paid_To': (data_list[1]).get(), 'Description': (data_list[2]).get(),
                         'Amount_Paid': float(data_list[3].get())})
            conn.commit()
            messagebox.showinfo("Success", "Successfully added the record to the database")
            for i in data_list:
                i.delete(0, END)
            tot = 0
            cur.execute("SELECT Amount_Paid FROM " + table_name)
            amt = cur.fetchall()
            for amount in amt:
                tot += amount[0]
            global total_expense
            total_expense = str(tot)
            root.title("Current Total Expense : Rupees " + total_expense)
            conn.close()
        else:
            messagebox.showwarning("WARNING!", "One or more than one fields are empty\nPlease Check Again")
            pass
    except(ValueError):
        messagebox.showwarning("WARNING!", "Amount Paid must be integer number\nPlease Check Again")

    new_screen.destroy()
    new_Records()



def manage():
    # initialize global variables
    global win
    global lt
    global lst
    global n

def select():
    global p
    global z
    global listv
    listv = []
    m = 0
    selection = my_tree.focus()
    name_box1.delete(0, END)
    name_box3.delete(0, END)
    name_box4.delete(0, END)
    name_box5.delete(0, END)

    values = my_tree.item(selection, 'values')
    if selection == "":
        messagebox.showwarning("Attention", "You must select atleast one record to perform this action")
    else:
        for k in range(0, 5):
            listv.append(values[k])

        try:
            name_box1.insert(0, values[0])
            name_box2.set(values[1])
            name_box3.insert(0, values[2])
            name_box4.insert(0, values[3])
            name_box5.insert(0, values[4])
            z = 1
        except(IndexError):
            pass

def update1():
    global p
    global z
    global listv
    m = 0
    selection = my_tree.focus()
    if [name_box1.get(), name_box2.get(), name_box3.get(), name_box4.get(), str(name_box5.get())] == listv:
        messagebox.showinfo("Attention", "Seems as if you didn't make any change to the existing record")
    else:
        if z == 1 and selection != "":
            z = 0
            try:
                conn = sqlite3.connect(r"Database\ExpenseTracker.db")
                cur = conn.cursor()
                selection = my_tree.focus()
                values = my_tree.item(selection, text="", values=(
                name_box1.get(), name_box2.get(), name_box3.get(), name_box4.get(), name_box5.get()))
                x = my_tree.selection()
                for record in x:
                    cur.execute("UPDATE " + str(
                    table_name) + " SET Date_Of_Payment = '"+str(name_box1.get()) + "' , Method_of_Payment = '"+str(name_box2.get()) +"' , Paid_To = '"+ str(name_box3.get())+"' , Description = '"+str(name_box4.get())+"' , Amount_Paid = "+str(name_box5.get())+" WHERE oid = " + str(ltt[(int(record) - 1)])+" ;")

                name_box1.delete(0, END)
                name_box3.delete(0, END)
                name_box4.delete(0, END)
                name_box5.delete(0, END)
                tot = 0
                cur.execute("SELECT Amount_Paid FROM " + table_name)
                amt = cur.fetchall()
                for amount in amt:
                    tot += amount[0]
                root.title("Current Total Expense : Rupees " + str(tot))
                conn.commit()
                conn.close()
            except(sqlite3.OperationalError):
                messagebox.showwarning("WARNING!", "Amount Paid must be a number\nPlease Check Again")
        else:
            messagebox.showwarning("Attention", "Seems You didn't select any record\nPlease Check Again")


def remove():
    ch = 0
    conn = sqlite3.connect(r"Database\ExpenseTracker.db")
    cur = conn.cursor()
    x = my_tree.selection()

    for record in x:

        cur.execute("DELETE FROM " + str(table_name) + " WHERE oid=" + str(ltt[(int(record) - 1)]))
        my_tree.delete(record)
        ch += 1
    if ch == 0:
        messagebox.showwarning("Attention", "You must select atleast one record to perform this action")
    tot = 0
    cur.execute("SELECT Amount_Paid FROM " + table_name)
    amt = cur.fetchall()
    for amount in amt:
        tot += int(amount[0])

    root.title("Current Total Expense : Rupees " + str(tot))
    conn.commit()
    conn.close()

def change():
    _i = 0
    _n = 0
    global table_name
    tempp = 0

    for _i in range(0, len(lst)):                                                                                                                                                                                                 # type: ignore

        if (lt[_i].get()) == 1:                                                                                                                                                                                                                      # type: ignore
            table_name = lst[_n]                                                                                                                                                                                                                   # type: ignore
            messagebox.showinfo("SUCCESS", "The current table has been changed to- '" + table_name + "'")
            entry = StringVar()
            _entry.set("Current Table(in use): " + table_name)                                                                                                                                                                                                          # type: ignore
            Entry(root, width=35, textvariable=_entry, state=DISABLED, relief=SOLID, bg="black", fg="white").place(                                                                                                                                                                                                                                                 # type: ignore
                x=265, y=100)
            tot = 0
            cur.execute("SELECT Amount_Paid FROM " + table_name)
            amt = cur.fetchall()
            for amount in amt:
                tot += int(amount[0])
            root.title("Current Total Expense : Rupees " + str(tot))

            tempp += 1
            break

        _n += 1
    if tempp == 0:
        messagebox.showwarning("WARNING", "SELECT ATLEAST ONE TABLE TO WORK ON")
        win.destroy()                                                                                                                                                                                                                              # type: ignore
        manage()
    else:
        win.destroy()                                                                                                                                                                                                                            # type: ignore
        tot = 0
        cur.execute("SELECT Amount_Paid FROM " + table_name)
        amt = cur.fetchall()
        for amount in amt:
            tot += int(amount[0])
            root.title("Current Total Expense : Rupees " + str(tot))


def new_Records():
    global new_screen
    global Method_Of_Payment_Entry

    new_screen = Toplevel(root)
    new_screen.iconbitmap(r'ex.ico')
    new_screen.title("New Records")
    new_screen.resizable(False, False)
    Amount_Paid = DoubleVar()
    Date_Of_Payment_Entry = DateEntry(new_screen, width=12,
background='darkblue', foreground='white', borderwidth=2)

    Date_Of_Payment_Entry.grid(row=0, column=1, padx=20)
    Method_Of_Payment_Entry=StringVar()
    Method_Of_Payment_Entry.set("CASH")
    OptionMenu(new_screen,Method_Of_Payment_Entry,"CASH","CARD","PAYTM","CHEQUE","ONLINE TRANSACTION").grid(padx=30,row=1, column=1)

    Paid_To_Entry = Entry(new_screen, width=30)
    Paid_To_Entry.grid(row=2, column=1)
    Description_Entry = Entry(new_screen, width=30)
    Description_Entry.grid(row=3, column=1)
    Amount_Paid_Entry = Entry(new_screen, width=30, textvariable=Amount_Paid)
    Amount_Paid_Entry.grid(row=4, column=1)

    Date_Of_Payment_Label = Label(new_screen, text="Date Of Payment\n (MM\DD\YY)").grid(row=0, column=0)                                                                                                                                                                                                                  # type: ignore
    Method_Of_Payment_Label = Label(new_screen, text="Method Of Payment\n").grid(row=1, column=0)
    Paid_To_Label = Label(new_screen, text="Paid To").grid(row=2, column=0)
    Description_Label = Label(new_screen, text="Description").grid(row=3, column=0)
    Amount_Paid_Label = Label(new_screen, text="Amount Paid(In Rupees)").grid(row=4, column=0)

    _list = [Date_Of_Payment_Entry, Paid_To_Entry, Description_Entry, Amount_Paid_Entry]

    conn = sqlite3.connect(r"Database\ExpenseTracker.db")
    cur = conn.cursor()
    submit_btn = Button(new_screen, text="Add Record to Database", command=lambda: submit(_list)).grid(row=5, column=0,columnspan=2,pady=10, padx=10,ipadx=100)
    conn.commit()
    conn.close()
    new_screen.mainloop()

def previous_Records():
    global new_screen1
    global my_tree
    global p
    global name_box1
    global name_box2
    global name_box3
    global name_box4
    global name_box5
    global name_box
    global ltt
    ltt = []

    new_screen1 = Toplevel(root)
    new_screen1.iconbitmap(r'ex.ico')
    new_screen1.title("Previous Records")
    new_screen1.resizable(False, False)

    conn = sqlite3.connect(r"Database\ExpenseTracker.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM " + table_name)
    records = cur.fetchall()
    cur.execute("SELECT oid FROM " + table_name)
    rec = cur.fetchall()

    for recc in rec:

        ltt.append(recc[0])
    style = ttk.Style(root)
    style.configure("Treeview", background="white", foreground="black", rowheight=25, fieldbackground="white")
    style.map('Treeview', background=[('selected', 'green')])

    tree_scroll = Scrollbar(new_screen1)
    tree_scroll.pack(side=RIGHT, fill=Y)

    my_tree = ttk.Treeview(new_screen1, yscrollcommand=tree_scroll.set)

    tree_scroll.config(command=my_tree.yview)

    my_tree.tag_configure("oddrow", background="WHITE")
    my_tree.tag_configure("evenrow", background="lightblue")
    my_tree['columns'] = ('Date Of Payment', 'Method Of Payment', 'Paid To', 'Description', 'Amount Paid(In Rupees)')
    my_tree.column("#0", width=0, anchor=W, minwidth=0, stretch=NO)
    my_tree.column("Date Of Payment", width=150, anchor=W, minwidth=25 )
    my_tree.column("Method Of Payment", width=150, anchor=W, minwidth=25)
    my_tree.column("Paid To", width=150, anchor=W, minwidth=25)
    my_tree.column("Description", width=150, anchor=W, minwidth=50)
    my_tree.column("Amount Paid(In Rupees)", width=150, anchor=W, minwidth=25)

    my_tree.heading("#0", text="Label", anchor=W)
    my_tree.heading("Date Of Payment", text="Date Of Payment (MM/DD/YY)", anchor=W)
    my_tree.heading("Method Of Payment", text="Method Of Payment", anchor=W)
    my_tree.heading("Paid To", text="Paid To", anchor=W)
    my_tree.heading("Description", text="Description", anchor=W)
    my_tree.heading("Amount Paid(In Rupees)", text="Amount Paid(In Rupees)", anchor=W)

    p, q = 1, 0
    for record in records:
        if p % 2 == 0:
            my_tree.insert(parent='', index='end', iid=p, text='Parent', values=record, tags=('evenrow',))                                                                                                                                                                                                              # type: ignore
        else:
            my_tree.insert(parent='', index='end', iid=p, text='Parent', values=record, tags=('oddrow',))                                                                                                                                                                                                                # type: ignore

        p += 1
    my_tree.pack(padx=10, ipadx=50, ipady=20)
    Button(new_screen1, text="DELETE THE SELECTED RECORD", bg="red", font=("BOLD", 15), command=remove).pack(padx=10,
                                                                                                             pady=10,
                                                                                                             ipadx=220)
    Label(new_screen1, text="UPDATE RECORDS :-", font=("BOLD", 15)).pack(pady=10)
    add_frame = Frame(new_screen1)
    add_frame.pack(pady=10, ipady=10)

    Button(new_screen1, text="PRESS THIS BUTTON TO EDIT THE SELECTED RECORD", bg="yellow", command=select).pack(padx=30,
                                                                                                                pady=10,
                                                                                                                ipadx=100)

    Button(new_screen1, text="UPDATE RECORD", bg="blue", font=("BOLD", 15), command=update1).pack(padx=25, pady=10,
                                                                                                 ipadx=300)

    n1 = Label(add_frame, text="Date Of Payment (MM/DD/YY)")
    n1.grid(row=1, column=0)
    n2 = Label(add_frame, text="Method Of Payment")
    n2.grid(row=1, column=1)
    n3 = Label(add_frame, text="Paid To")
    n3.grid(row=1, column=2)
    n4 = Label(add_frame, text="Description")
    n4.grid(row=1, column=3)
    n5 = Label(add_frame, text="Amount Paid")
    n5.grid(row=1, column=4)

    name_box = IntVar()
    name_box.set("")                                                                                                                                                                                                                                                                                          # type: ignore
    name_box1 = DateEntry(add_frame,
background='darkblue', foreground='white', borderwidth=2)
    name_box1.grid(row=2, column=0)

    name_box2 = StringVar()
    name_box2.set("CASH")
    OptionMenu(add_frame, name_box2,"CASH","CARD","PAYTM","CHEQUE","ONLINE TRANSACTION").grid(row=2, column=1)
    name_box3 = Entry(add_frame)
    name_box3.grid(row=2, column=2)
    name_box4 = Entry(add_frame)
    name_box4.grid(row=2, column=3)
    name_box5 = Entry(add_frame, textvariable=name_box)
    name_box5.grid(row=2, column=4)

    conn.commit()
    conn.close()

#------------------------------------------------SQL AND TABLE WORK ENDS HERE------------------------------------------

########################################################################################################################

def create_calculator(master):
    class Calculator:
        def __init__(self, master):
            self.master = master
            master.title("Calculator")
            # Create entry box
            self.entry = Entry(master, width=30, borderwidth=5, font=("Helvetica", 16), bg="#222222", fg="#FFFFFF")
            self.entry.grid(row=0, column=0, columnspan=4, padx=10, pady=10)
            # Create buttons using a grid layout
            buttons = [
                "C", "+/-", "%", "/",
                "7", "8", "9", "*",
                "4", "5", "6", "-",
                "1", "2", "3", "+",
                "0", ".", "pi", "="]
            row = 1
            col = 0
            for button in buttons:
                if col == 4:
                    row += 1
                    col = 0
                button_style = ttk.Style(root)
                button_style.configure("TButton", font=("Helvetica", 12), padding=10, background="#FFFFFF", foreground="#333333", borderwidth=2, relief="raised")
                button_style.map("TButton", background=[("active", "#FFFFFF")])
                ttk.Button(master, text=button, style="TButton", command=lambda text=button: self.button_click(text)).grid(row=row, column=col)
                col += 1

        def button_click(self, text):
            current = self.entry.get()

            if text == "C":
                self.entry.delete(0, END)
            elif text == "+/-":
                if current and current[0] == "-":
                    self.entry.delete(0)
                else:
                    self.entry.insert(0, "-")
            elif text == "%":
                try:
                    result = eval(current) / 100
                    self.entry.delete(0, END)
                    self.entry.insert(0, str(result))
                except:
                    messagebox.showerror("Error", "Invalid input")
            elif text == "pi":
                self.entry.delete(0, END)
                self.entry.insert(0, str(math.pi))
            elif text == "=":
                try:
                    result = eval(current)
                    self.entry.delete(0, END)
                    self.entry.insert(0, str(result))
                except:
                    messagebox.showerror("Error", "Invalid input")
            else:
                self.entry.delete(0, END)
                self.entry.insert(0, current + text)

            # Increase font size of result
            self.entry.config(font=("Helvetica", 24))

            self.entry.config(
            fg="white",
            bg="black",
            justify="right",
            relief="flat",
            highlightthickness=2,
            highlightcolor="orange",
            highlightbackground="#666666",
            )

    calculator = Calculator(master)
    return calculator

def open_calculator():
        calculator_window = Toplevel(root)
        calculator_window.configure(bg="#333333")
        calculator = create_calculator(calculator_window)

##############################################################################################################################################


def show_news():
    # Create a new window for the news
    news_window = tk.Toplevel()
    news_window.title("NBN FINANCE TRACKER - NEWS")
    news_window.geometry("900x600")
    news_window.configure(background="#191919")
    news_window.resizable(False, False)
    
    # Create a style for the labels
    style = ttk.Style()
    style.configure("TLabel", font=("TkDefaultFont", 12), foreground="white", background="#191919")

    # Create a label for the title
    title_label = ttk.Label(news_window, text="Latest News", font=("TkDefaultFont", 20))
    title_label.pack(pady=20)

    # Create a scrolled text widget for the news section
    news_section = ScrolledText(news_window, width=180, height=80, wrap=tk.WORD, bg="#191919", fg="white")
    news_section.pack(pady=0)

    # Fetch news from the API
    api_key = "8a3926f223eb45cdb02bff5616977b44"
    queries = ["national stock exchange", "bombay stock exchange"]
    for query in queries:
        url = f"https://newsapi.org/v2/everything?q=bombay stock exchange &apiKey={api_key}"
        response = requests.get(url)
        if response.status_code == 200:
            articles = response.json()["articles"]
            for article in articles:
                # Add the article title and description to the news section
                news_section.insert(tk.END, f"{article['title']}\n", "bold")
                news_section.insert(tk.END, f"{article['description']}\n\n")
                # Set the tag for the article title to be bold
                news_section.tag_configure("bold", font=("TkDefaultFont", 14, "bold"))
                # Add a separator line between articles
                news_section.insert(tk.END, "-"*100 + "\n\n")

    # Disable editing in the news section
    news_section.config(state=tk.DISABLED)

# Create the buttons and add them to the frame
add_expense_button = ttk.Button(button_frame, text="ADD EXPENSE",command=new_Records, width=20, padding=10)
add_expense_button.pack(pady=10)

view_expense_button = ttk.Button(button_frame, text="VIEW EXPENSE",command=previous_Records, width=20, padding=10)
view_expense_button.pack(pady=10)

calculator_button = ttk.Button(button_frame, text="CALCULATOR",command=open_calculator, width=20, padding=10)
calculator_button.pack(pady=10)

news_button = ttk.Button(button_frame, text="NEWS",command=show_news, width=20, padding=10)
news_button.pack(pady=10)

exit_button = ttk.Button(button_frame, text="EXIT", command=root.destroy, width=20, padding=10)
exit_button.pack(pady=10)

# Center the frame in the window
button_frame.place(relx=0.5, rely=0.5, anchor="center")

# Start the main loop
root.mainloop()
conn.commit()
conn.close()