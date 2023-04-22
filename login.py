from tkinter import *
from tkinter import messagebox
from PIL import ImageTk
import pymysql

#Functionality Part
def forgot_password():
    def change_password():
        if userEntry.get()=='' or passwordEntry.get()=='' or confirmpassEntry.get()=='':
            messagebox.showerror('Error',"All fields are required",parent=window)
        elif newpassEntry.get()!=confirmpassEntry.get():
            messagebox.showerror('Error',"New password and confirm password do not match",parent=window)
        else:
            con=pymysql.connect(host='localhost',user='root',password='1234',database='userdata')    
            mycursor=con.cursor()
            query='select * from data where username=%s'
            mycursor.execute(query,(userEntry.get()))
            row=mycursor.fetchone()
            if row==None:
                messagebox.showerror('Error',"Username does not exist",parent=window)
            else:
                query='update data set password=%s where username=%s'
                mycursor.execute(query,(newpassEntry.get(),userEntry.get()))
                con.commit()
                con.close()
                messagebox.showinfo('Success','Password reset, Please login with new password',parent=window)
                window.destroy()
                        
    window=Toplevel()
    window.title("Change Password")
    
    bgPic=ImageTk.PhotoImage(file='background.jpg')
    bgLabel=Label(window,image=bgPic)
    bgLabel.grid()
    
    heading_label=Label(window,text='RESET PASSWORD',font=('arial',12,'bold'),bg='white',fg='magenta2')
    heading_label.place(x=480,y=60) 
    
    userLabel=Label(window,text='Username',font=('arial',12,'bold'),bg='white',fg='orchid1')
    userLabel.place(x=470,y=130)        
    userEntry=Entry(window,width=25,fg='magenta2',font=('arial',11,'bold'),bd=0)
    userEntry.place(x=470,y=160)
    Frame(window,width=250,height=2,bg='orchid1').place(x=470,y=180)
    
    newpassLabel=Label(window,text='New Password',font=('arial',12,'bold'),bg='white',fg='orchid1')
    newpassLabel.place(x=470,y=210)
    newpassEntry=Entry(window,width=25,fg='magenta2',font=('arial',11,'bold'),bd=0)
    newpassEntry.place(x=470,y=240)    
    Frame(window,width=250,height=2,bg='orchid1').place(x=470,y=260)
    
    confirmpassLabel=Label(window,text='Confirm New Password',font=('arial',12,'bold'),bg='white',fg='orchid1')
    confirmpassLabel.place(x=470,y=290)
    confirmpassEntry=Entry(window,width=25,fg='magenta2',font=('arial',11,'bold'),bd=0)
    confirmpassEntry.place(x=470,y=320)    
    Frame(window,width=250,height=2,bg='orchid1').place(x=470,y=340)
    
    submitButton=Button(window,text="Submit",bd=0,bg='magenta2',fg='white',font=('arial',16,'bold'),width=19,cursor='hand2',command=change_password)
    submitButton.place(x=470,y=360)    
    window.mainloop()

def login_user():
    if usernameEntry.get()=='' or passwordEntry.get=='':
        messagebox.showerror('Error','All fields are required')
    else:
        try:
            con=pymysql.connect(host='localhost',user='root',password='1234')    
            mycursor=con.cursor()
        except:
            messagebox.showerror('Error','Connection is not established, Try Again')
            return
        query='use userdata'
        mycursor.execute(query)
        query='select * from  data where username=%s and password=%s'
        mycursor.execute(query,(usernameEntry.get(),passwordEntry.get()))
        row=mycursor.fetchone()
        if row==None:
            messagebox.showerror('Error','Invalid Username or Password')
        else:
            messagebox.showinfo('Welcome','Login Successful')
            window.destroy()
            import sms            
            
def signup_page():
    window.destroy()
    import signup
    
def hide():
    openeye.config(file="closedeye.png")
    passwordEntry.config(show='*')
    eyeButton.config(command=show)

def show():
    openeye.config(file="openeye.png")
    passwordEntry.config(show='')
    eyeButton.config(command=hide)
    
def user_enter(event):
    if usernameEntry.get()=="Username":
            usernameEntry.delete(0,END)
            
def pass_enter(event):
    if passwordEntry.get()=="Password":
            passwordEntry.delete(0,END)
#GUI Part
window=Tk()
window.geometry('990x660+0+0')
#window.resizable(False,False)
window.title("Login")

bgImage=ImageTk.PhotoImage(file='bg.jpg') #required only for jpg image
bgLabel=Label(window,image=bgImage)
bgLabel.place(x=0,y=0)

heading=Label(window,text="USER LOGIN",font=('Times New Roman',25,'bold'),fg='red')
heading.place(x=450,y=50)

usernameEntry=Entry(window,width=25,font=('Times New Roman',15), bg='white',fg='red')
usernameEntry.place(x=450,y=150)
usernameEntry.insert(0,"Username")
usernameEntry.bind('<FocusIn>',user_enter)

Frame(window,width=250,height=2,bg='red').place(x=450,y=175)

passwordEntry=Entry(window,width=25,font=('Times New Roman',15), bg='white',fg='red')
passwordEntry.place(x=450,y=200)
passwordEntry.insert(0,"Password")
passwordEntry.bind('<FocusIn>',pass_enter)

Frame(window,width=250,height=2,bg='red').place(x=450,y=225)

openeye=PhotoImage(file='openeye.png')
eyeButton=Button(window,image=openeye,bd=0,bg='white',activebackground='white',cursor='hand2',command=hide)
eyeButton.place(x=675,y=200)

forgotButton=Button(window,text="Forgot password?",bd=0,fg='blue',activebackground='white',cursor='hand2',font=('Times New Roman',10),command=forgot_password)
forgotButton.place(x=600,y=230)

loginButton=Button(window,text="Login",font=("Open Sans",16,"bold"),fg='white',bg='red',activeforeground='white',activebackground='red',cursor='hand2',bd=0,width=19,command=login_user)
loginButton.place(x=450,y=260)

orLabel=Label(window,text="-------------------OR---------------------",font=('Open Sans',16),fg='red',bd=0)
orLabel.place(x=400,y=335)

googleLogo=PhotoImage(file="google.png")
googleLabel=Label(window,image=googleLogo)
googleLabel.place(x=535,y=375)

signupLabel=Label(window,text="Don't have an account?",font=('Open Sans',10),bd=0)
signupLabel.place(x=400,y=420)

newaccountButton=Button(window,text="Create new account",font=("Open Sans",10,"bold underline"),fg='black',activeforeground='red',activebackground='white',cursor='hand2',bd=0,command=signup_page)
newaccountButton.place(x=540,y=415)

window.mainloop()