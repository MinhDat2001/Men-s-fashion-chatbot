
import sqlite3
import re

def create_database():
    conn = sqlite3.connect("Alio.db")
    print("create table start........")
    cursor = conn.cursor()
    sql1 = """
    CREATE TABLE user_info(
        sender_id VARCHAR,
        name VARCHAR,
        age VARCHAR,
        gender VARCHAR);
    """
    sql2 = """
    CREATE TABLE user_hobby(
        sender_id VARCHAR,
        hobby VARCHAR)
    """
    sql3 = """
    CREATE TABLE product(
        id INTEGER,
        name VARCHAR,
        type VARCHAR,
        description VARCHAR,
        price INTEGER,
        type_detail VARCHAR,
        quantity INTEGER,
        image TEXT,
        PRIMARY KEY("id" AUTOINCREMENT));
    """
    # cursor.execute(sql1)
    # cursor.execute(sql2)
    # cursor.execute(sql3)
    print("create table successfully........")

    # Commit your changes in the database
    conn.commit()

    #Closing the connection
    conn.close()

def insert_info(sender_id, name, gender, age):
    conn = sqlite3.connect("Alio.db")
    cursor = conn.cursor()

    print("connect to database success!") 

    cursor.execute('''INSERT INTO user_info(sender_id, name, gender, age) VALUES (?, ?, ?, ?)''',(sender_id, name, gender, age))
    
    print("insert successfully........")

    conn.commit()
    conn.close()

def insert_hobby(sender_id, hobby):
    conn = sqlite3.connect("Alio.db")
    cursor = conn.cursor()

    print("connect to database success!") 

    cursor.execute('''INSERT INTO user_hobby(sender_id, hobby) VALUES (?, ?)''',(sender_id, hobby))

    print("insert successfully........")

    conn.commit()
    conn.close()

def get_user_name(sender_id):
    conn = sqlite3.connect("Alio.db")
    cursor = conn.cursor()
    print("sender_id: " , sender_id)
    print("connect to database success!") 

    cursor.execute('''SELECT * from user_info WHERE sender_id=? LIMIT 1''',(sender_id,))
    
    print("select name successfully........")
    records = cursor.fetchone()
    print(records)
    if records:
        return records[1]
    else:
        return None
    
def update_info(sender_id, name, gender, age):
    conn = sqlite3.connect("Alio.db")
    cursor = conn.cursor()

    print("connect to database success!") 

    cursor.execute('''UPDATE user_info SET name=? WHERE sender_id=?;''',(name, sender_id))
    
    print("update successfully !........")

    conn.commit()
    conn.close()


def get_product_by_type(type):
    conn = sqlite3.connect("Alio.db")
    cursor = conn.cursor()
    print("type: " , type)
    print("get_product_by_type") 

    cursor.execute('''SELECT DISTINCT type_detail from product WHERE type=?''',(type,))
    
    print("select product type_detail successfully........")
    records = cursor.fetchall()
    print(records)
    return records

def get_limit_product_by_type(type):
    conn = sqlite3.connect("Alio.db")
    cursor = conn.cursor()
    print(" db_sqlite: get_limit_product_by_type") 
    print("type: " , type)

    cursor.execute('''SELECT * from product WHERE type=? LIMIT 3''',(type,))
    records = cursor.fetchall()
    return records

def get_image_by_type(type):
    conn = sqlite3.connect("Alio.db")
    cursor = conn.cursor()
    print("type: " , type)
    print("get_product_by_type") 

    cursor.execute('''SELECT image  from product WHERE type=? LIMIT 3''',(type,))
    
    print("select product type_detail successfully........")
    records = cursor.fetchall()
    print(records)
    return records

def get_product_by_price(start_price, end_price):
    conn = sqlite3.connect("Alio.db")
    cursor = conn.cursor()
    print("get_product_by_price") 
    print("start_price: " , start_price)
    print("end_price: " , end_price)
    number1 = re.findall(r'\d+', start_price)
    number2 = re.findall(r'\d+', end_price)
    start = int(number1[0])*1000
    end = int(number2[0])*1000
    print("start_price: " , start)
    print("end_price: " , end)

    cursor.execute('''SELECT name, image from product WHERE price>=? and price<=?''',(start,end))
    
    print("select product successfully........")
    records = cursor.fetchall()
    print(records)
    return records

def get_product_by_price_and_type(start_price, end_price, type):
    conn = sqlite3.connect("Alio.db")
    cursor = conn.cursor()
    print("get_product_by_price_and_type") 
    number1 = re.findall(r'\d+', start_price)
    number2 = re.findall(r'\d+', end_price)
    start = int(number1[0])*1000
    end = int(number2[0])*1000
    print("start_price: " , start)
    print("end_price: " , end)

    cursor.execute('''SELECT name, image from product WHERE price>=? and price<=? and type=?''',(start,end, type))
    
    print("select product successfully........")
    records = cursor.fetchall()
    print(records)
    return records

def get_product_by_name(name):
    conn = sqlite3.connect("Alio.db")
    cursor = conn.cursor()
    print("name: " , name)
    print("get_product_by_name") 

    cursor.execute('''SELECT * from product WHERE name LIKE ? LIMIT 1''',(name,))
    
    print("select product successfully........")
    records = cursor.fetchall()
    print(records)
    return records

def get_all_product_name():
    conn = sqlite3.connect("Alio.db")
    cursor = conn.cursor()
    print("get_all_product_name") 

    cursor.execute('''SELECT DISTINCT name from product ''')
    
    print("select product successfully........")
    records = cursor.fetchall()
    print("số sản phẩm: ",len(records))
    return records

def order_product(user_id):
    conn = sqlite3.connect("Alio.db")
    cursor = conn.cursor()
    print("get_all_product_name") 

    cursor.execute('''SELECT DISTINCT name from product ''')
    
    print("select product successfully........")
    records = cursor.fetchall()
    print("số sản phẩm: ",len(records))
    return records

def change_order_status(user_id, product_id):
    conn = sqlite3.connect("Alio.db")
    cursor = conn.cursor()
    print("get_all_product_name") 

    cursor.execute('''SELECT DISTINCT name from product ''')
    
    print("select product successfully........")
    records = cursor.fetchall()
    print("số sản phẩm: ",len(records))
    return records
