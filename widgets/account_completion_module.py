import tkinter as tk
from tkinter import ttk, Label, Frame, Entry, Button, messagebox
from widgets.mainpage import *

from DataFunc.accountmanagement import UserData
userinfo = UserData()

class Register:
    def __init__(self, userid, master):
        super().__init__()
        self.UserID = userid
        self.master = master
        self.root = tk.Toplevel(master)
        self.root.title("QuickCheckout - Registration Page")  # For Title of the page
        self.root.geometry("500x500")  # Resolution of the page , top, bottom
        self.root.config(bg="green")

        # ===Register Frame===
        frame1 = Frame(self.root, bg="green")
        frame1.place(x=0, y=0, width=500, height=500)

        title = Label(frame1, text="Complete Registration", font=("times new roman", 20, "bold"), bg="green",
                      fg="black").place(x=135, y=30)

        # --------First Row
        f_name = Label(frame1, text="First Name:", font=("times new roman", 15, "bold"), bg="green", fg="yellow").\
            place(x=50, y=100)
        self.txt_fname = Entry(frame1, font=("times new roman", 15), bg="white")
        self.txt_fname.place(x=220, y=100, width=250)

        # --------Second Raw
        l_name = Label(frame1, text="Last Name:", font=("times new roman", 15, "bold"), bg="green", fg="yellow").place(x=50,
                                                                                                                    y=140)
        self.txt_lname = Entry(frame1, font=("times new roman", 15), bg="white")
        self.txt_lname.place(x=220, y=140, width=250)


        # --------3rd Raw
        nationality = Label(frame1, text="Nationality:", font=("times new roman", 15, "bold"), bg="green", fg="yellow").\
            place(x=50, y=180)
        self.txt_nationality = Entry(frame1, font=("times new roman", 15), bg="white")
        self.txt_nationality.place(x=220, y=180, width=250)

        # -------Contact
        contact = Label(frame1, text="Contact Number:", font=("times new roman", 15, "bold"), bg="green", fg="yellow").\
            place(x=50, y=220)
        self.txt_contact = Entry(frame1, font=("times new roman", 15), bg="white")
        self.txt_contact.place(x=220, y=220, width=250)

        # -------Email
        email = Label(frame1, text="Email:", font=("times new roman", 15, "bold"), bg="green", fg="yellow").place(x=50, y=260)
        self.txt_email = Entry(frame1, font=("times new roman", 15), bg="white")
        self.txt_email.place(x=220, y=260, width=250)

        # -------Age
        age = Label(frame1, text="Age:", font=("times new roman", 15, "bold"), bg="green", fg="yellow").place(x=50, y=300)
        self.txt_age = Entry(frame1, font=("times new roman", 15), bg="white")
        self.txt_age.place(x=220, y=300, width=250)

        # -------Gender
        gender = Label(frame1, text="Gender:", font=("times new roman", 15, "bold"), bg="green", fg="yellow").place(x=50,
                                                                                                                 y=340)
        self.cmb_gender = ttk.Combobox(frame1, font=("times new roman", 13), state='readonly')
        self.cmb_gender['values'] = ("Select Gender", "Male", "Female", "Other")
        self.cmb_gender.place(x=220, y=340, width=250)
        self.cmb_gender.current(0)

        #Change Password
        password = Label(frame1, text="New Password", font=("times new roman", 15, "bold"), bg="green", fg="yellow").\
            place(x=50, y=380)
        self.txt_password = Entry(frame1, font=("times new roman", 15), bg="white")
        self.txt_password.place(x=220, y=380, width=250)

        # Registration Button
        Button(frame1, text='REGISTER', command=self.finish_register, activebackground= 'green').place(x=220, y=420)

        def on_closing():
            if messagebox.askokcancel("Quit", "Do you want to quit?"):
                self.root.destroy()
                sys.exit()
        self.root.protocol("WM_DELETE_WINDOW", on_closing)

    def finish_register(self):
        nationality = self.txt_nationality.get()
        contact = self.txt_contact.get()
        email = self.txt_email.get()
        gender = self.cmb_gender.get()
        age = self.txt_age.get()
        password = self.txt_password.get()
        f_name = self.txt_fname.get()
        l_name = self.txt_lname.get()
        name = str(f_name) + str(l_name)
        condition = (len(nationality) and len(contact) and len(email) and len(gender) and len(age) and len(password) and len(name))
        if condition == 0:
            messagebox.showerror("Error!", "All Fields are Required!", parent=self.root)
        else:
            userinfo.registration(userID=self.UserID, name=name, nationality=nationality, gender=
                                  gender, age=age, contactAddress=email, contactNumber=contact)
            userinfo.update_password(ID=self.UserID, password=password)
            userinfo.update_acc_complete(ID=self.UserID)
            self.root.destroy()
            if userinfo.checkadmin(userid=self.UserID) is True:
                AdminMainPage(master=self.master, userid=self.UserID)
            else:
                MainPage(master=self.master, userid=self.UserID)