"""
AAQIEL BEHARDIEN
CLASS 1
__________________________
Life Choices Online Project

Scope
------------ Users
Able to register themselves to the database
Able to log in
Able to log out
------------Administrator
Able to register a user
Able to declare that a user is an administrator
Able to log in
Able to delete user
Able to grant privileges to admin
"""
from tkinter import *
import mysql.connector as conn

import register_functions
import track_time_functions
import search_algorithms
import admin_functions

# set-up connection to database
db_name = "lifechoices_db"
db = conn.connect(host="localhost", user="root", password="1234", database=db_name)

# set-up cursor (to report the sql statement to mysql)
curs = db.cursor(buffered=True)


# -------------------------------------------------------------
# Main window class (SUPER)
# links the other 2 classes
# also acts as coordinator of the other 2 windows/classes
class LoginFrame(object):

    def __init__(self, parent):
        """
        initializing frame
        """
        self.screen = parent
        self.screen.title("Welcome to LC Online")
        self.frame = Frame(parent)
        self.frame.pack()

        Label(self.frame, text="").pack()
        Label(self.frame, text="").pack()

        # -------------------------------------------------------------

        Label(self.frame, text="Please enter log in details below").pack()
        Label(self.frame, text="").pack()

        """
        globalized so that they may be used in other functions appropriately. 
        I decided to not put them on top of the module since these variables originate from this class
        and it keeps everything together and makes the code more readable.
        """
        global username_verify, username_log_entry
        global password_verify, password_log_entry

        """
        Declaring variables their respective properties for tkinter to be able to source them correctly to their type
        """
        username_verify = StringVar()
        password_verify = StringVar()

        """
        Username entry box
        the users input will be recorded and will be returned here.
        """
        Label(self.frame, text="Username *").pack()
        username_log_entry = Entry(self.frame, textvariable=username_verify)
        username_log_entry.pack()

        """
        Password entry box
        the users input will be fetched from login_verify(self) and will be returned here.
        """
        Label(self.frame, text="").pack()
        Label(self.frame, text="Password *").pack()
        password_log_entry = Entry(self.frame, textvariable=password_verify)
        password_log_entry.pack()

        Label(self.frame, text="").pack()
        btn_verify_login = Button(self.frame, text="Login", width=10, height=1, command=self.login_verify)
        btn_verify_login.pack()

        password_log_entry.delete(0, END)

        # ------------------------------------------------------------
        Label(self.frame, text="").pack()
        btn_register = Button(self.frame, text="Register", height="1", width="20", command=self.openRegister)
        btn_register.pack()

    # -------------------------------------------------------------

    def login_verify(self):
        """
        The code below interacts with database
        It takes the given data and validates it with the database

        Conditions for successful log-in
        -------------------------------
        If user exists in database
        If password matches the users password in database

        Conditions for successful log-out
        -------------------------------
        If user has already logged in (otherwise log them in {current day})
        If user has not logged out already
        """
        global list_users
        user_in_list = []
        pass_in_list = []

        # Fetching user inputs

        try:
            # Exception handling
            username_checker = int(username_verify.get())
            password_checker = password_verify.get()
        except TypeError:
            MessageBox(self, "Oops! Make sure you are following the instructions!", "red")
        except ImportError:
            MessageBox(self, "Oops! Something went wrong... Contact admin!", "red")
        except ValueError:
            MessageBox(self, "Oops! Make sure you are using the correct values!", "red")
        else:
            if username_checker == 0 or password_checker == "":
                # if entry boxes are empty
                MessageBox(self, "Check username and/or password", "red")
            else:
                try:
                    # Fetching all username's from database
                    # then storing in as a list
                    # then checking if the user_input is in the list - True if found/ False if not found

                    # getting username's
                    curs.execute("SELECT username FROM users_tbl;")
                    list_users = curs.fetchall()
                    users_accounts = [row[0] for row in list_users]
                    user_in_list = username_checker in users_accounts

                    # getting password of the username selected
                    curs.execute("SELECT password FROM users_tbl WHERE username={}".format(username_checker))
                    list_passwords = curs.fetchall()
                    user_password = [row[0] for row in list_passwords]
                    pass_in_list = password_checker in user_password

                    # checking if the user is an admin or not
                    curs.execute("SELECT access FROM users_tbl WHERE username={}".format(username_checker))
                    list_privileges = curs.fetchall()
                    user_privilege = [row[0] for row in list_privileges]
                    is_admin = "Admin" in user_privilege

                except ImportError:
                    MessageBox(self, "Error! Contact admin", "red")
                else:
                    if user_in_list and pass_in_list and is_admin:
                        # if the user is an admin run code below
                        self.openAdmin()
                        username_log_entry.delete(0, END)
                        password_log_entry.delete(0, END)

                    elif user_in_list and pass_in_list and not is_admin:
                        # if the user is not an admin run code below
                        # ----------------------------------------------------

                        # checking is the user has logged in or not
                        curs.execute("SELECT username, day FROM timelogs_tbl WHERE username={} AND day='{}';".format(
                            username_checker, track_time_functions.get_day()))
                        u_list = curs.fetchall()
                        username_list = [row[0] for row in u_list]
                        day_list = [row[1] for row in u_list]
                        print(username_list)
                        print(day_list)

                        # returns true if the user has logged in
                        found_user = username_checker in username_list
                        # returns true if the user has logged in on current day
                        found_day = track_time_functions.get_day() in day_list

                        if not found_day and not found_user:
                            # If he was not logged in
                            curs.execute("INSERT IGNORE INTO timelogs_tbl (timeIn, username, day) VALUES ("
                                         "%s, %s, %s);", (track_time_functions.get_time(), username_checker,
                                                          track_time_functions.get_day()))
                            db.commit()
                            MessageBox(self, "Login Successful! Enjoy Your Day!", "green")
                        else:
                            # if he was logged in

                            # also trying to get the id so that we may place it in the log out table {it's a foreign
                            # key}
                            curs.execute("SELECT timelogs_id FROM timelogs_tbl WHERE username={} AND day='{}';".format(
                                username_checker, track_time_functions.get_day()))
                            logged_in_users = [row[0] for row in curs.fetchall()]
                            chosen_id = 0
                            for get_id in logged_in_users:
                                chosen_id = get_id

                            curs.execute("SELECT timelogs_id FROM timelogsout_tbl;")
                            signed_out_users = [row[0] for row in curs.fetchall()]
                            exists = chosen_id in signed_out_users

                            if exists:
                                # if the user has already been logged out
                                MessageBox(self, "Already logged out", "red")
                            else:
                                # if the user logs in a second time in one day log him out
                                curs.execute(
                                    "INSERT IGNORE INTO timelogsout_tbl (timeOut, timelogs_id) VALUES ("
                                    "%s, %s);", (track_time_functions.get_time(), chosen_id))
                                db.commit()

                                curs.execute("SELECT timelogs_id FROM timelogsout_tbl;")
                                print(curs.fetchall())

                        # ----------------------------------------------------

                    else:
                        MessageBox(self, "Login Unsuccessful", "red")
                        username_log_entry.delete(0, END)
                        password_log_entry.delete(0, END)

    # -------------------------------------------------------------

    def hide(self):
        self.screen.withdraw()

    # ---------------------------------------------------------------

    def openRegister(self):
        self.hide()
        RegisterFrame(self)

    # --------------------------------------------------------------

    def openError(self):
        self.hide()

    # --------------------------------------------------------------

    def openAdmin(self):
        self.hide()
        Admin_user(self)

    # --------------------------------------------------------------

    def onCloseOtherFrame(self, otherFrame):
        otherFrame.destroy()
        self.show()

    # --------------------------------------------------------------

    def show(self):
        self.screen.update()
        self.screen.deiconify()

    # --------------------------------------------------------------


# -------------------------------------------------------------
# A message box to easily report to the user on the process that occur
# in the code
class MessageBox(Toplevel):
    """
    This is for displaying error messages and so forth
    I have also included a colour scheme
    """

    def __init__(self, original_frame, err_message, bg_chosen):
        self.original_frame = original_frame
        self.err_message = err_message
        self.bg_chosen = bg_chosen
        Toplevel.__init__(self)
        self.geometry("{}x{}".format((10 * len(err_message)) - 25, 80))
        self.title("NOTIFIER")

        Label(self, text=err_message, bg=bg_chosen, width=len(err_message), height="2", font=("callibri", 11)).pack()
        Button(self, text="Ok", width=len(err_message), height="2", font=("callibri", 11), command=self.onRetry).pack()

    # ------------------------------------------------------------
    def onRetry(self):
        self.destroy()
        self.original_frame.show()


# -------------------------------------------------------------
# An admin only window where if log in details matches admin
# requirements, the will be redirected here and
# perform administrative functions
# such as:
# delete a user,
# add a user,
# make user admin,
# view all logged in/out
class Admin_user(Toplevel):

    def __init__(self, original):
        self.original_frame = original
        # initialising call super class
        Toplevel.__init__(self)
        self.geometry("400x500")
        self.title("Welcome administrator")

        global admin_username, admin_username_entry

        admin_username = StringVar()

        Label(self, text="Display user data:").pack()
        Label(self, text="_______________________").pack()
        Label(self, text=" ").pack()

        Label(self, text="Display all logged in users").pack()
        btn_show_login = Button(self, text="Display", width=10, height=1, command=lambda: show_login())
        btn_show_login.pack()
        Label(self, text=" ").pack()

        Label(self, text="Display all logged out users").pack()
        btn_show_login = Button(self, text="Display", width=10, height=1, command=lambda: show_logout())
        btn_show_login.pack()
        Label(self, text=" ").pack()

        Label(self, text="Username:").pack()
        admin_username_entry = Entry(self, textvariable=admin_username, width=30)
        admin_username_entry.pack()
        Label(self, text=" ").pack()

        Label(self, text="User data manipulation:").pack()
        Label(self, text="_____________________________________").pack()
        Label(self, text=" ").pack()

        btn_add_admin = Button(self, text="Create admin", width=10, height=1, command=self.add_administrator)
        btn_add_admin.pack()
        Label(self, text=" ").pack()

        btn_del_admin = Button(self, text="Delete user", width=10, height=1, command=self.del_user)
        btn_del_admin.pack()
        Label(self, text=" ").pack()

        btn_register = Button(self, text="Add user", width=10, height=1, command=lambda: [RegisterFrame(
            Toplevel), self.onClose()])
        btn_register.pack()
        Label(self, text=" ").pack()

        btn_close = Button(self, text="Close", width=10, height=1, command=lambda: self.onClose())
        btn_close.place(x=300, y=450)

    # ------------------------------------------------------------
    def onClose(self):
        self.destroy()
        self.original_frame.show()

    # ------------------------------------------------------------
    def show(self):
        self.update()
        self.deiconify()

    # ------------------------------------------------------------
    def add_administrator(self):
        try:
            admin_username_info = int(admin_username.get())
        except TypeError:
            MessageBox(self, "Oops! Make sure you are following the instructions!", "red")
        except ImportError:
            MessageBox(self, "Oops! Something went wrong... Contact admin!", "red")
        except ValueError:
            MessageBox(self, "Oops! Make sure you are using the correct values!", "red")
        else:
            if admin_username_info:
                curs.execute("SELECT username FROM users_tbl;")
                username_list = curs.fetchall()
                temp_user = [row[0] for row in username_list]
                user_taken = admin_username_info in temp_user

                if user_taken is True:
                    curs.execute(
                        "UPDATE users_tbl SET access='Admin' WHERE username={}".format(str(admin_username_info)))
                    db.commit()

                    # GRANT PRIVILEGES
                    curs.execute("SELECT password FROM users_tbl WHERE username={}".format(str(admin_username_info)))
                    found_password = [row[0] for row in curs.fetchall()]
                    got_pass = ""
                    for get_password in found_password:
                        got_pass = get_password

                    # Calling imported function
                    admin_functions.create_User(db, db_name, curs, admin_username_info, got_pass)

                    curs.execute("INSERT IGNORE INTO administrators_tbl "
                                 "(admin_username, admin_privileges)"
                                 "VALUES (%s, %s)",
                                 (admin_username_info, "SELECT, ALTER, DELETE, INSERT, UPDATE"))

                    MessageBox(self, "ADMIN CREATED SUCCESSFULLY", "green")
                    db.commit()

                else:
                    MessageBox(self, "This username does not exist", "red")
            else:
                MessageBox(self, "Please fill in the appropriate fields", "red")

    # ------------------------------------------------------------
    def del_user(self):
        try:
            admin_username_info = int(admin_username.get())
        except TypeError:
            MessageBox(self, "Oops! Make sure you are following the instructions!", "red")
        except ImportError:
            MessageBox(self, "Oops! Something went wrong... Contact admin!", "red")
        except ValueError:
            MessageBox(self, "Oops! Make sure you are using the correct values!", "red")
        else:
            if admin_username_info:
                curs.execute("SELECT username FROM users_tbl;")
                username_list = curs.fetchall()
                temp_user = [row[0] for row in username_list]
                user_taken = admin_username_info in temp_user

                if user_taken is True:
                    curs.execute("DELETE FROM users_tbl WHERE username={}".format(str(admin_username_info)))
                    db.commit()

                    # Calling imported function
                    admin_functions.del_user(db, curs, admin_username_info)

                else:
                    MessageBox(self, "This username does not exist", "red")
            else:
                MessageBox(self, "Please fill in the appropriate fields", "red")


# Here are some functions relating to the Admin class

def show_login():
    curs.execute(
        "SELECT fname FROM users_tbl INNER JOIN timelogs_tbl ON users_tbl.username = timelogs_tbl.username "
        "WHERE timelogs_tbl.day='{}';".format(track_time_functions.get_day()))
    fetched_list = curs.fetchall()
    users_logged_in = [row[0] for row in fetched_list]
    new_list = []
    try:
        # writes to a file all logged in users
        with open("LogIn.txt", "w+") as outFile:
            outFile.writelines("Users currently logged in\n")
            for users_name in users_logged_in:
                outFile.writelines("_________\n")
                outFile.writelines(users_name + "\n")

    except EXCEPTION:
        exit("Something went wrong when writing to file. Contact admin")
    finally:
        outFile.close()


def show_logout():
    curs.execute("SELECT username FROM timelogs_tbl INNER JOIN timelogsout_tbl ON timelogs_tbl.timelogs_id = "
                 "timelogsout_tbl.timelogs_id WHERE timelogs_tbl.day='{}'".format(track_time_functions.get_day()))
    got_list = curs.fetchall()
    users_logged_out = [row[0] for row in got_list]
    new_list = []

    curs.execute("SELECT username FROM users_tbl;")
    names = [row[0] for row in curs.fetchall()]

    for username in users_logged_out:
        curs.execute("SELECT fname FROM users_tbl WHERE username={}".format(search_algorithms.binary_search(names,
                                                                                                            username)))
        name_in = [row[0] for row in curs.fetchall()]
        new_list.append(name_in)

    display_user = [user[0] for user in new_list]

    try:
        # writes to a file all logged out users
        with open("LogOut.txt", "w+") as outFile:
            outFile.writelines("Users currently logged in\n")
            for users_name in display_user:
                outFile.writelines("_________\n")
                outFile.writelines(users_name + "\n")

    except EXCEPTION:
        exit("Something went wrong when writing to file. Contact admin")
    finally:
        outFile.close()


# -------------------------------------------------------------
# A register window
# When the button register is clicked
# the user/admin will be directed to this class
# you may enter the details of the user you want to register
# but only if you follow requirements
# to grant certain privileges go to admin class
class RegisterFrame(Toplevel):

    def __init__(self, original):
        self.original_frame = original
        Toplevel.__init__(self)
        self.geometry("500x600")
        self.title("Register")

        global username, name, surname, dob, address, role, access, holidays, password
        global username_entry, name_entry, surname_entry, dob_entry, address_entry, role_entry, access_entry, \
            holidays_entry, password_entry

        y_int = 25
        x_int = 50
        len_width = 45

        username = StringVar()
        name = StringVar()
        surname = StringVar()
        dob = StringVar()
        address = StringVar()
        role = StringVar()
        access = StringVar()
        holidays = StringVar()
        password = StringVar()

        label_list = ["Username * (000009)", "Name * (Name)", "Surname * (Surname)", "Date of birth * (2000-02-01)",
                      "Address * (48 Derby Road Lansdowne 7780)", "Role * (Student/Lecturer/Employee)",
                      "Holidays (Taken in days e.g. '3')", "Password (12)* (fweryu234)"]
        y_count = 1
        while y_count < len(label_list):
            for label_name in label_list:
                label = Label(self, text=label_name)
                label.place(x=40, y=y_int * (2 * y_count))
                y_count += 1

        Label(self, text="Please enter details below:").place(x=20, y=y_int)

        username_entry = Entry(self, textvariable=username, width=len_width)
        username_entry.place(x=x_int, y=y_int * 3)

        name_entry = Entry(self, textvariable=name, width=len_width)
        name_entry.place(x=x_int, y=y_int * 5)

        surname_entry = Entry(self, textvariable=surname, width=len_width)
        surname_entry.place(x=x_int, y=y_int * 7)

        dob_entry = Entry(self, textvariable=dob, width=len_width)
        dob_entry.place(x=x_int, y=y_int * 9)

        address_entry = Entry(self, textvariable=address, width=len_width)
        address_entry.place(x=x_int, y=y_int * 11)

        role_entry = Entry(self, textvariable=role, width=len_width)
        role_entry.place(x=x_int, y=y_int * 13)

        holidays_entry = Entry(self, textvariable=holidays, width=len_width)
        holidays_entry.place(x=x_int, y=y_int * 15)

        password_entry = Entry(self, textvariable=password, width=len_width)
        password_entry.place(x=x_int, y=y_int * 17)

        btn_register_new = Button(self, text="Register", width=10, height=1, command=self.register_user)
        btn_register_new.place(x=x_int, y=y_int * 19)

        btn_close = Button(self, text="Close", width=10, height=1, command=self.onClose)
        btn_close.place(x=350, y=y_int * 19)

    # ------------------------------------------------------------
    def onClose(self):
        self.destroy()
        self.original_frame.show()

    # ------------------------------------------------------------

    def show(self):
        self.update()
        self.deiconify()

    # ------------------------------------------------------------

    def register_user(self):
        try:
            username_info = int(username.get())
            name_info = name.get()
            surname_info = surname.get()
            dob_info = dob.get()
            address_info = address.get()
            role_info = role.get()
            holidays_info = int(holidays.get())
            password_info = password.get()
        except TypeError:
            MessageBox(self, "Oops! Make sure you are following the instructions!", "red")
        except ImportError:
            MessageBox(self, "Oops! Something went wrong... Contact admin!", "red")
        except ValueError:
            MessageBox(self, "Oops! Make sure you are using the correct values!", "red")
        else:
            entries_list = [
                username_info,
                name_info,
                surname_info,
                dob_info,
                address_info,
                role_info,
                holidays_info,
                password_info
            ]
            is_empty = 8

            for entry in entries_list:
                if not entry:
                    print("Checking...")
                else:
                    is_empty -= 1
            print(str(is_empty))
            if is_empty != 0:
                MessageBox(self, "Please fill all fields", "red")
            elif is_empty == 0:
                print(str(len(password_info)))
                curs.execute("SELECT username FROM users_tbl;")
                username_list = curs.fetchall()
                temp_user = [row[0] for row in username_list]
                user_taken = username_info in temp_user

                while not user_taken:
                    while register_functions.username_valid(username_info):
                        while register_functions.password_valid(password_info):
                            adding_account(db, curs,
                                           username_info,
                                           name_info,
                                           surname_info,
                                           dob_info,
                                           address_info,
                                           role_info,
                                           holidays_info,
                                           password_info
                                           )
                            Label(self, text="Registration successful", fg="green", font=("callibri", 11)).pack()
                            break
                        else:
                            password_entry.delete(0, END)
                            MessageBox(self, "Password must be between 4 - 12 characters!", "orange")
                        break
                    else:
                        username_entry.delete(0, END)

                        MessageBox(self, "Username must be between 1 - 6 characters!", "orange")
                    break
                else:
                    username_entry.delete(0, END)
                    password_entry.delete(0, END)

                    MessageBox(self, "'Username' has been taken", "red")

    # ---------------------------------------------------------


# Here are some functions for registering user
def adding_account(my_db, my_curs, username_info, name_info, surname_info, dob_info, address_info,
                   role_info, holidays_info, password_info):
    try:
        # using INSERT IGNORE INTO to make sure no duplication errors occur
        statement = "INSERT IGNORE INTO users_tbl (username, fname, fsurname, date_of_birth, " \
                    "address, role, access, holidays, password) VALUES (%s, %s, %s, %s, %s, %s, %s, " \
                    "%s, %s) "
        # executing multiple sql statements
        my_curs.execute(statement,
                        (username_info, name_info, surname_info, dob_info, address_info, role_info,
                         "None", holidays_info, password_info))
        # commit to finalize changes to database
        my_db.commit()

        username_entry.delete(0, END)
        name_entry.delete(0, END)
        surname_entry.delete(0, END)
        dob_entry.delete(0, END)
        address_entry.delete(0, END)
        role_entry.delete(0, END)
        holidays_entry.delete(0, END)
        password_entry.delete(0, END)
    except TypeError:
        print("!!!Please make sure that the correct values have been used!!!")
    except ImportError:
        print("!!!Import error!!!")
    except ValueError:
        pass
    else:
        print("...Running...")
    finally:
        print("...Tried adding accounts...")
        # reports number of accounts added
        print(my_curs.rowcount, "account added...")


# -------------------------------------------------------------

if __name__ == "__main__":
    screen = Tk()
    screen.geometry("300x300")
    application = LoginFrame(screen)
    screen.mainloop()
