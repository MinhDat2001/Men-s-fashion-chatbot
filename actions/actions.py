from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import sqlite3
from typing import Any, Text, Dict, List

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

    cursor.execute('''UPDATE user_info SET name=? WHERE CustomerID=?;''',(sender_id, name))
    
    print("update successfully !........")

    conn.commit()
    conn.close()