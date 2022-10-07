from tkinter import *
from product import add_product,start_database

def clearFrame(frame):
    # destroy all widgets from frame
    for widget in frame.winfo_children():
       widget.destroy()
    
    # this will clear frame and frame will be empty
    # if you want to hide the empty panel then
    frame.pack_forget()

def mainFrame(container):
    frame=Frame(container)
    frame.pack(side="top",padx=5,pady=5)
    frame['relief'] = 'ridge'
    frame['borderwidth']=1
    cart= Button(frame, text = "Open Cart", fg = "Black", bg = "Red", command = lambda: clearFrame(frame))    
    cart.grid(row=0,column=0)
    dart= Button(frame, text = "Add Product", fg = "Black", bg = "Red", command = lambda: addProducts(container))    
    dart.grid(row=0,column=1)


def addProducts(container):
    frame = Frame(container)
    frame.pack(side="left",padx=5,pady=5)
    frame['relief'] = 'ridge'
    frame['borderwidth']=1

    id = Label(frame, text = "ID",padx=3,pady=3)
    name = Label(frame, text = "Name",padx=3,pady=3)
    quantity = Label(frame, text = "Quantity",padx=3,pady=3)
    price = Label(frame, text = "Price",padx=3,pady=3)
    expiry = Label(frame, text = "Expiry",padx=3,pady=3)

    id_field = Entry(frame)
    name_field = Entry(frame)
    quantity_field = Entry(frame)
    price_field = Entry(frame)
    expiry_field = Entry(frame)

    id.grid(row = 0, column = 0)
    id_field.grid(row = 0, column = 1)
    name.grid(row = 1, column = 0)
    name_field.grid(row = 1, column = 1)
    quantity.grid(row = 2, column = 0)
    quantity_field.grid(row = 2, column = 1)
    price.grid(row = 3, column = 0)
    price_field.grid(row = 3, column = 1)
    expiry.grid(row = 4, column = 0)
    expiry_field.grid(row = 4, column = 1)
    add = Button(frame, text = "Add", fg = "Black", bg = "Red", command =lambda: add_product(con,id_field.get(),name_field.get(),quantity_field.get(),price_field.get(),expiry_field.get()))
    close = Button(frame, text = " X ", fg = "Black", bg = "Red", command =lambda: clearFrame(frame))
    close.grid(row=0,column=2,padx=5,pady=5)
    add.grid(row=5,column=1,padx=5,pady=5)


print("ok")
con= start_database()


gui = Tk()
gui.configure(background="light green")
gui.title("Age Calculator")
gui.geometry("1024x720")
mainFrame(gui)



gui.mainloop()