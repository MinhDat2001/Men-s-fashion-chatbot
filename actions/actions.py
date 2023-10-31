from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import sqlite3
from typing import Any, Text, Dict, List
import json
import re
import Levenshtein as lev
import db_sqlite as DB
# Constant

AlioConstant_Dress = "Váy"
AlioConstant_Trousers = "Quần"
AlioConstant_Shirt = "Áo"

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
        user_name = DB.get_user_name(user_id)

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
        user_message = tracker.latest_message.get('text').lower()
        if "trên" in user_message or "tren" in user_message:
            end_price = str(100000)
        if "dưới" in user_message or "duoi" in user_message:
            start_price = str(0)

        products = get_product_by_price(start_price, end_price)
        
        if len(products):
            dispatcher.utter_message(
                    response="utter_ask_products_price"
                )
            for i in products:
                dispatcher.utter_message(
                        text = i[0],
                        image = i[1]
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
        user_message = tracker.latest_message.get('text').lower()
        if "trên" in user_message or "tren" in user_message:
            end_price = str(100000)
        if "dưới" in user_message or "duoi" in user_message:
            start_price = str(0)
        products = get_product_by_price_and_type(start_price, end_price, AlioConstant_Dress)
        
        if len(products):
            dispatcher.utter_message(
                    response="utter_ask_products_price"
                )
            for i in products:
                dispatcher.utter_message(
                        text = i[0],
                        image = i[1]
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
        user_message = tracker.latest_message.get('text').lower()
        if "trên" in user_message or "tren" in user_message:
            end_price = str(100000)
        if "dưới" in user_message or "duoi" in user_message:
            start_price = str(0)
        products = get_product_by_price_and_type(start_price, end_price, AlioConstant_Shirt)

        if len(products):
            dispatcher.utter_message(
                    response="utter_ask_products_price"
                )
            for i in products:
                dispatcher.utter_message(
                        text = i[0],
                        image = i[1]
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
        user_message = tracker.latest_message.get('text').lower()
        if "trên" in user_message or "tren" in user_message:
            end_price = str(100000)
        if "dưới" in user_message or "duoi" in user_message:
            start_price = str(0)

        products = get_product_by_price_and_type(start_price, end_price, AlioConstant_Trousers)
        
        if len(products):
            dispatcher.utter_message(
                    response="utter_ask_products_price"
                )
            for i in products:
                dispatcher.utter_message(
                        text = i[0],
                        image = i[1]
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

        records = get_product_by_type(AlioConstant_Dress)
        dresses = ""
        for i in records:
            dresses += i[0] +", "

        dispatcher.utter_message(
                response="utter_ask_dress_type",
                dress = dresses
            )
        images = get_image_by_type(AlioConstant_Dress)
        dispatcher.utter_message("Sau đây là một số ảnh: ")
        for i in images:
            dispatcher.utter_message(
                image = i[0]
            )
        return []

class ActionShirtType(Action):
    def name(self):
        return "action_shirt_type"

    def run(self, dispatcher, tracker, domain):
        print("action_shirt_type")

        records = get_product_by_type(AlioConstant_Shirt)
        shirts = ""
        for i in records:
            shirts += i[0] +", "
        dispatcher.utter_message(
                response="utter_ask_shirt_type",
                shirt = shirts
            )
        images = get_image_by_type(AlioConstant_Shirt)
        dispatcher.utter_message("Sau đây là một số ảnh: ")
        for i in images:
            dispatcher.utter_message(
                image = i[0]
            )
        return []

class ActionTrousersType(Action):
    def name(self):
        return "action_trousers_type"

    def run(self, dispatcher, tracker, domain):
        print("action_trousers_type")

        records = get_product_by_type(AlioConstant_Trousers)
        
        trouser = ""
        for i in records:
            trouser += i[0] +", "
        dispatcher.utter_message(
                response="utter_ask_trousers_type",
                trousers = trouser
            )
        images = get_image_by_type(AlioConstant_Trousers)
        dispatcher.utter_message("Sau đây là một số ảnh: ")
        for i in images:
            dispatcher.utter_message(
                image = i[0]
            )
        return []
    
class ActionAskProductOrder(Action):
    def name(self):
        return "action_ask_product_order"

    def run(self, dispatcher, tracker, domain):
        print("action_ask_product_order")

        
        product_order = tracker.get_slot("product_order")
        order = resolve_product_order(product_order)
        previous_actions = []
        for event in tracker.events:
            if event.get('event') == 'action':
                previous_actions.append(event.get('name'))
        action = get_previous_action(previous_actions)
        
        if action is None or order is None:
            dispatcher.utter_message(
                response="utter_dont_know_product"
            )
        else:
            print("")

        dispatcher.utter_message(f"The previous actions were: {previous_actions}")
        return []


# Thông tin sản phẩm---------End-------------


# Mua hàng---------Start-------------

class ActionBuyProduct(Action):
    def name(self):
        return "action_buy_product"

    def run(self, dispatcher, tracker, domain):
        conversation = tracker.export_stories()
        print("write conversation!")
        with open("conversation.json", "w") as file:
            json.dump(conversation, file)

        return []

class ActionProductDetail(Action):
    def name(self):
        return "action_product_detail"

    def run(self, dispatcher, tracker, domain):
        latest_message = tracker.latest_message
        entities = latest_message['entities']
        print("message: ",latest_message)
        print("entities: ",entities)
        product_detail = entities[0]['value']
        print("product detail: ", product_detail)

        product_name = get_product_correct_name(product_detail)
        
        product = get_product_by_name(product_name)
        if product:
            dispatcher.utter_message(
                response="utter_ask_product_detail",
                name = product[0][1],
                price = product[0][4],
                description = product[0][3],
                image = product[0][7]
            )
        else:
            dispatcher.utter_message(
                response="utter_not_have_product_detail",
                name = product_detail
            )

        return []

class ActionCancleBuyProduct(Action):
    def name(self):
        return "action_cancle_buy_product"

    def run(self, dispatcher, tracker, domain):
        conversation = tracker.export_stories()
        print("write conversation!")
        with open("conversation.json", "w") as file:
            json.dump(conversation, file)

        return []

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
    
# hàm common

def get_product_correct_name(pre_name):

    max_distance = 1000
    name = ""
    product = get_all_product_name()

    for i in product:
        distance = lev.distance(pre_name.lower(), i[0].lower())/len(i[0])
        print("i[0]:", i[0])
        print("pre_name:", pre_name)
        print("distance:", distance)
        if distance<max_distance:
            name = i[0]
            max_distance = distance

    return name

def get_previous_action(list):
    listSkip = ["action_ask_product_order","action_unlikely_intent","action_listen"]
    for i in list:
        if i in listSkip:
            continue
        else:
            return i

    return None

def resolve_product_order(product_order):
    if product_order.lower() == "đầu" or product_order.lower() == "dầu":
        return 1
    if product_order.lower() == "giữa" or product_order.lower() == "giua":
        return 2
    if product_order.lower() == "cuối" or product_order.lower() == "cuoi":
        return 3
    try:
        return int(product_order)
    except:
        return None
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
