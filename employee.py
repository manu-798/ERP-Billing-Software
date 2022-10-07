import mysql.connector

def create_new_user(con,name,password,database,permissions):
    cursorObject = con.cursor()
    cursorObject.execute('select current_user()')
    r=cursorObject.fetchall()
    if r[0][0] == "root@localhost":
        cursorObject.execute(f"CREATE USER IF NOT EXISTS {name}@localhost IDENTIFIED BY {password}") 
        con.commit()
        cursorObject.execute(f"GRANT {permissions} ON {database}. * TO @localhost")
        con.commit()
        cursorObject.execute("FLUSH PRIVILEGES")
        con.commit()
    else:
        print("Access Denied")

def delete_user(con,name):
    cursorObject = con.cursor()
    cursorObject.execute('select current_user()')
    r=cursorObject.fetchall()
    if r[0][0] == "root@localhost":
        host="localhost"
        cursorObject.execute(f"DROP user {name}@{host}")
        con.commit()
    else:
        print("Access Denied")
