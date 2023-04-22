from tkinter import *
import time
import ttkthemes
from tkinter import ttk,messagebox
import pymysql

#Functionality
def toplevel_fields(title,button_text,command):
    global idEntry,nameEntry,emailEntry,ageEntry,screen
    screen=Toplevel()
    screen.grab_set()
    screen.title(title)
    screen.resizable(0,0)
    
    idLabel=Label(screen,text='Id',font=('Times New Roman', 20,'bold'))
    idLabel.grid(row=0,column=0,padx=30,pady=15)
    idEntry=Entry(screen,font=('Roman',15,'bold'),width=25)
    idEntry.grid(row=0,column=1,padx=10,pady=15)
    
    nameLabel=Label(screen,text='Name',font=('Times New Roman', 20,'bold'))
    nameLabel.grid(row=1,column=0,padx=30,pady=15)
    nameEntry=Entry(screen,font=('Roman',15,'bold'),width=25)
    nameEntry.grid(row=1,column=1,padx=10,pady=15)
    
    emailLabel=Label(screen,text='Email',font=('Times New Roman', 20,'bold'))
    emailLabel.grid(row=2,column=0,padx=30,pady=15)
    emailEntry=Entry(screen,font=('Roman',15,'bold'),width=25)
    emailEntry.grid(row=2,column=1,padx=10,pady=15)
    
    ageLabel=Label(screen,text='Age',font=('Times New Roman', 20,'bold'))
    ageLabel.grid(row=3,column=0,padx=30,pady=15)
    ageEntry=Entry(screen,font=('Roman',15,'bold'),width=25)
    ageEntry.grid(row=3,column=1,padx=10,pady=15)
    
    studentButton=ttk.Button(screen,text=button_text,command=command)
    studentButton.grid(row=4,columnspan=2,pady=15)
    
    if title=='Update Student':
        indexing=studentTable.focus()
        content=studentTable.item(indexing)
        listdata=content['values']
        idEntry.insert(0,listdata[0])
        nameEntry.insert(0,listdata[1])
        emailEntry.insert(0,listdata[2])
        ageEntry.insert(0,listdata[3])
    
def iexit():
    result=messagebox.askyesno("Confirm","Do you want to exit?")
    if result:
        root.destroy()
    else:
        pass
    
def update_data():
    query='update student set name=%s,email=%s,age=%s,date=%s,time%s where id=%s'
    mycursor.execute(query,(nameEntry.get(),emailEntry.get(),ageEntry.get(),date,currtime,idEntry.get()))
    con.commit()
    messagebox.showinfo('Success',"Updated Successfully",parent=screen)
    screen.destroy()
    show_student()
    
    

def show_student():
    query='select * from student'
    mycursor.execute(query)
    fetched_data=mycursor.fetchall()
    studentTable.delete(*studentTable.get_children())
    for data in fetched_data:
        studentTable.insert("",END,values=data)
    
def delete_student():
    indexing=studentTable.focus()
    content=studentTable.item(indexing)
    contentId=content['values'][0]
    query='delete from student where id=%s'
    mycursor.execute(query,contentId)
    con.commit()
    messagebox.showinfo('Deleted','Deleted Successfully')
    query='select * from student'
    mycursor.execute(query)
    fetched_data=mycursor.fetchall()
    studentTable.delete(*studentTable.get_children())
    for data in fetched_data:
        studentTable.insert("",END,values=data)    

def search_data():
    query='select * from student where id=%s or name=%s or email=%s or age=%s'
    mycursor.execute(query,(idEntry.get(),nameEntry.get(),emailEntry.get(),ageEntry.get()))
    studentTable.delete(*studentTable.get_children())
    fetched_data=mycursor.fetchall()
    for data in fetched_data:
        studentTable.insert('',END,values=data)
        
def add_data():
    if idEntry=='' or nameEntry=='' or emailEntry=='' or ageEntry=='':
        messagebox.showerror('Error','All fields are required',parent=screen)
    else:
        try:
            query='insert into student values(%s,%s,%s,%s,%s,%s)'
            mycursor.execute(query,(idEntry.get(),nameEntry.get(),emailEntry.get(),ageEntry.get(),date,currtime))
            con.commit()
            result=messagebox.askyesno('Confirm','Data added successfully. Do you want to clean the form?')
            if result:
                idEntry.delete(0,END)
                nameEntry.delete(0,END)
                emailEntry.delete(0,END)
                ageEntry.delete(0,END)
            else:
                pass
        except:
            messagebox.showerror('Error','Id cannot be repeated',parent=screen)
            return
        
        query='select * from student'
        mycursor.execute(query)
        fetched_data=mycursor.fetchall()
        studentTable.delete(*studentTable.get_children())
        for data in fetched_data:
            studentTable.insert('',END,values=data)
    
def connect_db():
    def connect():
        global mycursor,con
        try:
            con=pymysql.connect(host=hostnameEntry.get(),user=usernameEntry.get(),password=passwordEntry.get())
            mycursor=con.cursor()
        except:
            messagebox.showerror('Error',"Invalid Details",parent=connectWindow)
            return
        try:
            query='create database sms'
            mycursor.execute(query)
            query='use sms'
            mycursor.execute(query)
            query='create table student(id int not null primary key,name varchar(20),email varchar(30),age int,date varchar(50),time varchar(50))'
            mycursor.execute(query)
        except:
            query='use sms'
            mycursor.execute(query)
            
        messagebox.showinfo('Success','Connection to database established',parent=connectWindow)
        connectWindow.destroy()
        addStudentButton.config(state=NORMAL)
        searchStudentButton.config(state=NORMAL)
        deleteStudentButton.config(state=NORMAL)
        updateStudentButton.config(state=NORMAL)
        showStudentButton.config(state=NORMAL)
        
    connectWindow=Toplevel()
    connectWindow.grab_set()
    connectWindow.geometry('470x250+730+230')
    connectWindow.title("Database Connection")
    connectWindow.resizable(0,0)
    
    hostnameLabel=ttk.Label(connectWindow,text="Hostname",font=('arial',20,'bold'))
    hostnameLabel.grid(row=0,column=0,padx=20)
    usernameLabel=ttk.Label(connectWindow,text="Username",font=('arial',20,'bold'))
    usernameLabel.grid(row=1,column=0,padx=20)
    passwordLabel=ttk.Label(connectWindow,text="Password",font=('arial',20,'bold'))
    passwordLabel.grid(row=2,column=0,padx=20)
    
    hostnameEntry=ttk.Entry(connectWindow,font=('roman',15,'bold'))
    hostnameEntry.grid(row=0,column=1,padx=40,pady=20)
    usernameEntry=ttk.Entry(connectWindow,font=('roman',15,'bold'))
    usernameEntry.grid(row=1,column=1,padx=40,pady=20)
    passwordEntry=ttk.Entry(connectWindow,font=('roman',15,'bold'))
    passwordEntry.grid(row=2,column=1,padx=40,pady=20)
    
    connectButton=ttk.Button(connectWindow,text="CONNECT",command=connect)
    connectButton.grid(row=3,columnspan=2)
    
def clock():
    global date,currtime
    date=time.strftime('%d/%m/%Y')
    currtime=time.strftime('%H:%M:%S')
    datetimeLabel.config(text=f'    Date: {date}\n Time: {currtime}')
    datetimeLabel.after(1000,clock)

count=0
stext=''
def slider():
    global stext,count
    if count==len(s):
        count=0
        stext=''
    stext=stext+s[count]
    sliderLabel.config(text=stext)
    count+=1 
    sliderLabel.after(300,slider)
    
#GUI
root=ttkthemes.ThemedTk()
root.get_themes()
root.set_theme('itft1')
root.geometry('1174x800+0+0')
root.resizable(False,False)
root.title('Student Management System')


datetimeLabel=Label(root,font=('Times New Roman',18,'bold'))
datetimeLabel.place(x=5,y=5)
clock()

s='Student Management System'
sliderLabel=Label(root,text=s,font=('Arial',20,'italic bold'),width=30)
sliderLabel.place(x=350,y=0)
slider()

connectButton=ttk.Button(root,text='Connect To Database',command=connect_db)
connectButton.place(x=1000,y=5)

leftFrame=Frame(root)
leftFrame.place(x=50,y=80,width=300,height=600)

logo=PhotoImage(file='graduates.png')
logoLabel=Label(leftFrame,image=logo)
logoLabel.grid(row=0,column=0)

addStudentButton=ttk.Button(leftFrame,text="Add Student",state=DISABLED,command=lambda: toplevel_fields("Add Student","Add Student",add_data))
addStudentButton.grid(row=1,column=0,pady=20)

searchStudentButton=ttk.Button(leftFrame,text="Search Student",state=DISABLED,command=lambda: toplevel_fields("Search Student","Search Student",search_data))
searchStudentButton.grid(row=2,column=0,pady=20)

deleteStudentButton=ttk.Button(leftFrame,text="Delete Student",state=DISABLED,command=delete_student)
deleteStudentButton.grid(row=3,column=0,pady=20)

updateStudentButton=ttk.Button(leftFrame,text="Update Student",state=DISABLED,command=lambda: toplevel_fields("Update Student","Update Student",update_data))
updateStudentButton.grid(row=4,column=0,pady=20)

showStudentButton=ttk.Button(leftFrame,text="Show Student",state=DISABLED,command=show_student)
showStudentButton.grid(row=5,column=0,pady=20)

exitButton=ttk.Button(leftFrame,text="Exit",command=iexit)
exitButton.grid(row=6,column=0,pady=20)

rightFrame=Frame(root)
rightFrame.place(x=350,y=80,width=820,height=500)

scrollBarX=Scrollbar(rightFrame,orient=HORIZONTAL)
scrollBarY=Scrollbar(rightFrame,orient=VERTICAL)

studentTable=ttk.Treeview(rightFrame,columns=('Id','Name','Email','Age','Added Date','Added Time'),xscrollcommand=scrollBarX.set,yscrollcommand=scrollBarY.set)

scrollBarX.config(command=studentTable.xview)
scrollBarY.config(command=studentTable.yview)
scrollBarX.pack(side=BOTTOM,fill=X)
scrollBarY.pack(side=RIGHT,fill=Y)
studentTable.pack(fill=BOTH,expand=1)

studentTable.heading("Id",text="ID")
studentTable.heading("Name",text="NAME")
studentTable.heading("Email",text="EMAIL")
studentTable.heading("Age",text="AGE")
studentTable.heading("Added Date",text="ADDED DATE")
studentTable.heading("Added Time",text="ADDED TIME")

studentTable.column("Id",width=50,anchor=CENTER)
studentTable.column("Name",width=200,anchor=CENTER)
studentTable.column("Email",width=300,anchor=CENTER)
studentTable.column("Age",width=50,anchor=CENTER)
studentTable.column("Added Date",width=200,anchor=CENTER)
studentTable.column("Added Time",width=200,anchor=CENTER)

style=ttk.Style()
style.configure('Treeview',rowheight=40,font=('arial',12,'italic'))
style.configure('Treeview.Heading',font=('Times New Roamn',14,'bold'))

studentTable.config(show='headings')

root.mainloop()