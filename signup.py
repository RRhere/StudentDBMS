from tkinter import *
from tkinter import messagebox
from PIL import ImageTk
import pymysql

def clear():
    emailEntry.delete(0,END)
    usernameEntry.delete(0,END)
    passwordEntry.delete(0,END)
    confirmpasswordEntry.delete(0,END)
    check.set(0)
    
def signup_page():
    signup_window.destroy()
    import login

def connect_db():
    if emailEntry.get()=='' or passwordEntry.get()=='' or confirmpasswordEntry.get()=='':
        messagebox.showerror('Error','All fields are required')
    elif passwordEntry.get()!=confirmpasswordEntry.get():
        messagebox.showerror('Error','Passwords mismatch')
    elif check.get()==0:
        messagebox.showerror('Error','Please accpet Terms & Conditions')
    else:
        try:
            con=pymysql.connect(host='localhost',user='root',password='1234')
            mycursor=con.cursor()
        except:
            messagebox.showerror('Error','Database Connectivity Issue,Please Try Again')
            return
        try:
            query='create database userdata'
            mycursor.execute(query)
            query='use userdata'
            mycursor.execute(query)
            query='create table data(id int auto_increment primary key not null,email varchar(50),username varchar(10),password varchar(20))'
            mycursor.execute(query)
        except:
            mycursor.execute('use userdata')

        query='select * from data where username=%s'
        mycursor.execute(query,(usernameEntry.get()))
        
        row=mycursor.fetchone()
        if row!=None:
            messagebox.showerror('Error','Username already exists')
        else:
            query='insert into data(email,username,password) values(%s,%s,%s)'
            mycursor.execute(query,(emailEntry.get(),usernameEntry.get(),passwordEntry.get()))
            con.commit()
            con.close()
            messagebox.showinfo('Success','Registration successful')
            clear()
            signup_window.destroy()
            import login

signup_window=Tk()
signup_window.geometry('990x660+0+0')
signup_window.title("Signup Page")
signup_window.resizable(False,False)
background=ImageTk.PhotoImage(file='bg.jpg')

bgLabel=Label(signup_window,image=background)
bgLabel.grid()

frame=Frame(signup_window)
frame.place(x=400,y=75)

heading=Label(frame,text="CREATE ACCOUNT",font=('Times New Roman',25,'bold'),fg='gold')
heading.grid(row=0,column=0)

emailLabel=Label(frame,text='Email',font=('Times New Roman',15,'bold'),fg='gold')
emailLabel.grid(row=1,column=0,sticky='w',pady=(10,0))
emailEntry=Entry(frame,width=25,font=('Times New Roman',15,'bold'),fg='white',bg='gold')
emailEntry.grid(row=2,column=0,sticky='w')

usernameLabel=Label(frame,text='Username',font=('Times New Roman',15,'bold'),fg='gold')
usernameLabel.grid(row=3,column=0,sticky='w',pady=(10,0))
usernameEntry=Entry(frame,width=25,font=('Times New Roman',15,'bold'),fg='white',bg='gold')
usernameEntry.grid(row=4,column=0,sticky='w')

passwordLabel=Label(frame,text='Password',font=('Times New Roman',15,'bold'),fg='gold')
passwordLabel.grid(row=5,column=0,sticky='w',pady=(10,0))
passwordEntry=Entry(frame,width=25,font=('Times New Roman',15,'bold'),fg='white',bg='gold')
passwordEntry.grid(row=6,column=0,sticky='w')

confirmpasswordLabel=Label(frame,text='Confirm Password',font=('Times New Roman',15,'bold'),fg='gold')
confirmpasswordLabel.grid(row=7,column=0,sticky='w',pady=(10,0))
confirmpasswordEntry=Entry(frame,width=25,font=('Times New Roman',15,'bold'),fg='white',bg='gold')
confirmpasswordEntry.grid(row=8,column=0,sticky='w')

check=IntVar()
termsandconditions=Checkbutton(frame,text="I agree to the Terms & Conditions",font=('Times New Roman',15,'bold'),fg='gold',activeforeground='gold',cursor='hand2',variable=check)
termsandconditions.grid(row=9,column=0,pady=(10,0))

signupButton=Button(frame,text='Signup',font=('Times New Roman',15,'bold'),bd=0,bg='gold',fg='white',activebackground='gold',activeforeground='white',width=20,cursor='hand2',command=connect_db)
signupButton.grid(row=10,column=0,pady=10)

alreadyAccount=Label(frame,text='Dont have an account?',font=('Open Sans',10,'bold'),fg='gold')
alreadyAccount.grid(row=11,column=0,sticky='w')

loginButton=Label(frame,text='Login',font=('Open Sans',10,'bold underline'),fg='blue',activeforeground='blue',cursor='hand2')
loginButton.place(x=670,y=150)

signup_window.mainloop()