from tkinter import *
import tkinter as tk
from tkcalendar import *
import mysql.connector
from tkinter import messagebox
from tkinter.ttk import Combobox

# Constants
LARGE_FONT = ("Verdana", 20)

# Base Classes for Multiple Inheritance
class DatabaseHandler:
    def __init__(self):
        self.db_connection = self.connect_to_database()

    def connect_to_database(self):
        return mysql.connector.connect(host="localhost", user="root", passwd="")#use your password

    def execute_query(self, query, values=None):
        cursor = self.db_connection.cursor(buffered=True)
        cursor.execute(query, values or ())
        self.db_connection.commit()
        return cursor

class UserInterface:
    def show_warning(self, message):
        messagebox.showwarning("Warning", message)

# Main Application Class
class ws(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (Welcome, SignIn, SignUp, Registration, Numbergenerator, endpg):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(Welcome)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

# Welcome Page
class Welcome(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Welcome to Yatra", font=LARGE_FONT, fg="purple")
        label.pack(pady=10, padx=10)

        button2 = tk.Button(self, text="Sign Up", bg="pink", borderwidth=1, height=1, width=8,
                            command=lambda: controller.show_frame(SignUp))
        button2.config(font=("Courier", 15))
        button2.pack()

        button = tk.Button(self, text="Sign In", bg="pink", borderwidth=1, height=1, width=8,
                           command=lambda: controller.show_frame(SignIn))
        button.config(font=("Courier", 15))
        button.pack()

        info = tk.Label(self, text="For queries: yatra@gmail.com", font=("Arial", 18))
        info.place(x=573, y=705)

        info1 = tk.Label(self, text=u'\u00A9', font=("Arial", 18))
        info1.place(x=657, y=750)
        info2 = tk.Label(self, text="Yatra 2025", font=("Arial", 18))
        info2.place(x=680, y=750)

# SignUp Page with Multiple Inheritance
class SignUp(tk.Frame, DatabaseHandler, UserInterface):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        DatabaseHandler.__init__(self)
        UserInterface.__init__(self)
        self.controller = controller
        self.setup_ui()

    def setup_ui(self):
        label = tk.Label(self, text="Sign Up", font=LARGE_FONT, fg="forestgreen")
        label.pack(pady=10, padx=10)

        self.name = StringVar()
        self.aadhar = IntVar()
        self.phone = IntVar()
        self.gender = StringVar()
        self.username = StringVar()
        self.password = StringVar()
        self.confirm_password = StringVar()

        # Add UI elements
        tk.Label(self, text="Name of the applicant", font=("Arial", 16)).place(x=40, y=55)
        Entry(self, textvariable=self.name, width=80, font=("Arial", 16)).place(x=300, y=55, height=30)

        tk.Label(self, text="Aadhar Number", font=("Arial", 16)).place(x=40, y=95)
        Entry(self, textvariable=self.aadhar, width=80, font=("Arial", 16)).place(x=300, y=95, height=30)

        tk.Label(self, text="Phone Number", font=("Arial", 16)).place(x=40, y=135)
        Entry(self, textvariable=self.phone, width=80, font=("Arial", 16)).place(x=300, y=135, height=30)

        tk.Label(self, text="Gender", font=("Arial", 16)).place(x=40, y=175)
        Combobox(self, values=['Female', 'Male', 'Other'], font=("Arial", 18)).place(x=300, y=175)

        tk.Label(self, text="Username", font=("Arial", 16)).place(x=40, y=215)
        Entry(self, textvariable=self.username, width=80, font=("Arial", 16)).place(x=300, y=215, height=30)

        tk.Label(self, text="Create a new password", font=("Arial", 16)).place(x=40, y=255)
        Entry(self, textvariable=self.password, width=80, font=("Arial", 16), show="*").place(x=300, y=255, height=30)

        tk.Label(self, text="Confirm your password", font=("Arial", 16)).place(x=40, y=295)
        Entry(self, textvariable=self.confirm_password, width=80, font=("Arial", 16), show="*").place(x=300, y=295, height=30)

        tk.Label(self, text="Date Of Birth", font=("Arial", 16)).place(x=40, y=335)
        DateEntry(self, selectmode="day", year=2025, day=22, month=12).place(x=300, y=335)

        Checkbutton(self, text="I agree that all the information entered above is correct", width=80).place(x=500, y=370)

        # Buttons
        tk.Button(self, text="Sign Up", bg="pink", borderwidth=1, height=1, width=8,
                  command=self.validate_signup).place(x=700, y=600)
        tk.Button(self, text="Back", borderwidth=1, height=1, width=8,
                  command=lambda: self.controller.show_frame(Welcome)).place(x=700, y=700)

    def validate_signup(self):
        if not all([self.name.get(), self.aadhar.get(), self.phone.get(), self.username.get(), self.password.get(), self.confirm_password.get()]):
            self.show_warning("All fields are required")
        elif self.password.get() != self.confirm_password.get():
            self.show_warning("Passwords do not match")
        else:
            self.save_to_database()
            self.controller.show_frame(Signups)

    def save_to_database(self):
        query = "INSERT INTO signup (Name, Aadhar_number, Phone_number, Gender, Username, Password, DOB) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        values = (self.name.get(), self.aadhar.get(), self.phone.get(), self.gender.get(), self.username.get(), self.password.get(), "2025-12-22")
        self.execute_query(query, values)

# SignIn Page with Multiple Inheritance
class SignIn(tk.Frame, DatabaseHandler, UserInterface):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        DatabaseHandler.__init__(self)
        UserInterface.__init__(self)
        self.controller = controller
        self.setup_ui()

    def setup_ui(self):
        label = tk.Label(self, text="Sign In", font=LARGE_FONT, fg="forestgreen")
        label.pack(pady=10, padx=10)

        self.username = StringVar()
        self.password = StringVar()

        tk.Label(self, text="Username", font=("Arial", 16)).place(x=40, y=55)
        Entry(self, textvariable=self.username, width=80, font=("Arial", 16)).place(x=300, y=55, height=30)

        tk.Label(self, text="Password", font=("Arial", 16)).place(x=40, y=95)
        Entry(self, textvariable=self.password, width=80, font=("Arial", 16), show="*").place(x=300, y=95, height=30)

        tk.Button(self, text="Sign In", bg="pink", borderwidth=1, height=1, width=8,
                  command=self.validate_login).place(x=700, y=135)
        tk.Button(self, text="Back", borderwidth=1, height=1, width=8,
                  command=lambda: self.controller.show_frame(Welcome)).place(x=700, y=700)

    def validate_login(self):
        if not self.username.get() or not self.password.get():
            self.show_warning("All fields are required")
        else:
            query = "SELECT * FROM signup WHERE Username = %s AND Password = %s"
            values = (self.username.get(), self.password.get())
            cursor = self.execute_query(query, values)
            if cursor.fetchone():
                self.controller.show_frame(Registration)
            else:
                self.show_warning("Incorrect username or password")
##FRAME REGISTRATION
class Registration(tk.Frame):
   
     def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text=" Registration for tour", font=LARGE_FONT, fg = "purple")
        label.pack(pady=10,padx=10)
        from tkinter import messagebox
       
        global s
        global aadharno1
        global phoneno1
        global persons1
        global childs1
        global combo
        global combo1
        global combo2
        global place_of_visit

                #######reg detAILS TO COLLECT#######
               
        s_name=tk.Label(self,text="Name of the applicant",font=("Arial",16))
        s_name.place(x=40,y=55)
        s=StringVar()
        s_ans=Entry(self,textvariable=s,width=80,font=("Arial",16))
        s_ans.place(x=300,y=55,height=30)
       
       
        #
        aadhar1=tk.Label(self,text="Aadhar Number",font=("Arial",16))
        aadhar1.place(x=40,y=95)
        aadharno1=IntVar()
        aadharans1=Entry(self,textvariable=aadharno1,width=80,font=("Arial",16))
        aadharans1.place(x=300,y=95,height=30)
        #
        phone1=tk.Label(self,text="Phone Number",font=("Arial",16))
        phone1.place(x=40,y=135)
        phoneno1=IntVar()
        phoneans1=Entry(self,textvariable=phoneno1,width=80,font=("Arial",16),)
        phoneans1.place(x=300,y=135,height=30)
        #
        persons1=tk.Label(self,text="Number of persons ",font=("Arial",16))
        persons1.place(x=40,y=175)
        persons1=IntVar()
        persons1ans=Entry(self,textvariable=persons1,width=80,font=("Arial",16))
        persons1ans.place(x=300,y=175,height=30)
       #
        childs1=tk.Label(self,text="Number of children ",font=("Arial",16))
        childs1.place(x=40,y=215)
        childs1=IntVar()
        childs1ans=Entry(self,textvariable=childs1,width=80,font=("Arial",16))
        childs1ans.place(x=300,y=215,height=30)
       
        from tkinter.ttk import Combobox
        mode=tk.Label(self,text="Mode of Transport",font=("Arial",16))
        mode.place(x=40,y=255)
        combo=Combobox(self,values=['PUBLIC','PRIVATE'],font=("Arial",18) )
        combo.place(x=300,y=255)
       #
        from tkinter.ttk import Combobox
        mode1=tk.Label(self,text="Type of Transport",font=("Arial",16))
        mode1.place(x=40,y=295)
        combo1=Combobox(self,values=['Bus','Car','Bike','Van','Cycle','Auto','Other'],font=("Arial",18) )
        combo1.place(x=300,y=295)
       #
        from tkinter.ttk import Combobox
        vac1=tk.Label(self,text="Vaccination status",font=("Arial",16))
        vac1.place(x=40,y=335)
        combo2=Combobox(self,values=['Vaccinated','Not Vaccinated'],font=("Arial",18) )
        combo2.place(x=300,y=335,height =30)
       #
        Date=tk.Label(self,text="Date Of Arrival",font=("Arial",16))
        Date.place(x=40,y=375)
        cal1 = DateEntry(self, selectmode="day", year=2025, day=22,month=12 )
        cal1.place(x=300,y=375)
       #
        place=tk.Label(self,text="Place of Visit",font=("Arial",16))
        place.place(x=40,y=415)
        place_of_visit=StringVar()
        placeans=Entry(self,textvariable=place_of_visit,width=80,font=("Arial",16))
        placeans.place(x=300,y=415,height=30)
       ###MYSQL
        import mysql.connector
        mydb=mysql.connector.connect(host="localhost",user="root",passwd="newrules20.")
        m1=mydb.cursor(buffered=True)
        try:
            m1.execute("use yatra")
        except:
            m1.execute("create database yatra")
            m1.execute("use yatra")
        try:
            m1.execute("describe registration")
        except:
            m1.execute("create table registration(Name varchar(18),Aadhar_Number varchar(12),Phone_Number varchar(10),Number_of_persons int,Number_of_children int,Mode_of_transport varchar(18),Type_of_transport varchar(18),Vaccination_status varchar(20),Date_of_arrival varchar(10),Place_of_visit varchar(50)) ")
        def new1():
            m1.execute(f"insert into registration(Name,Aadhar_Number,Phone_Number,Number_of_persons,Number_of_children,Mode_of_transport,Type_of_transport,Vaccination_status,Date_of_arrival,Place_of_visit) values('{s.get()}','{aadharno1.get()}','{phoneno1.get()}','{persons1.get()}','{childs1.get()}','{combo.get()}','{combo1.get()}' ,'{combo2.get()}','{cal1.get()}','{place_of_visit.get()}')")
            mydb.commit()
 
       ##WARNINGS
        def  warn ():
                if s.get()=="":
                        messagebox.showwarning("Warning", "All field required")
                        controller.show_frame(Registration)
                elif aadharno1.get()=="":
                        messagebox.showwarning("Warning", "All field required")
                        controller.show_frame(Registration)
                elif phoneno1.get()=="":
                        messagebox.showwarning("Warning", "All field required")
                        controller.show_frame(Registration)
                elif persons1.get()=="":
                        messagebox.showwarning("Warning", "All field required")
                        controller.show_frame(Registration)
                elif childs1.get()=="":
                        messagebox.showwarning("Warning", "All field required")
                        controller.show_frame(Registration)
               
                elif combo.get()=="":
                        messagebox.showwarning("Warning", "All field required")
                        controller.show_frame(Registration)
                elif combo1.get()=="":
                        messagebox.showwarning("Warning", "All field required")
                        controller.show_frame(Registration)
                elif combo2.get()=="":
                        messagebox.showwarning("Warning", "All field required")
                        controller.show_frame(Registration)
                elif place_of_visit.get()=="":
                        messagebox.showwarning("Warning", "All field required")
                        controller.show_frame(Registration)
                else:
                        new1()
                        controller.show_frame(Numbergenerator)
               

        button5 = tk.Button(self, text="Register",bg="pink",borderwidth=1,height=1,width=8,
                            command=lambda: warn())
        button5.config(font=("Courier",15))
        button5.place(x=700,y=525)
       #
        buttonback12=tk.Button(self, text="Back",borderwidth=1,height=1,width=8,
                  command=lambda: controller.show_frame(SignIn))                  
        buttonback12.config(font=("Courier",15))
        buttonback12.place(x=700,y=700)

###Random number page numbergenerator
class Numbergenerator(tk.Frame):
   
     def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text=" REGISTRATION SUCCESSFUL!!!", font=LARGE_FONT, fg = "forest green")
        label.pack(pady=10,padx=10)
        from tkinter import messagebox
        #######
        global xy1
        import random
        code1=tk.Label(self,text="Your Registration number is  ",font=("Arial",24))
        code1.place(x=40,y=95)
        code2=tk.Label(self,text=str(random.randint(1,100000)),font=("Arial",30),fg="indigo")
        code2.place(x=500,y=95)
        #cofirm num
        xy=tk.Label(self,text="Enter the registration number given above to ensure that you have seen it",font=("Arial",16))
        xy.place(x=40,y=190)
        xy1=StringVar()
        xyans1=Entry(self,textvariable=xy1,width=40,font=("Arial",16))
        xyans1.place(x=800,y=190,height=30)
        #end
        #####num to database
        import mysql.connector
        mydb=mysql.connector.connect(host="localhost",user="root",passwd=" ")#use your password
        m12=mydb.cursor(buffered=True)
        try:
            m12.execute("use yatra")
        except:
            m12.execute("create database yatra")
            m12.execute("use yatra")
        try:
            m12.execute("describe registration_number")
        except:
            m12.execute("create table registration_number(Name varchar(18),Aadhar_Number varchar(12),Phone_Number varchar(10),Registration_number int) ")
        def new12():
            m12.execute(f"insert into registration_number(Name,Aadhar_Number,Phone_Number,Registration_number) values('{s.get()}','{aadharno1.get()}','{phoneno1.get()}','{xy1.get()}')")
            mydb.commit()
        ####num to database ends

        ### clear reg
        def clearreg():
            s.set('')
            aadharno1.set('')
            phoneno1.set('')
            persons1.set('')
            childs1.set('')
            combo.set('')
            combo1.set('')
            combo2.set('')
            place_of_visit.set('')

        ###END

###WARNING

        def warning1():
            if xy1.get()!=code2.cget("text"):
                messagebox.showwarning("Warning", "Enter the correct registration number")
                controller.show_frame(Numbergenerator)
           
            else:
                new12()
                clearreg()
                controller.show_frame(endpg)
         #ok button
        buttonok=tk.Button(self, text="Ok",borderwidth=1,height=1,width=8,bg="pink",
                  command= lambda:warning1())                  
        buttonok.config(font=("Courier",15))
        buttonok.place(x=710,y=500)    
        #ok button end


       
        #back button
        buttonback123=tk.Button(self, text="Back",borderwidth=1,height=1,width=8,
                  command=lambda: controller.show_frame(Welcome))                  
        buttonback123.config(font=("Courier",15))
        buttonback123.place(x=710,y=710)
        info11=tk.Label(self,text=u'\u00A9',font=("Arial",18) )
        info11.place(x=650,y=750)
        info21=tk.Label(self,text="Yatra 2025",font=("Arial",18) )
        info21.place(x=673,y=750)
####End

##end page

class endpg(tk.Frame):
   
     def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text="You are all set to visit your interested place. Wishing you a safe journey ahead.", font=LARGE_FONT, fg = "forest green")
        label.pack(pady=10,padx=10)
       
        info1a=tk.Label(self,text="For quries : yatra@gmail.com",font=("Arial",18) )
        info1a.place(x=573,y=705)
       
        info1b=tk.Label(self,text=u'\u00A9',font=("Arial",18) )
        info1b.place(x=657,y=750)
        info2a=tk.Label(self,text="Yatra 2025",font=("Arial",18) )
        info2a.place(x=680,y=750)
       
        buttonback123a=tk.Button(self, text="Back",borderwidth=1,height=1,width=8,
                  command=lambda: controller.show_frame(Numbergenerator))                  
        buttonback123a.config(font=("Courier",15))
        buttonback123a.place(x=710,y=600)
       

       
###end of end pg

       


# Main Application
app = ws()
app.title("Yatra - For Tourism Registration")
app.geometry('1500x780')
app.mainloop()