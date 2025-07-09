from kivy.uix.accordion import ObjectProperty ,StringProperty ,NumericProperty ,BooleanProperty ,ListProperty ,DictProperty
from kivy.animation import Animation
from kivymd.uix.card import MDCard
from kivymd.uix.button import MDIconButton
from kivy.animation import Animation
from kivymd.uix.scrollview import MDScrollView
from kivy.uix.label import Label
from kivy.properties import *

class Post(MDCard):
    image = StringProperty()
    data = ObjectProperty()
    price = NumericProperty()
    title = StringProperty()
class Float_notice(MDCard):
    text = StringProperty()
    screen = ObjectProperty()
class Float_notice_icon(MDCard):
    text = StringProperty()
    screen = ObjectProperty()

class AppDrop(MDCard):
    valu = False

    def check(self):
        if self.valu:
            self.on_close()
            self.valu = False
        else:
            self.on_open()
            self.valu = True
    def on_open(self):
        Animation(
            duration = .7, 
            # size_hint_x = 0.9,
            pos_hint= {'center_y': 0.85 }
        ).start(self)
        

    def on_close(self):
        
        Animation(
            duration = .7,
            # size_hint_x = 0.9,
            pos_hint= {'center_y': 1.5}
        ).start(self)
class MyScroll(MDScrollView):
    pass
    # def on_scroll_start(self, touch, check_children=True):
    #     # print(self.scroll_y)
    #     if self.scroll_y > 1:
    #         print('update!')
    #     elif self.scroll_y < 0:
    #         print('more!')
        # return super().on_scroll_start(touch, check_children)
class MDARLabel(Label):
    """الخط العربي"""
class Cart_card(MDCard):
    '''كرت عربه التسوق'''
    total_price = NumericProperty()

class Delivery_item_card(MDCard):
    '''كرت عرض العناصر داخل قسم التوصيل'''
    cash = BooleanProperty(True)
    time = StringProperty('15')
    price = NumericProperty(43)
    icon = StringProperty('assets/images/chef.png')
    data = ObjectProperty()
class Delivery_card(MDCard):
    '''كرت قسم التوصيلات'''
class Account_card(MDCard):
    '''كرت عرض الحساب'''
class Custom_button(MDCard):
    '''زر مخصص
    مثل المستخدم في تحديد  خيارات اخرى للمنتج اثناء عرضه
    '''
    title = StringProperty()
    num=NumericProperty
    link_with = ListProperty()
    status = BooleanProperty()
class ProductCard(MDCard):
    '''كرت لعرض محتوى المنتج'''
    image=StringProperty()
    title=StringProperty()
    price=NumericProperty(1)
    number=NumericProperty(1)
    sauce=NumericProperty(1)
    pickle=BooleanProperty(True)
    vegetable=BooleanProperty(True)
    data=ObjectProperty()
    types = DictProperty() 
    groups = ListProperty()
    basic_price = NumericProperty()
    buttons = ListProperty()
    def add_buttons(self):
        buttons = ['one','tow','three','four']
        for buton in buttons:
            button = self.ids[buton]
            if button.num in self.types:
                button.title=str(self.types[button.num])
                for lnk in self.groups:
                    if button.num in lnk:
                        button.link_with = lnk
                if self.types[f'check{button.num}']:
                    button.md_bg_color = [0.7,0.7,0.7,0.9]
                    button.rgb = [0.2, 0.2, 0.2, 0.3]
                else:
                    button.md_bg_color= [0.2,0.2,0.2,0.5] 
                    button.rgb= 0.7, 0.7, 0.7, 0.2
                self.buttons.append(button)
            else:
                self.ids['float_prodect'].remove_widget(button)
       
    def check(self,item):
        '''تحديد وظائف الازرار بنائا على الاقسام الخاصه بها '''
                     
        
        for button in self.buttons:
            if button == item:
                if self.types[f'check{button.num}']:
                    
                    button.md_bg_color = [0.2,0.2,0.2,0.5]
                    button.rgb = 0.7, 0.7, 0.7, 0.2
                    self.types[f'check{button.num}'] = False
                else:
                    
                    button.md_bg_color = [0.7,0.7,0.7,0.9]
                    button.rgb = [0.2, 0.2, 0.2, 0.3]
                    self.types[f'check{button.num}'] = True
            elif button.num in item.link_with:
                button.md_bg_color = [0.2,0.2,0.2,0.5]
                button.rgb = 0.7, 0.7, 0.7, 0.2
                self.types[f'check{button.num}'] = False
        self.price = self.data.price
        for button in self.buttons:
            if self.types[f'check{button.num}']:
                self.price = self.price * float(self.types[f'value{button.num}'])
                
            
        

        self.data.types = self.types
        
class Card_card_item(MDCard):
    '''الكرت الذي يعرض العناصر في السله'''
    image = StringProperty('assets/images/beef burger.png')
    number = NumericProperty(5)
    price = NumericProperty(6)
    data=ObjectProperty()
class Mang_order_card(MDCard):
    '''كرت منبثق لتوجيه الطلبات'''
    card = ObjectProperty()#الكرت الاب في الشاشه الرئيسيه الخاص بعرض هذا النوع من المحتوى
    data = ObjectProperty()
    total_price = NumericProperty()
    disabled_chef_button = BooleanProperty(False)
    