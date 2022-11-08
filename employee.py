def create_new_users(con,name,password,database,permissions,status):
    cursorObject = con.cursor()
    cursorObject.execute('select current_user()')
    r=cursorObject.fetchall()
    if permissions==0:
        permissions='SELECT,UPDATE, CREATE'
    if permissions==1:
        permissions='*'    
    if r[0][0] == "root@localhost":
        cursorObject.execute(f"CREATE USER IF NOT EXISTS {name}@localhost IDENTIFIED BY '{password}'") 
        con.commit()
        cursorObject.execute(f"GRANT {permissions} ON {database}.* TO '{name}'@localhost")
        con.commit()
        cursorObject.execute("FLUSH PRIVILEGES")
        con.commit()
    else:
        status.set("Access Denied")

def delete_users(con,name,status):
    cursorObject = con.cursor()
    cursorObject.execute('select user from mysql.user')
    r=cursorObject.fetchall()
    print(r)
    cursorObject.execute('select current_user()')
    r=cursorObject.fetchall()
    if r[0][0] == "root@localhost":
        host="localhost"
        cursorObject.execute(f"DROP user {name}@{host}")
        con.commit()
        status.set("User Dropped")
    else:
        status.set("Access Denied, only Root could.")

def modify_users():
    pass
def view_users(con):
    cursorObject = con.cursor()
    cursorObject.execute('select user from mysql.user')
    r=cursorObject.fetchall()
    print(r)
