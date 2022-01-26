import random
import tkinter as tk
from tkinter import *
from tkinter import messagebox
import json

from DataFunc.transactions import *
from DataFunc.inventory import *


class BillApp(tk.Frame):
    def construct(self, userid, root):
        self.userid = userid
        self.root = root
        tk.Frame.__init__(self, root)
        self.root.geometry("1300x700+0+0")
        self.root.title("QuickCheckout")

        self.transac = Transactions()
        self.inventory = Inventory()
        itemlist = self.inventory.getitems()
        self.itemdict = {}

        # ====================Variables========================#
        self.cus_name = StringVar()
        self.c_phone = StringVar()
        # For Generating Random Bill Numbers
        self.c_bill_no = StringVar()
        # Seting Value to variable
        self.c_bill_no.set(str(self.transac.billno()))

        self.total = StringVar()
        self.vat_total = StringVar()

        # ===================================
        bg_color = "blue"
        fg_color = "white"
        lbl_color = 'white'
        # Title of App
        Label(self.root, text="QuickCheckout", bd=12, relief=GROOVE, fg=fg_color, bg=bg_color,
              font=("times new roman", 30,"bold"), pady=3).pack(fill=X)

        # ==========Customers Frame==========#
        F1 = LabelFrame(self.root, text="Customer Details", font=("time new roman", 12, "bold"), fg="gold", bg=bg_color,
                        relief=GROOVE, bd=10)
        F1.place(x=0, y=80, relwidth=1)

        # ===============Customer Name===========#
        Label(F1, text="Customer Name", bg=bg_color, fg=fg_color,
              font=("times new roman", 15, "bold")).grid(row=0, column=0, padx=10, pady=5)
        cname_en = Entry(F1, bd=8, relief=GROOVE, textvariable=self.cus_name)
        cname_en.grid(row=0, column=1, ipady=4, ipadx=30, pady=5)

        # =================Customer Phone==============#
        Label(F1, text="Phone No", bg=bg_color, fg=fg_color, font=("times new roman", 15, "bold")).grid(
            row=0, column=2, padx=20)
        cphon_en = Entry(F1, bd=8, relief=GROOVE, textvariable=self.c_phone)
        cphon_en.grid(row=0, column=3, ipady=4, ipadx=30, pady=5)

        # ====================Customer Bill No==================#
        cbill_lbl = Label(F1, text="Bill No.", bg=bg_color, fg=fg_color, font=("times new roman", 15, "bold"))
        cbill_lbl.grid(row=0, column=4, padx=20)
        cbill_en = Entry(F1, bd=8, relief=GROOVE, textvariable=self.c_bill_no)
        cbill_en.grid(row=0, column=5, ipadx=30, ipady=4, pady=5)

        # ==================Food Frame=====================#
        F2 = LabelFrame(self.root, text='Item Selection', bd=10, relief=GROOVE, bg=bg_color, fg="gold",
                        font=("times new roman", 13, "bold"))
        F2.place(x=5, y=180, width=325, height=380)

        self.itemlistbox_scrollbar = Scrollbar(F2)
        self.itemlistbox_scrollbar.pack(side=RIGHT, fill=Y)

        self.itemlistbox = Listbox(F2, font=("times new roman", 13, "bold"), height=15, selectmode=SINGLE, width=30)
        self.itemlistbox.pack()
        for item in itemlist:
            self.itemlistbox.insert(END, item)

        self.itemlistbox.config(yscrollcommand=self.itemlistbox_scrollbar.set)
        self.itemlistbox_scrollbar.config(command=self.itemlistbox.yview)

        Button(F2, text='Select', command=self.itemselect).pack(pady=10)

        # ==================Grocery Frame=====================#
        F3 = LabelFrame(self.root, text='Amount Selection', bd=10, relief=GROOVE, bg=bg_color, fg="gold",
                        font=("times new roman", 13, "bold"))
        F3.place(x=330, y=180, width=650, height=190)

        Label(F3, text='Select Item: ', font=("times new roman", 13, "bold")).grid(column=0, padx=10, pady=10)
        Label(F3, text='Select Quantity: ', font=("times new roman", 13, "bold")).grid(column=0, row=1, padx=10,
                                                                                       pady=10)

        self.itemamtlabel = Label(F3, text='', font=("times new roman", 13, "bold"), relief=GROOVE, padx=20)
        self.itemamtlabel.grid(column=1, row=0, padx=10, pady=10)

        self.itemamt = IntVar()
        self.itemamtentry = Entry(F3, relief=GROOVE, textvariable=self.itemamt)
        self.itemamtentry.grid(row=1, column=1, ipadx=5, ipady=5, padx=10, pady=10)

        Button(F3, text='Add Item', bg="green",
               command=self.additemdict).grid(row=2, column=0, padx=20, pady=20)

        Button(F3, text='Delete Item', bg="red", command=self.delitemdict).grid(row=2, column=1, padx=20, pady=20)

        # Items Selected LabelFrame #

        itemselected = LabelFrame(self.root, text='Items Selected', bd=10, relief=GROOVE, bg=bg_color, fg="gold",
                                  font=("times new roman", 13, "bold"))
        itemselected.place(x=330, y=370, width=325, height=190)
        scrollbar_itemselected = Scrollbar(itemselected)
        scrollbar_itemselected.pack(side=RIGHT, fill=Y)
        self.itemselected_textbox = Text(itemselected)
        self.itemselected_textbox.pack()
        self.itemselected_textbox.config(yscrollcommand=scrollbar_itemselected.set)
        scrollbar_itemselected.config(command=self.itemselected_textbox.yview)

        # Output Message Box #
        outputmsgbox = LabelFrame(self.root, text='Output', bd=10, relief=GROOVE, bg=bg_color, fg="gold",
                                  font=("times new roman", 13, "bold"))
        outputmsgbox.place(x=655, y=370, width=325, height=190)
        self.outputmsgbox_textbox = Text(outputmsgbox)
        self.outputmsgbox_textbox.pack()
        self.outputmsgbox_textbox.tag_config('warning', background="yellow", foreground="red")
        self.outputmsgbox_textbox.tag_config('noerror', foreground="green")
        # Bill Area #
        F3 = Label(self.root, bd=10, relief=GROOVE)
        F3.place(x=960, y=180, width=325, height=380)
        # ===========
        bill_title = Label(F3, text="Bill List", font=("Lucida", 13, "bold"), bd=7, relief=GROOVE)
        bill_title.pack(fill=X)

        # ============
        scroll_y = Scrollbar(F3, orient=VERTICAL)
        self.txt = Text(F3, yscrollcommand=scroll_y.set)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_y.config(command=self.txt.yview)
        self.txt.pack(fill=BOTH, expand=1)

        # ===========Buttons Frame=============#
        F4 = LabelFrame(self.root, text='Bill Menu', bd=10, relief=GROOVE, bg=bg_color, fg="gold",
                        font=("times new roman", 13, "bold"))
        F4.place(x=0, y=560, relwidth=1, height=145)

        # ===================
        cosm_lbl = Label(F4, font=("times new roman", 15, "bold"), fg=lbl_color, bg=bg_color, text="Total: ")
        cosm_lbl.grid(row=0, column=0, padx=10, pady=0)
        cosm_en = Entry(F4, bd=8, relief=GROOVE, textvariable=self.total)
        cosm_en.grid(row=0, column=1, ipady=2, ipadx=5)



        # ================
        cosmt_lbl = Label(F4, font=("times new roman", 15, "bold"), fg=lbl_color, bg=bg_color, text="VAT: ")
        cosmt_lbl.grid(row=0, column=2, padx=30, pady=0)
        cosmt_en = Entry(F4, bd=8, relief=GROOVE, textvariable=self.vat_total)
        cosmt_en.grid(row=0, column=3, ipady=2, ipadx=5)



        # ====================
        total_btn = Button(F4, text="Total", bg=bg_color, fg=fg_color, font=("lucida", 12, "bold"), bd=7, relief=GROOVE,
                           command=self.totaldisplay)
        total_btn.grid(row=1, column=4, ipadx=20, padx=30)

        # ========================
        genbill_btn = Button(F4, text="Generate Bill", bg=bg_color, fg=fg_color, font=("lucida", 12, "bold"), bd=7,
                             relief=GROOVE, command=self.bill_area)
        genbill_btn.grid(row=1, column=5, ipadx=20)

        # ====================
        clear_btn = Button(F4, text="Clear", bg=bg_color, fg=fg_color, font=("lucida", 12, "bold"), bd=7, relief=GROOVE,
                           command=self.clear)
        clear_btn.grid(row=1, column=6, ipadx=20, padx=30)

        # ======================
        exit_btn = Button(F4, text="Finish", bg=bg_color, fg=fg_color, font=("lucida", 12, "bold"), bd=7, relief=GROOVE,
                          command=self.finish)
        exit_btn.grid(row=1, column=7, ipadx=20)

    def itemselect(self):
        self.itemamtlabel.config(text=self.itemlistbox.get(ANCHOR))
        self.itemamtentry.delete(0, END)

    def additemdict(self):
        amt = self.itemamt.get()
        item = self.itemamtlabel['text']
        availableamt = self.inventory.getitemamt(item=item)
        if amt > availableamt[0]:
            self.enteroutputbox(msg=f"Error: Amount entered exceeds quantity available\n"
                                    f"Quantity Available: {availableamt}", error=1)
        else:
            if item in self.itemdict:
                self.itemdict[item] += amt
                self.enteroutputbox(msg=f"Change registered successfully", error=0)
            else:
                self.itemdict[item] = amt
                self.enteroutputbox(msg=f"{item} with quantity {amt} has been added successfully", error=0)
        self.itemdictoutput()

    def delitemdict(self):
        item = self.itemamtlabel['text']
        amt = self.itemamt.get()
        if item in self.itemdict:
            if amt == 0:
                del self.itemdict[item]
            elif amt > self.itemdict[item]:
                self.enteroutputbox(msg=f'Error: Quantity exceeds stock registered for {item}', error=1)
            else:
                if self.itemdict[item] == amt:
                    del self.itemdict[item]
                    self.enteroutputbox(msg=f"{item} has been removed successfully", error=0)
                else:
                    self.itemdict[item] -= amt
                    self.enteroutputbox(msg=f"Change registered successfully", error=0)
        else:
            self.enteroutputbox(msg="Error: Cannot delete an item which hasn't been registered for the bill yet",
                                error=1)
        self.itemdictoutput()

    def itemdictoutput(self):
        self.itemselected_textbox.delete("1.0", "end")
        prettydict = json.dumps(self.itemdict, sort_keys=True, indent=4)
        self.itemselected_textbox.insert(INSERT, prettydict)

    def enteroutputbox(self, msg, error):
        self.outputmsgbox_textbox.delete("1.0", "end")
        if error == 1:
            self.outputmsgbox_textbox.insert('end', msg, 'warning')
        else:
            self.outputmsgbox_textbox.insert('end', msg, 'noerror')

    # Function to get total prices
    def totalitems(self):
        # Arranging in format dict = {pos_no : [name, qty, price]}
        itemsbought = [key for key in self.itemdict]
        itemsval = self.inventory.getmultipleitemprice(itemsbought)
        i = 0
        totalitemsdict = {}
        for item in itemsbought:
            i += 1
            qty = self.itemdict[item]
            val = itemsval[item]
            totalval = qty * val
            totalitemsdict[i] = [item, qty, totalval]
        return totalitemsdict

    def totaldisplay(self):
        total, tax = self.totalbill()
        self.total.set("$" + str(total))
        self.vat_total.set("$" + str(tax))

    def totalbill(self):
        itemtotal = self.totalitems()
        vals = list(itemtotal.values())
        sum = 0
        for i in range(0, len(vals)):
            sum += vals[i][2]
        return round(sum, 2), round(sum*0.10, 2)

    # Function For Text Area
    def welcome_soft(self):
        self.txt.delete('1.0', END)
        self.txt.insert(END, "       Welcome To Store's Retail\n")
        self.txt.insert(END, f"\nBill No. : {str(self.c_bill_no.get())}")
        self.txt.insert(END, f"\nCustomer Name : {str(self.cus_name.get())}")
        self.txt.insert(END, f"\nPhone No. : {str(self.c_phone.get())}")
        self.txt.insert(END, f"\nVAT %  : 10%")
        self.txt.insert(END, "\n\n===================================")
        format_str = "\n{:<3} {:<15} {:<5} {:<1} ".format('Pos', 'Product', 'Qty', 'Price')
        self.txt.insert(END, format_str)
        self.txt.insert(END, "\n===================================")

    # Function to clear the bill area
    def clear(self):
        self.txt.delete('1.0', END)

    def input_transaction(self):
        total, tax = self.totalbill()
        total += tax
        self.transac.newtransaction(customer_name=self.cus_name.get(),
                               customer_phone=self.c_phone.get(),
                               total=total,
                               cashierid=self.userid,
                               items_bought=self.itemdict
                               )

    def bill_area(self):
        totalitemsdict = self.totalitems()
        self.welcome_soft()
        for k, v in totalitemsdict.items():
            name, qty, totalval = v
            format_str = "\n{:<3} {:<15} {:<5} {:<1}".format(k, name, qty, totalval)
            self.txt.insert(END, format_str)

        total, tax = self.totalbill()
        str = f"\n\nTotal: {round(total+tax, 2)} Tax: {round(tax, 2)}"
        self.txt.insert(END, str)


    def finish(self):
        self.input_transaction()
        self.inventory.amt_change_on_transaction(itemdict=self.itemdict)
        self.construct(root=self.root, userid=self.userid)


    def deconstruct(self, root):
        checkstr = '.!toplevel2.!menu'
        children = root.winfo_children()
        str_children = [str(elem) for elem in children]
        ind = -1
        try:
            ind = str_children.index(checkstr)
        except Exception as e:
            print(e)
            print(str_children)

        for widgets in children:
            if widgets == children[ind]:
                pass
            else:
                widgets.destroy()