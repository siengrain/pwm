from tkinter import *
import sqlite3
import pyperclip
from tkinter import messagebox

root = Tk()

# Database
conn = sqlite3.connect('dbpwm.db')

c = conn.cursor()

c.execute("""CREATE TABLE IF NOT EXISTS acc_data (
        acc_id text,
        acc_pw text
        )""")

conn.commit()

conn.close()


# Popups :)
def popup():
    messagebox.showinfo("Password Manager", "Your password was copied to your clipboard")


def popup_r():
    messagebox.showinfo("Password Manager", "Your account was removed from the database")


def popup_a():
    messagebox.showinfo("Password Manager", "Your account was added to the database")


# Popup bad :(
def badup():
    messagebox.showerror("ERROR", "Account/Password field is empty")


def badempt():
    messagebox.showerror("ERROR", "Account field is empty")


def non_exis():
    messagebox.showerror("ERROR", "That account is not registered in the database :(")


def exist():
    messagebox.showerror("ERROR", "That account is already registered in the database")


def readme_up():
    messagebox.showinfo("Help",
                        "Hi! Thanks for using Password Manager, if you have any doubt about how the program works check readme.txt :)")


def contact():
    messagebox.showinfo("Contact", "test@test.com :)")


# Add Account Window (Class based)
class AddWindow(Toplevel):

    def __init__(self, master=None):
        super().__init__(master=master)
        self.title("Password Manager")
        self.geometry("320x150")
        self.resizable(False, False)
        icon = Image("photo", file="icon_test.png")
        self.tk.call('wm', 'iconphoto', self._w, icon)
        add_label = Label(self, text="Account/username/etc: ")
        add_label.grid(row=0, column=0, padx=20)
        add_acc = Entry(self, width=25)
        add_acc.grid(row=1, column=0, padx=20, pady=5)
        pw_label = Label(self, text="Password: ")
        pw_label.grid(row=3, column=0, padx=20)
        add_pw = Entry(self, width=25)
        add_pw.grid(row=4, column=0, padx=20)

        # Submit Function
        def submit():
            acc = add_acc.get()
            pw = add_pw.get()
            if len(acc) > 0 and len(pw) > 0:
                conn = sqlite3.connect('dbpwm.db')
                c = conn.cursor()
                c.execute("SELECT acc_id from acc_data WHERE acc_id = '" + acc + "'")
                dacc = c.fetchone()
                conn.commit()
                conn.close()
                if dacc is not None:
                    exist()
                    add_acc.delete(0, END)
                    add_pw.delete(0, END)
                else:
                    # Add the stuff to the database

                    conn = sqlite3.connect('dbpwm.db')
                    c = conn.cursor()
                    c.execute("INSERT INTO acc_data VALUES (:add_acc, :add_pw)",
                              {
                                  'add_acc': add_acc.get(),
                                  'add_pw': add_pw.get()
                              })
                    conn.commit()
                    conn.close()
                    add_acc.delete(0, END)
                    add_pw.delete(0, END)
                    self.destroy()
                    popup_a()
            else:
                badup()

        add_button = Button(self, text="Add", command=submit)
        add_button.grid(row=2, column=2)


# Remove Account Window
def rem_window():
    bot = Toplevel()
    bot.geometry("350x100")
    bot.resizable(False, False)
    icon = Image("photo", file="icon_test.png")
    bot.tk.call('wm', 'iconphoto', bot._w, icon)
    rem_label = Label(bot, text="Account to delete: ")
    rem_label.grid(row=0, column=0, padx=20)
    rem_acc = Entry(bot, width=25)
    rem_acc.grid(row=1, column=0, padx=20, pady=5)

    # Remove function
    def remove():
        acc_d = rem_acc.get()
        if len(acc_d) > 0:
            conn = sqlite3.connect('dbpwm.db')
            c = conn.cursor()
            c.execute("SELECT acc_id FROM acc_data WHERE acc_id = '" + acc_d + "'")
            d = c.fetchall()
            dd = str(d)
            ddd = dd[3:-4]
            c.execute("DELETE from acc_data WHERE acc_id = '" + acc_d + "'")
            conn.commit()
            conn.close()
            rem_acc.delete(0, END)
            if ddd == acc_d:
                popup_r()
                bot.destroy()
            else:
                non_exis()
                bot.destroy()
        else:
            badempt()
            bot.destroy()

    rem_button = Button(bot, text="Remove", command=remove)
    rem_button.grid(row=1, column=1)


# Title
root.title("Password Manager")

# Menu
menu_bar = Menu(root)
help_menu = Menu(root)

menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Options", menu=menu)
menu.add_command(label="Add Account", command=AddWindow)
menu.add_command(label="Remove Account", command=rem_window)
helpp = Menu(help_menu, tearoff=0)
menu_bar.add_cascade(label="Help", menu=helpp)
helpp.add_command(label="Readme", command=readme_up)
helpp.add_command(label="Contact", command=contact)
root.config(menu=menu_bar)

# Window Size
root.geometry("340x100")

# Disable Resize
root.resizable(False, False)

# Icon
icon = Image("photo", file="icon_test.png")
root.tk.call('wm', 'iconphoto', root._w, icon)


# Search function
def search():
    s = search_field.get()
    if len(s) > 0:
        conn = sqlite3.connect('dbpwm.db')
        c = conn.cursor()
        c.execute("SELECT acc_pw from acc_data WHERE acc_id = '" + s + "'")
        rows = c.fetchall()
        conn.commit()
        conn.close()
        pww = str(rows)
        pww2 = pww[3:-4]
        search_field.delete(0, END)
        if len(rows) == 0:
            non_exis()
        else:
            pyperclip.copy(str(pww2))
            popup()
    else:
        badempt()


# Boxes and stuff
search_label = Label(root, text="Search account: ").grid(row=1, column=0, padx=15, pady=5)
search_field = Entry(root, width=25)
search_field.grid(row=2, column=0, padx=20)
search_button = Button(root, text="Search", command=search).grid(row=2, column=2)

mainloop()
