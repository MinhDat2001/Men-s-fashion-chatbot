# import sqlite3

# def create_database():
#     conn = sqlite3.connect("Alio.db")
#     cursor = conn.cursor()
#     sql = """

#     CREATE TABLE user_info(
#         sender_id VARCHAR,
#         name VARCHAR,
#         age VARCHAR,
#         gender VARCHAR);
    
#     CREATE TABLE user_hobby(
#         sender_id VARCHAR,
#         hobby VARCHAR)
# """
#     cursor.execute(sql)
#     print("create table successfully........")

#     # Commit your changes in the database
#     conn.commit()

#     #Closing the connection
#     conn.close()

# def insert_info(sender_id, name, gender, age):
#     conn = sqlite3.connect("Alio.db")
#     cursor = conn.cursor()

#     print("connect to database success!") 

#     cursor.execute('''INSERT INTO user_info(sender_id, name, gender, age) VALUES (?, ?, ?, ?)''',(sender_id, name, gender, age))
    
#     print("insert successfully........")

#     conn.commit()
#     conn.close()

# def insert_hobby(sender_id, hobby):
#     conn = sqlite3.connect("Alio.db")
#     cursor = conn.cursor()

#     print("connect to database success!") 

#     cursor.execute('''INSERT INTO user_hobby(sender_id, hobby) VALUES (?, ?)''',(sender_id, hobby))

#     print("insert successfully........")

#     conn.commit()
#     conn.close()

# if __name__ == "__main__":
#     create_database()