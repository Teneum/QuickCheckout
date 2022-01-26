from tkinter import *
from tkinter import messagebox
from tkinter.messagebox import askyesno
import tkinter as tk

from DataFunc.inventory import *
import json

class ItemView(tk.Frame):
    def construct(self, userid, root):
        self.userid = userid
        self.root = root
        tk.Frame.__init__(self, root)
        self.root.geometry("750x500+0+0")
        self.root.title("QuickCheckout - ItemViewer")

        bg_color = "blue"
        fg_color = "white"
        lbl_color = 'white'
        self.inventory = Inventory()
        itemlist = self.inventory.getitems()
        

        itemview = LabelFrame(self.root, text="ItemView", font=("time new roman", 12, "bold"), fg="gold", bg=bg_color,
                              relief=GROOVE, bd=10)
        itemview.place(x=0, y=0, width=375, height=500)

        itemlist_scrollbar = Scrollbar(itemview)
        itemlist_scrollbar.pack(side=RIGHT, fill=Y)

        self.itemlistbox = Listbox(itemview, font=("times new roman", 13, "bold"), height=20, selectmode=SINGLE,
                                   width=30)
        self.itemlistbox.pack()
        for item in itemlist:
            self.itemlistbox.insert(END, item)

        self.itemlistbox.config(yscrollcommand=itemlist_scrollbar.set)
        itemlist_scrollbar.config(command=self.itemlistbox.yview)

        Button(itemview, text='Select', command=self.itemselect).pack(pady=10)


        itemview = LabelFrame(self.root, text="Details", font=("times new roman", 12, "bold"), fg="gold",
                                 bg=bg_color,
                                 relief=GROOVE, bd=10)
        itemview.place(x=375, y=0, width=370, height=250)

        self.itemdisplay = Label(itemview, text=' ', font=('times new roman', 13, "bold"), relief=GROOVE,
                                 padx=10)
        self.itemdisplay.place(x=47, y=30)
        
        self.transactextbox = Text(itemview, width=20, height=2, padx=10, pady=10)
        self.transactextbox.place(x=47, y=65)
        self.transactextbox.config(font=("arial", 14, "bold"))

        itemdetailview = LabelFrame(self.root, text="Edit", font=("times new roman", 12, "bold"), fg="gold",
                                    bg=bg_color, relief=GROOVE, bd=10)
        itemdetailview.place(x=375, y=250, width=370, height=250)

        self.itemnamevar = StringVar()
        self.itemamtvar = IntVar()
        self.itemvalvar = DoubleVar()

        Label(itemdetailview, text="Item Name: ", font=('times new roman', 13, "bold"), relief=GROOVE,
              padx=10, pady=10).place(x=5, y=5)
        self.itemname_entry = Entry(itemdetailview, textvariable=self.itemnamevar, relief=GROOVE, width=35)
        self.itemname_entry.place(x=135, y=13)

        Label(itemdetailview, text="Item Amt in Total: ", font=('times new roman', 13, "bold"),
              relief=GROOVE).place(x=5, y=65)
        self.itemamt_entry = Entry(itemdetailview, textvariable=self.itemamtvar, relief=GROOVE, width=6)
        self.itemamt_entry.place(x=160, y=66)

        Label(itemdetailview, text="Price: ", font=('times new roman', 13, "bold"),
              relief=GROOVE).place(x=5, y=106)
        self.itemval_entry = Entry(itemdetailview, textvariable=self.itemvalvar, relief=GROOVE, width=6)
        self.itemval_entry.place(x=160, y=106)

        Button(itemdetailview, text='Save', command=self.savedetails, bg="green").place(x=165, y=136)
        Button(itemdetailview, text='Add Item', command=self.additem, bg="green").place(x=155, y=166)
        Button(itemdetailview, text='Delete Item', command=self.deleteitem, bg="red").place(x=150, y=196)

    def savedetails(self):
        self.inventory.savedetails(itemname=self.itemnamevar.get(),
                                   amt=self.itemamtvar.get(),
                                   value=self.itemvalvar.get())
        self.deconstruct(self.root)
        self.construct(root=self.root, userid=self.userid)

    def additem(self):
        if self.inventory.checkitemexists(itemName=self.itemnamevar.get()):
            messagebox.showerror("Error!", "Cannot add item that already exists", parent=self.root)
        else:
            self.inventory.additem(itemName=self.itemnamevar.get(),
                                   amount=self.itemamtvar.get(),
                                   value=self.itemvalvar.get())
            self.deconstruct(self.root)
            self.construct(root=self.root, userid=self.userid)

    def deleteitem(self):
        item=self.itemnamevar.get()
        if self.inventory.checkitemexists(itemName=item):
            answer = askyesno(title="Confirmation", message=f"Are you sure you want to delete item: {item}")
            if answer:
                self.inventory.delitem(itemname=item)
                self.deconstruct(self.root)
                self.construct(root=self.root, userid=self.userid)
            else:
                pass
        else:
            messagebox.showerror("Error!", "Cannot delete item that doesn't exist", parent=self.root)

    def itemselect(self):
        self.transactextbox.delete("1.0", END)
        itemid = self.itemlistbox.get(ANCHOR)
        details = self.inventory.getdetails(str(itemid))
        self.itemdisplay.config(text=str(itemid))
        amt = 0
        val = 0.0
        for key, value in details.items():
            if isinstance(value, list):
                value = value[0]
                amt = value
            else:
                val = value
            self.transactextbox.insert(END, f'{key}: {value}\n')

        self.itemnamevar.set(str(itemid))
        self.itemvalvar.set(val)
        self.itemamtvar.set(amt)

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
