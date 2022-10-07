import datetime
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

def add_product(con,id,name,quantity,price,expiry):
    data = (id,name,quantity,price,expiry)
    c = con.cursor()
    c.execute(f"select * from products where Id = {id}")
    r=c.fetchall()
    if r ==[]:
        sql = 'insert into products values(%s,%s,%s,%s,%s)'
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
def fetch_product(con,cart):
    c = con.cursor()
    date = "M" + datetime.datetime.now().strftime("%x").replace("/","")
    for i in cart.keys():
        x=cart[i][0]
        c.execute(f"UPDATE products SET quantity = quantity -{x} WHERE id = {i}")
        con.commit()
        try:
            c.execute(f"SELECT * from {date} where id = {i}")
            c.execute(f"UPDATE {date} SET quantity = quantity + {x} WHERE id = {i}")
            con.commit()
        except MySQLdb.ProgrammingError:
            c.execute(f"CREATE TABLE {date} (Id INT NOT NULL, quantity INT NOT NULL, PRIMARY KEY(Id))")
            con.commit()
        except:    
            c.execute(f"INSERT INTO {date} values({i},{x})")
            con.commit()
    print("Succesful")  
def fetch_detail(con,id):
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

