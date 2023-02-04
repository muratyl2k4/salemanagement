import tkinter as tk 
import sqlite3
from tkinter import ttk
from tkcalendar import DateEntry
from ctypes import windll
from datetime import datetime
windll.shcore.SetProcessDpiAwareness(1)
class Scrollbar():
    def __init__(self, parent , width , height):
        self.parent = parent
        # STEPS TO CREATE A SCROLLBAR
        # 1. Create A Main Frame in root
        self.main_frame = tk.Frame(self.parent , width=width , height=height)
        self.main_frame.pack(fill='both', expand=1)
        # 2. Create A Canvas in Main Frame
        self.my_canvas = tk.Canvas(self.main_frame , width=width , height=height)
        self.my_canvas.pack(side='left', fill='both', expand=1)
        # 3. Add A Scrollbar To The Canvas
        self.my_scrollbar = ttk.Scrollbar(self.main_frame, orient='vertical', command=self.my_canvas.yview)
        self.my_scrollbar.pack(side='right', fill='y')
        # 4. Configure The Canvas
        self.my_canvas.configure(yscrollcommand=self.my_scrollbar.set)
        # 5. Create ANOTHER Frame INSIDE the Canvas. 
        self.window = tk.Frame(self.my_canvas)
        # 6. Add that New frame To a Window In The Canvas
        self.my_canvas.create_window((0,0), window=self.window, anchor="nw", tags="windowTag")
        self.my_canvas.bind("<Configure>", self.onCanvasConfigure)
    def onCanvasConfigure(self, event):
        self.my_canvas.itemconfig('windowTag', width=self.my_canvas.winfo_width()) #resize the frame with double height of canvaz. The internal frame need to be larger than scrollregion(=canvas size) for scrollbar to be activated.
        # update scrollregion to the same size as the canvas
        self.my_canvas.configure(scrollregion = self.my_canvas.bbox("all"))



class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self._frame = None
        ##Main Settings 
        self.resizable(False , False)
        self.config(bg='black')
        photo = tk.PhotoImage(file = 'money.png')
        self.wm_iconphoto(False, photo)
        self.title('Kumluca Sanayi Lokantasi Muhasebe')

        self.switch_frame(Anasayfa)

    def switch_frame(self, frame_class):
        """Destroys current frame anda replaces it with a new one."""
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack(fill = 'both' , expand= 'yes')



class Anasayfa(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        ## Anasayfa Frame ayarlari
        swidth = self.winfo_screenwidth()-200
        sheight = self.winfo_screenheight()
        self.config(width=swidth , height=sheight)
        ##Navbar Canvas 
        navbar_canvas = tk.Canvas(self , bg='white' , width=swidth , height=sheight/3)
        navbar_canvas.pack(padx=10,pady=5 , fill='both')  
        navbar_frame = tk.Frame(navbar_canvas , bg='white')
        navbar_frame.place(relheight=1 , relwidth=1)
        
        ##Customer Canvas
        customer_canvas = tk.Canvas(self , bg='#222222',  width=int((swidth/4)) , height=int(sheight/3))
        customer_canvas.pack(padx=10,pady=5,anchor='s' , side='left')

        customer_payment_canvas = tk.Canvas(self , bg='white' , width=int(swidth/4*3) +10, height=int(sheight/3))
        customer_payment_canvas.pack(pady=10 , padx=10 , side='bottom' , anchor='s')
        customer_payment_frame = tk.Frame(customer_payment_canvas , bg='white')
        customer_payment_frame.place(relheight=1 , relwidth=1)

        #scrollbar for customer Canvas 
        
        db = sqlite3.connect('database.db')     
        cursor = db.cursor()   
        ##Activate foreign keys
        cursor.execute(""" PRAGMA foreign_keys = ON """)
        ##customer table
        cursor.execute('''CREATE TABLE IF NOT EXISTS customers(customer_id INTEGER PRIMARY KEY,customer_name TEXT)''')
        ##payment table 
        cursor.execute("""CREATE TABLE IF NOT EXISTS payment(customer INTEGER , message TEXT , date BLOB , payment FLOAT  , FOREIGN KEY(customer) REFERENCES customers(customer_id))""")

        #cursor.execute(f""" INSERT INTO payment (customer , message , date,  payment ) VALUES (1, '2s','2014/12/11',50.0) """)
        db.commit()
        ## ADD CUSTOMERS ON DATABASE
        def add_customer(textbox):
            value=textbox.get("1.0","end-1c")
            cursor.execute("select customer_name from customers")
            results = cursor.fetchall()
            cursor.execute(f""" INSERT or IGNORE INTO customers (customer_id , customer_name) VALUES ({len(results)+1}, '{value}') """)
            cursor.execute("select customer_name from customers")
            results = cursor.fetchall()
            results.reverse()
            db.commit()
            draw_customer(results)

        ##ADD PAYMENT    
        def add_payment(customerid ,message , date , payment):
            print(customerid , message , date , payment)
            cursor.execute(f""" INSERT INTO payment (customer , 'message' , 'date',  payment ) VALUES ({customerid}, {message}, '{date}' ,{float(payment)}) """)
            db.commit()
        #DRAW PAYMENTS TO SCREEN
        
        def draw_payment(customer_name):
            global Selectedcusid
            ###GET SELECTED CUSTOMERS ID 
            cursor.execute(f""" select customer_id from customers where customer_name = ? """ , (customer_name,))
            result = cursor.fetchone()
            Selectedcusid = result[0]
            cursor.execute(f""" select * from payment where customer = ? """ , (result[0],))
            resultp = cursor.fetchall()
            for i in resultp:
                print(i)
            
        
        ## DRAW CUSTOMERS TO SCREEN 
        def draw_customer(listee):
            for widget in customer_canvas.winfo_children():
                widget.destroy()
            scrollbar = Scrollbar(customer_canvas , width = int(customer_canvas.cget('width')) -50 , height=int(customer_canvas.cget('height')))
            
            for x in listee:
                for i in x:    
                    ttk.Button(scrollbar.window, text=i , width=100 , command=lambda x=i : draw_payment(x)).pack()

        ##get customers from database
        cursor.execute("select customer_name from customers")
        resultss = cursor.fetchall()
        resultss.reverse()    
        draw_customer(resultss)
        
        ## customer adding in new window 
        def add_customer_w():
            new= tk.Toplevel(master)
            new.geometry("750x250")
            new.title("Müşteri Ekleme")
            #Creating a text box widget
            my_text_box=tk.Text(new , font='Verdana 25 bold')
            my_text_box.place(relx= 0.1 , rely=0.1 , relwidth=0.8 , relheight=0.3)
            #Create a button for Comment
            comment= ttk.Button(new,text="Müşteri Ekle", command=lambda: add_customer(my_text_box))
            #command=get_input() will wait for the key to press and displays the entered text
            comment.place(relx= 0.1 , rely=0.4 , relwidth=0.8 , relheight=0.3)
        
            
        def add_payment_w():
            new= tk.Toplevel(master)
            new.geometry("750x250")
            new.title("Ödeme Ekleme")
            new.resizable(False,False)
            #message label and textbox
            msg_text_box=tk.Text(new , font='Verdana 10')
            msg_text_box.place(relx= 0.10 , rely=0.2 , relwidth=0.30 , relheight=0.10)
            msgStringVariable = tk.StringVar()
            msg_label = tk.Label(new ,textvariable=msgStringVariable ,font='Verdana 10 bold')
            msgStringVariable.set('Odeme Mesaji')
            msg_label.place(relx=0.1 , rely=0.05)

            
            paymentDateEntry=DateEntry(new,locale='tr' ,selectmode='day' , date_pattern="y/mm/dd")
            paymentDateEntry.place(relx = 0.45 , rely=0.2)
            paymentDateVariable = tk.StringVar()
            paymentDateLabel = tk.Label(new , textvariable= paymentDateVariable , font='Verdana 10 bold')
            paymentDateVariable.set('Odeme Tarihi')
            paymentDateLabel.place(relx=0.45 , rely=0.05)

            paymentVariable = tk.StringVar()
            paymentEntry = tk.Entry(new , font='Verdana 10')
            paymentEntry.place(relx=0.7 , rely=0.2 , relwidth=0.2 , relheight=0.1)
            paymentEntryLabel = tk.Label(new , textvariable=paymentVariable,font='Verdana 10 bold')
            paymentVariable.set('Odeme Miktari')
            paymentEntryLabel.place(relx=0.7 , rely=0.05)

            print(type(paymentDateEntry.get_date().strftime("%Y/%m/%d")))
            

            s = ttk.Style()
            s.configure('my.TButton', font=('Verdana', 36))
            paymentSaveButton = ttk.Button(new , text='Odemeyi Kaydet' , style='my.TButton',command= lambda : add_payment(
                customerid= Selectedcusid,
                message= msg_text_box.get("1.0","end-1c"),
                date = paymentDateEntry.get_date().strftime("%d/%m/%Y"),
                payment=int(paymentEntry.get())
            ))
            paymentSaveButton.place(relx=0.1 , rely=0.4 , relwidth=0.8 , relheight=0.3)


        addCustomerButton = ttk.Button(navbar_frame, text="Müşteri Ekle" , command=add_customer_w)
        addCustomerButton.pack(padx=10 , pady=10)

        addPaymentButton = ttk.Button(customer_payment_frame , text='Odeme Ekle' , command=add_payment_w)
        addPaymentButton.pack(side='top' , pady=5)

        
        
class PageOne(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text="This is page one").pack(side="top", fill="x", pady=10)
        tk.Button(self, text="Return to start page",
                  command=lambda: master.switch_frame(Anasayfa)).pack()

class PageTwo(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text="This is page two").pack(side="top", fill="x", pady=10)
        tk.Button(self, text="Return to start page",
                  command=lambda: master.switch_frame(Anasayfa)).pack()

if __name__ == "__main__":
    app = App()
    app.update_idletasks()
    app.mainloop()


