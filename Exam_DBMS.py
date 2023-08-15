import mysql.connector
import sys
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkinter.ttk import Combobox
import os
import pickle

# Function to design a window for registration
def register():
    global register_screen
    register_screen = Toplevel(main_screen)
    register_screen.title("Register")
    register_screen.geometry("300x250")

    global username
    global password
    global username_entry
    global password_entry
    username = StringVar()
    password = StringVar()

    Label(register_screen, text="Please enter details below", bg="blue").pack()
    Label(register_screen, text="").pack()
    username_lable = Label(register_screen, text="Username * ")
    username_lable.pack()
    username_entry = Entry(register_screen, textvariable=username)
    username_entry.pack()
    password_lable = Label(register_screen, text="Password * ")
    password_lable.pack()
    password_entry = Entry(register_screen, textvariable=password, show='*')
    password_entry.pack()
    Label(register_screen, text="").pack()
    Button(register_screen, text="Register", width=10, height=1, bg="blue", command = register_verify).pack()

# Function to design a window for login
def login():
    global login_screen
    login_screen = Toplevel(main_screen)
    login_screen.title("Login")
    login_screen.geometry("300x250")
    Label(login_screen, text="Please enter details below to login").pack()
    Label(login_screen, text="").pack()

    global username_verify
    global password_verify
    username_verify = StringVar()
    password_verify = StringVar()
    global username_login_entry
    global password_login_entry

    Label(login_screen, text="Username * ").pack()
    username_login_entry = Entry(login_screen, textvariable=username_verify)
    username_login_entry.pack()
    Label(login_screen, text="").pack()
    Label(login_screen, text="Password * ").pack()
    password_login_entry = Entry(login_screen, textvariable=password_verify, show= '*')
    password_login_entry.pack()
    Label(login_screen, text="").pack()
    Button(login_screen, text="Login", width=10, height=1, command = login_verify).pack()

# Function to implement an event onClick register button. A binary file(pickle) is created to store user data
def register_user():
    username_info = username.get()
    password_info = password.get()
    file = open(username_info, "w")
    file.write(username_info + "\n")
    file.write(password_info)
    file.close()
    username_entry.delete(0, END)
    password_entry.delete(0, END)
    Label(register_screen, text="Registration Success", fg="green", font=("calibri", 11)).pack()

# Function for user registration. User is verified using the binary file called save1.dat that stores user data
# register only if user does not already exist
def register_verify():
    username_info = username.get()
    password_info = password.get()
    f=open("save1.dat","ab+")
    d={"username_info":"key","password_info":"value"}
    pickle.dump(d,f)
    flag=True
    f.close()
    try:
        f=open("save1.dat","rb")
        while True:
            record=pickle.load(f)
            z=record["username_info"]
            if username_info==z:
                flag=False
                break
            else:
                flag=True
    except EOFError:
        f.close()

    f1=open("save1.dat","ab")
    if flag==True:
        k={}
        k["username_info"]=username_info
        k["password_info"]=password_info
        pickle.dump(k,f1)
        Label(register_screen, text="Registration Success", fg="green", font=("calibri", 11)).pack()
    else:
        messagebox.showerror("Error","Already Registered User Id")

# Implementing event of login (verify user and corresponding passeord) onClick login button
#If user doesnt not exist ask to register
def login_verify():
    username1 = username_verify.get()
    password1 = password_verify.get()
    username_login_entry.delete(0, END)
    password_login_entry.delete(0, END)
    flag=False
    try:
        f=open("save1.dat","rb")
        while True:
            record=pickle.load(f)
            m=record["username_info"]
            print(record)
            if username1 == m:
                flag=True
                break
            else:
                flag=False
                pass
    except EOFError:
        f.close()
    except FileNotFoundError:
        messagebox.showerror("Error","Please register before login")
        return
    if flag==True:
        found=0
        try:
            f1=open("save1.dat","rb")
            while True:
                record=pickle.load(f1)
                if record["password_info"]==password1:
                    found=1
                    break
                else:
                    found=0
        except EOFError:
            f1.close()
        if found==1:
            main_screen.destroy()
            main_user_screen()
        else:
            messagebox.showerror("Error","Invalid Password")
    if flag==False:
        messagebox.showerror("Error","User ID not found")

# Designing popup for login invalid password
def password_not_recognised():
    global password_not_recog_screen
    password_not_recog_screen = Toplevel(login_screen)
    password_not_recog_screen.title("Success")
    password_not_recog_screen.geometry("150x100")
    Label(password_not_recog_screen, text="Invalid Password ").pack()
    Button(password_not_recog_screen, text="OK", command=delete_password_not_recognised).pack()

# Designing popup for user not found
def user_not_found():
    global user_not_found_screen
    user_not_found_screen = Toplevel(login_screen)
    user_not_found_screen.title("Success")
    user_not_found_screen.geometry("150x100")
    Label(user_not_found_screen, text="User Not Found").pack()
    Button(user_not_found_screen, text="OK", command=delete_user_not_found_screen).pack()

# Deleting popups
def delete_login_success():
    login_success_screen.destroy()
def delete_password_not_recognised():
    password_not_recog_screen.destroy()
def delete_user_not_found_screen():
    user_not_found_screen.destroy()

# Designing Main(first) window
def m():
    main_screen.destroy()
    main_account_screen()

# Window for user to Log in or Register
def main_account_screen():
    global main_screen
    main_screen = Tk()
    main_screen.geometry("350x280")
    main_screen.title("Account Login")
    Label(text="EXAM MANAGEMENT", bg="black",fg='white', width="300", height="2", font=("Calibri", 13)).pack()
    Label(text="Select your choice", height="1", width="35").pack()
    Label(text="").pack()
    Button(text="Login", height="2", width="30", command = login).pack()
    Label(text="").pack()
    Button(text="Register", height="2", width="30", command=register).pack()
    Label(text="").pack()
    Button(text="Exit", height="2", width="30", command=main_screen.destroy).pack()
    main_screen.mainloop()

# Window to display a menu with 9 options as follows:
# 1. Add an exam
# 2. Modify an exam
# 3. Delete an exam
# 4. Display all exam details
# 5. Register a student
# 6. Delete a student
# 7. List the students registered for an exam
# 8. List the no. of students for each exam
# 9. List the exams registered by a student
def create_menu1():
    global main_screen
    Label(text="EXAM MANAGEMENT SYSTEM", bg="black",fg='white', width="300", height="3", font=("Calibri", 13)).pack()
    Label(text="").pack()
    Label(text="MENU", height="1", width="35").pack()
    Button(text="1. Add an exam",bd=3,activebackground='white',bg="blue",fg='white', height="2", width="30", command = None).pack()
    Label(text="").pack()
    Button(text="2. Modify an exam",bd=3,activebackground='white',bg="blue",fg='white', height="2", width="30", command=None).pack()
    Label(text="").pack()
    Button(text="3. Delete an exam",bd=3,activebackground='white',bg="blue",fg='white', height="2", width="30", command = None).pack()
    Label(text="").pack()
    Button(text="4. Display all exam details",bd=3,activebackground='white',bg="blue",fg='white', height="2", width="30", command=None).pack()
    Label(text="").pack()
    Button(text="5. Register a student",bd=3,activebackground='white',bg="blue",fg='white', height="2", width="30", command =None ).pack()
    Label(text="").pack()
    Button(text="6. Delete a student",bd=3,activebackground='white',bg="blue",fg='white', height="2", width="30", command=None).pack()
    Label(text="").pack()
    Button(text="7. List the students registered for an exam",bd=3,activebackground='white',bg="blue",fg='white', height="2", width="30", command =None ).pack()
    Label(text="").pack()
    Button(text="8. List the no. of students for each exam",bd=3,activebackground='white',bg="blue",fg='white', height="2", width="30", command=None).pack()
    Label(text="").pack()
    Button(text="9. List the exams registered by a student",bd=3,activebackground='white',bg="blue",fg='white', height="2", width="30", command =None ).pack()
    Label(text="").pack()
    Button(text=" Exit ",bd=3,activebackground='Red',bg="Red",fg='white', height="2", width="30", command = m ).pack()
# End of login page

# Main program utility Main(second) window
def main_user_screen():
    global main_screen
    main_screen = Tk()
    main_screen.geometry("775x675")
    main_screen.title("Exam Management")
    create_menu()
    main_screen.mainloop()


# SQL CONNECTION

# SQL connection to root user at localhost:3306
mydb=mysql.connector.connect(host="localhost",user="root",port='3306', passwd="Vaibhav28@",auth_plugin='mysql_native_password')
print("Logged in successfully")
mycursor=mydb.cursor()
print("Please wait while we configure the software......\n")
try:
    mycursor.execute("CREATE DATABASE edms")
except:
    print("DB already exists")

# SQL connection to database edms in user root at localhost 3306
mydb=mysql.connector.connect(host="localhost",user="root",port='3306', passwd="Vaibhav28@",database="edms")
mycursor=mydb.cursor()
print("Connected to the database successfully")

# Create tables Exam and Student
try:
    mycursor.execute("CREATE TABLE EXAM(Examno INT PRIMARY KEY,Examname VARCHAR(30) UNIQUE,Examday INT NOT NULL,Exammonth INT NOT NULL,Examyear INT NOT NULL,Class INT NOT NULL,Fee INT NOT NULL)")
except:
    print("Exam Table not created")
try:
    mycursor.execute("CREATE TABLE STUDENT(STID INT PRIMARY KEY,Firstname VARCHAR(30),Lastname VARCHAR(30) NOT NULL,Mobilenumber BIGINT NOT NULL,Emailid VARCHAR(30) NOT NULL,Schoolname VARCHAR(50) NOT NULL,Class INT NOT NULL)")
except:
    print(" Student Table not created")


#############----------Menu 1---------#############
#############-------Add an Exam-------#############

def choice1():
    main_screen.destroy()
    window=Tk()
    window.geometry("500x500")
    window.title("Exam mangement")

    # Exam Number Validation
    def no():
        Examno=fn1.get()
        if Examno.isdigit():
            return True
        else:
            messagebox.showerror("Invalid Exam id"," Only Numbers Allowed for Exam id")
            return False

    # Exam Name Validation
    def name():
        Examname=fn2.get().upper()
        if Examname.isalpha():
            return True
        else:
            messagebox.showerror("Invalid Examination Name"," Only Alphabets Allowed for Exam Name")
            return False

    # Exam Date Validation
    def date():
        day=fn3.get()
        month=fn4.get()
        year=fn5.get()
        if day.isdigit() and month.isdigit() and year.isdigit():
            day=int(fn3.get())
            month=int(fn4.get())
            year=int(fn5.get())
            if (month==1 or month==3 or month==5 or month==7 or month==8 or month==10 or month==12):
                max1=31
            elif (month==4 or month==6 or month==9 or month==11):
                max1=30
            elif (year%4==0 and year%100!=0 or year%400==0):                     # for february with leap year
                max1=29
            else:
                max1=28                                                          # for february without leap year
            if (month<1 or month>12):
                messagebox.showerror("Invalid Date"," Date entered does not exist")
                return False
            elif (day<1 or day>max1):
                messagebox.showerror("Invalid Date"," Date entered does not exist")
                return False
            elif year<2020:
                messagebox.showerror("Invalid Date"," Please enter a date that is yet to come")
                return False
            else:
                return True
        else:
            if day.isdigit()==False:
                messagebox.showerror("Invalid Date","Date should be a number")
            if month.isdigit()==False:
                messagebox.showerror("Invalid Month","Month should be a number")
            if year.isdigit()==False:
                messagebox.showerror("Invalid Year","Year should be a number")

    # Class from 1st to 12th Validation
    def classs():
        classs=combobox.get()
        if classs.isdigit():
            if int(classs)<1 or int(classs)>12:
                messagebox.showerror("Invalid Class"," Value for Class is invalid")
                return False
            return True
        else:
            messagebox.showerror("Invalid Class"," Only Numbers Allowed for class")
            return False

    # Fee amount validation
    def fee():
        fee=entry_6.get()
        if fee.isdigit():
            return True
        else:
            messagebox.showerror("Invalid Fee"," Only Numbers Allowed for fee")
            return False

    #Fnc. to return True if no error and False otherwise
    def stuff():
        x1=no()
        x2=name()
        x3=date()
        x4=fee()
        x5=classs()
        return (x1 and x2 and x3 and x4 and x5 and x5)

    #creating window
    label1=Label(window,text="Exam Management",fg="white",bg="black",font=("arial",16))
    label1.pack()

    label2=Label(window,text="Adding an Exam",font=("arial",12,))
    label2.place(x=160,y=60)

    label3=Label(window,text="Enter the Exam id",font=("arial",12))
    label3.place(x=10,y=120)

    fn1=StringVar()

    entry_1= Entry(window,textvar=fn1)
    entry_1.place(x=240,y=120)

    label2=Label(window,text="Enter the Examination name",font=("arial",12))
    label2.place(x=10,y=140)

    fn2=StringVar()

    entry_2= Entry(window,textvar=fn2)
    entry_2.place(x=240,y=140)

    label5=Label(window,text="Enter the Examination Day",font=("arial",12))
    label5.place(x=10,y=160)

    fn3=StringVar()

    entry_3= Entry(window,textvar=fn3)
    entry_3.place(x=240,y=160)

    label6=Label(window,text="Enter the Examination Month",font=("arial",12))
    label6.place(x=10,y=180)

    fn4=StringVar()

    entry_4= Entry(window,textvar=fn4)
    entry_4.place(x=240,y=180)

    label7=Label(window,text="Enter the Examination Year",font=("arial",12))
    label7.place(x=10,y=200)

    fn5=StringVar()

    entry_5= Entry(window,textvar=fn5)
    entry_5.place(x=240,y=200)

    label8=Label(window,text="Enter Fee",font=("arial",12))
    label8.place(x=10,y=220)

    fn6=StringVar()

    entry_6= Entry(window,textvar=fn6)
    entry_6.place(x=240,y=220)

    label8=Label(window,text="Enter Class",font=("arial",12))
    label8.place(x=10,y=240)

    combobox=Combobox(window)
    items=("1","2","3","4","5","6","7","8","9","10","11","12")
    combobox['values']=items
    combobox.bind("<<ComboboxSelected>>")
    combobox.place(x=240,y=240)

    #Fnc. to create window to add exam details
    def pt():
        Examno=fn1.get()
        Examname=fn2.get().upper()
        Examday=fn3.get()
        Exammonth=fn4.get()
        Examyear=fn5.get()
        classs=combobox.get()
        Fee=fn6.get()
        mycursor.execute("SELECT Examno FROM EXAM")
        idraw=mycursor.fetchall()
        idlist=[]

        # Exam window validation
        for i in idraw:
            idlist.append(i[0])
        if Examno=='' or Examname=='' or Examday==''  or Examyear=='' or Fee=='' or Exammonth=='' or classs=='' :
            messagebox.showerror("Error","All fields Required")
        elif not Examno.isdigit():
            messagebox.showerror("Error","Exam ID has to be a number")
        elif int(Examno) in idlist:
            messagebox.showerror("Error","Given Exam ID already exists")
        
        # Insert exam details into table
        else:
            if stuff():
                label10=Label(window,text="Exam Details are Added Successfully",font=("arial",12))
                label10.place(x=100,y=350)
                l=[]
                l.append(Examno)
                l.append(Examname)
                l.append(Examday)
                l.append(Exammonth)
                l.append(Examyear)
                l.append(classs)
                l.append(Fee)
                insertsql= "INSERT INTO EXAM (Examno, Examname, Examday , Exammonth, Examyear, Class, Fee) VALUES(%s,%s,%s,%s,%s,%s,%s)"
                mycursor.executemany(insertsql, (l,))
                insertsql= "ALTER TABLE STUDENT ADD {0} INT DEFAULT 0".format(Examname)
                mycursor.execute(insertsql)
                mydb.commit()
    button=Button(window,text="Submit",fg="white",bg="green",relief="ridge",font=("arial",12,"bold"),command=pt)
    button.place(x=220,y=300)

    # Funtion to clear input boxes in window
    def clear():
        fn1.set("")
        fn2.set("")
        fn3.set("")
        fn4.set("")
        fn5.set("")
        fn6.set("")
        combobox.set('')
    button1=Button(window,text="clear",fg="white",bg="red",relief="ridge",font=("arial",12,"bold"),command=clear)
    button1.place(x=40,y=440)

    # Exit window
    def leave():
        window.destroy()
        main_user_screen()
    button2=Button(window,text="Exit",fg="white",bg="Red",relief="ridge",font=("arial",12,"bold"),command=leave)
    button2.place(x=420,y=440)
    window.mainloop()



#############----------Menu 2---------#############
#############-----Modify an Exam------#############
def modify(key):
    window1 = Tk()
    window1.geometry("500x500")
    window1.title("Exam mangement")

    # Date validation
    def date():
        day=entry_3.get()
        month=entry_4.get()
        year=entry_5.get()
        if day.isdigit() and month.isdigit() and year.isdigit():
            day=int(entry_3.get())
            month=int(entry_4.get())
            year=int(entry_5.get())
            if (month==1 or month==3 or month==5 or month==7 or month==8 or month==10 or month==12):
                max1=31
            elif (month==4 or month==6 or month==9 or month==11):
                max1=30
            elif (year%4==0 and year%100!=0 or year%400==0):        # for february with leap year
                max1=29
            else:
                max1=28                                             # for february without leap year
            if (month<1 or month>12):
                messagebox.showerror("Invalid Date"," Date entered does not exist")
                return False
            elif (day<1 or day>max1):
                messagebox.showerror("Invalid Date"," Date entered does not exist")
                return False
            elif year<2020:
                messagebox.showerror("Invalid Date"," Please enter a date that is yet to come")
                return False
            else:
                return True
    
        else:
            if day.isdigit()==False:
                messagebox.showerror("Invalid Date","Date should be a number")
            if month.isdigit()==False:
                messagebox.showerror("Invalid Month","Month should be a number")
            if year.isdigit()==False:
                messagebox.showerror("Invalid Year","Year should be a number")

    # Class validation   
    def classs():
        classs=combobox.get()
        if classs.isdigit():
            if int(classs)<1 or int(classs)>12:
                messagebox.showerror("Invalid Class"," Value for Class is invalid")
                return False
            return True
        else:
            messagebox.showerror("Invalid Class"," Only Numbers Allowed for class")
            return False

    # Fee Validation
    def fee():
        fee=entry_6.get()
        if fee.isdigit():
            return True
        else:
            messagebox.showerror("Invalid Fee"," Only Numbers Allowed for fee")
            return False

    #Fnc. to return True if no error and False otherwise
    def stuff():
        x3=date()
        x4=fee()
        x5=classs()
        return (x3 and x4 and x5)

    a = "SELECT * FROM EXAM WHERE Examno={0}".format(key)
    mycursor.execute(a)
    iresult = mycursor.fetchall()

    iresult = iresult[0]
    label1 = Label(window1, text="Exam Mangement", fg="white", bg="black", font=("arial", 16))
    label1.pack()

    label2 = Label(window1, text="MODIFYING an Exam", font=("arial", 12,))
    label2.place(x=160, y=60)

    label3 = Label(window1, text=("The Exam id is " + str(iresult[0])), font=("arial", 12))
    label3.place(x=10, y=120)

    label2 = Label(window1, text=("The Examination name is " + str(iresult[1])), font=("arial", 12))
    label2.place(x=10, y=140)

    label5 = Label(window1, text="Enter the Examination Day", font=("arial", 12))
    label5.place(x=10, y=160)

    entry_3 = Entry(window1)
    entry_3.place(x=240, y=160)
    entry_3.insert(0, iresult[2])

    label6 = Label(window1, text="Enter the Examination Month", font=("arial", 12))
    label6.place(x=10, y=180)

    entry_4 = Entry(window1)
    entry_4.place(x=240, y=180)
    entry_4.insert(0, iresult[3])

    label7 = Label(window1, text="Enter the Examination Year", font=("arial", 12))
    label7.place(x=10, y=200)

    entry_5 = Entry(window1)
    entry_5.place(x=240, y=200)
    entry_5.insert(0, iresult[4])

    label8 = Label(window1, text="Enter Fee", font=("arial", 12))
    label8.place(x=10, y=220)

    entry_6 = Entry(window1)
    entry_6.place(x=240, y=220)
    entry_6.insert(0, iresult[6])

    label8 = Label(window1, text="Enter Class", font=("arial", 12))
    label8.place(x=10, y=240)

    combobox = Combobox(window1)
    items = ("1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12")
    combobox['values'] = items
    combobox.set(iresult[5])
    combobox.bind("<<ComboboxSelected>>")
    combobox.place(x=240, y=240)

    # Function to Modify Exam Details
    def pt():
        Examday = entry_3.get()
        Exammonth = entry_4.get()
        Examyear = entry_5.get()
        classs = combobox.get()
        Fee = entry_6.get()
        if Examday == '' or Examyear == '' or Fee == '' or Exammonth == '' or classs == '':
            messagebox.showerror("Error", "All fields Required")
        
        # Modify Exam Details 
        else:
            if stuff():
                b = "ALTER TABLE STUDENT DROP COLUMN {0}".format(iresult[1])
                mycursor.execute(b)
                mydb.commit()
                a = "DELETE FROM EXAM WHERE Examno=%s"
                mycursor.execute(a, [key])
                mydb.commit()
                l = []
                l.append(key)
                l.append(iresult[1])
                l.append(Examday)
                l.append(Exammonth)
                l.append(Examyear)
                l.append(classs)
                l.append(Fee)
                label10 = Label(window1, text="Exam Details are Modified Successfully", font=("arial", 12))
                label10.place(x=100, y=350)
                insertsql = "INSERT INTO EXAM (Examno, Examname, Examday , Exammonth, Examyear, Class, Fee) VALUES(%s,%s,%s,%s,%s,%s,%s)"
                mycursor.executemany(insertsql, (l,))
                insertsql = "ALTER TABLE STUDENT ADD {0} INT DEFAULT 0".format(iresult[1])
                mycursor.execute(insertsql)
                mydb.commit()
    button = Button(window1, text="Submit", fg="white", bg="green", relief="ridge", font=("arial", 12, "bold"), command=pt)
    button.place(x=220, y=300)

    # Function to clear input boxes
    def clear():
        entry_2.delete(0, 100)
        entry_3.delete(0, 100)
        entry_4.delete(0, 100)
        entry_5.delete(0, 100)
        entry_6.delete(0, 100)
        combobox.set("")

    button1 = Button(window1, text="clear", fg="white", bg="red", relief="ridge", font=("arial", 12, "bold"), command=clear)
    button1.place(x=40, y=440)

    #Function to exit
    def leave():
        window1.destroy()
    button2 = Button(window1, text="Exit", fg="white", bg="Red", relief="ridge", font=("arial", 12, "bold"), command=leave)
    button2.place(x=420, y=440)
    window1.mainloop()

#############----------Menu 2---------#############
#############------Modify an Exam-----#############

def choice2():
    main_screen.destroy()
    window = Tk()
    window.geometry("500x500")
    window.title("Exam mangement")

    label1 = Label(window, text="Exam Management", fg="white", bg="black", font=("arial", 16))
    label1.pack()

    label2 = Label(window, text="Modifying an Exam", font=("arial", 12,))
    label2.place(x=160, y=60)

    label3 = Label(window, text="Enter the Exam id", font=("arial", 12))
    label3.place(x=10, y=120)
    fn1 = StringVar()
    entry_1 = Entry(window, textvar=fn1)
    entry_1.place(x=260, y=120)
    Examno = fn1.get()

    # Validate Exam number / id
    def check():
        Examno = fn1.get()
        mycursor.execute("SELECT Examno FROM EXAM")
        idraw = mycursor.fetchall()
        l = []
        for i in idraw:
            l.append(i[0])
        if not Examno.isdigit():
            messagebox.showerror("Error", "Enter only numbers for Exam id")
        elif int(Examno) not in l:
            messagebox.showerror("Error", "Exam id DOES NOT EXIST")
        else:
            Examno=int(Examno)
            modify(fn1.get())
    
    # Exit function
    def leave():
        window.destroy()
        main_user_screen()

    button2 = Button(window, text="Exit", fg="white", bg="Red", relief="ridge", font=("arial", 12, "bold"), command=leave)
    button2.place(x=420, y=440)

    button = Button(window, text="Submit", fg="white", bg="green", relief="ridge", font=("arial", 12, "bold"), command=check)
    button.place(x=220, y=300)

    # Clear Input
    def clear():
        fn1.set("")

    button1 = Button(window, text="clear", fg="white", bg="red", relief="ridge", font=("arial", 12, "bold"), command=clear)
    button1.place(x=40, y=440)
    window.mainloop()

#############----------Menu 3---------#############
#############------Delete an Exam-----#############

def choice3():
    main_screen.destroy()
    window=Tk()
    window.geometry("500x500")
    window.title("Exam mangement")

    #Fnc. to fetch all records
    def prt():
        def leave1():
            window1.destroy()
        def check_empty():
            Examno=fn1.get()
            z="SELECT Examname FROM EXAM WHERE Examno=%s"
            mycursor.execute(z,[Examno])
            t=mycursor.fetchall()
            mydb.commit()
            a="SELECT STID,Firstname,Lastname,Class FROM STUDENT WHERE {0}=1".format(t[0][0])
            mycursor.execute(a)
            idraw=mycursor.fetchall()
            l=[]
            for i in idraw:
                l.append(list(i))
            if l==[]:
                return False
            else:
                return True

        # Function to delete an exam that already exists
        def dele():
            Examno=[fn1.get()]
            z="SELECT Examname FROM EXAM WHERE Examno=%s"
            mycursor.execute(z,Examno)
            t=mycursor.fetchall()
            mydb.commit()
            a="DELETE FROM EXAM WHERE Examno=%s"
            mycursor.execute(a,Examno)
            mydb.commit()
            b="ALTER TABLE STUDENT DROP COLUMN {0}".format(t[0][0])
            mycursor.execute(b)
            mydb.commit()
            label3=Label(window1,text="Deleted Details Successfully",font=("arial",12,))
            label3.place(x=110,y=340)
        #To create window for deletion
        Examno=[fn1.get()]
        mycursor.execute("SELECT Examno FROM EXAM")
        idraw=mycursor.fetchall()
        idlist=[]
        for i in idraw:
            idlist.append(i[0])
        k=fn1.get()
        if not k.isdigit():
            messagebox.showerror("Error", "Enter only numbers for Exam id")
        elif int(k) not in idlist:
            messagebox.showerror("Error","Exam id DOES NOT EXIST")
        elif check_empty():
            messagebox.showerror("Error","Students have registered for this exam")
        else:
            window1=Tk()
            window1.geometry("500x500")
            window1.title("Exam mangement")
            label2=Label(window1,text="Existing Details of Exam",font=("arial",12,))
            label2.place(x=160,y=10)
            a=("SELECT * FROM EXAM WHERE Examno=%s")
            mycursor.execute(a,Examno)
            idraw=mycursor.fetchall()
            l=[]
            for i in idraw:
                if i[0]==int(k):
                    l.append(list(i))
            # create Treeview with 7 columns
            cols = ('Exam id', 'Exam Name', 'Day', 'Month', 'Year', 'Exam Fee', 'Class')
            tree = ttk.Treeview(window1, columns=cols, show='headings')
            # set column headings
            for col in cols:
                tree.heading(col, text=col)
            for i, (number, name, day, month, year, fee, clas) in enumerate(l, start=1):
                tree.insert("", "end", values=(number, name, day, month, year, fee, clas))
            tree.place(x=10,y=50)  #,row=1, column=0, columnspan=1

            label2=Label(window1,text="Do You Still Want to Delete Exam????",font=("arial",12,))
            label2.place(x=110,y=300)
            button1=Button(window1,text="Yes",fg="white",bg="green",relief="ridge",font=("arial",12,"bold"),command=dele)
            button1.place(x=80,y=370)
            button2=Button(window1,text="No",fg="white",bg="Red",relief="ridge",font=("arial",12,"bold"),command= leave1)
            button2.place(x=380,y=370)
            button3=Button(window1,text="EXIT",fg="black",bg="Red",relief="ridge",font=("arial",12,"bold"),command= leave1)
            button3.place(x=210,y=400)
            window1.mainloop()
    
    # Function to exit
    def leave():
        window.destroy()
        main_user_screen()
    button=Button(window,text="Submit",fg="white",bg="green",relief="ridge",font=("arial",12,"bold"),command=prt)
    button.place(x=80,y=340)
    button2=Button(window,text="Exit",fg="white",bg="Red",relief="ridge",font=("arial",12,"bold"),command= leave)
    button2.place(x=380,y=340)

    label1=Label(window,text="Exam Management",fg="white",bg="black",font=("arial",16))
    label1.pack()

    label2=Label(window,text="Deleting an Exam",font=("arial",12,))
    label2.place(x=160,y=60)

    label3=Label(window,text="Enter the Exam id",font=("arial",12))
    label3.place(x=10,y=120)
    fn1=StringVar()
    entry_1= Entry(window,textvar=fn1)
    entry_1.place(x=240,y=120)
    window.mainloop()

#############----------Menu 4---------#############
#############---Display Exam Details--#############

def choice4():
    main_screen.destroy()
    window = Tk()
    window.geometry("1430x300")
    window.title("Exam mangement")
    def show():
        mycursor.execute("SELECT * FROM EXAM")
        idraw=mycursor.fetchall()
        l=[]
        for i in idraw:
            l.append(list(i))
        # create Treeview with 7 columns
        cols = ('Exam id', 'Exam Name', 'Day', 'Month', 'Year', 'Class', 'Exam Fee')
        tree = ttk.Treeview(window, columns=cols, show='headings')
        # set column headings
        for col in cols:
            tree.heading(col, text=col)
        for i, (number, name, day, month, year, clas, fee) in enumerate(l, start=1):
            tree.insert("", "end", values=(number, name, day, month, year, clas, fee))
        tree.place(x=10,y=10)  #,row=1, column=0, columnspan=1
    show()

    # Function to Exit
    def leave():
        window.destroy()
        main_user_screen()
    closeButton = Button(window, text="Close", width=15, command=leave)
    closeButton.place(x=630,y=260)


#############----------Menu 5---------#############
#############----Register a Student---#############

def choice5():
    main_screen.destroy()
    window=Tk()
    window.geometry("500x500")
    window.title("Exam mangement")
    label1=Label(window,text="Exam Management",fg="white",bg="black",font=("arial",16))
    label1.pack()

    label2=Label(window,text="Registering A Student",font=("arial",12,))
    label2.place(x=160,y=60)

    label3=Label(window,text="Have You Registered Once Before??",font=("arial",12,))
    label3.place(x=120,y=120)

    # Verify exam and student details
    def unwanted():
        window.destroy()
        window1=Tk()
        window1.geometry("500x500")
        window1.title("Exam mangement")
        mycursor.execute("SELECT STID FROM STUDENT")
        idraw=mycursor.fetchall()
        l=[]
        for i in idraw:
            l.append(i[0])
        mycursor.execute("SELECT Examname FROM EXAM")
        idraw1=mycursor.fetchall()
        e=[]
        for i in idraw1:
            e.append(i[0])
        
        # Student id verification
        def STID():
                stid=fn3.get()
                if stid.isdigit():
                    if int(stid) in l:
                        return True
                    else:
                        messagebox.showerror("Error","Student Id not found")
                        return False
                else:
                    messagebox.showerror("Invalid Input"," Only Numbers Allowed")
                    return False

        # Exam name verification
        def Enames():
                Ename=fn4.get()
                if Ename.isalpha():
                    if Ename.upper() in e:
                        return True
                    else:
                        messagebox.showerror("Error","Exam Name not found")
                        return False
                else:
                    messagebox.showerror("Invalid Input"," Only Letters Allowed")
                    return False

        #Fnc. to return True if no error and False otherwise
        def stuff():
            x1=STID()
            x2=Enames()
            return(x1 and x2)

        label1=Label(window1,text="Exam Management",fg="white",bg="black",font=("arial",16))
        label1.pack()


        label2=Label(window1,text="Registering A Student",font=("arial",12,))
        label2.place(x=160,y=60)

        label3=Label(window1,text="Enter Student ID",font=("arial",12))
        label3.place(x=10,y=120)
        fn3=StringVar()
        entry_3= Entry(window1,textvar=fn3)
        entry_3.place(x=240,y=120)

        label4=Label(window1,text="Enter the Exam Name",font=("arial",12))
        label4.place(x=10,y=140)
        fn4=StringVar()
        entry_4= Entry(window1,textvar=fn4)
        entry_4.place(x=240,y=140)

        Ename=fn4.get()
        stid=fn3.get()

        def pt1():
            Ename=fn4.get().upper()
            stid=fn3.get()
            if stid=='' or Ename=='' :
                    messagebox.showerror("Error","All fields Required")
            else:
                if stuff():
                    print(Ename)
                    b="SELECT Class FROM EXAM WHERE Examname=%s"
                    mycursor.execute(b,(Ename,))
                    q=mycursor.fetchall()
                    print('q:',q)
                    c="SELECT Class FROM STUDENT WHERE STID={0}".format(stid)
                    mycursor.execute(c)
                    r=mycursor.fetchall()
                    print('r:',r)
                    if r[0][0] == q[0][0]:
                        a='SELECT {0} FROM STUDENT WHERE STID={1}'.format(Ename,stid)
                        mycursor.execute(a)
                        p=mycursor.fetchall()
                        if p[0][0]==1:
                            messagebox.showinfo("Already registered","You have already registered for this exam")
                        else:
                            update="UPDATE STUDENT SET {0}=1 WHERE STID={1}".format(Ename,stid)
                            mycursor.execute(update)
                            mydb.commit()
                            label101=Label(window1,text="Student registered for exam successfully",font=("arial",16))
                            label101.place(x=50,y=330)

                    else:
                        messagebox.showerror("Class Error","This Exam is not availabe for your class")

        button121=Button(window1,text="Submit",fg="white",bg="green",relief="ridge",font=("arial",12,"bold"),command=pt1)
        button121.place(x=220,y=300)

        # Function to Exit
        def leave():
            window1.destroy()
            main_user_screen()

        button2=Button(window1,text="Exit",fg="white",bg="Red",relief="ridge",font=("arial",12,"bold"),command=leave)
        button2.place(x=220,y=440)

    # Verifying registration
    def menu5_1():

        window=Tk()
        window.geometry("500x500")
        window.title("Exam mangement")
        label1=Label(window,text="Exam Management",fg="white",bg="black",font=("arial",16))
        label1.pack()


        label2=Label(window,text="Registering A Student",font=("arial",12,))
        label2.place(x=160,y=60)


        label3=Label(window,text="Have You Registered Before Itself??",font=("arial",12,))
        label3.place(x=120,y=120)


        button1=Button(window,text="Yes",fg="white",bg="green",relief="ridge",font=("arial",12,"bold"))
        button1.place(x=80,y=300)

    # Menu 5 Window
    def menu5():
        window.destroy()
        window1=Tk()
        window1.geometry("500x500")
        window1.title("Exam mangement")

        # Verify Student ID
        def STID():
                stid=fn29.get()
                if stid.isdigit():
                    return True
                else:
                    messagebox.showerror("Invalid Input"," Only Numbers Allowed for Student ID")
                    return False

        # First name verification
        def Fname():
                Fname=fn1.get()
                if Fname.isalpha():
                    return True
                else:
                    messagebox.showerror("Invalid Input"," Only Letters Allowed for Firstname")
                    return False

        # Last name verification
        def Lname():
                Examname=fn2.get()
                if Examname.isalpha():
                    return Lname
                else:
                    messagebox.showerror("Invalid Input"," Only Letters Allowed for Lastname")
                    return False

        # Mobile number verification
        def Mobileno():
                Mobileno=fn3.get()
                if Mobileno.isdigit():
                    if len(Mobileno)==10:
                        return True
                    else:
                        messagebox.showerror("Error","Mobile Number should be of 10 digits")
                        return False
                else:
                    messagebox.showerror("Error","Mobile Number should consist of digits only")
                    return False

        # Email Verification
        def mail():
            mail=fn4.get()
            if ('@' in mail) and (('.com' in mail) or ('.in'  in mail)):
                return True
            else:
                    messagebox.showerror("Error","Invalid MailID")
                    return False

        #Class Verification
        def classs():
            classs=combobox.get()
            if classs.isdigit():
                if int(classs)<1 or int(classs)>12:
                    messagebox.showerror("Invalid Class"," Value for Class is invalid")
                    return False
                return True
            else:
                messagebox.showerror("Invalid Class"," Only Numbers Allowed for class")
                return False

        # Exam Name Verification
        def name1():
            Examinationname=fn5.get().upper()
            mycursor.execute("SELECT Examname FROM EXAM")
            idraw1=mycursor.fetchall()
            e=[]
            for i in idraw1:
                e.append(i[0])
            if Examinationname not in e:
                messagebox.showerror("Invalid Input"," The Exam you have entered doesn't exist")
                return False
            elif Examinationname.isalpha():
                return True
            else:
                messagebox.showerror("Invalid Input"," Only Letters Allowed")
                return False

        #Fnc. to return True if no error and False otherwise
        def stuff():
            x1=Fname()
            x2=Lname()
            x3=Mobileno()
            x4=mail()
            x5=STID()
            x6=classs()
            x7=name1()
            return(x1 and x2 and x3 and x4 and x5 and x6 and x7)

        label1=Label(window1,text="Exam Management",fg="white",bg="black",font=("arial",16))
        label1.pack()


        label2=Label(window1,text="Registering A Student",font=("arial",12,))
        label2.place(x=160,y=60)


        label29=Label(window1,text="Enter Student ID",font=("arial",12))
        label29.place(x=10,y=120)
        fn29=StringVar()
        entry_29= Entry(window1,textvar=fn29)
        entry_29.place(x=240,y=120)

        label3=Label(window1,text="Enter the Student First Name",font=("arial",12))
        label3.place(x=10,y=140)
        fn1=StringVar()
        entry_1= Entry(window1,textvar=fn1)
        entry_1.place(x=240,y=140)

        label2=Label(window1,text="Enter the Student Last Name",font=("arial",12))
        label2.place(x=10,y=160)
        fn2=StringVar()
        entry_2= Entry(window1,textvar=fn2)
        entry_2.place(x=240,y=160)

        label5=Label(window1,text="Enter Mobile No.",font=("arial",12))
        label5.place(x=10,y=180)
        fn3=StringVar()
        entry_3= Entry(window1,textvar=fn3)
        entry_3.place(x=240,y=180)

        label6=Label(window1,text="Enter Email ID",font=("arial",12))
        label6.place(x=10,y=200)
        fn4=StringVar()
        entry_4= Entry(window1,textvar=fn4)
        entry_4.place(x=240,y=200)

        label7=Label(window1,text="Enter the Examination name",font=("arial",12))
        label7.place(x=10,y=220)
        fn5=StringVar()
        entry_5= Entry(window1,textvar=fn5)
        entry_5.place(x=240,y=220)

        label8=Label(window1,text="Enter School Name",font=("arial",12))
        label8.place(x=10,y=240)
        fn6=StringVar()
        entry_6= Entry(window1,textvar=fn6)
        entry_6.place(x=240,y=240)

        combobox=Combobox(window1)
        label9=Label(window1,text="Enter Class",font=("arial",12))
        label9.place(x=10,y=260)
        items=("1","2","3","4","5","6","7","8","9","10","11","12")
        combobox['values']=items
        combobox.bind("<<ComboboxSelected>>")
        combobox.place(x=240,y=260)

        def pt():
            Firstname=fn1.get()
            Lastname=fn2.get()
            stid=fn29.get()
            Mobilenumber=fn3.get()
            Emailid=fn4.get()
            Examinationname=fn5.get().upper()
            Schoolname=fn6.get()
            Class=combobox.get()
            if stid=='' or Firstname=='' or Lastname=='' or Mobilenumber==''  or Emailid=='' or Examinationname=='' or Schoolname=='' or Class=='' :
                    messagebox.showerror("Error","All fields Required")
            else:
                if stuff():
                    b="SELECT Class FROM EXAM WHERE Examname=%s"
                    mycursor.execute(b,(Examinationname,))
                    q=mycursor.fetchall()
                    print('q:',q)
                    if q[0][0]==int(Class):
                        label10=Label(window1,text="Student Details are Added Successfully",font=("arial",12))
                        label10.place(x=100,y=350)
                        l=[]
                        l.append(stid)
                        l.append(Firstname)
                        l.append(Lastname)
                        l.append(Mobilenumber)
                        l.append(Emailid)
                        l.append(Schoolname)
                        l.append(Class)
                        insertsql= "INSERT INTO STUDENT (STID ,Firstname, Lastname, Mobilenumber , Emailid, Schoolname, Class) VALUES(%s,%s,%s,%s,%s,%s,%s)"
                        mycursor.executemany(insertsql, (l,))
                        mydb.commit()
                        update="UPDATE STUDENT SET {0}=1 WHERE STID={1}".format(Examinationname,stid)
                        mycursor.execute(update)
                        mydb.commit()

                    else:
                        messagebox.showerror("Class Error","This Exam is not availabe for your class")

        button=Button(window1,text="Submit",fg="white",bg="green",relief="ridge",font=("arial",12,"bold"),command=pt)
        button.place(x=220,y=300)

        # Clear input boxes
        def clear():
            fn1.set("")
            fn2.set("")
            fn3.set("")
            fn4.set("")
            fn5.set("")
            fn6.set("")
            fn29.set("")
            combobox.set("")

        button1=Button(window1,text="clear",fg="white",bg="red",relief="ridge",font=("arial",12,"bold"),command=clear)
        button1.place(x=40,y=440)

        # Function to Exit
        def leave():
            window1.destroy()
            main_user_screen()

        button2=Button(window1,text="Exit",fg="white",bg="Red",relief="ridge",font=("arial",12,"bold"),command=leave)
        button2.place(x=420,y=440)
        window1.mainloop()

    button2=Button(window,text="No",fg="white",bg="red",relief="ridge",font=("arial",12,"bold"),command=menu5)
    button2.place(x=390,y=300)

    button4=Button(window,text="Yes",fg="white",bg="Green",relief="ridge",font=("arial",12,"bold"),command=unwanted)
    button4.place(x=80,y=300)
    window.mainloop()

#############----------Menu 6---------#############
#############----Delete a student-----#############
def choice6():
    main_screen.destroy()
    window=Tk()
    window.geometry("500x500")
    window.title("Exam mangement")

    # Deleting
    def prt():
        def dele():
            a="DELETE FROM STUDENT WHERE STID=%s"
            STID=[fn1.get()]
            mycursor.execute(a,STID)
            mydb.commit()
            label3=Label(window1,text="Deleted Details Successfully",font=("arial",12,))
            label3.place(x=110,y=340)
        STID=[fn1.get()]
        mycursor.execute("SELECT STID FROM STUDENT")
        idraw=mycursor.fetchall()
        idlist=[]
        for i in idraw:
            idlist.append(i[0])
        k=fn1.get()
        if not str(k).isdigit():
            messagebox.showerror("Error","Student Number Should be a Digit")
        elif int(k) not in idlist:
            messagebox.showerror("Error","STUDENT WITH GIVEN ID DOES NOT EXIST")
        else:
            window1=Tk()
            window1.geometry("500x500")
            window1.title("Exam Management")
            label2=Label(window1,text="Existing Details of STUDENT",font=("arial",12,))
            label2.place(x=160,y=10)
            a=("SELECT STID,Firstname,Lastname,Class FROM STUDENT WHERE STID=%s")
            mycursor.execute(a,STID)
            idraw=mycursor.fetchall()
            l=[]
            for i in idraw:
                l.append(list(i))
            print(l)
            # create Treeview with 4 columns
            cols = ('STID', 'Firstname', 'Lastname', 'Class')
            tree = ttk.Treeview(window1, columns=cols, show='headings')
            # set column headings
            for col in cols:
                tree.heading(col, text=col)

            for i, (STID, Firstname, Lastname, Class) in enumerate(l, start=1):
                tree.insert("", "end", values=(STID, Firstname, Lastname, Class))
            tree.place(x=10,y=50)  #,row=1, column=0, columnspan=1

            label2=Label(window1,text="Do You Still Want to Delete Student record????",font=("arial",12,))
            label2.place(x=110,y=300)
            button1=Button(window1,text="Yes",fg="white",bg="green",relief="ridge",font=("arial",12,"bold"),command=dele)
            button1.place(x=80,y=370)
            button2=Button(window1,text="No",fg="white",bg="Red",relief="ridge",font=("arial",12,"bold"),command= lambda : window1.destroy())
            button2.place(x=380,y=370)
            button3=Button(window1,text="Exit",fg="black",bg="Red",relief="ridge",font=("arial",12,"bold"),command= lambda : window1.destroy())
            button3.place(x=210,y=400)
            window1.mainloop()

    # Function to Exit
    def leave():
        window.destroy()
        main_user_screen()

    button2=Button(window,text="Exit",fg="white",bg="Red",relief="ridge",font=("arial",12,"bold"),command= leave)
    button2.place(x=380,y=340)

    label1=Label(window,text="Exam Management",fg="white",bg="black",font=("arial",16))
    label1.pack()

    label2=Label(window,text="Deleting a student record",font=("arial",12,))
    label2.place(x=160,y=60)

    label3=Label(window,text="Enter the STID",font=("arial",12))
    label3.place(x=10,y=120)
    fn1=StringVar()
    entry_1= Entry(window,textvar=fn1)
    entry_1.place(x=240,y=120)
    button=Button(window,text="Submit",fg="white",bg="green",relief="ridge",font=("arial",12,"bold"),command=prt)
    button.place(x=80,y=340)
    window.mainloop()

#############------------------Menu 7-----------------#############
#############---List Students registered for an exam--#############
def choice7():
    main_screen.destroy()
    def display_7(Examno):
        window=Tk()
        window.geometry("800x400")
        window.title("Exam mangement")
        label1=Label(window,text="Exam Management",fg="white",bg="black",font=("arial",16))
        label1.pack()
        label2=Label(window,text="Displaying Number of Students registered for an Exam",font=("arial",12,))
        label2.place(x=50,y=60)
        z="SELECT Examname FROM EXAM WHERE Examno=%s"
        mycursor.execute(z,[Examno])
        t=mycursor.fetchall()
        mydb.commit()
        a="SELECT STID,Firstname,Lastname,Class FROM STUDENT WHERE {0}=1".format(t[0][0])
        mycursor.execute(a)
        idraw=mycursor.fetchall()
        l=[]
        for i in idraw:
            l.append(list(i))
        xyz="Students registered for :"+t[0][0]
        label50=Label(window,text=xyz,font=("arial",12,))
        label50.place(x=5,y=5)

        # create Treeview with 3 columns
        cols = ('STID', 'Firstname', 'Lastname','Class')
        tree = ttk.Treeview(window, columns=cols, show='headings')
        # set column headings
        for col in cols:
            tree.heading(col, text=col)

        for i, (id1, Fname,Lname, classs) in enumerate(l, start=1):
            tree.insert("", "end", values=(id1, Fname,Lname, classs))
        tree.place(x=10,y=30)  #,row=1, column=0, columnspan=1

        closeButton = Button(window, text="Close", width=15, command=lambda: window.destroy())
        closeButton.place(x=350, y=345)

    # Verify Exam ID
    def check_7():
        Examno = fn1.get()
        mycursor.execute("SELECT Examno FROM EXAM")
        idraw = mycursor.fetchall()
        l = []
        for i in idraw:
            l.append(i[0])
        if not Examno.isdigit():
            messagebox.showerror("Error", "Enter only numbers for Exam id")
        elif int(Examno) not in l:
            messagebox.showerror("Error", "Exam id DOES NOT EXIST")
        else:
            Examno=int(Examno)
            display_7(fn1.get())
    window=Tk()
    window.geometry("500x500")
    window.title("Exam mangement")
    label1=Label(window,text="Exam Management",fg="white",bg="black",font=("arial",16))
    label1.pack()

    label2=Label(window,text="Displaying Students registered for an Exam",font=("arial",12,))
    label2.place(x=50,y=60)

    label3=Label(window,text="Enter the Exam ID",font=("arial",12))
    label3.place(x=10,y=120)

    fn1=StringVar()

    entry_1= Entry(window,textvar=fn1)
    entry_1.place(x=240,y=120)

    label2=Label(window,text="",font=("arial",12,))
    label2.place(x=100,y=400)

    button=Button(window,text="Submit",fg="white",bg="green",relief="ridge",font=("arial",12,"bold"),command=check_7)
    button.place(x=220,y=300)

    # Function to Exit
    def leave():
        window.destroy()
        main_user_screen()

    button45=Button(window,text="Exit",fg="white",bg="red",relief="ridge",font=("arial",12,"bold"),command=leave)
    button45.place(x=220,y=350)

    window.mainloop()

#############----------Menu 8----------#############
#############-List the no. of students-#############
def choice8():
    main_screen.destroy()
    def display_8():
        window=Tk()
        window.geometry("800x400")
        window.title("Exam mangement")
        label1=Label(window,text="Exam Management",fg="white",bg="black",font=("arial",16))
        label1.pack()
        label2=Label(window,text="Displaying Number of Students registered for an Exam",font=("arial",12,))
        label2.place(x=50,y=60)
        mycursor.execute("SELECT Examname FROM EXAM ")
        t=mycursor.fetchall()
        mydb.commit()
        mycursor.execute("SELECT Examno FROM EXAM")
        idraw1 = mycursor.fetchall()
        L = []
        for i in idraw1:
            L.append(i[0])
        l=[]
        for i in range(len(L)):
            a="SELECT Examno,Examname FROM EXAM WHERE Examno={0}".format(L[i])
            mycursor.execute(a)
            idraw=mycursor.fetchall()
            temp='SELECT COUNT(*) FROM STUDENT WHERE {0}=1'.format(t[i][0])
            mycursor.execute(temp)
            studval=mycursor.fetchall()
            L_idraw=list(idraw[0])
            L_idraw.append(studval[0][0])
            l.append(L_idraw)

        # create Treeview with 3 columns
        cols = ('Exam id', 'Exam Name', 'No of Students registered')
        tree = ttk.Treeview(window, columns=cols, show='headings')
        # set column headings
        for col in cols:
            tree.heading(col, text=col)
        for i, (number, name, stud) in enumerate(l, start=1):
            tree.insert("", "end", values=(number, name, stud))
        tree.place(x=10,y=50)  #,row=1, column=0, columnspan=1
        closeButton = Button(window, text="Close", width=15, command=lambda: window.destroy())
        closeButton.place(x=350, y=345)
    # Verify Exam ID
    def check_8():
        Examno = fn1.get()
        mycursor.execute("SELECT Examno FROM EXAM")
        idraw = mycursor.fetchall()
        l = []
        for i in idraw:
            l.append(i[0])
        if not Examno.isdigit():
            messagebox.showerror("Error", "Enter only numbers for Exam id")
        elif int(Examno) not in l:
            messagebox.showerror("Error", "Exam id DOES NOT EXIST")
        else:
            Examno=int(Examno)
            display_8(fn1.get())
    display_8()
    # Function to Exit
    def leave():
        window.destroy()
        main_user_screen()

#############------------------Menu 9----------------#############
#############-List all exams registered by a student-#############
def choice9():
    main_screen.destroy()
    def display_9(stid):
        window=Tk()
        window.geometry("800x400")
        window.title("Exam mangement")
        label1=Label(window,text="Exam Management",fg="white",bg="black",font=("arial",16))
        label1.pack()
        print(type(stid))
        mycursor.execute("SELECT Examname FROM EXAM")
        L=mycursor.fetchall()
        print(L)
        lst1=[]
        for i in L:
            lst1.append(i[0])
        z="SELECT STID FROM STUDENT WHERE STID=%s"
        mycursor.execute(z,[stid])
        t=mycursor.fetchall()
        mydb.commit()
        lst=[]
        for i in lst1:
            a="SELECT {0},Firstname FROM STUDENT WHERE STID={1}".format(i,t[0][0])
            mycursor.execute(a)
            p=mycursor.fetchall()
            print(p)
            if p[0][0]==1:
                lst.append(list(i))
        print(lst)
        xyz="Exams registered by Student with ID "+str(t[0][0])+"and name:"+str(p[0][1])
        label50=Label(window,text=xyz,font=("arial",12,))
        label50.place(x=5,y=35)
        # create Treeview with 3 columns
        cols = ('Exam name',)
        tree = ttk.Treeview(window, columns=cols, show='headings')
        # set column headings
        for col in cols:
            tree.heading(col, text=col)
        for i, (ename) in enumerate(lst, start=1):
            tree.insert("", "end", values=(ename,))
        tree.place(x=300,y=70)  #,row=1, column=0, columnspan=1
        closeButton = Button(window, text="Close", width=15, command=lambda: window.destroy())
        closeButton.place(x=350, y=345)
    # Verify Student ID
    def check_9():
        stid = fn1.get()
        mycursor.execute("SELECT STID FROM STUDENT")
        idraw = mycursor.fetchall()
        l = []
        for i in idraw:
            l.append(i[0])
        print(l)
        print(type(stid))
        if stid.isalpha()==True:
            messagebox.showerror("Error", "Only Numbers Allowed for Student ID")
        elif int(stid) not in l:
            messagebox.showerror("Error", "STUDENT WITH GIVEN ID DOES NOT EXIST")
        else:
            display_9(fn1.get())
    window=Tk()
    window.geometry("500x500")
    window.title("Exam mangement")
    label1=Label(window,text="Exam Management",fg="white",bg="black",font=("arial",16))
    label1.pack()

    label2=Label(window,text="Displaying Exams registered by an Student",font=("arial",12,))
    label2.place(x=50,y=60)

    label3=Label(window,text="Enter the Student ID",font=("arial",12))
    label3.place(x=10,y=120)

    fn1=StringVar()

    entry_1= Entry(window,textvar=fn1)
    entry_1.place(x=240,y=120)

    label2=Label(window,text="",font=("arial",12,))
    label2.place(x=100,y=400)

    button=Button(window,text="Submit",fg="white",bg="green",relief="ridge",font=("arial",12,"bold"),command=check_9)
    button.place(x=220,y=300)

    # Function to Exit
    def leave():
        window.destroy()
        main_user_screen()

    button45=Button(window,text="Exit",fg="white",bg="red",relief="ridge",font=("arial",12,"bold"),command=leave)
    button45.place(x=220,y=350)

    window.mainloop()



#############----------Menu 10---------#############
###############-Display all details-################
def choice10():
    main_screen.destroy()
    window=Tk()
    window.geometry("1500x800")
    window.title("Exam mangement")
    label1=Label(window,text="Exam Management",fg="white",bg="black",font=("arial",16))
    label1.pack()

    mycursor.execute("SELECT Examname FROM EXAM")
    L=mycursor.fetchall()
    lst1=[]
    for i in L:
        lst1.append(i[0])
    mycursor.execute("SELECT STID FROM STUDENT")
    idraw=mycursor.fetchall()
    idlist=[]
    for i in idraw:
        idlist.append(i[0])
    L_main=[]
    for i in idlist:
        lst=[]
        for j in lst1:
            a="SELECT STID,Firstname,Lastname,Class FROM STUDENT WHERE STID={0}".format(i)
            mycursor.execute(a)
            p=mycursor.fetchall()
            p=p[0]
            p=list(p)
            b="SELECT {0} FROM STUDENT WHERE STID={1}".format(j,i)
            mycursor.execute(b)
            q=mycursor.fetchall()
            if q[0][0]==1:
                lst.append(j)
        l123=''
        for i in lst:
            if l123:
                l123=l123+','+i
            else:
                l123=l123+i
        p.append(l123)
        L_main.append(p)
    print('L_main:',L_main)

    # create Treeview with 5 columns
    cols = ('STID', 'Fname', 'Lname','Class','Exams')
    tree = ttk.Treeview(window, columns=cols, show='headings',height=30)

    # set column headings
    for col in cols:
        tree.heading(col, text=col)

    for i, (num,Fname, Lname, Class,Exam) in enumerate(L_main, start=1):
        tree.insert("", "end", values=(num,Fname, Lname, Class,Exam))
    tree.place(x=150,y=30)  #,row=1, column=0, columnspan=2

    # Function to Exit
    def leave():
        window.destroy()
        main_user_screen()

    button45=Button(window,text="Exit",fg="white",bg="red",relief="ridge",font=("arial",12,"bold"),command=leave)
    button45.place(x=670,y=650)
    window.mainloop()

###########################################
# Window to display a menu with 10 options as follows:
# 1. Add an exam
# 2. Modify an exam
# 3. Delete an exam
# 4. Display all exam details
# 5. Register a student
# 6. Delete a student
# 7. List the students registered for an exam
# 8. List the no. of students for each exam
# 9. List the exams registered by a student
#10. Display all details
def create_menu():
    global main_screen
    Label(text="EXAM MANAGEMENT SYSTEM", bg="black",fg='white', width="300", height="3", font=("Calibri", 13)).pack()
    Label(text="MENU", height="1", width="35").pack()
    Button(text="1. Add an exam",bd=3,activebackground='white',bg="blue",fg='white', height="2", width="35", command = choice1).pack()
    Button(text="2. Modify an exam",bd=3,activebackground='white',bg="blue",fg='white', height="2", width="35", command=choice2).pack()
    Button(text="3. Delete an exam",bd=3,activebackground='white',bg="blue",fg='white', height="2", width="35", command = choice3).pack()
    Button(text="4. Display all exam details",bd=3,activebackground='white',bg="blue",fg='white', height="2", width="35", command=choice4).pack()
    Button(text="5. Register a student",bd=3,activebackground='white',bg="blue",fg='white', height="2", width="35", command =choice5 ).pack()
    Button(text="6. Delete a student",bd=3,activebackground='white',bg="blue",fg='white', height="2", width="35", command=choice6).pack()
    Button(text="7. List the students registered for an exam",bd=3,activebackground='white',bg="blue",fg='white', height="2", width="35", command =choice7).pack()
    Button(text="8. List the no. of students for each exam",bd=3,activebackground='white',bg="blue",fg='white', height="2", width="35", command=choice8).pack()
    Button(text="9. List the exams registered by a student",bd=3,activebackground='white',bg="blue",fg='white', height="2", width="35", command =choice9).pack()
    Button(text="10. Display all details",bd=3,activebackground='white',bg="blue",fg='white', height="2", width="35", command=choice10).pack()
    buttone=Button(text="Exit",fg="white",bg="Red",relief="ridge",font=("arial",12,"bold"),command=m).pack()

def main_user_screen():
    global main_screen
    main_screen = Tk()
    main_screen.geometry("775x790")
    main_screen.title("Exam Management")
    create_menu()

    # write stuff above this
    main_screen.mainloop()

## __main__
main_account_screen()