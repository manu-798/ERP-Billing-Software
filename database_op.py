from csv import writer
import datetime
import os
import mysql.connector
import employee
import MySQLdb
def start_database():
    #con = employee.login(id,pass)
    con = mysql.connector.connect(host="localhost", user="root", password="manu")
    # preparing a cursor object
    cursorObject = con.cursor()
    # creating database
    try:
        cursorObject.execute("CREATE DATABASE product_db")
    except:
        pass
    cursorObject.execute("USE product_db")
    # creating tables
    try:
        cursorObject.execute("CREATE TABLE products ( Id INT NOT NULL ,Name Varchar(255) NOT NULL, Quantity INT NOT NULL, Price INT, Expiry Varchar(255), PRIMARY KEY(Id))")
    except:
        pass
    try:
        cursorObject.execute("CREATE TABLE invoice (invoice_num INT NOT NULL AUTO_INCREMENT, PRIMARY KEY(invoice_num))") # maybe day date 
    except:
        pass
    try:
        date = datetime.datetime.now().strftime("%x")
        cursorObject.execute(f"CREATE TABLE {date} (Id INT NOT NULL, quantity INT NOT NULL, PRIMARY KEY(Id))") # maybe day date 
    except:
        pass
    return con

def add_product(con,id,name,quantity,price,expiry,costprice,info):
    data = (id,name,quantity,price,expiry,costprice,info)
    c = con.cursor()
    c.execute(f"select * from products where Id = {id}")
    r=c.fetchall()
    if r ==[]:
        sql = 'insert into products values(%s,%s,%s,%s,%s,%s,%s)'
        # Executing the sql Query

        c.execute(sql, data)

        # Commit() method to make changes in the table
        con.commit()
    else:
        print(f"{r[1]} - {r[0]} items are already in stock")
        quantity+=r[2]
        data = (id,name,quantity,price,expiry)
        sql = 'insert into products values(%s,%s,%s,%s,%s)'
        # Executing the sql Query

        c.execute(sql, data)

        # Commit() method to make changes in the table
        con.commit()
    print("Successfully Added")
def fetch_product(con,cart,customer_id):
    c = con.cursor()
    today = str(datetime.date.today())
    total_item=0
    total=0
    c.execute('insert into transaction() values()')
    con.commit()
    c.execute('select last_insert_id()')
    r=c.fetchall()
    invoice_num=r[0][0]
    m_date="M"+today
    try:
        with open(f"data/{m_date}/{invoice_num}.csv",'w',newline='') as f:
            write = writer(f)
            for i in cart.keys():
                x=cart[i][2]
                total_item+=x
                total+=x*cart[i][3]
                write.writerow([i,x])
                threshold=5
                c.execute(f"SELECT quantity from products WHERE id = {i}")
                q=c.fetchall()[0][0]
                p=q-x
                if q - x < threshold:
                    try:
                        c.execute(f'insert into borderline_products values({i},"{cart[i][1]}",{p},{cart[i][3]})')
                        con.commit()
                    except:
                        c.execute(f'update borderline_products set quantity = {p} where id={i}')
                        con.commit()
                c.execute(f"UPDATE products SET quantity = quantity -{x} WHERE id = {i}")
                con.commit()
    except:
        foldername=f"data/{m_date}"
        os.makedirs(foldername)
        with open(f"data/{m_date}/{invoice_num}.csv",'w',newline='') as f:
            write = writer(f)
            for i in cart.keys():
                x=cart[i][2]
                total_item+=x
                total+=x*cart[i][3]
                write.writerow([i,x])
                threshold=5
                c.execute(f"SELECT quantity from products WHERE id = {i}")
                q=c.fetchall()[0][0]
                if q - x < threshold:
                    try:
                        c.execute(f'insert into borderline_products values({i},"{cart[i][1]}",{p},{cart[i][3]})')
                        con.commit()
                    except:
                        c.execute(f'update borderline_products set quantity = {p} where id={i}')
                        con.commit()
                # this cannot be done, if a person takes a long time to checkout and on other system
                # someone has checked out same item, so we have to calculate it here only.
                c.execute(f"UPDATE products SET quantity = quantity -{x} WHERE id = {i}")
                con.commit()
    c.execute(f"UPDATE transaction SET customer_id ='{customer_id}',i_date='{today}',total ={total}, total_item={x} WHERE invoice={invoice_num}")
    con.commit()
    #try:
    # address=f"{date}/{cart_no}.csv"
    # c.execute(f"INSERT INTO {date} VALUES({cart_no},{customer_id},{total},{total_item})")
    # con.commit()
    # except MySQLdb.ProgrammingError:
    #     c.execute(f"CREATE TABLE {date} (Id INT NOT NULL, quantity INT NOT NULL, PRIMARY KEY(Id))")
    #     con.commit()   ## incase 12AM
    # except:    
    #     print("something's wrong")
        
    print("Succesful")  
def fetch_detail(con,id):
    # both id or dictionary of id could be thrown at the function
    arr=[]
    c = con.cursor()
    if type(id) is dict:
        for i in id.keys():
            q=id[i][0]
            c.execute(f'select * from products where id={i}')
            r=c.fetchall()
            arr.append([r[0][0],r[0][1],r[0][3],q])
        return arr
    else:
        sql = f'select * from products where id={id}'
        c.execute(sql)
        r = c.fetchall()
        return r

