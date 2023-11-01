
import re
import Levenshtein as lev
from actions import db_sqlite as DB, AlioConstant

def get_product_correct_name(pre_name):

    max_distance = 1000
    name = ""
    product = DB.get_all_product_name()

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
    listSkip = ["action_ask_product_order","action_unlikely_intent","action_listen", "action_session_start", "utter_out_scope_other"]
    for i in range(len(list)-1, 0, -1):
        if list[i] in listSkip:
            continue
        else:
            return list[i]

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
    
def get_product_by_action(action, order):
    type = ""
    if action == "action_dress_type":
        type = AlioConstant.Dress
    elif action == "action_shirt_type":
        type = AlioConstant.Shirt
    elif action == "action_trousers_type":
        type = AlioConstant.Trousers
    records = DB.get_limit_product_by_type(type)
    if len(records) >= order:
        print(records[order-1])
        return records[order-1]
    return None