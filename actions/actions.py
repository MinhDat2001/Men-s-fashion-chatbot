from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import sqlite3
from typing import Any, Text, Dict, List
import json
import re

# Cơ bản ---------Start-------------
class SaveConversationAction(Action):
    def name(self):
        return "action_save_conversation"

    def run(self, dispatcher, tracker, domain):
        conversation = tracker.export_stories()
        print("write conversation!")
        with open("conversation.json", "w") as file:
            json.dump(conversation, file)

        return []

class ActionGreet(Action):
    def name(self) -> Text:
        return "action_greet"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        user_id = tracker.sender_id
        user_name = get_user_name(user_id)

        if user_name:
            dispatcher.utter_message(
                response="utter_greet_name",
                name=user_name
            )
        else:
            dispatcher.utter_message(
                response="utter_greet"
            )

        return []

# Cơ bản ---------End-------------

# Thông tin sản phẩm---------Start-------------

class ActionProductPrice(Action):
    def name(self):
        return "action_product_price"

    def run(self, dispatcher, tracker, domain):
        print("action_product_price")

        start_price = tracker.get_slot("start_price")
        end_price = tracker.get_slot("end_price")
        if not start_price:
            start_price = 0
        if not end_price:
            start_price = 100000000
        products = get_product_by_price(start_price, end_price)
        
        productString = ""
        for i in products:
            productString += i[0] +", "
        if len(products):
            dispatcher.utter_message(
                    response="utter_ask_products_price",
                    products = productString
                )
        else:
            dispatcher.utter_message(
                    response="utter_not_have_product"
                )
        return []

class ActionDressPrice(Action):
    def name(self):
        return "action_dress_price"

    def run(self, dispatcher, tracker, domain):
        print("action_dress_price")

        start_price = tracker.get_slot("start_price")
        end_price = tracker.get_slot("end_price")
        if not start_price:
            start_price = 0
        if not end_price:
            start_price = 100000000
        products = get_product_by_price_and_type(start_price, end_price, "Váy")
        
        productString = ""
        for i in products:
            productString += i[0] +", "
        if len(products):
            dispatcher.utter_message(
                    response="utter_ask_dress_price",
                    dress = productString
                )
        else:
            dispatcher.utter_message(
                    response="utter_not_have_dress"
                )
        return []

class ActionShirtsPrice(Action):
    def name(self):
        return "action_shirts_price"

    def run(self, dispatcher, tracker, domain):
        print("action_shirts_price")
        start_price = tracker.get_slot("start_price")
        end_price = tracker.get_slot("end_price")
        if not start_price:
            start_price = 0
        if not end_price:
            start_price = 100000000
        products = get_product_by_price_and_type(start_price, end_price, "Áo")

        productString = ""
        for i in products:
            productString += i[0] +", "
        if len(products):
            dispatcher.utter_message(
                    response="utter_ask_shirts_price",
                    shirt = productString
                )
        else:
            dispatcher.utter_message(
                    response="utter_not_have_shirt"
                )
        return []

class ActionTrousersPrice(Action):
    def name(self):
        return "action_trousers_price"

    def run(self, dispatcher, tracker, domain):
        print("action_trousers_price")

        start_price = tracker.get_slot("start_price")
        end_price = tracker.get_slot("end_price")
        if not start_price:
            start_price = 0
        if not end_price:
            start_price = 100000000

        products = get_product_by_price_and_type(start_price, end_price, "Quần")
        
        productString = ""
        for i in products:
            productString += i[0] +", "
        if len(products):
            dispatcher.utter_message(
                    response="utter_ask_trousers_price",
                    trousers = productString
                )
        else:
            dispatcher.utter_message(
                    response="utter_not_have_trousers"
                )
        return []

class ActionDressType(Action):
    def name(self):
        return "action_dress_type"

    def run(self, dispatcher, tracker, domain):
        print("action_dress_type")

        records = get_product_by_type("Váy")
        dresses = ""
        for i in records:
            dresses += i[0] +", "

        dispatcher.utter_message(
                response="utter_ask_dress_type",
                dress = dresses
            )
        return []

class ActionShirtType(Action):
    def name(self):
        return "action_shirt_type"

    def run(self, dispatcher, tracker, domain):
        print("action_shirt_type")

        records = get_product_by_type("Áo")
        shirts = ""
        for i in records:
            shirts += i[0] +", "
        dispatcher.utter_message(
                response="utter_ask_shirt_type",
                shirt = shirts
            )
        return []

class ActionTrousersType(Action):
    def name(self):
        return "action_trousers_type"

    def run(self, dispatcher, tracker, domain):
        print("action_trousers_type")

        records = get_product_by_type("Quần")
        
        trouser = ""
        for i in records:
            trouser += i[0] +", "
        dispatcher.utter_message(
                response="utter_ask_trousers_type",
                trousers = trouser
            )
        return []


# Thông tin sản phẩm---------End-------------


# Mua hàng---------Start-------------

# Mua hàng---------End-------------


# Thông tin người dùng---------Start-------------

class ActionSaveUserName(Action):
    def name(self) -> Text:
        return "action_save_user_name"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        first_name = tracker.get_slot("first_name")
        user_id = tracker.sender_id
        if get_user_name(user_id) == None:
            insert_info(user_id,first_name,"","")
        else:
            update_info(user_id, first_name, "","")

        if first_name:
            dispatcher.utter_message(
                response="utter_greet_name",
                name=first_name
            )
        else:
            dispatcher.utter_message(
                response="utter_greet"
            )

        return []

class ActionAskCustomerName(Action):
    def name(self) -> Text:
        return "action_ask_customer_name"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        user_id = tracker.sender_id
        user_name = get_user_name(user_id)

        if user_name:
            dispatcher.utter_message(
                response="utter_ask_customer_name",
                name=user_name
            )
        else:
            dispatcher.utter_message(
                response="utter_forget_customer_name"
            )

        return []

# Thông tin người dùng---------End-------------

class ActionCreateDB(Action):
    def name(self) -> Text:
        return "action_create_db"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        create_database()
        dispatcher.utter_message("Đã tạo DB")

        return []
    
# connect DB
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

    cursor.execute('''UPDATE user_info SET name=? WHERE sender_id=?;''',(sender_id, name))
    
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

def get_product_by_price(start_price, end_price):
    conn = sqlite3.connect("Alio.db")
    cursor = conn.cursor()
    print("get_product_by_price") 
    number1 = re.findall(r'\d+', start_price)
    number2 = re.findall(r'\d+', end_price)
    start = int(number1[0])*1000
    end = int(number2[0])*1000
    print("start_price: " , start)
    print("end_price: " , end)

    cursor.execute('''SELECT name from product WHERE price>=? and price<=?''',(start,end))
    
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

    cursor.execute('''SELECT name from product WHERE price>=? and price<=? and type=?''',(start,end, type))
    
    print("select product successfully........")
    records = cursor.fetchall()
    print(records)
    return records

def get_product_by_name(name):
    conn = sqlite3.connect("Alio.db")
    cursor = conn.cursor()
    print("name: " , name)
    print("get_product_by_name") 

    cursor.execute('''SELECT DISTINCT type_detail from product WHERE name LIKE '%?%' ''',(name,))
    
    print("select product successfully........")
    records = cursor.fetchall()
    print(records)
    return records
