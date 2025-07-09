from kivy.config import Config
Config.set('graphics', 'fullscreen', 'auto') 

import kivy 
from kivy.app import App
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager ,FadeTransition
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.utils import platform
#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-
import webbrowser
import random
import threading
import datetime
#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-
from libs.widgets.widgets import Post ,Float_notice  ,Cart_card ,Delivery_card ,Account_card ,ProductCard
from libs.widgets.widgets import Card_card_item ,Delivery_item_card ,Custom_button ,Mang_order_card
from libs.materials.classes import Order ,Product ,Delivery ,Item
from libs.materials.DBM import DBM 

# Config.set('graphics', 'multisamples', '0')
# Config.set('graphics', 'width', '360')
# Config.set('graphics', 'height', '640')
class WindowManager(ScreenManager):
    '''الشاشه الام للبرنامج '''
    
class Start(MDScreen):
    '''شاشه التحميل(بدء التشغيل)'''
    note = 'checking your account ..! '
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(lambda dt: self.change_note(), 2)
    def change_note(self):
        self.ids['note'].text = 'You will be redirected to \nthe next page after verification.'
class SignIn(MDScreen):
    '''شاشه انشاء حساب'''
    def change_enter_button_pos(self,name ,email ,passowrd ,v_passowrd):
        '''تغيير موقع زر الادخال في حال كان هناك خانه ناقصه'''
        if name and "@" in email and "." in email and passowrd and passowrd == v_passowrd:
            self.ids['enter_button_helper'].text = 'signup'
        else:
            self.ids['enter_button_helper'].pos_hint = self.ids['enter_button'].pos_hint
            self.ids['enter_button'].pos_hint = {'center_x':round(random.uniform(0.2, .8), 3),'center_y':round(random.uniform(0.1, 0.4), 3)}
            self.ids['enter_button_helper'].text = 'Check the input process ...!'
            if self.ids['login_button'].pos_hint != {'center_y': 0.95 ,'center_x':0.17}:
                Animation(
                    duration = .7,
                    # size_hint_x = 0.9,
                    pos_hint= {'center_y': 0.05 ,'center_x':0.17}
                ).start(self.ids['login_button'])
                Animation(
                    duration = .7,
                    # size_hint_x = 0.9,
                    pos_hint= {'center_y': 0.1 ,'center_x':0.17}
                ).start(self.ids['login_button_helper'])
                Animation(
                    duration = .7,
                    # size_hint_x = 0.9,
                    pos_hint= {'center_y': 0.05 ,'center_x':0.83}
                ).start(self.ids['visitor_button'])
                Animation(
                    duration = .7,
                    # size_hint_x = 0.9,
                    pos_hint= {'center_y': 0.1 ,'center_x':0.83}
                ).start(self.ids['visitor_button_helper'])
class LogIn(MDScreen):
    '''شاشه تسجيل الدخول'''
    def change_enter_button_pos(self,email ,passowrd ):
        '''تغيير موقع زر الادخال في حال كان هناك خانه ناقصه'''
        if "@" in email and "." in email and passowrd :
            self.ids['login_button_helper'].text = 'LogIn'
        else:
            self.ids['login_button_helper'].pos_hint = self.ids['login_button'].pos_hint
            self.ids['login_button'].pos_hint = {'center_x':round(random.uniform(0.2, .8), 3),'center_y':round(random.uniform(0.1, 0.4), 3)}
            self.ids['login_button_helper'].text = 'Check the input process ...!'
            if self.ids['signin_button'].pos_hint != {'center_y': 0.9 ,'center_x':0.17}:
                Animation(
                    duration = .7,
                    # size_hint_x = 0.9,
                    pos_hint= {'center_y': 0.8 ,'center_x':0.17}
                ).start(self.ids['signin_button'])
                Animation(
                    duration = .7,
                    # size_hint_x = 0.9,
                    pos_hint= {'center_y': 0.85 ,'center_x':0.17}
                ).start(self.ids['signin_button_helper'])
                Animation(
                    duration = .7,
                    # size_hint_x = 0.9,
                    pos_hint= {'center_y': 0.8 ,'center_x':0.83}
                ).start(self.ids['visitor_button'])
                Animation(
                    duration = .7,
                    # size_hint_x = 0.9,
                    pos_hint= {'center_y': 0.85 ,'center_x':0.83}
                ).start(self.ids['visitor_button_helper'])
class Home(MDScreen):
    '''الواجه الرئيسيه للبرنامج'''
    def __init__(self, **kw):
        super().__init__(**kw)
        self.app = App.get_running_app()
        self.add_products()
        self.add_orders()
    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.app.remove_widgets(self,self.app.notes_on_screen)

        
        return super().on_touch_down(touch)
    def move_card_item(self ,old,card):
        old.remove_widget(card)
        if old == self.ids['Received_items']:
            self.ids['orders_items'].add_widget(card)
        elif old == self.ids['orders_items']:
            self.ids['Received_items'].add_widget(card)
    def add_mang_order_card(self ,data ,card):
        '''اظافه الكرت الخاص بمتابعه الطلبات وعرض محتواها'''
        order = Mang_order_card()
        order.card = card
        order.data = data
        if data.status == 'kitchened':
            order.disabled_chef_button = True
        for item in data.orders:
            item_card = Card_card_item()
            item_card.image = item.image
            item_card.price = item.price
            item_card.number = item.number
            item_card.data = item
            order.total_price += item.price * item.number
            order.ids['orders_items'].add_widget(item_card)
        self.ids['home_float'].add_widget(order)
        
            
    def add_orders(self):
        '''اظافه الطلبات الى القوائم المخصصه لها'''
        self.ids['Received_items'].clear_widgets()
        self.ids['orders_items'].clear_widgets()
        for key ,value in self.app.DBM.orders.items():
            order = Delivery_item_card()
            order.icon = value.icon
            order.time = str(value.time)
            order.price = value.total_price
            order.cash = value.cash
            order.data = value
            if value.status == 'Received':
                self.ids['Received_items'].add_widget(order)
            elif value.status == 'kitchened':
                
                self.ids['orders_items'].add_widget(order)
    def add_products(self):
        '''اظافه بطاقات المنتجات الى الواجهه الرئيسيه'''
        for key ,item in self.app.DBM.products.items():
            card = Post()
            card.data = item
            card.image = item.image
            card.title = item.title
            card.price = item.price
            self.ids['home_scrol'].add_widget(card)
    def add_productcard(self ,data,number):
        '''اظافه بطاقه عرض تفاصيل المنتج'''
        for wid in self.ids['home_float'].children:
            if isinstance(wid,ProductCard):
                self.remove_wid(wid)
        productcard = ProductCard()
        productcard.data = data
        productcard.image = data.image
        productcard.title = data.title
        productcard.price = data.price
        productcard.types = data.types
        productcard.number = number
        productcard.sauce = data.sauce
        productcard.vegetable = data.vegetable
        productcard.pickle = data.pickle
        productcard.groups = data.groups
        productcard.add_buttons()
        self.ids['home_float'].add_widget(productcard)
    def add_Cart_card(self):
        '''اظافه عربه التسوق الى الشاشه'''
        for wid in self.ids['home_float'].children:
            if isinstance(wid,Cart_card) :
                self.remove_wid(wid)
        crat_card = Cart_card()
        for key ,item in self.app.DBM.orders.items():
            new_item = Card_card_item()
            new_item.data = item
            new_item.image = item.image
            new_item.price = item.price
            new_item.number = item.number
            crat_card.total_price += new_item.number * new_item.price
            crat_card.ids['cart_card_items'].add_widget(new_item)
        self.ids['home_float'].add_widget(crat_card)
    def add_delivery_card(self):
        '''اظافه معرض التوصيل الى الشاشه'''
        for wid in self.ids['home_float'].children:
            if  isinstance(wid,Delivery_card) :
                self.remove_wid(wid)
        delivery_card = Delivery_card()
        for key ,value in self.app.DBM.delivery.items():
            deli = Delivery_item_card()
            deli.price = value.price
            deli.cash = value.cash
            deli.time = value.time
            delivery_card.ids['delivery_card_items'].add_widget(deli)
        
        self.ids['home_float'].add_widget(delivery_card)
    def add_account_card(self):
        '''اظافه معرض الحساب الى الشاشه'''
        for wid in self.ids['home_float'].children:
            if isinstance(wid ,Account_card) :
                self.remove_wid(wid)
        account_card = Account_card()
        self.ids['home_float'].add_widget(account_card)
    def add_order(self,data,price,number,sauce,vegetable,pickle,types):
        time='tody'
        order = Order(len(self.app.DBM.orders)+1,'00000001',data.title,time,data.image,price,number,sauce,pickle,vegetable,types,data.groups)
        self.app.DBM.orders[order.id]=order
    def remove_wid(self,wid):
        '''ازاله عناصر من الشاشه'''
        self.ids['home_float'].remove_widget(wid)
    def add_delivery_order(self,cash,price):
        '''اظافه طلب الى قائمه التوصيل'''
        current_time = datetime.datetime.now()
        # تنسيق الوقت للحصول على الساعة والدقائق مع AM/PM
        # %I: الساعة بنظام 12 ساعة (01-12)
        # %M: الدقائق (00-59)
        # %p: مؤشر AM/PM
        formatted_time = current_time.strftime("%I:%M %p")
        self.app.DBM.sender(Delivery(bool(cash),float(price),str(formatted_time)))
    def add_product_data(self,title,image,price,types ,groups):
        '''اظافه عنصر الى قائمه الطعام'''
        try:
            import ast
            if groups:
                groups = [ast.literal_eval(groups)]
            else:
                groups = []
            for key,value in list(types.items()):
                if key == '' or value == '':
                    del types[key]
                
            product = Product(len(self.app.DBM.products),title,image,float(price),1,False,False,types,groups)
            self.app.DBM.products[product.id] = product
            card = Post()
            card.data = product
            card.image = product.image
            card.title = product.title
            card.price = product.price
            self.ids['home_scrol'].add_widget(card)
        
            sender_thread = threading.Thread(target=self.app.DBM.sender, args=(product,))
            sender_thread.daemon = True # يجعل الخيط خيطًا ثانويًا (daemon thread)
                                    # بحيث ينتهي عند إغلاق التطبيق الرئيسي
            sender_thread.start() # يبدأ تنفيذ الخيط
            print('run a "sender" [def]')
        except:
            self.app.PopupfloatNotice(self,'cant add this !')
    
        # self.ids['home_scrol'].clear_widgets()
        # self.add_products()
    def remove_product(self,product):
        for wid in self.ids['home_scrol'].children:
            if wid.data == product:
                self.ids['home_scrol'].remove_widget(wid)
class Connect(MDScreen):
    '''للتواصل'''
class Main(MDApp):
    def build(self):
        self.theme_cls.theme_style = 'Dark'
        self.theme_cls.primary_palette = 'Teal'
        self.theme_cards = [.5,.5,.5,.5 ]
        self.theme_cls.accent_palette = 'Teal'
        self.theme_cls.accent_hue = '400'
        self.title = "MANZEL"
        self.load_all_kv_file()
        self.DBM = DBM(self)
        thread_reciver = threading.Thread(target=self.DBM.reciver)
        thread_reciver.daemon = True 
        thread_reciver.start()
        # self.add_data()
        self.notes_on_screen = []
        self.wm = WindowManager(transition=FadeTransition())
        screens = [
            Start(name='start-sc'),Home(name = 'home-sc'),Connect(name = 'connect-sc'),SignIn(name='signin-sc'),LogIn(name='login-sc')
        ]
        for screen in screens:
            self.wm.add_widget(screen)
        self.check_acount()
        
        return self.wm
    def check_acount(self):
        '''التحقق من وجود حساب 
        محاوله تسجيل الدخول بالحساب الى السيرفر
        تبديل الصفحات بنائاً على ذلك'''
        if self.DBM.my_account:
            Clock.schedule_once(lambda dt: self.change_screen('home-sc'), 4)
        else:
            Clock.schedule_once(lambda dt: self.change_screen('signin-sc'), 4)
        
    def change_screen(self ,screen):
        '''الداله المسؤوله عن تغغير الشاشه الحاليه'''
        self.wm.current = screen
            
    def load_all_kv_file(self):
        '''تحميل الصفحات والتصاميم'''
        Builder.load_file('libs/widgets/widgets.kv')
        Builder.load_file('libs/pages/home.kv')
        Builder.load_file('libs/pages/start.kv')
        Builder.load_file('libs/pages/signin.kv')
        Builder.load_file('libs/pages/login.kv')
        # Builder.load_file('libs/pages/connect.kv')
    def PopupfloatNotice(self ,screen ,notice ):
        '''لإظهار الإشعارات في اعلى الشاشه'''
        
        notic = Float_notice()
        notic.text = notice
        self.notes_on_screen.append(notic)
        screen.add_widget(notic)
        Clock.schedule_once(lambda dt: self.remove_widgets(screen,self.notes_on_screen), 4)
    def remove_widgets(self ,screen ,widget):
        if isinstance(widget,list) :
            for wid in widget:
                screen.remove_widget(wid)
        else:
            screen.remove_widget(widget)
    def open_whatsapp_link(self, url):
        """فتح المتصفح"""
        if platform == 'android':
            from jnius import autoclass
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            Intent = autoclass('android.content.Intent')
            Uri = autoclass('android.net.Uri')
            intent = Intent(Intent.ACTION_VIEW, Uri.parse(url))
            PythonActivity.mActivity.startActivity(intent)
        else:
            # للتشغيل على سطح المكتب (Windows/Linux/macOS)
            
            webbrowser.open(url)
    def add_data(self):
        self.DBM.products[1]= Product(1,'beef burger','assets/images/beef burger.png',15,1,True,False,{'small':0.8,'Medium':1,'Larg':1.2},[[1,2,3]])
        self.DBM.products[2]= Product(2,'zenjer','assets/images/zenjer.png',8,1,False,True,{'Small':0.8,'Medium':1,'Larg':1.2 ,'Double':2},[[1,2,3]])
        self.DBM.products[3]= Product(3,'shaworma','assets/images/shaworma (1).png',12,1,True,False,{'small':0.8,'Medium':1,'Larg':1.2},[[1,2,3]])
        self.DBM.products[4]= Product(4,'Cheeseburger','assets/images/cheken burgar.png',9,1,False,True,{'small':0.8,'Medium':1,'Larg':1.2},[[1,2,3]])
        self.DBM.products[5]= Product(5,'Meat Platter ','assets/images/mex.png',20,1,True,False,{'small':0.8,'Medium':1,'Larg':1.2},[[1,2,3]])
        self.DBM.products[6]= Product(6,'Shish Taouk','assets/images/mex2.png',14,1,True,False,{'small':0.8,'Medium':1,'Larg':1.2},[[1,2,3]])
        self.DBM.products[7]= Product(7,'pizza','assets/images/pizza.png',11,1,True,False,{'small':0.8,'Medium':1,'Larg':1.2},[[1,2,3]])
        self.DBM.products[8]= Product(8,'Shish Taouk    ','assets/images/vecteezy.png',13,1,True,False,{'small':0.8,'Medium':1,'Larg':1.2},[[1,2,3]])
        self.DBM.products[9]= Product(9,'Beef Burger','assets/images/burger.png',14,1,True,False,{'small':0.8,'Medium':1,'Larg':1.2},[[1,2,3]])
        self.DBM.orders[1] = Order(1,1,[Item(1,'shaworma','assets/images/shaworma (1).png',13,2,2,True,False,{'small':0.8,'Medium':1,'Larg':1.2},[[1,2,3]])],'3:15 PM','Received','assets/images/chef.png','abudhabi-shamkha-14-16',False)
        self.DBM.orders[2] = Order(2,1,[Item(1,'shaworma','assets/images/shaworma (1).png',13,2,2,True,False,{'small':0.8,'Medium':1,'Larg':1.2},[[1,2,3]])],'3:15 PM','kitchened','assets/images/chef.png','abudhabi-shamkha-14-16',False)
        self.DBM.orders[3] = Order(3,1,[Item(1,'shaworma','assets/images/shaworma (1).png',13,2,2,True,False,{'small':0.8,'Medium':1,'Larg':1.2},[[1,2,3]])],'3:15 AM','Received','assets/images/chef.png','abudhabi-shamkha-14-16',False)
        self.DBM.orders[4] = Order(4,1,[Item(1,'shaworma','assets/images/shaworma (1).png',13,2,2,True,False,{'small':0.8,'Medium':1,'Larg':1.2},[[1,2,3]]),
                                        Item(1,'shaworma','assets/images/shaworma (1).png',13,2,2,True,False,{'small':0.8,'Medium':1,'Larg':1.2},[[1,2,3]]),
                                        Item(1,'shaworma','assets/images/shaworma (1).png',13,2,2,True,False,{'small':0.8,'Medium':1},[[1,2,3]]),
                                        
                                        ],'3:15 AM','kitchened','assets/images/chef.png','abudhabi-shamkha-14-16',False)
        
    def remove_order(self,order):
        if order == 'all':
            self.DBM.orders = {}
        else:
            del self.DBM.orders[order]
if __name__ == '__main__':
    thread_mainapp = threading.Thread(target=Main().run())
    