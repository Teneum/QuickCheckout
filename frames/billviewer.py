import tkinter as tk
from tkinter import *
import json

from DataFunc.transactions import *

class BillView(tk.Frame):
    def construct(self, userid, root):
        self.userid = userid
        self.root = root
        tk.Frame.__init__(self, root)
        self.root.geometry("750x500+0+0")
        self.root.title("QuickCheckout-BillViewer")

        bg_color = "blue"
        fg_color = "white"
        lbl_color = 'white'
        self.bills = TransactionHistory()
        billlst = self.bills.transactionlist()
        
        
        billview = LabelFrame(self.root, text="BillView", font=("time new roman", 12, "bold"), fg="gold", bg=bg_color,
                              relief=GROOVE, bd=10)
        billview.place(x=0, y=0, width=375, height=500)

        self.billlistbox_scrollbar = Scrollbar(billview)
        self.billlistbox_scrollbar.pack(side=RIGHT, fill=Y)

        self.billlistbox = Listbox(billview, font=("times new roman", 13, "bold"), height=20, selectmode=SINGLE, width=30)
        self.billlistbox.pack()
        for item in billlst:
            self.billlistbox.insert(END, item)

        self.billlistbox.config(yscrollcommand=self.billlistbox_scrollbar.set)
        self.billlistbox_scrollbar.config(command=self.billlistbox.yview)

        Button(billview, text='Select', command=self.itemselect).pack(pady=10)

        transacview= LabelFrame(self.root, text="TransactionView", font=("time new roman", 12, "bold"), fg="gold", bg=bg_color,
                              relief=GROOVE, bd=10)
        transacview.place(x=375, y=0, width=370, height=500)
        self.transactextbox = Text(transacview, width=150)
        self.transactextbox.pack(padx=10, pady=10)
        self.transactextbox.config(font=("arial", 14, "bold"))

    def itemselect(self):
        self.transactextbox.delete("1.0", END)
        billid = self.billlistbox.get(ANCHOR)
        details = self.bills.getdata(str(billid))
        prettydict = json.dumps(details, sort_keys=False, indent=4)
        self.transactextbox.insert(INSERT, prettydict)

    def deconstruct(self, root):
        checkstr = '.!toplevel2.!menu'
        children = root.winfo_children()
        str_children = [str(elem) for elem in children]
        ind = -1
        try:
            ind = str_children.index(checkstr)
        except Exception as e:
            print(e)

        for widgets in children:
            if widgets == children[ind]:
                pass
            else:
                widgets.destroy()