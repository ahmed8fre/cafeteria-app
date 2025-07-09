
class Account():
    '''تمثيل الحسابات في الذاكره'''
    def __init__(self ,name ,id ,email ,phone_num ,image ,orders):
        self.name = name
        self.id = id
        self.email = email
        self.phone_num = phone_num 
        self.image = image
        self.orders = orders
class Order:
    '''حاويه عناصر الطلب وبياناته'''
    def __init__(self ,id ,sender_id ,orders ,time ,status,icon,location ,cash):
        self.id = id #معرف الطلب
        self.sender_id = sender_id # معرف المرسل
        self.orders = orders #عناصر الطلب
        self.time = time # وقت الطلب
        self.total_price = 0 # السعر الاجمالي للطلب
        self.status = status #حاله الطلب "قي المطبخ او قيد التوصيل"
        self.icon = icon # ايقونه تمثل حاله الطلب
        self.location = location # موقع المرسل
        self.cash = cash
        self.Total_price()
    def Total_price(self):
        '''تعيين السعر الاجمالي من قائمه الطلبات'''
        price = 0
        for order in self.orders:
            price += order.price * order.number
        self.total_price = price
class Item:
    '''عنصر في الطلب'''
    def __init__(self ,id  ,title  ,image ,price ,number ,sauce ,pickle ,vegetable ,types ,groups):
        self.id = id
        self.title = title
        self.image = image
        self.price = price
        self.number = number
        self.sauce = sauce
        self.pickle = pickle
        self.vegetable = vegetable
        self.types = self.retypes(types)
        self.groups = groups
    def retypes(self,types):
        '''اعاده تعديل القائمه المدخله لتناسب وظع التصميم'''
        new_types = {}
        num = 0
        for key ,value in types.items():
            num += 1
            new_types[num] = key
            new_types[f'check{num}'] = False
            new_types[f'value{num}'] = value
        return new_types

class Product:
    '''بيانات المنتج'''
    def __init__(self,id,title ,image ,price ,sauce ,vegetable ,pickle ,types ,groups):
        self.id = id
        self.title = title
        self.image = image
        self.price = price
        self.sauce = sauce
        self.pickle = pickle
        self.vegetable = vegetable
        self.types = self.retypes(types)
        self.groups = groups
    def retypes(self,types):
        '''اعاده تعديل القائمه المدخله لتناسب وظع التصميم'''
        new_types = {}
        num = 0
        for key ,value in types.items():
            num += 1
            new_types[num] = key
            new_types[f'check{num}'] = False
            new_types[f'value{num}'] = float(value)
        return new_types

class Delivery:
    '''طلبات التوصيل'''
    def __init__(self,cash,price,time):
        self.cash = cash
        self.price = price
        self.time = time