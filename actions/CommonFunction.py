
import re
from actions import db_sqlite as DB, AlioConstant

def levenshtein_distance(str1, str2):
    m, n = len(str1), len(str2)
    
    
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j
    
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if str1[i - 1] == str2[j - 1]:
                cost = 0
            else:
                cost = 1
            dp[i][j] = min(dp[i - 1][j] + 1,  
                          dp[i][j - 1] + 1,  
                          dp[i - 1][j - 1] + cost)  
    
    return dp[m][n]/len(str2)

def get_product_correct_name(pre_name):

    max_distance = 1000
    name = ""
    product = DB.get_all_product_name()

    for i in product:
        distance = levenshtein_distance(pre_name.lower(), i[0].lower())
        print("i[0]:", i[0])
        print("pre_name:", pre_name)
        print("distance:", distance)
        if distance<max_distance:
            name = i[0]
            max_distance = distance

    return name

def get_previous_action(list):
    listSkip = ["action_ask_product_order","action_unlikely_intent","action_listen", "action_session_start", "utter_out_scope_other"]
    for i in range(len(list)-1, 0, -1):
        if list[i] in listSkip:
            continue
        else:
            return list[i]

    return None

def resolve_product_order(product_order):
    if product_order.lower() == "đầu" or product_order.lower() == "dầu" or product_order.lower() == "nhất":
        return 1
    if product_order.lower() == "giữa" or product_order.lower() == "giua" or product_order.lower() == "hai":
        return 2
    if product_order.lower() == "cuối" or product_order.lower() == "cuoi" or product_order.lower() == "ba":
        return 3
    try:
        return int(product_order)
    except:
        return None
    
def get_product_by_action(action, order, start_price, end_price):
    print("get_product_by_action")
    records = None
    if action == "action_dress_type":
        records = DB.get_limit_product_by_type(AlioConstant.Dress, order)
    elif action == "action_shirt_type":
        records = DB.get_limit_product_by_type(AlioConstant.Shirt, order)
    elif action == "action_trousers_type":
        records = DB.get_limit_product_by_type(AlioConstant.Trousers, order)
    if action == "action_product_price":
        records = get_limit_product_by_price(start_price, end_price, order)
    elif action == "action_dress_price":
        records = get_limit_product_by_price_and_type(start_price, end_price, order, AlioConstant.Dress)
    elif action == "action_shirts_price":
        records = get_limit_product_by_price_and_type(start_price, end_price, order, AlioConstant.Shirt)
    elif action == "action_trousers_price":
        records = get_limit_product_by_price_and_type(start_price, end_price, order, AlioConstant.Trousers)
    return records

def get_limit_product_by_price(start_price, end_price, order):
    record = DB.get_product_by_price(start_price, end_price)
    if len(record)>= order:
        return record[order-1]
    return None

def get_limit_product_by_price_and_type(start_price, end_price, order, type):
    print("start_price: ", start_price)
    print("end_price: ", end_price)
    print("order: ", order)
    print("type: ", type)
    record = DB.get_limit_product_by_price_and_type(start_price, end_price, type)
    if len(record)>= order:
        return record[order-1]
    return None

def change_money(price):
    print("price: ", price)
    price = str(price)
    res = ""
    for i in range(len(price) -1, -1, -1):
        res = price[i] + res
        if (i+1) % 3 == 0 :
            res = '.'+res
    print("after change: ",res)
    return res + " vnđ"