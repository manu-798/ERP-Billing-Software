from tkinter import *
import datetime
from product import fetch_product,fetch_detail
import mysql.connector
import threading
def get_connector():
    return con
def login_sql(user,key):
    global con
    global invoice_num
    try:
        con = mysql.connector.connect(host="localhost", user=f"{user}", password=f"{key}")
        cursorObject=con.cursor()
        try:
            cursorObject.execute("CREATE DATABASE product_db")
            con.commit()
        except:
            pass
        cursorObject.execute("USE product_db")
        try:
            cursorObject.execute("CREATE TABLE products ( Id INT NOT NULL ,Name Varchar(255) NOT NULL, Quantity INT NOT NULL, Price INT, Expiry Varchar(255), PRIMARY KEY(Id))")
            con.commit()
        except:
            pass
        try:
            cursorObject.execute("CREATE TABLE invoice (invoice_num INT NOT NULL, PRIMARY KEY(invoice_num))") # maybe day date 
            con.commit()
            cursorObject.execute("INSERT INTO invoice values(10000)")
            con.commit()
            invoice_num = 10001
        except:
            cursorObject.execute("SELECT MAX(invoice_num) FROM invoice")
            r=cursorObject.fetchall()
            invoice_num = 1 + r[0][0]
        try:
            date = "M" + datetime.datetime.now().strftime("%x").replace("/","")
            cursorObject.execute(f"CREATE TABLE {date} (Id INT NOT NULL, quantity INT NOT NULL, PRIMARY KEY(Id))") # maybe day date 
            con.commit()
        except:
            pass

        status.config(text=f"Logged IN. Welcome {user}")
    except:
        status.config(text="Error wile Logging In.")
def logout_sql():
    global con
    try:
        con.close()
        status.config(text="Logged Out.")
        del con
    except:
        status.config(text="Error wile Logging Out.")

class Carts():
    def __init__(self,num):
        self.cart={}
        self.cart_number=num

    def checkout(self,frame):
        fetch_product(con,self.cart)
        arr=fetch_detail(con,self.cart)
        print(*arr)
        frame.destroy()
        
    def commonFrame(self,container):
        global invoice_num
        invoice_num+=1
        frame = Frame(container)
        frame.pack(side="left",padx=5,pady=5)
        frame['relief'] = 'ridge'
        frame['borderwidth']=1
        
        cart_label =Label(frame,text=f"{self.cart_number}",padx=3,pady=3)
        id_field = Entry(frame)
        name = Label(frame, text = "Name",padx=3,pady=3)
        price = Label(frame, text = "Price",padx=3,pady=3)
        id = Label(frame, text = "ID",padx=3,pady=3)
        id_label = Label(frame, text = "ID",padx=3,pady=3)
        quantity = Label(frame, text = "Quantity",padx=3,pady=3)
        close = Button(frame, text = " X ", fg = "Black",takefocus=False, bg = "Red", command =lambda: frame.destroy())
        ok = Button(frame, text = "ADD", fg = "Black", bg = "Red", command =lambda: self.addItem(frame,id_field))
        checkout=Button(frame,text="Checkout",fg = "Black",takefocus=False, bg = "Green",command= lambda: self.checkout(frame))
        
        
        id_field.focus_set()
        id_field.bind("<Return>",lambda event: ok.focus_set())
        ok.bind("<Return>",lambda event: self.addItem(frame,id_field))
        
        cart_label.grid(row=0,column=0,padx=5,pady=5)
        id.grid(row=1,column=0,padx=5,pady=5)
        id_field.grid(row = 1, column = 1,padx=5,pady=5)
        ok.grid(row=2,column=2,padx=5,pady=5)
        id_label.grid(row=3,column=0,padx=5,pady=5)
        name.grid(row=3,column=1,padx=5,pady=5)
        quantity.grid(row=3,column=2,padx=5,pady=5)
        price.grid(row=3,column=3,padx=5,pady=5)    
        close.grid(row=0,column=2,padx=5,pady=5)
        checkout.grid(padx=5,pady=5)

    def alter_quantity(self,quantity,id):
        quantity.config(text=f"{self.cart[id][0] + 1}")
        self.cart[id][0] +=1

    def remove_item(self,frame,id):
        del self.cart[id]
        frame.destroy()

    def addItem(self,container,id_field):
        id=id_field.get()
        if id =="":
            print("Invalid Barcode")
            id_field.delete(0, END)
            id_field.focus_set()
            return
        try:
            self.cart[id][0] +=1
        except:
            self.cart[id]=[1,Frame(container)]

        x=self.cart[id][1]
        x.grid(padx=5,pady=5)
        x['relief'] = 'ridge'
        x['borderwidth']=1

        arr=fetch_detail(con,id)
        if arr == []:
            print("Invalid Barcode")
            id_field.delete(0, END)
            id_field.focus_set()
            return

        i=len(self.cart)
        id_label = Label(x, text = f"{id}",padx=3,pady=3)
        id_label.grid(row=i+2,column=0)
        name = Label(x, text = f"{arr[0][1]}",padx=3,pady=3)
        name.grid(row=i+2,column=1)
        quantity = Label(x, text = f"{self.cart[id][0]}",padx=3,pady=3)
        quantity.grid(row=i+2,column=2)
        price = Label(x, text = f"{arr[0][3]}",padx=3,pady=3)
        price.grid(row=i+2,column=3)
        add = Button(x, text = "+",padx=3,pady=3,fg = "Black", bg = "Red",command=lambda: self.alter_quantity(quantity,id))
        cross = Button(x, text = "x",padx=3,pady=3,fg = "Black", bg = "Red",command=lambda: self.remove_item(x,id))
        cross.grid(row=i+2,column=5)
        add.grid(row=i+2,column=4)
        
        id_field.delete(0, END)
        id_field.focus_set()

#con= start_database()
gui = Tk()
gui.configure(background="light green")
gui.title("Age Calculator")
gui.geometry("1024x720")

menubar = Menu(gui)
file = Menu(menubar, tearoff=0)
menubar.add_cascade(label='File',menu = file)
edit=Menu(menubar, tearoff=0)
menubar.add_cascade(label='Edit',menu = edit)
file.add_command(label='New File',command='None')
file.add_command(label='Exit',command=lambda: gui.destroy())
gui.config(menu=menubar)

status=Label(text=".....................")
status.pack(side="bottom")
login=Button(gui, text = "Login",padx=3,pady=3,fg = "Black", bg = "Pink",command=lambda :login_sql('root','manu'))
login.pack(side="top")
logout=Button(gui, text = "Logout",padx=3,pady=3,fg = "Black", bg = "Pink",command=lambda :logout_sql())
logout.pack(side="top")

butt=Button(gui, text = "Start A Cart",padx=3,pady=3,fg = "Black", bg = "Pink",
    command=lambda: threading.Thread(target=Carts(invoice_num).commonFrame(gui)))
butt.pack(side="top")

####################i don't know are all threads running########
# for thread in threading.enumerate():
#     print(thread.name)

gui.mainloop()

