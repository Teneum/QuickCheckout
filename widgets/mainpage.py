from tkinter import *
import tkinter as tk
from DataFunc.accountmanagement import UserData

from frames.invoice import *
from frames.billviewer import *
from frames.itemviewer import *
from frames.empviewer import *

userinfo = UserData()

class MainPage:
    def __init__(self, userid, master):
        self.root = tk.Toplevel(master)
        self.UserID = userid
        self.root.title('QuickCheckout')
        self.root.geometry("1300x700+0+0")
        self.billapp = BillApp()
        self.billapp.construct(root=self.root, userid=self.UserID)

class AdminMainPage:
    def __init__(self, userid, master):
        super().__init__()
        self.root = tk.Toplevel(master)
        self.UserID = userid
        self.root.title('QuickCheckout')
        self.root.geometry("1300x700+0+0")

        # Frames
        self.billapp = BillApp()
        self.billview = BillView()
        self.itemview = ItemView()
        self.empview = EmpView()

        self.billview.construct(root=self.root, userid=self.UserID)
        menu = Menu(self.root)
        self.root.config(menu=menu)
        mainmenu = Menu(menu)
        menu.add_cascade(label="Menu", menu=mainmenu)
        mainmenu.add_command(label="Checkout", command=self.command_billapp)
        mainmenu.add_separator()
        mainmenu.add_command(label="Transaction History", command=self.command_billview)
        mainmenu.add_separator()
        mainmenu.add_command(label="Item Management", command=self.command_itemview)
        mainmenu.add_separator()
        mainmenu.add_command(label="Employee Management", command=self.command_empview)

    def command_billapp(self):
        self.hideallframe()
        self.billapp.construct(root=self.root, userid=self.UserID)

    def command_billview(self):
        self.hideallframe()
        self.billview.construct(root=self.root, userid=self.UserID)
    
    def command_itemview(self):
        self.hideallframe()
        self.itemview.construct(root=self.root, userid=self.UserID)
    
    def command_empview(self):
        self.hideallframe()
        self.empview.construct(root=self.root, userid=self.UserID)
        
    # Hide all frames func
    def hideallframe(self):
        self.billapp.deconstruct(root=self.root)
        self.billview.deconstruct(root=self.root)
        self.itemview.deconstruct(root=self.root)
        self.empview.deconstruct(root=self.root)