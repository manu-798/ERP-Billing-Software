import mysql.connector
from testing import get_connector

#con= get_connector()

#after every 10 transactions or 10 invoices after generate the [[[stock update]]]
#on calling generate report on most sold items,least sold items, most worthy items - depends on profit 
# and sales, like 3blue1brown problem , most worthless items,  
cn=mysql.connector.connect(host="localhost", user="root", password="manu")
cursorObject=cn.cursor()
cursorObject.execute("USE DATABASE product_db")