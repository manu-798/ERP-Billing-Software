from PIL import ImageTk,Image as Im
from matplotlib import widgets
from matplotlib.pyplot import table
import mysql.connector
from tkinter import *

from pyparsing import col
from invoices import CustomNotebook
from product import fetch_product,fetch_detail,add_product
from employee import delete_users, create_new_users, view_users
import mysql.connector
import tkinter as tk
from tkinter import ttk
#con= get_connector()

def create_new_user(con,navigation_frame):
    container=Frame(navigation_frame,height=1025,width=1500)
    container.pack()
    navigation_frame.add(container,text="Create New User")
    container.pack_propagate(False)

    frame = Frame(container)
    frame.pack(side="left",padx=5,pady=5)
    frame['relief'] = 'ridge'
    frame['borderwidth']=1

    ename=Label(frame,text="Name")
    ename.grid(row=0,column=0)
    ename_field=Entry(frame)
    ename_field.grid(row=0,column=1)
    epassword=Label(frame,text="Password")
    epassword.grid(row=2,column=0)
    epassword_field=Entry(frame)
    epassword_field.grid(row=2,column=1)
    # re_password=Label(frame,text="Password")
    # re_password.grid(row=2,column=0)
    # re_password_field=Entry(frame)
    # re_password_field.grid(row=2,column=1)
    database=Label(frame,text="Database Access")
    database.grid(row=3,column=0)
    database_field=Entry(frame)
    database_field.grid(row=3,column=1)
    var1 = tk.IntVar()
    var2 = tk.IntVar()
    base=Label(frame,text="Permissions")
    base.grid(row=4,column=0)
    c1 = tk.Checkbutton(frame, text='SELECT, CREATE, UPDATE',variable=var1, onvalue=0, offvalue=0)
    c1.grid(row=4,column=1)
    c2 = tk.Checkbutton(frame, text='ALL PERMISSIONS',variable=var1, onvalue=1, offvalue=0)
    c2.grid(row=4,column=2)

    but=Button(frame, text = "Submit",padx=3,pady=3,fg = "white",borderwidth=0, bg = "grey20",command=lambda: create_new_users(con,ename_field.get(),epassword_field.get(),database_field.get(),var1.get(),status))
    but.grid(row=5,column=0,padx=6,pady=10)
    
def view_user(con,navigation_frame):
    list = view_users(con)
    container=Frame(navigation_frame,height=1025,width=1500)
    container.pack()
    navigation_frame.add(container,text="View User")
    container.pack_propagate(False)
    frame = Frame(container)
    frame.pack(side="left",padx=5,pady=5)
    frame['relief'] = 'ridge'
    frame['borderwidth']=1

def delete_user(con,navigation_frame):
    container=Frame(navigation_frame,height=1025,width=1500)
    container.pack()
    navigation_frame.add(container,text="Drop User")
    container.pack_propagate(False)
    
    frame = Frame(container)
    frame.pack(side="left",padx=5,pady=5)
    frame['relief'] = 'ridge'
    frame['borderwidth']=1
    name=Label(frame,text="Name")
    name.grid(row=0,column=0)
    name_field=Entry(frame)
    name_field.grid(row=0,column=1)
    but=Button(frame, text = "Submit",padx=3,pady=3,fg = "white",borderwidth=0, bg = "grey20",command=lambda: delete_users(con,name_field.get(),status))
    but.grid(row=0,column=0,padx=6,pady=10)

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
            cursorObject.execute("CREATE TABLE products ( Id INT NOT NULL ,Name Varchar(255) NOT NULL, Quantity INT NOT NULL, Price INT, Expiry Varchar(255), costprice INT, info Varchar(225), PRIMARY KEY(Id))")
            con.commit()
        except:
            pass
        try:
            cursorObject.execute(f"CREATE TABLE transaction (invoice INT NOT NULL AUTO_INCREMENT,i_date VARCHAR(20), customer_id VARCHAR(225),total INT, total_item INT,  PRIMARY KEY(invoice))") # maybe day date 
            con.commit()
            cursorObject.execute("ALTER TABLE transaction AUTO_INCREMENT = 1000")
            con.commit()
        except:
            pass
        try:
            cursorObject.execute("CREATE TABLE borderline_products ( Id INT NOT NULL ,Name Varchar(255) NOT NULL, Quantity INT , Price INT, PRIMARY KEY(Id))")
            con.commit()
        except:
            pass
        status.set(f"Logged IN. Welcome {user}")
    except:
        status.set("Error wile Logging In.")
def logout_sql():
    global con
    try:
        con.close()
        status.set("Logged Out.")
        del con
    except:
        status.set("Error wile Logging Out.")
def clear(container):
    for widget in container.winfo_children():
        if widget == navigation_frame:
            continue
        widget.pack_forget()
def reappear(container):
    clear(container)
    for widget in container.winfo_children():
        widget.pack() 
def remove_instance(container):
    for widget in container.winfo_children():
        if widget == navigation_frame:
            continue
        widget.destroy()
        widget.pack_forget()
class Carts():
    def __init__(self,num):
        self.cart={}
        self.cart_number=num
    def remove(self,my_tree,id_field,quantity_field):
        x=my_tree.selection()
        for i in x:
            my_tree.delete(i)
        id_field.delete(0, END)
        quantity_field.delete(0, END)
        id_field.focus_set()
    def checkout(self,my_tree,customer_field):
        customer_id=customer_field.get()
        fetch_product(con,self.cart,customer_id)
        status.set("Successful")
        for item in my_tree.get_children():
            print(my_tree.item(item)["values"])
        navigation_frame.after(2000,lambda:navigation_frame.forget("current"))
    def clear(self,container):
        for widget in container.winfo_children():
            if widget == navigation_frame:
                continue
            widget.pack_forget()
    def reappear(self,container):
        self.clear(container)
        for widget in container.winfo_children():
            widget.pack() 
    def remove_instance(self,container):
        for widget in container.winfo_children():
            if widget == navigation_frame:
                continue
            widget.destroy()
    
    def newFrame(self,navigation_frame):
        container=Frame(navigation_frame,height=1025,width=1100)
        container.pack()
        navigation_frame.add(container,text="Cart")
        container.pack_propagate(False)
        tree_frame= Frame(container,bg='grey12')
        tree_frame.pack(side=TOP,anchor=N,pady=10)
     

        style = ttk.Style()
        style.theme_use('default')
        style.configure("Treeview",background="grey24",foreground="white",rowheight=25,fieldbackground="white")
        style.map('Treeview', background=[('selected',"#347083")])

        #create treeview scrollbar
        tree_scroll= Scrollbar(tree_frame)
        tree_scroll.pack(side="right",fill=Y)
        #create treeview
        my_tree= ttk.Treeview(tree_frame,yscrollcommand=tree_scroll.set,selectmode="extended")
        my_tree.pack()
        #configure scrollbar
        tree_scroll.config(command=my_tree.yview)
        #create table
        my_tree['columns']=("id","product name","quantity","price")
        my_tree.column("#0",width=0,stretch=NO)
        my_tree.column("id",anchor=W,width=300)
        my_tree.column("product name",anchor=W,width=240)
        my_tree.column("quantity",anchor=CENTER,width=240)
        my_tree.column("price",anchor=W,width=240)

        my_tree.heading("#0",text="",anchor=W)
        my_tree.heading("id",text="id",anchor=W)
        my_tree.heading("product name",text="product name",anchor=W)
        my_tree.heading("quantity",text="quantity",anchor=CENTER)
        my_tree.heading("price",text="price",anchor=CENTER)

        my_tree.tag_configure('oddrow',background="white",)
        my_tree.tag_configure('evenrow',background="light blue")
        my_tree.bind("<ButtonRelease-1>",lambda event: self.select(my_tree,id_field,quantity_field))

        data_frame = LabelFrame(container,text="Record")
        data_frame.pack(fill=X,side=TOP,anchor=N,expand="yes",padx=20)
        id_label = Label(data_frame,text="Product ID")
        id_label.grid(row = 0,column=0,padx=10, pady=10)
        id_field= Entry(data_frame)
        id_field.grid(row = 0,column=1,padx=10, pady=10)
        id_field.focus_set()
        id_field.bind("<Return>",lambda event: self.addItem(my_tree,id_field,quantity_field))
        id_field.bind("<Shift-Return>",lambda event: customer_field.focus_set())
  

        quantity = Label(data_frame,text="Quantity")
        quantity.grid(row = 0,column=4,padx=10, pady=10)
        quantity_field= Entry(data_frame)
        quantity_field.grid(row = 0,column=5,padx=10, pady=10)
        quantity_field.bind("<Shift-Return>",lambda event: customer_field.focus_set())
        #quantity_field.bind("<Return>",lambda event: id_field.focus_set())
        quantity_field.bind("<Return>",lambda event: self.addItem(my_tree,id_field,quantity_field))

        customer_label = Label(data_frame,text="Customer Phone Number")
        customer_label.grid(row = 1,column=0,padx=10, pady=10)
        customer_field= Entry(data_frame)
        customer_field.grid(row = 1,column=1,padx=10, pady=10)
        customer_field.bind("<Shift-Return>",lambda event: self.checkout(my_tree,customer_field))

        button_frame= LabelFrame(container,text="Command")
        button_frame.pack(side=TOP,anchor=N,expand="yes",fill=X,padx=20,pady=20)
        but1=Button(button_frame,text="ADD IN CART",command=lambda: self.addItem(my_tree,id_field,quantity_field))
        but1.grid(row=0,column=0,padx=10)
        but2=Button(button_frame,text="DELETE",command= lambda: self.remove(my_tree,id_field,quantity_field))
        but2.grid(row=0,column=1,padx = 10,pady=10)
        but=Button(button_frame,text="CHECKOUT",command=lambda:self.checkout(my_tree,customer_field))
        but.grid(row=0,column=2,padx = 10,pady=10)

    def select(self,my_tree,id_field,quantity_field):
        id_field.delete(0,END)
        quantity_field.delete(0,END)

        selected=my_tree.focus()

        if selected =='':
            return
        values =my_tree.item(selected,'values')

        id_field.insert(0,values[0])
        quantity_field.insert(0,values[2])

    def addItem(self,my_tree,id_field,quantity_field):
        id=id_field.get()
        if id =="":
            print("Invalid Barcode")
            id_field.delete(0, END)
            quantity_field.delete(0, END)
            id_field.focus_set()
            return

        arr=fetch_detail(con,id)
        if arr == []:
            print("Invalid Barcode")
            id_field.delete(0, END)
            id_field.focus_set()
            return
        try:
            self.cart[id][2] +=1
            if quantity_field.get()=='':
                quant=self.cart[id][2]
            else:
                quant = self.cart[id][2] + int(quantity_field.get())
            my_tree.item(id,text="",values=(arr[0][0],arr[0][1],quant,arr[0][3]))
            self.cart[id] = [arr[0][0],arr[0][1],quant,arr[0][3]]
        except:
            self.cart[id]=[arr[0][0],arr[0][1],1,arr[0][3]]
            if quantity_field.get()=='':
                quant=self.cart[id][2]
            else:
                quant = int(quantity_field.get())
            my_tree.insert(parent='',index='end',iid=id,text='',values=(arr[0][0],arr[0][1],quant,arr[0][3]))
            self.cart[id] = [arr[0][0],arr[0][1],quant,arr[0][3]]
                
        id_field.delete(0, END)
        quantity_field.delete(0, END)
        id_field.focus_set()
def addProducts(navigation_frame):

    container=Frame(navigation_frame,height=1025,width=1500)
    container.pack()
    navigation_frame.add(container,text="Add Product in Inventory")
    container.pack_propagate(False)

    frame = Frame(container,borderwidth=0)
    frame.pack(side="top",anchor=NW,padx=5,pady=5)

    id = Label(frame, text = "ID",padx=3,pady=3)
    name = Label(frame, text = "Name",padx=3,pady=3)
    quantity = Label(frame, text = "Quantity",padx=3,pady=3)
    price = Label(frame, text = "Price",padx=3,pady=3)
    expiry = Label(frame, text = "Expiry",padx=3,pady=3)
    cp=Label(frame,text="Cost Price",padx=3,pady=3)
    info=Label(frame,text="Info",padx=3,pady=3)

    id_field = Entry(frame)
    name_field = Entry(frame)
    quantity_field = Entry(frame)
    price_field = Entry(frame)
    expiry_field = Entry(frame)
    cp_field = Entry(frame)
    info_field= Entry(frame)

    id.grid(row = 0, column = 0,padx=5,pady=10)
    id_field.grid(row = 0, column = 1,padx=5,pady=10)
    name.grid(row = 1, column = 0,padx=5,pady=10)
    name_field.grid(row = 1, column = 1,padx=5,pady=10)
    quantity.grid(row = 2, column = 0,padx=5,pady=10)
    quantity_field.grid(row = 2, column = 1,padx=5,pady=10)
    price.grid(row = 3, column = 0,padx=5,pady=10)
    price_field.grid(row = 3, column = 1,padx=5,pady=10)
    expiry.grid(row = 4, column = 0,padx=5,pady=10)
    expiry_field.grid(row = 4, column = 1,padx=5,pady=10)
    cp.grid(row = 5, column = 0,padx=5,pady=10)
    cp_field.grid(row = 5, column = 1,padx=5,pady=10)
    info.grid(row = 6, column = 0,padx=5,pady=10)
    info_field.grid(row = 6, column = 1,padx=5,pady=10)
    add = Button(frame, text = "Add", fg = "Black", bg = "Red", command =lambda: add_product(con,id_field.get(),name_field.get(),quantity_field.get(),price_field.get(),expiry_field.get(),cp_field.get(),info_field.get()))
    close = Button(frame, text = " DRop ", fg = "Black", bg = "Red", command =lambda: removeProduct(id_field.get()))
    close.grid(row=7,column=0,padx=5,pady=5)
    add.grid(row=7,column=1,padx=5,pady=10)
def removeProduct(id):
    c=con.cursor()
    c.execute(f'delete from products where id={id}')  
    con.commit()
    status.set(f"{id} product dropped")
def reminder_frame(con,c_bar,understock):
    remove_instance(c_bar)
    c=con.cursor()
    c.execute('select * from borderline_products')
    understock = c.fetchall()
    for index,i in enumerate(understock):
        id= i[0]
        name=i[1]
        quantity=i[2]
        price=i[3]
        x=Label(c_bar,text=f"{index+1} : {id}/{name}/{quantity}/{price}")
        x.grid(row=index, column=0,sticky=N,padx=5,pady=10)
gui = Tk()
gui.title("Age Calculator")
#gui.attributes('-fullscreen',True)
gui.state('zoomed')
wide= gui.winfo_screenwidth()               
ht= gui.winfo_screenheight()               

menubar = Menu(gui,bg='grey22',fg='white')
file = Menu(menubar, tearoff=0,bg='grey22',fg='white')
menubar.add_cascade(label='File',menu = file)
edit=Menu(menubar, tearoff=0,bg='grey22',fg='white')
menubar.add_cascade(label='Edit',menu = edit)
file.add_command(label='New File',command='None')
file.add_command(label='Exit',command=lambda: gui.destroy())
windowmenu = Menu(menubar, name='window',bg='grey22',fg='white')
menubar.add_cascade(menu=windowmenu, label='Window')
gui.config(menu=menubar)

ht=1005
l_bar=Frame(gui,bg='gray20',height=ht,width=60)
l_bar.grid(row=0,column=0,sticky=W)
l_bar.grid_propagate(False)
#,width=50,height = 1025
#tuquoise,aquamarine
c_bar=Frame(gui,bg='grey16',height=ht,width=360)
c_bar.grid(row=0,column=1,sticky=W)
c_bar.grid_propagate(False)

r_bar=Frame(gui,bg='gray12',height=ht,width=1100)
r_bar.grid(row=0,column=2,sticky=W)
r_bar.pack_propagate(False)
r_bar.grid_propagate(False)

rr_bar=Frame(gui,bg='grey30',height=ht,width=400)
rr_bar.grid(row=0,column=3,sticky=W)
rr_bar.grid_propagate(False)

def hide_button(widget):
    widget.grid_forget()
def show_button(widget,r):
    widget.grid(row=r,column=0,sticky=NW)
    widget.grid_propogate(False)
##
op_button=Button(rr_bar,text="> Operation",width=50, command=lambda: show_button(op_bar,1))
op_button.grid(row=0,column=0,sticky=NW)
#op_button.grid_propagate(False)
op_bar=Frame(rr_bar,bg='grey16',height=470,width=400)
op_bar.grid(row=1,column=0,sticky=NW)
op_bar.grid_propagate(False)
B1 = Button(op_bar, text="Button 1")
B1.grid()
B2 = Button(op_bar, text="Button 2", command=lambda: hide_button(op_bar))
B2.grid()
B3 = Button(op_bar, text="Button 3")
B3.grid()
##
pop_button=Button(rr_bar,text="> Notification",width=50, command=lambda: show_button(pop_bar,3))
pop_button.grid(row=2,column=0,sticky=NW)
pop_button.grid_propagate(False)
pop_bar=Frame(rr_bar,bg='pink',height=470,width=400)
pop_bar.grid(row=3,column=0,sticky=NW)
pop_bar.grid_propagate(False)
B11 = Button(pop_bar, text="Not 1")
B11.grid()
B22 = Button(pop_bar, text="Not 2", command=lambda: hide_button(pop_bar))
B22.grid()
B33 = Button(pop_bar, text="not 3")
B33.grid()
style = ttk.Style()
s = ttk.Style()
#s.theme_use('default')
# s.configure('TNotebook.Tab', background="light yellow")
# s.map("TNotebook.Tab", background= [('selected',"#347083")])

navigation_frame=CustomNotebook(r_bar)
navigation_frame.grid()
navigation_frame.grid_propagate(False)

footer=Frame(gui,bg="turquoise",height=25,width=wide)
footer.grid(row=1,column=0,columnspan=4)
footer.grid_propagate(False)


status=StringVar()
status.set("Active")
cd=Label(footer,textvariable=status,font=("Helvetica", 7),bg='yellow')
cd.grid(row=0,column=0,padx=3)

understock=[[1,2,3,4],[5,6,7,8],[2,3,4,5],[6,7,4,5]]
invoice_num=1543
accounts_img=ImageTk.PhotoImage(Im.open("account.png").resize((50,50)))
accounts_but=Button(l_bar,text = "Accounts",image=accounts_img,padx=3,pady=3,fg = "Black", bg = "grey20",borderwidth=0,command= lambda:accounts_c_bar())
accounts_but.grid(row=0)
cart_img=ImageTk.PhotoImage(Im.open("cart.png").resize((40,40)))
cart=Button(l_bar, text = "Start A Cart",image=cart_img,padx=3,pady=3,fg = "white",borderwidth=0, bg = "grey20",
    command=lambda: cart_c_bar())
cart.grid(row=1,column=0,padx=6,pady=10)
invent_img=ImageTk.PhotoImage(Im.open("inventory.png").resize((50,50)))
checkInventory=Button(l_bar,text = "Inventory Management",image=invent_img,borderwidth=0,padx=3,pady=3,fg = "Black", bg = "grey20",command= lambda:inventory_c_bar())
checkInventory.grid(row=2,column=0,padx=6,pady=10)
customer_img=ImageTk.PhotoImage(Im.open("customer.png").resize((50,50)))
Customer=Button(l_bar,text = "Customer Management",image=customer_img,padx=3,pady=3,fg = "Black",borderwidth=0, bg = "grey20",command= lambda:customer_c_bar())
Customer.grid(row=3)
employee_img=ImageTk.PhotoImage(Im.open("employee.png").resize((50,50)))
employee_but=Button(l_bar,text = "Employee Management",image=employee_img,padx=3,pady=3,fg = "Black",borderwidth=0, bg = "grey20",command= lambda:employee_c_bar())
employee_but.grid(row=4,sticky=N)

#l_bar.rowconfigure(3,weight=2)
def cart_c_bar():
    remove_instance(c_bar)
    cart=Button(c_bar, text = "Open Cart",padx=3,pady=3,fg = "white",borderwidth=0, bg = "grey20",
    command=lambda: Carts(invoice_num).newFrame(navigation_frame))
    cart.grid(row=0,column=0,padx=6,pady=10)
def inventory_c_bar():
    remove_instance(c_bar)
    addtodb=Button(c_bar,text = "Add Product IN Inventory",borderwidth=0,padx=10,pady=10,fg = "white", bg = "grey20",command=lambda :addProducts(navigation_frame))
    addtodb.grid(row=0,column=0)
    check=Button(c_bar,text = "Check Border Items",borderwidth=0,padx=10,pady=10,fg = "white", bg = "grey20",command=lambda :reminder_frame(con,c_bar,understock))
    check.grid(row=1,column=0)
def employee_c_bar():
    remove_instance(c_bar)
    but1=Button(c_bar, text = "ADD EMPLOYEE",padx=3,pady=3,fg = "white",borderwidth=0, bg = "grey20",
    command=lambda: create_new_user(con,navigation_frame))
    but1.grid(row=0,column=0,padx=6,pady=10)
    cart=Button(c_bar, text = "DELETE EMPLOYEE",padx=3,pady=3,fg = "white",borderwidth=0, bg = "grey20",
    command=lambda: delete_user(con,navigation_frame))
    cart.grid(row=1,column=0,padx=6,pady=10)

def customer_c_bar():
    remove_instance(c_bar)
    cart=Button(c_bar, text = "ADD EMPLOYEE",padx=3,pady=3,fg = "white",borderwidth=0, bg = "grey20")
    cart.grid(row=0,column=0,padx=6,pady=10)
def accounts_c_bar():
    remove_instance(c_bar)
    login=Button(c_bar, text = "Login",padx=10,pady=10,fg = "white",borderwidth=0, bg = "grey12",command=lambda :login_sql('root','manu'))
    login.grid(row=0,column=0,padx=10,pady=5)
    logout=Button(c_bar, text = "Logout",padx=10,pady=10,fg = "white", bg = "grey12",borderwidth=0,command=lambda :logout_sql())
    logout.grid(row=1,column=0,padx=10,pady=5)

gui.mainloop()

