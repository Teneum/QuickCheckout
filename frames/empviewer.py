import tkinter as tk
from tkinter import *
from tkinter.messagebox import askyesno
from tkinter import ttk

from DataFunc.accountmanagement import *

class EmpView(tk.Frame):
    def construct(self, userid, root):
        self.userid = userid
        self.root = root
        tk.Frame.__init__(self, root)
        self.root.geometry("900x660+0+0")
        self.root.title("QuickCheckout - EmployeeViewer")

        bg_color = "blue"
        fg_color = "white"
        lbl_color = 'white'

        self.userdata = UserData()

        empview = LabelFrame(self.root, text="EmployeeView", font=("time new roman", 12, "bold"), fg="gold", bg=bg_color,
                             relief=GROOVE, bd=10)
        empview.place(x=0, y=0, width=300, height=660)
        emplist_scrollbar = Scrollbar(empview)
        emplist_scrollbar.pack(side=RIGHT, fill=Y)

        self.emplistbox = Listbox(empview, font=("times new roman", 13, "bold"), height=25, selectmode=SINGLE,
                                  width=30)
        self.emplistbox.pack()

        emplistwid = self.userdata.emplistwithid()
        for item in emplistwid:
            self.emplistbox.insert(END, item)

        self.emplistbox.config(yscrollcommand=emplist_scrollbar.set)
        emplist_scrollbar.config(command=self.emplistbox.yview)
        Button(empview, text='Select', command=self.itemselect).place(x=125, y=525)
        Button(empview, text='Add', command=self.addemp, bg="green").place(x=125, y=555)
        empdetails = LabelFrame(self.root, text="Details", font=("time new roman", 12, "bold"), fg="gold",
                                bg=bg_color, relief=GROOVE, bd=10)
        empdetails.place(x=300, y=0, width=600, height=220)
        self.emptextbox = Text(empdetails, width=50, height=30, padx=10, pady=10)
        self.emptextbox.pack()
        self.emptextbox.config(font=("arial", 14, "bold"))

        empdetailsedit = LabelFrame(self.root, text="Edit", font=("time new roman", 12, "bold"), fg="gold",
                                bg=bg_color, relief=GROOVE, bd=10)
        empdetailsedit.place(x=300, y=220, width=600, height=440)


        self.empsalary_var = DoubleVar()
        self.empperformance_var = StringVar()
        self.hoursperweek_var = DoubleVar()
        self.empnotes_var = StringVar()

        Label(empdetailsedit, text="Salary: ", font=('times new roman', 13, "bold"),
              padx=10, pady=10).place(x=5, y=30)
        self.empsalary_entry = Entry(empdetailsedit, textvariable=self.empsalary_var, relief=GROOVE, width=35)
        self.empsalary_entry.place(x=150, y=40)

        Label(empdetailsedit, text='Performance: ', font=('times new roman', 13, "bold")).place(x=5, y=90)
        self.empperformance_entry = Entry(empdetailsedit, textvariable=self.empperformance_var, width=35)
        self.empperformance_entry.place(x=150, y=90)

        Label(empdetailsedit, text='Hours/Week: ', font=('times new roman', 13, "bold")).place(x=5, y=150)
        self.emphours_entry = Entry(empdetailsedit, textvariable=self.hoursperweek_var, width=35)
        self.emphours_entry.place(x=150, y=150)


        Label(empdetailsedit, text='Notes: ', font=('times new roman', 13, "bold")).place(x=5, y=210)
        self.empnotes = Text(empdetailsedit, width=35, height=5)
        self.empnotes.place(x=150, y=210)
        self.empnotes.config(font=('times new roman', 15, "bold"))

        Button(empdetailsedit, text='Save', command=self.get_moderdetails, bg="green").place(x=300, y=350)
        Button(empdetailsedit, text='Delete ID', command=self.deleteacc, bg="red").place(x=290, y=380)

    def clean_emp_id(self):
        empid = self.emplistbox.get(ANCHOR)
        if empid == '':
            return
        startind = empid.index('/')
        empid = empid[startind + 2:len(empid)]
        return empid

    def deleteacc(self):
        empid = self.clean_emp_id()
        answer = askyesno(title="Confirmation", message=f"Are you sure you want to delete account?")
        if answer:
            self.userdata.delete_account(employeeID=empid)
            self.deconstruct(self.root)
            self.construct(root=self.root, userid=self.userid)
        else:
            pass

    def addemp(self):
        AddEmp(master=self.root)

    def itemselect(self):
        self.emptextbox.delete("1.0", END)
        empid = self.clean_emp_id()
        empdetails = self.userdata.getempdetails(empid)
        if empdetails is None:
            self.emptextbox.insert(END, "No Details Saved")
        else:
            for key, value in empdetails.items():
                self.emptextbox.insert(END, f'{key}: {value}\n')
        self.set_moderdetails()

    def set_moderdetails(self):
        self.empnotes.delete("1.0", END)
        empid = self.clean_emp_id()
        details = self.userdata.get_mod_details(employeeID=empid)
        self.hoursperweek_var.set(details[1])
        self.empsalary_var.set(details[2])
        self.empperformance_var.set(details[3])
        self.empnotes.insert(END, details[4])

    def get_moderdetails(self):
        empid= self.clean_emp_id()
        hours7D = self.hoursperweek_var.get()
        salary = self.empsalary_var.get()
        performance = self.empperformance_var.get()
        notes = self.empnotes.get("1.0", END)
        self.userdata.set_mod_details(employeeID=empid,
                                      hours7D=hours7D,
                                      salary=salary,
                                      performance=performance,
                                      notes=notes)
        self.deconstruct(root=self.root)
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

        for widgets in children:
            if widgets == children[ind]:
                pass
            else:
                widgets.destroy()

class AddEmp:
    def __init__(self, master):
        super().__init__()
        self.root = tk.Toplevel(master)
        self.root.geometry("500x100")
        self.root.title("Add Employee")
        self.userdata = UserData()

        self.userid = StringVar()
        self.password = StringVar()

        Label(self.root, text='USERID: ', relief=GROOVE, font=('times new roman', 13, "bold")).grid()
        self.id_entry = Entry(self.root, textvariable=self.userid, font=('times new roman', 13, "bold"),
                              relief=GROOVE, width=35)
        self.id_entry.grid(column=1, row=0)

        Label(self.root, text='PASSWORD: ', relief=GROOVE, font=('times new roman', 13, "bold")).grid(column=0, row=1)
        self.password_entry = Entry(self.root, textvariable=self.password, font=('times new roman', 13, "bold"),
                              relief=GROOVE, width=35)
        self.password_entry.grid(column=1, row=1)

        Label(self.root, text='TYPE: ', relief=GROOVE, font=('times new roman', 13, "bold")).grid(column=0, row=2)
        self.accounttype = ttk.Combobox(self.root, font=("times new roman", 13), state='readonly')
        self.accounttype['values'] = ("admin", "default")
        self.accounttype.grid(column=1, row=2)
        self.accounttype.current(1)

        Button(self.root, text='Add', bg="green", command=self.addaccount).grid(column=1, row=4)

    def addaccount(self):
        id = self.userid.get()
        password = self.password.get()
        type = self.accounttype.get()

        condition = self.userdata.check_account_exist(employeeID=id)
        if condition is True:
            messagebox.showerror("Error!", "Account Already Exists", parent=self.root)
        else:
            self.userdata.createUser(userID=id, password=password, accountType=type, username='Null', acccompl=False)
            self.root.destroy()

