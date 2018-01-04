##########################################################
# PyPhoneBook

# Description: PyPhoneBook is a phonebook developed 
# in python with Tkinter. The goal of this application 
# is to save contacts. It is useful if you lose your 
# mobilephone.

# Author: Nicolas Chen
##########################################################

from Tkinter import *
import ttk
import sqlite3
import tkMessageBox

class PyPhoneBook:
    def __init__(self, master):
        menubar = Menu(master)
        master.config(menu=menubar)
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="Exit", accelerator='Alt+F4', command=lambda: self.exit_phonebook(master))
        menubar.add_cascade(label="Menu", menu=filemenu)

        helpmenu = Menu(menubar, tearoff=0)
        helpmenu.add_command(label="Instructions", command=self.help_phonebook)
        helpmenu.add_command(label="About", command=self.about_phonebook)
        menubar.add_cascade(label="Help", menu=helpmenu)

        self.tree = ttk.Treeview(columns=('First Name', 'Last Name', 'Mobile Phone', 'Home Phone', 'Email', 'Title'),
                                 selectmode="extended")
        self.tree.grid(row=0)

        self.tree.heading("#1", text="First Name", anchor=CENTER)
        self.tree.heading("#2", text="Last Name", anchor=CENTER)
        self.tree.heading("#3", text="Mobile Phone", anchor=CENTER)
        self.tree.heading("#4", text="Home Phone", anchor=CENTER)
        self.tree.heading("#5", text="Email", anchor=CENTER)
        self.tree.heading("#6", text="Title", anchor=CENTER)

        self.tree.column("#0", stretch=NO, minwidth=0, width=0)
        self.tree.column("#1", stretch=NO, minwidth=0, width=150, anchor=CENTER)
        self.tree.column("#2", stretch=NO, minwidth=0, width=150, anchor=CENTER)
        self.tree.column("#3", stretch=NO, minwidth=0, width=150, anchor=CENTER)
        self.tree.column("#4", stretch=NO, minwidth=0, width=150, anchor=CENTER)
        self.tree.column("#5", stretch=NO, minwidth=0, width=200, anchor=CENTER)
        self.tree.column("#6", stretch=NO, minwidth=0, width=150, anchor=CENTER)

        addBtn = ttk.Button(text="Add Contact", command=lambda: self.open_modify_window(False))
        addBtn.grid(row=1, column=0, sticky=W)

        updateBtn = ttk.Button(text="Modify Contact", command=lambda: self.open_modify_window(True))
        updateBtn.grid(row=1, column=0, sticky=N + S)

        deleteBtn = ttk.Button(text="Delete Contact", command=self.delete_contact)
        deleteBtn.grid(row=1, column=0, sticky=E)

        self.show_contacts()

    # function to show the contacts
    def show_contacts(self):
        x = self.tree.get_children()
        for item in x:
            self.tree.delete(item)
        conn = sqlite3.connect('contacts_database.db')
        c = conn.cursor()
        list = c.execute("SELECT * FROM contacts ORDER BY first_name asc")
        for row in list:
            self.tree.insert("", "end", "", values=((row[1], row[2], row[3], row[4], row[5], row[6])))
        c.close()

    #function to display the edit window
    def open_modify_window(self, editMode):
        if editMode:
            try:
                self.tree.item(self.tree.selection())['values'][0]

                if not self.tree.item(self.tree.selection())['values']:
                    first_name = ""
                else:
                    first_name = self.tree.item(self.tree.selection())['values'][0]

                if not self.tree.item(self.tree.selection())['values']:
                    last_name = ""
                else:
                    last_name = self.tree.item(self.tree.selection())['values'][1]

                if not self.tree.item(self.tree.selection())['values']:
                    mobile_phone = ""
                else:
                    mobile_phone = self.tree.item(self.tree.selection())['values'][2]

                if not self.tree.item(self.tree.selection())['values']:
                    home_phone = ""
                else:
                    home_phone = self.tree.item(self.tree.selection())['values'][3]

                if not self.tree.item(self.tree.selection())['values']:
                    email = ""
                else:
                    email = self.tree.item(self.tree.selection())['values'][4]

                if not self.tree.item(self.tree.selection())['values']:
                    title = ""
                else:
                    title = self.tree.item(self.tree.selection())['values'][5]

                self.edit_window = Tk()
                self.edit_window.title("Edit contact")
                self.edit_window.iconbitmap('phone1.ico')
                self.edit_window.resizable(width=FALSE, height=FALSE)

                Label(self.edit_window, text='First Name:').grid(row=0, column=1, sticky=W)
                varnewfirstname = StringVar()
                newfirstname = Entry(self.edit_window, textvariable=varnewfirstname)
                newfirstname.grid(row=0, column=2, sticky=W)
                newfirstname.insert(0, first_name)

                Label(self.edit_window, text='Last Name:').grid(row=1, column=1, sticky=W)
                varnewlastname = StringVar()
                newlastname = Entry(self.edit_window, textvariable=varnewlastname)
                newlastname.grid(row=1, column=2, sticky=W)
                newlastname.insert(0, last_name)

                Label(self.edit_window, text='Mobile Phone:').grid(row=2, column=1, sticky=W)
                varnewmobilephone = IntVar()
                newmobilephone = Entry(self.edit_window, textvariable=varnewmobilephone)
                newmobilephone.grid(row=2, column=2, sticky=W)
                newmobilephone.insert(0, str(mobile_phone))

                Label(self.edit_window, text='Home Phone:').grid(row=3, column=1, sticky=W)
                varnewmobilephone = IntVar()
                newhomephone = Entry(self.edit_window, textvariable=varnewmobilephone)
                newhomephone.grid(row=3, column=2, sticky=W)
                newhomephone.insert(0, str(home_phone))

                Label(self.edit_window, text='Email:').grid(row=4, column=1, sticky=W)
                varnewemail = StringVar()
                newemail = Entry(self.edit_window, textvariable=varnewemail)
                newemail.grid(row=4, column=2, sticky=W)
                newemail.insert(0, email)

                Label(self.edit_window, text='Title:').grid(row=5, column=1, sticky=W)
                varnewtitle = StringVar()
                newtitle = Entry(self.edit_window, textvariable=varnewtitle)
                newtitle.grid(row=5, column=2, sticky=W)
                newtitle.insert(0, title)

                list_old_names = [first_name, last_name, mobile_phone, home_phone, email, title]

                upbtn = Button(self.edit_window, text='Update',
                               command=lambda: self.update_contact(newfirstname.get(), newlastname.get(),
                                                                  newmobilephone.get(),
                                                                  newhomephone.get(), newemail.get(), newtitle.get(),
                                                                  list_old_names))
                upbtn.grid(row=6, column=2, sticky=W, pady=5)

                cancelbtn = Button(self.edit_window, text='Cancel', command=lambda: self.cancel(editMode))
                cancelbtn.grid(row=6, column=2, sticky=E, pady=5, padx =5)
                self.edit_window.mainloop()

            except IndexError:
                self.select_item()

        else:
            try:
                self.add_window = Tk()
                self.add_window.title("Add contact")
                self.add_window.iconbitmap('phone1.ico')
                self.add_window.resizable(width=FALSE, height=FALSE)

                Label(self.add_window, text='First Name:').grid(row=0, column=0, sticky=W)
                self.firstname = StringVar()
                self.firstnameEntry = Entry(self.add_window, textvariable=self.firstname)
                self.firstnameEntry.grid(row=0, column=1, sticky=W)

                Label(self.add_window, text='Last Name:').grid(row=1, column=0, sticky=W)
                self.lastname = StringVar()
                self.lastnameEntry = Entry(self.add_window, textvariable=self.lastname)
                self.lastnameEntry.grid(row=1, column=1, sticky=W)

                Label(self.add_window, text='Mobile Phone:').grid(row=2, column=0, sticky=W)
                self.mobilephone = IntVar()
                self.mobilephoneEntry = Entry(self.add_window, textvariable=self.mobilephone)
                self.mobilephoneEntry.grid(row=2, column=1, sticky=W)

                Label(self.add_window, text='Home Phone:').grid(row=3, column=0, sticky=W)
                self.homephone = IntVar()
                self.homephoneEntry = Entry(self.add_window, textvariable=self.homephone)
                self.homephoneEntry.grid(row=3, column=1, sticky=W)

                Label(self.add_window, text='Email:').grid(row=4, column=0, sticky=W)
                self.email = StringVar()
                self.emailEntry = Entry(self.add_window, textvariable=self.email)
                self.emailEntry.grid(row=4, column=1, sticky=W)

                Label(self.add_window, text='Title:').grid(row=5, column=0, sticky=W)
                self.title = StringVar()
                self.titleEntry = Entry(self.add_window, textvariable=self.title)
                self.titleEntry.grid(row=5, column=1, sticky=W)

                addContactbtn = Button(self.add_window, text='Add', command=self.add_contact)
                addContactbtn.grid(row=6, column=1, sticky=W, pady=5, padx=5)

                cancelbtn = Button(self.add_window, text='Cancel', command=lambda: self.cancel(editMode))
                cancelbtn.grid(row=6, column=1, sticky=E, pady=5, padx=5)

                self.add_window.mainloop()

            except IndexError:
                self.select_item()

    def cancel(self, editMode):
        if editMode:
            self.edit_window.destroy()
        else:
            self.add_window.destroy()
    
    #function to add a contact
    def add_contact(self):
        firstname = self.firstnameEntry.get()
        lastname = self.lastnameEntry.get()
        mobilephone = self.mobilephoneEntry.get()
        homephone = self.homephoneEntry.get()
        email = self.emailEntry.get()
        title = self.titleEntry.get()

        if not firstname and not lastname and not mobilephone and not homephone and not email and not title:
           self.add_window.destroy()
           self.not_contact()
        elif not firstname and not lastname:
            self.select_firstname_lastname()
        else:
            conn = sqlite3.connect('contacts_database.db')
            c = conn.cursor()
            c.execute(
                "INSERT INTO contacts (first_name, last_name, mobile, home_phone, email, title) VALUES(?, ?, ?, ?, ?, ?)",
                (firstname, lastname, mobilephone, homephone, email, title))
            conn.commit()
            c.close()
            self.add_window.destroy()
            self.show_contacts()

    def update_contact(self, newfirstname, newlastname, newmobilephone, newhomephone,
                      newemail, newtitle, list_old_names):
        if not newfirstname or not newlastname:
            self.select_firstname_lastname()

        if newfirstname and newlastname and newmobilephone and newhomephone:
            conn = sqlite3.connect('contacts_database.db')
            c = conn.cursor()
            query = "SELECT contactid FROM contacts WHERE first_name='%s' AND last_name='%s' AND " \
                    "mobile='%s' AND home_phone='%s' AND email='%s' AND title='%s';" % (
                        list_old_names[0], list_old_names[1],
                        list_old_names[2], list_old_names[3],
                        list_old_names[4], list_old_names[5])
            c.execute(query)

            a = c.fetchall()

            for row in a:
                c.execute("UPDATE contacts SET first_name=?, last_name=?, mobile=?, home_phone=?, "
                          "email=?, title=? WHERE contactid=?", (newfirstname, newlastname,
                                                                 newmobilephone, newhomephone, newemail, newtitle,
                                                                 row[0]))
            conn.commit()
            c.close()
            self.edit_window.destroy()

            self.show_contacts()

    def delete_contact(self):
        try:
            self.tree.item(self.tree.selection())['values'][0]

            if not self.tree.item(self.tree.selection())['values']:
                first_name = ""
            else:
                first_name = self.tree.item(self.tree.selection())['values'][0]

            if not self.tree.item(self.tree.selection())['values']:
                last_name = ""
            else:
                last_name = self.tree.item(self.tree.selection())['values'][1]

            if not self.tree.item(self.tree.selection())['values']:
                mobile_phone = ""
            else:
                mobile_phone = self.tree.item(self.tree.selection())['values'][2]

            if not self.tree.item(self.tree.selection())['values']:
                home_phone = ""
            else:
                home_phone = self.tree.item(self.tree.selection())['values'][3]

            if not self.tree.item(self.tree.selection())['values']:
                email = ""
            else:
                email = self.tree.item(self.tree.selection())['values'][4]

            if not self.tree.item(self.tree.selection())['values']:
                title = ""
            else:
                title = self.tree.item(self.tree.selection())['values'][5]

            if self.confirm_delete():
                conn = sqlite3.connect('contacts_database.db')
                c = conn.cursor()
                query = "DELETE FROM contacts WHERE contactid = (SELECT contactid FROM contacts WHERE first_name='%s' AND last_name='%s' AND " \
                        "mobile='%s' AND home_phone='%s' AND email='%s' AND title='%s');" % (
                            first_name, last_name, mobile_phone,
                            home_phone, email, title)
                c.execute(query)
                conn.commit()
                c.close()
                self.show_contacts()

        except IndexError:
            self.select_item()

    def about_phonebook(self, event=None):
        self.version_window = Toplevel()
        self.version_window.title("Version - PyPhoneBook")
        self.version_window.resizable(width=False, height=False)

        message0 = Label(self.version_window, text='PyPhoneBook: Information - Version', font='arial 16')
        message0.grid(column=0, row=0, columnspan=2, pady=5, padx=10)
        message1 = Label(self.version_window, text='\n - Developer: Nicolas Chen')
        message1.grid(column=1, row=1, sticky=W)
        message2 = Label(self.version_window, text=' - Version: 1.0')
        message2.grid(column=1, row=2, sticky=W)
        message3 = Label(self.version_window, text=' - Release: 2016')
        message3.grid(column=1, row=3, sticky=W)
        message4 = Label(self.version_window, text=' - Copyright (c) 2016 nchen\n\n')
        message4.grid(column=1, row=4, sticky=W)

        message5 = Label(self.version_window,
                         text=' - For any information or suggestion, you can contact me at this email address:')
        message5.grid(column=1, row=5, sticky=W)
        message6 = Label(self.version_window, text='nchen.info@gmail.com', foreground='blue')
        message6.grid(column=1, row=6, columnspan=2)

        button_quit = Button(self.version_window, text='OK', relief='ridge', command=self.version_window.destroy)
        button_quit.grid(column=1, row=7, columnspan=2, pady=5)

    def help_phonebook(self, event=None):
        self.help_window = Toplevel()
        self.help_window.title("Help - PyPhoneBook")
        self.help_window.resizable(width=False, height=False)

        message1 = Label(self.help_window, text='Presentation:', font='arial 12 underline bold')
        message1.pack()

        message2 = Label(self.help_window, text='The PyPhoneBook allows you to save your contacts if you lose your mobilephone.')
        message2.pack()
        message3 = Label(self.help_window, text='\nOverview', font='arial 12 underline bold')
        message3.pack()
        message4 = Label(self.help_window, text='In the PyPhoneBook, you can provide the following information: '
                                                 '\nFirst Name\nLast Name\nMobile Phone\nHome Phone\nEmail\nTitle')
        message4.pack()
        message5 = Label(self.help_window, text='\nActions', font='arial 12 underline bold')
        message5.pack()
        message6 = Label(self.help_window, text='To add a contact, you click on the button "Add Contact", and '
                                                 'you have to indicate at least a firstname or lastname.\n'
                                                 'To update a contact, you have to select a contact then click on the '
                                                 'button "Update Contact".\n'
                                                 'To delete a contact, you have to select a contact then confirm the delete.')
        message6.pack()

        button_quit = Button(self.help_window, text='OK', relief='ridge', command=self.help_window.destroy)
        button_quit.pack(side='bottom', pady=5)

    ### MessageBox ###
    def confirm_delete(self):
        if tkMessageBox.askokcancel("Delete Contact", "Do you really want to delete this contact?"):
            return True
        else:
            return False

    def exit_phonebook(self, master):
        if tkMessageBox.askokcancel("Quit", "Do you really want to quit?"):
            master.destroy()

    def select_item(event=None):
        tkMessageBox.showwarning("Warning", "Please select a contact to modify")

    def select_firstname_lastname(self):
        tkMessageBox.showwarning("Warning", "Please enter a first name or a lastname")

    def not_contact(self):
        tkMessageBox.showinfo("Information", "No contact added")

    def select_homephone(self):
        tkMessageBox.showwarning("Warning", "Please enter an homephone")

def main():
    root = Tk()
    root.resizable(width=FALSE, height=FALSE)
    root.title("PyPhoneBook")
    root.iconbitmap('phone1.ico')
    PyPhoneBook(root)
    root.mainloop()

if __name__ == '__main__':
    main()