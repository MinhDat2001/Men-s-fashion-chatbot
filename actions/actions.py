from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from typing import Any, Text, Dict, List
import json
from actions import db_sqlite as DB, AlioConstant, CommonFunction
from time import gmtime, strftime

product_detail_list = {}
# Cơ bản ---------Start-------------

class ActionGetTime(Action):
    def name(self) -> Text:
        return "action_get_time"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        print(strftime("%H:%M:%S", gmtime()))
        string = "Bây giờ là" + strftime("%H:%M:%S", gmtime())
        dispatcher.utter_message(
            text=string
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
        tracker.slots["previous_action"] = "action_product_price"

        try:
            start_price = "0"
            end_price = "10000"
            user_message = tracker.latest_message.get('text').lower()

            lastest_message = tracker.latest_message
            entities = lastest_message.get("entities", [])

            if len(entities) > 1:
                start_price = entities[0]["value"]
                end_price = entities[1]["value"]
            elif len(entities) > 0:
                start_price = entities[0]["value"]
                end_price = entities[0]["value"]
            if "trên" in user_message or "tren" in user_message:
                end_price = str(100000)
            if "dưới" in user_message or "duoi" in user_message:
                start_price = str(0)
            
            tracker.slots["start_price"] = start_price
            tracker.slots["end_price"] = end_price
            products = DB.get_product_by_price(start_price, end_price)
            
            if len(products):
                dispatcher.utter_message(
                        response="utter_ask_products_price"
                    )
                for i in products:
                    message = "Sản phẩm "+i[1] +" có giá là " + CommonFunction.change_money(i[4])
                    dispatcher.utter_message(
                            text = message,
                            image = i[7]
                        )
            else:
                dispatcher.utter_message(
                        response="utter_not_have_product"
                    )
        except:
            dispatcher.utter_message(
                response="utter_error"
            )
        return []

class ActionDressPrice(Action):
    def name(self):
        return "action_dress_price"

    def run(self, dispatcher, tracker, domain):
        print("action_dress_price")
        tracker.slots["previous_action"] = "action_dress_price"

        try:
            start_price = "0"
            end_price = "10000"
            user_message = tracker.latest_message.get('text').lower()

            lastest_message = tracker.latest_message
            entities = lastest_message.get("entities", [])

            if len(entities) > 1:
                start_price = entities[0]["value"]
                end_price = entities[1]["value"]
            elif len(entities) > 0:
                start_price = entities[0]["value"]
                end_price = entities[0]["value"]
            if "trên" in user_message or "tren" in user_message:
                end_price = str(100000)
            if "dưới" in user_message or "duoi" in user_message:
                start_price = str(0)
            
            tracker.slots["start_price"] = start_price
            tracker.slots["end_price"] = end_price
            products = DB.get_product_by_price_and_type(start_price, end_price, AlioConstant.Dress)
            
            if len(products):
                dispatcher.utter_message(
                        response="utter_ask_products_price"
                    )
                for i in products:
                    message = "Sản phẩm "+i[1] +" có giá là " + CommonFunction.change_money(i[4])
                    dispatcher.utter_message(
                            text = message,
                            image = i[7]
                        )
            else:
                dispatcher.utter_message(
                        response="utter_not_have_dress"
                    )
        except:
            dispatcher.utter_message(
                response="utter_error"
            )
        return []

class ActionShirtsPrice(Action):
    def name(self):
        return "action_shirts_price"

    def run(self, dispatcher, tracker, domain):
        print("action_shirts_price")
        tracker.slots["previous_action"] = "action_shirts_price"

        try:
            start_price = "0"
            end_price = "10000"
            user_message = tracker.latest_message.get('text').lower()

            lastest_message = tracker.latest_message
            entities = lastest_message.get("entities", [])

            if len(entities) > 1:
                start_price = entities[0]["value"]
                end_price = entities[1]["value"]
            elif len(entities) > 0:
                start_price = entities[0]["value"]
                end_price = entities[0]["value"]
            if "trên" in user_message or "tren" in user_message:
                end_price = str(100000)
            if "dưới" in user_message or "duoi" in user_message:
                start_price = str(0)
                
            
            tracker.slots["start_price"] = start_price
            tracker.slots["end_price"] = end_price
            print(tracker.slots["start_price"])
            print(tracker.slots["end_price"])
            products = DB.get_product_by_price_and_type(start_price, end_price, AlioConstant.Shirt)

            if len(products):
                dispatcher.utter_message(
                        response="utter_ask_products_price"
                    )
                for i in products:
                    message = "Sản phẩm "+i[1] +" có giá là " + CommonFunction.change_money(i[4])
                    dispatcher.utter_message(
                            text = message,
                            image = i[7]
                        )
            else:
                dispatcher.utter_message(
                        response="utter_not_have_shirt"
                    )
        except:
            dispatcher.utter_message(
                response="utter_error"
            )
        return []

class ActionTrousersPrice(Action):
    def name(self):
        return "action_trousers_price"

    def run(self, dispatcher, tracker, domain):
        print("action_trousers_price")
        tracker.slots["previous_action"] = "action_trousers_price"

        try:
            start_price = "0"
            end_price = "10000"
            user_message = tracker.latest_message.get('text').lower()

            lastest_message = tracker.latest_message
            entities = lastest_message.get("entities", [])

            if len(entities) > 1:
                start_price = entities[0]["value"]
                end_price = entities[1]["value"]
            elif len(entities) > 0:
                start_price = entities[0]["value"]
                end_price = entities[0]["value"]
            if "trên" in user_message or "tren" in user_message:
                end_price = str(100000)
            if "dưới" in user_message or "duoi" in user_message:
                start_price = str(0)
            
            tracker.slots["start_price"] = start_price
            tracker.slots["end_price"] = end_price

            products = DB.get_product_by_price_and_type(start_price, end_price, AlioConstant.Trousers)
            
            if len(products):
                dispatcher.utter_message(
                        response="utter_ask_products_price"
                    )
                for i in products:
                    message = "Sản phẩm "+i[1] +" có giá là " + CommonFunction.change_money(i[4])
                    dispatcher.utter_message(
                            text = message,
                            image = i[7]
                        )
            else:
                dispatcher.utter_message(
                        response="utter_not_have_trousers"
                    )
        except:
            dispatcher.utter_message(
                response="utter_error"
            )
        return []

class ActionDressType(Action):
    def name(self):
        return "action_dress_type"

    def run(self, dispatcher, tracker, domain):
        print("action_dress_type")
        tracker.slots["previous_action"] = "action_dress_type"

        try:
            records = DB.get_product_by_type(AlioConstant.Dress)
            dresses = ""
            for i in records:
                dresses += i[0] +", "

            dispatcher.utter_message(
                    response="utter_ask_dress_type",
                    dress = dresses
                )
            images = DB.get_image_by_type(AlioConstant.Dress)
            dispatcher.utter_message("Sau đây là một số ảnh: ")
            for i in images:
                dispatcher.utter_message(
                    image = i[0]
                )
        except:
            dispatcher.utter_message(
                response="utter_error"
            )
        return []

class ActionShirtType(Action):
    def name(self):
        return "action_shirt_type"

    def run(self, dispatcher, tracker, domain):
        print("action_shirt_type")
        tracker.slots["previous_action"] = "action_shirt_type"

        records = DB.get_product_by_type(AlioConstant.Shirt)
        shirts = ""
        for i in records:
            shirts += i[0] +", "
        dispatcher.utter_message(
                response="utter_ask_shirt_type",
                shirt = shirts
            )
        images = DB.get_image_by_type(AlioConstant.Shirt)
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
        tracker.slots["previous_action"] = "action_trousers_type"
        try:
            records = DB.get_product_by_type(AlioConstant.Trousers)
            
            trouser = ""
            for i in records:
                trouser += i[0] +", "
            dispatcher.utter_message(
                    response="utter_ask_trousers_type",
                    trousers = trouser
                )
            images = DB.get_image_by_type(AlioConstant.Trousers)
            dispatcher.utter_message("Sau đây là một số ảnh: ")
            for i in images:
                dispatcher.utter_message(
                    image = i[0]
                )
        except:
            dispatcher.utter_message(
                response="utter_error"
            )
        return []
    
class ActionAskProductOrder(Action):
    def name(self):
        return "action_ask_product_order"

    def run(self, dispatcher, tracker, domain):
        print("action_ask_product_order")
        tracker.slots["previous_action"] = "action_ask_product_order"

        try:
            product_order = tracker.get_slot("product_order")
            order = CommonFunction.resolve_product_order(product_order)
            previous_actions = []
            for event in tracker.events:
                if event.get('event') == 'action':
                    previous_actions.append(event.get('name'))
            action = CommonFunction.get_previous_action(previous_actions)
            
            if action is None or order is None:
                dispatcher.utter_message(
                    response="utter_dont_know_product"
                )
            else:
                print("action: ",action)
                start_price = tracker.get_slot("start_price")
                end_price = tracker.get_slot("end_price")
                print(start_price)
                print(end_price)
                product = CommonFunction.get_product_by_action(action, order, start_price, end_price)
                
                print("product get:", product)
                product_detail_list[tracker.sender_id] = product[1]
                dispatcher.utter_message(
                    response="utter_ask_product_detail",
                    name = product[1],
                    price = CommonFunction.change_money(product[4]),
                    description = product[3],
                    image = product[7]
                )
                dispatcher.utter_message(
                    image = product[8]
                )
                dispatcher.utter_message(
                    image = product[9]
                )
                dispatcher.utter_message(
                    image = product[10]
                )
        except:
            dispatcher.utter_message(
                response="utter_error"
            )
        return []


# Thông tin sản phẩm---------End-------------


# Mua hàng---------Start-------------

class ActionBuyProduct(Action):
    def name(self):
        return "action_buy_product"

    def run(self, dispatcher, tracker, domain):
        print("action_buy_product")
        tracker.slots["previous_action"] = "action_buy_product"

        try:
            buy_product = tracker.get_slot("buy_product")
            print("buy product: ", buy_product)
            user_id = tracker.sender_id
            if not buy_product is None:
                product_name = CommonFunction.get_product_correct_name(buy_product)
                
                product = DB.get_product_by_name(product_name)
                print(product)
                
                DB.change_order_status(user_id, product[0][0])
                tracker.slots["buy_product"] = None
            user = DB.get_user(user_id)
            print("user buy product: ",user)

            if user[6] == 0:
                print("return")
                return []
            
            if user[1] is None or len(user[1])<1:
                print("utter_ask_cumtomer_name")
                dispatcher.utter_message(
                    response= "utter_ask_cumtomer_name"
                )
            elif user[4] is None or len(user[4])<1:
                print("utter_ask_cumtomer_phone")
                dispatcher.utter_message(
                    response= "utter_ask_cumtomer_phone"
                )
            else:

            # elif user[5] is None or len(user[5])<1:
            #     print("utter_ask_cumtomer_address")
            #     dispatcher.utter_message(
            #         response= "utter_ask_cumtomer_address"
            #     )
            
                dispatcher.utter_message(
                        text = "Bạn" + user[1] + " đã đặt hàng thành công, \n Hàng sẽ được gửi về địa chỉ " + user[5]+" trong vài ngày tới \n Bạn chú ý nghe máy nhé"
                    )

            if DB.order_product(user_id) is None:
                dispatcher.utter_message(
                    text = "Đã đặt hàng thành công"
                )
            else:
                dispatcher.utter_message()
        except:
            dispatcher.utter_message(
                response="utter_error"
            )
        return []

class ActionProductDetail(Action):
    def name(self):
        return "action_product_detail"

    def run(self, dispatcher, tracker, domain):
        print("action_product_detail")
        tracker.slots["previous_action"] = "action_product_detail"

        try:

            latest_message = tracker.latest_message
            entities = latest_message['entities']
            print("message: ",latest_message)
            print("entities: ",entities)
            product_detail = entities[0]['value']
            print("product detail: ", product_detail)

            product_name = CommonFunction.get_product_correct_name(product_detail)
            
            product = DB.get_product_by_name(product_name)
            product_detail_list[tracker.sender_id] = product[0][1]
            print(product_detail_list[tracker.sender_id])
            if product:
                dispatcher.utter_message(
                    response="utter_ask_product_detail",
                    name = product[0][1],
                    price = CommonFunction.change_money(product[0][4]),
                    description = product[0][3],
                    image = product[0][7]
                )
                dispatcher.utter_message(
                    image = product[0][8]
                )
                dispatcher.utter_message(
                    image = product[0][9]
                )
                dispatcher.utter_message(
                    image = product[0][10]
                )
            else:
                dispatcher.utter_message(
                    response="utter_not_have_product_detail",
                    name = product_detail
                )
        except:
            dispatcher.utter_message(
                response="utter_error"
            )

        return []

class ActionCancleBuyProduct(Action):
    def name(self):
        return "action_cancle_buy_product"

    def run(self, dispatcher, tracker, domain):
        print("action_cancle_buy_product")
        tracker.slots["previous_action"] = "action_cancle_buy_product"
        
        dispatcher.utter_message(
            text = "Đã hủy mua áo thun dây rút tay ngắn"
        )

        return []

class ActionAskSize(Action):
    def name(self):
        return "action_ask_size"

    def run(self, dispatcher, tracker, domain):
        print("action_ask_size")
        tracker.slots["previous_action"] = "action_ask_size"

        print(product_detail_list[tracker.sender_id])
        product = DB.get_product_by_name(product_detail_list[tracker.sender_id])
        dispatcher.utter_message(
            response= "utter_ask_size",
            image=product[0][10]
        )

        return []

class ActionAskOtherProduct(Action):
    def name(self):
        return "action_ask_other_product"

    def run(self, dispatcher, tracker, domain):
        print("action_ask_other_product")

        previous_action = tracker.get_slot("previous_action")
        dispatcher.utter_message(
            response= "utter_ask_size"
        )

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
        if DB.get_user_name(user_id) == None:
            DB.insert_info(user_id,first_name,"","")
        else:
            DB.update_info(user_id, first_name, "","")

        print("Đã lưu tên")

        return []
    
class ActionSavePhone(Action):
    def name(self) -> Text:
        return "action_save_phone"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print("action_save_phone")
        tracker.slots["previous_action"] = "action_save_phone"
        
        phone = tracker.get_slot("phone")
        user_id = tracker.sender_id
        DB.update_phone(user_id,phone)

        print("Đã lưu số điện thoại")
        ActionBuyProduct.run(self, dispatcher=dispatcher, tracker=tracker, domain=domain)
        return []
    
class ActionSaveAddress(Action):
    def name(self) -> Text:
        return "action_save_address"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print("action_save_address")
        tracker.slots["previous_action"] = "action_save_address"
        
        user_mesage = tracker.latest_message.get('text').lower()
        user_id = tracker.sender_id
        DB.update_address(user_id,user_mesage)

        print("Đã lưu địa chỉ")

        ActionBuyProduct.run(self,dispatcher=dispatcher, tracker=tracker, domain=domain)
        return []
    
class ActionAskCustomerName(Action):
    def name(self) -> Text:
        return "action_ask_customer_name"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        user_id = tracker.sender_id
        user_name = DB.get_user_name(user_id)

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
        
        DB.create_database()
        dispatcher.utter_message("Đã tạo DB")

        return []
    
# hàm common