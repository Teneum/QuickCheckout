from DataFunc.accountmanagement import UserData
from widgets.account_completion_module import Register
from widgets.mainpage import *
import sys
import tkinter as tk
from tkinter import ttk, Label, messagebox

userinfo = UserData()


class LoginPage:
    def __init__(self, master):
        super().__init__()
        self.counter = 0
        self.master = master
        self.root = tk.Toplevel(master)
        self.root.title("QuickPay")
        self.root.geometry('300x200')
        Label(self.root, width="300", text="Please enter details below", bg="green", fg="white").pack()
        Label(self.root, text="UserID * ").place(x=20, y=40)
        self.username = tk.Entry(self.root)
        self.username.place(x=90, y=42)

        Label(self.root, text="Password * ").place(x=20, y=80)
        self.password = tk.Entry(self.root, show='*')
        self.password.place(x=90, y=82)
        ttk.Button(self.root, text='LOGIN', command=self.login_user).place(x=105, y=130)

        def on_closing():
            if messagebox.askokcancel("Quit", "Do you want to quit?"):
                self.root.destroy()
                sys.exit()
        self.root.protocol("WM_DELETE_WINDOW", on_closing)

    def login_user(self):
        global userid
        userid = self.username.get()
        validation = userinfo.login(userID=userid, password=self.password.get().strip())
        if validation == "Found":
            check_if_acc_completed = userinfo.check_if_account_complete(userID=userid)
            if 0 in check_if_acc_completed[0]:
                self.root.destroy()
                Register(userid=userid, master=self.master)
            else:
                self.root.destroy()
                if userinfo.checkadmin(userid) is True:
                    AdminMainPage(userid=userid, master=self.master)
                else:
                    MainPage(userid=userid, master=self.master)

        else:
            if self.counter == 3:
                messagebox.showerror("Error!", "Default Credentials:\nUserID: admin\nPassword: password",
                                     parent=self.root)
            else:
                self.counter += 1
                self.message = Label(self.root, text='Username or Password incorrect. Try again!', fg='Red')
                self.message.place(x=20, y=100)
