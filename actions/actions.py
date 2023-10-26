from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import sqlite3
from typing import Any, Text, Dict, List
import json

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

        dispatcher.utter_message(
                response="utter_ask_products_price"
            )
        return []

class ActionDressPrice(Action):
    def name(self):
        return "action_dress_price"

    def run(self, dispatcher, tracker, domain):
        print("action_dress_price")

        dispatcher.utter_message(
                response="utter_ask_dress_price"
            )
        return []

class ActionShirtsPrice(Action):
    def name(self):
        return "action_shirts_price"

    def run(self, dispatcher, tracker, domain):
        print("action_shirts_price")

        dispatcher.utter_message(
                response="utter_ask_shirts_price"
            )
        return []

class ActionTrousersPrice(Action):
    def name(self):
        return "action_trousers_price"

    def run(self, dispatcher, tracker, domain):
        print("action_trousers_price")

        dispatcher.utter_message(
                response="utter_ask_trousers_price"
            )
        return []

class ActionDressType(Action):
    def name(self):
        return "action_dress_type"

    def run(self, dispatcher, tracker, domain):
        print("action_dress_type")

        dispatcher.utter_message(
                response="utter_ask_dress_type"
            )
        return []

class ActionShirtType(Action):
    def name(self):
        return "action_shirt_type"

    def run(self, dispatcher, tracker, domain):
        print("action_shirt_type")

        dispatcher.utter_message(
                response="utter_ask_shirt_type"
            )
        return []

class ActionTrousersType(Action):
    def name(self):
        return "action_trousers_type"

    def run(self, dispatcher, tracker, domain):
        print("action_trousers_type")

        dispatcher.utter_message(
                response="utter_ask_trousers_type"
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
        
        # create_database()
        dispatcher.utter_message("Đã tạo DB")

        return []
    
# connect DB
def create_database():
    conn = sqlite3.connect("Alio.db")
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
    cursor.execute(sql1)
    cursor.execute(sql2)
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