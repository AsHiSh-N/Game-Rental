import json
import string
import random
from json import JSONDecodeError
from datetime import datetime, date

def Register(type,gamers_json_file,sellers_json_file,Email_ID,Username,Password,Contact_Number):
    '''Register Function || Already Given'''
    if type.lower()=='seller':
        f=open(sellers_json_file,'r+')
        d={
            "Email":Email_ID,
            "Username":Username,
            "Password":Password,
            "Contact Number":Contact_Number,
        }
        try:
            content=json.load(f)
            if d not in content and d["Username"] not in str(content):
                content.append(d)
                f.seek(0)
                f.truncate()
                json.dump(content,f)
        except JSONDecodeError:
            l=[]
            l.append(d)
            json.dump(l,f)
        f.close()
        return True
    elif type.lower()=='gamer':
        f=open(gamers_json_file,'r+')
        d={
            "Email":Email_ID,
            "Username":Username,
            "Password":Password,
            "Contact Number":Contact_Number,
            "Wishlist":[],
            "Cart":[],
        }
        try:
            content=json.load(f)
            if d not in content and d["Username"] not in str(content):
                content.append(d)
                f.seek(0)
                f.truncate()
                json.dump(content,f)
        except JSONDecodeError:
            l=[]
            l.append(d)
            json.dump(l,f)
        f.close()

def Login(type,gamers_json_file,sellers_json_file,Username,Password):
    '''Login Functionality || Return True if successfully logged in else False || Already Given'''
    d=0
    if type.lower()=='seller':
        f=open(sellers_json_file,'r+')
    else:
        f=open(gamers_json_file,'r+')
    try:
        content=json.load(f)
    except JSONDecodeError:
        return False
    for i in range(len(content)):
        if content[i]["Username"]==Username and content[i]["Password"]==Password:
            d=1
            break
    f.seek(0)
    f.truncate()
    json.dump(content,f)
    f.close()
    if d==0:
        return False
    return True

def AutoGenerate_ProductID():
    '''Return a autogenerated random product ID || Already Given'''
    product_ID=''.join(random.choices(string.ascii_uppercase+string.digits,k=4))
    return product_ID

def AutoGenerate_OrderID():
    '''Return a autogenerated random product ID || Already Given'''
    Order_ID=''.join(random.choices(string.ascii_uppercase+string.digits,k=3))
    return Order_ID

def days_between(d1, d2):
    '''Calculating the number of days between two dates || Already Given'''
    d1 = datetime.strptime(d1, "%Y-%m-%d")
    d2 = datetime.strptime(d2, "%Y-%m-%d")
    return abs((d2 - d1).days)

def Create_Product(owner,product_json_file,product_ID,product_title,product_type,price_per_day,total_stock_available):
    '''Creating a product || Return True if successfully created else False'''
    '''Write your code below'''
    data = {
        "Seller Username": owner,
        "Product ID": product_ID,
        "Product Title": product_title,
        "Product Type": product_type,
        "Price Per Day": price_per_day,
        "Total Stock Available": total_stock_available
    }
    try:
        fp = open(product_json_file, "r+")
        content = json.load(fp)
        content.append(data)
        fp.seek(0)
        fp.truncate()
        json.dump(content, fp)
    except JSONDecodeError:
        l = []
        l.append(data)
        json.dump(l, fp)
    fp.close()
    return True

def Fetch_all_Products_created_by_seller(owner,product_json_file):
    '''Get all products created by the seller(owner)'''
    '''Write your code below'''
    All_Products_list=[]
    f=open(product_json_file,'r')
    try:
        content=json.load(f)
        All_Products_list=content
    except JSONDecodeError:
        pass
    return All_Products_list

def Fetch_all_products(products_json_file):
    '''Get all products created till now || Helper Function || Already Given'''
    All_Products_list=[]
    f=open(products_json_file,'r')
    try:
        content=json.load(f)
        All_Products_list=content
    except JSONDecodeError:
        pass
    return All_Products_list

def Fetch_Product_By_ID(product_json_file,product_ID):
    '''Get product deatils by product ID'''
    '''Write your code below'''
    fp = open(product_json_file, "r+")
    my_products = []
    try:
        content=json.load(fp)
        for i in content:
            if i["Product ID"] == product_ID:
                my_products.append(i)
    except JSONDecodeError:
        pass
    return my_products

def Update_Product(Username,product_json_file,product_ID,detail_to_be_updated,new_value):
    '''Updating Product || Return True if successfully updated else False'''
    '''Write your code below'''
    fp = open(product_json_file, "r+")
    data = json.load(fp)
    for i in data :
        if i["Seller Username"]==Username and i["Product ID"] == product_ID:
            i[detail_to_be_updated] = new_value
            fp.seek(0)
            fp.truncate()
            json.dump(data, fp)
            return True
    fp.close()
    return False

def Add_item_to_wishlist(Username,product_ID,gamers_json_file):
    '''Add Items to wishlist || Return True if added successfully else False'''
    '''Write your code below'''
    fp = open(gamers_json_file, "r+")
    data = json.load(fp)
    for i in data:
        if i["Username"] == Username:
            i["Wishlist"].append(product_ID)
            fp.seek(0)
            fp.truncate()
            json.dump(data, fp)
            return True
    fp.close()
    return False

def Remove_item_from_wishlist(Username,product_ID,gamers_json_file):
    '''Remove items from wishlist || Return True if removed successfully else False'''
    '''Write your code below'''
    fp = open(gamers_json_file, "r+")
    data = json.load(fp)
    for i in data:
        if i["Username"] == Username:
            i["Wishlist"].remove(product_ID)
            fp.seek(0)
            fp.truncate()
            json.dump(data, fp)
            return True
    fp.close()
    return False

def Add_item_to_cart(Username,product_ID,Quantity,gamers_json_file,booking_start_date,booking_end_date,products_json_file):
    '''Add item to the cart || Check whether the quantity mentioned is available || Return True if added successfully else False'''
    '''Add the Product ID, Quantity, Price, Booking Start Date, Booking End Date in the cart as list of dictionaries'''
    '''Write your code below'''
    f = open (products_json_file, "r")
    data = json.load(f)
    price = 0
    for i in data:
        if i["Product ID"] == product_ID and i["Total Stock Available"] >= Quantity:
            price = i["Price Per Day"]
            item_data = {
                "Product ID": product_ID,
                "Quantity": Quantity,
                "Price": price,
                "Booking Start Date": booking_start_date,
                "Booking End Date": booking_end_date
            }
            fp = open(gamers_json_file, "r+")
            data1 = json.load(fp)
            for i in data1:
                if i["Username"] == Username:
                    i["Cart"].append(item_data)
                    fp.seek(0)
                    fp.truncate()
                    json.dump(data1, fp)
                    return True
            fp.close()
    f.close()
    return False

def Remove_item_from_cart(Username,product_ID,gamers_json_file):
    '''Remove items from the cart || Return True if removed successfully else False'''
    '''Write your code below'''
    fp = open(gamers_json_file, "r+")
    data = json.load(fp)
    for i in data:
        if i["Username"] == Username:
            cart = i["Cart"]
            for x in range(len(cart)):
                if cart[x]["Product ID"] == product_ID:
                    i["Cart"].pop(x)
                    fp.seek(0)
                    fp.truncate()
                    json.dump(data, fp)
                    return True
    fp.close()
    return False

def View_Cart(Username,gamers_json_file):
    '''Return the current cart of the user'''
    '''Write your code below'''
    cart = []
    f = open(gamers_json_file, 'r')
    try:
        content = json.load(f)
        for i in content:
            if i["Username"] == Username:
                cart = i["Cart"]
    except JSONDecodeError:
        pass
    return cart

def Place_order(Username,gamers_json_file,Order_Id,orders_json_file,products_json_file):
    '''Place order || Return True is order placed successfully else False || Decrease the quantity of the product orderd if successfull'''
    '''Write your code below'''
    fp = open(gamers_json_file, "r")
    data = json.load(fp)
    cart_data = []
    fp.close()
    for i in data:
        if i["Username"] == Username:
            if len(i["Cart"]) == 0:
                return False
            else:
                cart_data = i["Cart"]
    no_of_days = []
    quan = []
    price = []
    for i in cart_data:
        quan.append(i["Quantity"])
        price.append(i["Price"])
        start_date = i["Booking Start Date"].split("-")
        end_date = i["Booking End Date"].split("-")
        date_1 = date(int(start_date[0]), int(start_date[1]), int(start_date[2]))
        date_2 = date(int(end_date[0]), int(end_date[1]), int(end_date[2]))
        num = (date_2 - date_1).days
        no_of_days.append(num)
        with open(products_json_file, "r") as fp1:
            product_data = json.load(fp1)
        for x in product_data:
            if x["Seller Username"] == Username:
                if x["Product ID"] == i["Product ID"]:
                    x["Total Stock Available"] = x["Total Stock Available"] - i["Quantity"]
                    with open(products_json_file, 'w') as fp8:
                        json.dump(product_data, fp8)

    total_price = 0
    for i in range(len(cart_data)):
        total_price += (price[i] * quan[i] * no_of_days[i])

    order_data = {
        "Order ID": Order_Id,
        "Ordered by": Username,
        "Items": cart_data,
        "Total Cost": total_price
    }

    try:
        with open(orders_json_file, "r+") as fp6:
            content = json.load(fp6)
            content.append(order_data)
    except JSONDecodeError:
        l = []
        l.append(order_data)
        with open(orders_json_file, "w+") as fp5:
            json.dump(l, fp5)
    else:
        with open(orders_json_file, "w+") as fp5:
            json.dump(content, fp5)
    for i in data:
        if i["Username"] == Username:
            i["Cart"] = []
            with open(gamers_json_file, "w+") as fp3:
                json.dump(data, fp3)
            return True
    return False

def View_User_Details(gamers_json_file,Username):
    '''Return a list with all gamer details based on the username || return an empty list if username not found'''
    '''Write your code below'''
    fp = open(gamers_json_file, "r+")
    my_products = []
    try:
        content = json.load(fp)
        for i in content:
            if i["Username"] == Username:
                my_products.append(i)
    except JSONDecodeError:
        pass
    return my_products

def Update_User(gamers_json_file,Username,detail_to_be_updated,updated_detail):
    '''Update the detail_to_be_updated of the user to updated_detail || Return True if successful else False'''
    '''Write your code below'''
    with open(gamers_json_file, "r+") as fp:
        data = json.load(fp)

    for i in data :
        if i["Username"]==Username :
            i[detail_to_be_updated] = updated_detail
            with open(gamers_json_file, "w") as fp1:
                json.dump(data, fp1)
            return True
    return False

def Fetch_all_orders(orders_json_file,Username):
    '''Fetch all previous orders for the user and return them as a list'''
    '''Write your code below'''
    all_orders = []
    with open(orders_json_file, "r") as fp:
        data = json.load(fp)
    for i in data:
        if i["Ordered by"] == Username:
            all_orders.append(i)
    return all_orders
    

