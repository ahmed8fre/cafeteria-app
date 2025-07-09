import sqlite3
import socket
import threading
import pickle
import datetime
from libs.materials.classes import *
from kivy.clock import Clock
class Client():
    '''in order to deal with the customer directly'''   
    def __init__(self ,conn ,adrr ):
        self.conn = conn
        self.adrr = adrr

class DBM : 
    '''مدير البيانات'''
    def __init__(self ,core):
        self.core = core
        self.orders = {}
        self.products = {}
        self.delivery = {}
        self.rady_to_send =[]
        self.my_account = True
        self.path = "assets/data/db.db"
        self.create_database()
        self.Server_init()
    
    def create_database(self):
        """Create the database and table if they do not exist."""
        conn = sqlite3.connect(self.path)
        cr = conn.cursor()
        cr.execute('''
            CREATE TABLE IF NOT EXISTS work_days (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                day TEXT NOT NULL,
                status TEXT NOT NULL,
                over_time TEXT NOT NULL,
                note TEXT NOT NULL,
                withdraw TEXT NOT NULL
                )
        ''')
        conn.commit()
        conn.close()
    def Server_init(self):
        '''تهيئه السيرفر'''
        PORT = 5050
        HOST = '0.0.0.0'#socket.gethostbyname(socket.gethostname())
        ADDR = (HOST ,PORT)
        print(HOST)
        self.server = socket.socket(socket.AF_INET ,socket.SOCK_STREAM)
        self.server.bind(ADDR)
        self.HEADERSIZE = 64
        self.Clients = []        
    def sender(self,data ): 
        '''for shear data '''
        print(len(self.Clients))
        for client in self.Clients:
            try:
                pickle_login = pickle.dumps(data)
                msg_len = len(pickle_login)
                header = f'{msg_len:<{self.HEADERSIZE}}'.encode('utf-8')

                # Check if header length matches HEADERSIZE, crucial for receiving
                if len(header) != self.HEADERSIZE:
                    print(f"Warning: Header size mismatch for client {client.addr}. Expected {self.HEADERSIZE}, got {len(header)}")
                    continue # Skip this client
                pickle_login = bytes(f'{len(pickle_login):<{self.HEADERSIZE}}','utf-8') + pickle_login
                client.conn.sendall(pickle_login)
                print(f'send to {client.conn}')
            except (BrokenPipeError, ConnectionResetError) as e:
                print(f"Error sending to client {client.adrr}: {e} (Client disconnected)")
                # clients_to_remove.append(client) # Mark client for removal
            except Exception as e:
                print(f"An unexpected error occurred while sending to {client.adrr}: {e}")
                # clients_to_remove.append(client) # Consider removing on unexpected errors too

        print('sender is end !')
    def reciveing(self,conn ,adrr ,client):
        '''for recive data from clients for manage and shear data ,orders'''
        print(f'we are reciveing from [{conn}]')
        self.Clients.append(client)
        new_data = True
        full_data =b''
        while True :
            try:
                data = conn.recv(1024)
                if new_data:
                    data_len = int(data[:self.HEADERSIZE])
                    new_data = False
                full_data += data
                if len(full_data) - self.HEADERSIZE == data_len:
                    D = pickle.loads(full_data[self.HEADERSIZE:])
                    
                    full_data = b''
                    new_data = True
                    print(D)
                    if isinstance(D,Order):
                        D.id = len(self.orders)
                        self.orders[D.id+1] = D
                        Clock.schedule_once(lambda dt:self.core.wm.current_screen.add_orders(), 0)
                        # معالجة البيانات ...
            except : # استثناء قد يحدث عند محاولة الكتابة أو القراءة
                print(f"Client {conn} forcibly disconnected.")
            
                print('the client is kiked out')
                if client in self.Clients:
                    self.Clients.pop(self.Clients.index(client))
                conn.close() 
                
                break
    def new_client(self ,conn):
        '''تزويد المتصل الجديد بالبيانات'''
        for key , pr in self.products.items():
            pickle_login = pickle.dumps(pr)
            pickle_login = bytes(f'{len(pickle_login):<{self.HEADERSIZE}}','utf-8') + pickle_login
            conn.send(pickle_login)
    def reciver(self):
        '''for connect with clients'''
        self.server.listen()
        id = 0
        print('sever is listeningn')
        while True:
            conn ,adrr = self.server.accept()
            print('\n\n'+' *-* '*30+f'\nnew connection to this server [{adrr}]\n'+'* '*50)
            # Clients.append(Client(conn ,adrr))
            id += 1
            # self.new_client(conn)

            thread_reciving = threading.Thread(target=self.reciveing, args=(conn ,adrr , Client(conn,adrr),))
            thread_reciving.start()
           