import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import messagebox
import requests
import math
import random
from tkcalendar import DateEntry
import math
# Create the main window
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
                button_style = ttk.Style()
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
# Create the buttons and add them to the frame
add_expense_button = ttk.Button(button_frame, text="ADD EXPENSE", width=20, padding=10)
add_expense_button.pack(pady=10)

view_expense_button = ttk.Button(button_frame, text="VIEW EXPENSE", width=20, padding=10)
view_expense_button.pack(pady=10)

calculator_button = ttk.Button(button_frame, text="CALCULATOR",command=open_calculator, width=20, padding=10)
calculator_button.pack(pady=10)

news_button = ttk.Button(button_frame, text="NEWS", width=20, padding=10)
news_button.pack(pady=10)

exit_button = ttk.Button(button_frame, text="EXIT", width=20, padding=10, command=root.destroy)
exit_button.pack(pady=10)

# Center the frame in the window
button_frame.place(relx=0.5, rely=0.5, anchor="center")

# Start the main loop
root.mainloop()