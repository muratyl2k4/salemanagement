import tkinter as tk 
import sqlite3
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import DateEntry
from datetime import datetime





class Scrollbar():
    def __init__(self, parent , width , height , background_color):
        self.parent = parent
        # STEPS TO CREATE A SCROLLBAR
        # 1. Create A Main Frame in root
        self.main_frame = tk.Frame(self.parent , width=width , height=height , bg=background_color)
        self.main_frame.pack(fill='both', expand=1)
        # 2. Create A Canvas in Main Frame
        self.my_canvas = tk.Canvas(self.main_frame , width=width , height=height , bg=background_color)
        self.my_canvas.pack(side='left', fill='both', expand=1)
        # 3. Add A Scrollbar To The Canvas
        self.my_scrollbar = ttk.Scrollbar(self.main_frame, orient='vertical', command=self.my_canvas.yview)
        self.my_scrollbar.pack(side='right', fill='y')
        # 4. Configure The Canvas
        self.my_canvas.configure(yscrollcommand=self.my_scrollbar.set)
        # 5. Create ANOTHER Frame INSIDE the Canvas. 
        self.window = tk.Frame(self.my_canvas , background='white')
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
        
        self.config(bg='black')
        photo = tk.PhotoImage(file = "money.png")
        self.wm_iconphoto(False, photo)
        self.title('M.Y.Tech Kumluca Sanayi Lokantasi Muhasebe V2.0')

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
        swidth = self.winfo_screenwidth()-50
        sheight = self.winfo_screenheight()-150
        self.config(width=swidth , height=sheight)
        ##Navbar Canvas 
        navbar_canvas = tk.Canvas(self , bg='white' , width=swidth , height=sheight/5*2)
        navbar_canvas.pack(padx=10,pady=5 , fill='both')  
        navbar_frame = tk.Frame(navbar_canvas , bg='white')
        navbar_frame.place(relheight=1 , relwidth=1)
        
        ##Customer Canvas
        customer_canvas = tk.Canvas(self , bg='#222222',  width=int((swidth/4)) , height=int(sheight/5*4))
        customer_canvas.pack(padx=10,pady=5,anchor='s' , side='left')

        customer_payment_canvas = tk.Canvas(self , bg='white' , width=int(swidth/4*3) +10, height=int(sheight/5*4))
        customer_payment_canvas.pack(pady=10 , padx=10 , side='bottom' , anchor='s')
        
        #scrollbar for customer Canvas 
        
        db = sqlite3.connect('database.db')     
        cursor = db.cursor()   
        ##Activate foreign keys
        cursor.execute(""" PRAGMA foreign_keys = ON """)
        ##customer table
        cursor.execute('''CREATE TABLE IF NOT EXISTS customers(customer_id INTEGER PRIMARY KEY,customer_name TEXT)''')
        ##payment table 
        cursor.execute("""CREATE TABLE IF NOT EXISTS payment(id INTEGER,customer INTEGER , message TEXT , date BLOB , payment FLOAT  , FOREIGN KEY(customer) REFERENCES customers(customer_id))""")
        cursor.execute("""CREATE TABLE IF NOT EXISTS debt(id INTEGER,customer INTEGER , message TEXT , date BLOB , debt FLOAT  , FOREIGN KEY(customer) REFERENCES customers(customer_id))""")


        
        ## ADD CUSTOMERS ON DATABASE
        def add_customer(textbox , frame):
            value=textbox.get("1.0","end-1c")
            frame.destroy()
            if not value == '':
                cursor.execute("select customer_name from customers")
                results = cursor.fetchall()
                cursor.execute(f""" INSERT or IGNORE INTO customers (customer_id , customer_name) VALUES ({len(results)+1}, '{value}') """)
                cursor.execute("select customer_name from customers")
                results = cursor.fetchall()
                results.reverse()
                db.commit()
                messagebox.showinfo("İŞLEM BAŞARILI" ,f"{value} İsimli müşteri kaydedildi !")
                draw_customer(results)
            elif value =='':
                messagebox.showerror(f"Müşteri ismi boş olamaz !")    
        ##ADD PAYMENT    
        def add_payment(customerid ,message , date , payment , frame):
            cursor.execute(""" select id from payment """)
            idResults = cursor.fetchall()
            cursor.execute(f""" INSERT INTO payment (id , customer , 'message' , 'date',  payment ) VALUES ({len(idResults) + 1} ,{customerid}, '{message}', '{date}' ,{float(payment)}) """)
            db.commit()
            frame.destroy()
            messagebox.showinfo("İŞLEM BAŞARILI" , "ÖDEME KAYDEDİLDİ")
        ###ADD DEBT
        def add_debt(customerid ,message , date , debt , frame):
            cursor.execute(""" select id from debt """)
            idResults = cursor.fetchall()
            cursor.execute(f""" INSERT INTO debt (id ,customer , 'message' , 'date',  debt ) VALUES ({len(idResults) + 1} , {customerid}, '{message}', '{date}' ,{float(debt)}) """)
            db.commit()
            frame.destroy()
            messagebox.showinfo("İŞLEM BAŞARILI" , "BORÇ KAYDEDİLDİ")
        ##UPDATE PAYMENT 
        def update_payment(msg , date , payment , id , frame):
            cursor.execute(f""" UPDATE payment 
            SET message = '{msg}',
            date = '{date}' , 
            payment = {float(payment)} 
            where id = {id} """)
            db.commit()
            frame.destroy()
            messagebox.showinfo("İŞLEM BAŞARILI" , "ÖDEME GÜNCELLENDİ")
        ##UPDATE DEBT 
        def update_debt(msg , date , debt , id , frame):
            cursor.execute(f""" UPDATE debt 
            SET message = '{msg}',
            date = '{date}' , 
            debt = {float(debt)} 
            where id = {id} """)
            db.commit() 
            frame.destroy()
            messagebox.showinfo("İŞLEM BAŞARILI" , "BORÇ GÜNCELLENDİ")
        ##DELETE DEBT 
        def delete_debt(debtid):
            msg_box = messagebox.askquestion('Borcu Sil', 'Borcu silmek istediginizden emin misiniz?',
                                    icon='warning')
            if msg_box == 'yes':
                cursor.execute(f"""
                DELETE FROM debt where id = {debtid} 
                """)
                db.commit()        
            else:
                messagebox.showinfo('Islem Basarisiz', 'Odeme Silinmedi')
        ##DELETE  
        def delete_payment(paymentid):
            
            msg_box = messagebox.askquestion('Odemeyi Sil', 'Odemeyi silmek istediginizden emin misiniz?',
                                    icon='warning')
            if msg_box == 'yes':
                cursor.execute(f"""
                DELETE FROM payment where id = {paymentid} 
                """)
                db.commit()        
            else:
                messagebox.showinfo('Islem Basarisiz', 'Odeme Silinmedi')
        ##EDITINGS
        delPhoto = tk.PhotoImage(file='delete.png')
        def edit_payment(paymentid):
            print(paymentid)
            ##select payment 
            newpf= tk.Toplevel(master)
            newpf.geometry("750x250")
            newpf.resizable(False,False)
            newpf.title("Ödeme Düzenleme")

            cursor.execute(""" select * from payment where id =  ? """ , (paymentid,))
            pResult = cursor.fetchone()
            print(pResult)
            #message label and textbox
            msg_text_box=tk.Text(newpf ,font='Verdana 10')
            msg_text_box.insert(tk.END , pResult[2])
            msg_text_box.place(relx= 0.10 , rely=0.2  ,relwidth=0.30 , relheight=0.10)
            msgStringVariable = tk.StringVar()
            msg_label = tk.Label(newpf ,textvariable=msgStringVariable ,font='Verdana 10 bold')
            msgStringVariable.set('Odeme Mesaji')
            msg_label.place(relx=0.1 , rely=0.05)
            
            paymentDateEntry=DateEntry(newpf,locale='tr' , selectmode='day' , date_pattern="y/mm/dd")
            paymentDateEntry.set_date(datetime.strptime(pResult[3] , '%d/%m/%Y'))
            paymentDateEntry.place(relx = 0.45 , rely=0.2)
            paymentDateVariable = tk.StringVar()
            paymentDateLabel = tk.Label(newpf , textvariable= paymentDateVariable , font='Verdana 10 bold')
            paymentDateVariable.set('Odeme Tarihi')
            paymentDateLabel.place(relx=0.45 , rely=0.05)

            paymentVariable = tk.StringVar()
            paymentEntry = tk.Entry(newpf , font='Verdana 10')
            paymentEntry.insert(tk.END , pResult[4])
            paymentEntry.place(relx=0.7 , rely=0.2 , relwidth=0.2 , relheight=0.1)
            paymentEntryLabel = tk.Label(newpf , textvariable=paymentVariable,font='Verdana 10 bold')
            paymentVariable.set('Odeme Miktari')
            paymentEntryLabel.place(relx=0.7 , rely=0.05)

            s = ttk.Style()
            s.configure('my.TButton', font=('Verdana', 36))
            paymentUpdateButton = ttk.Button(newpf , text='Odemeyi Guncelle' , style='my.TButton' , command= lambda : update_payment(
                msg = str(msg_text_box.get("1.0","end-1c")),
                date = paymentDateEntry.get_date().strftime("%d/%m/%Y"),
                payment = float(paymentEntry.get()) ,
                id = paymentid ,
                frame=newpf
            ))
            paymentUpdateButton.pack(side='right' , pady=20 , padx=100)
            paymentDeleteButton = tk.Button(newpf , bg='white' , image=delPhoto , command= lambda : delete_payment(paymentid))
            paymentDeleteButton.place(relx=0.1 , rely=0.7 )

        def edit_debt(debtid):
            ##select payment 
            newpf= tk.Toplevel(master)
            newpf.geometry("750x250")
            newpf.resizable(False,False)
            newpf.title("Borc Düzenleme")

            cursor.execute(""" select * from debt where id =  ? """ , (debtid,))
            dResult = cursor.fetchone()
            print(dResult)
            #message label and textbox
            msg_text_box=tk.Text(newpf ,font='Verdana 10')
            msg_text_box.insert(tk.END , dResult[2])
            msg_text_box.place(relx= 0.10 , rely=0.2  ,relwidth=0.30 , relheight=0.10)
            msgStringVariable = tk.StringVar()
            msg_label = tk.Label(newpf ,textvariable=msgStringVariable ,font='Verdana 10 bold')
            msgStringVariable.set('Odeme Mesaji')
            msg_label.place(relx=0.1 , rely=0.05)
            
            debtDateEntry=DateEntry(newpf,locale='tr' , selectmode='day' , date_pattern="y/mm/dd")
            debtDateEntry.set_date(datetime.strptime(dResult[3] , '%d/%m/%Y'))
            debtDateEntry.place(relx = 0.45 , rely=0.2)
            debtDateVariable = tk.StringVar()
            debtDateLabel = tk.Label(newpf , textvariable= debtDateVariable , font='Verdana 10 bold')
            debtDateVariable.set('Odeme Tarihi')
            debtDateLabel.place(relx=0.45 , rely=0.05)

            debtVariable = tk.StringVar()
            debtEntry = tk.Entry(newpf , font='Verdana 10')
            debtEntry.insert(tk.END , dResult[4])
            debtEntry.place(relx=0.7 , rely=0.2 , relwidth=0.2 , relheight=0.1)
            debtEntryLabel = tk.Label(newpf , textvariable=debtVariable,font='Verdana 10 bold')
            debtVariable.set('Odeme Miktari')
            debtEntryLabel.place(relx=0.7 , rely=0.05)

            s = ttk.Style()
            s.configure('my.TButton', font=('Verdana', 36))
            debtUpdateButton = ttk.Button(newpf , text='Borcu Guncelle' , style='my.TButton' , command= lambda : update_debt(
                msg = str(msg_text_box.get("1.0","end-1c")),
                date = debtDateEntry.get_date().strftime("%d/%m/%Y"),
                debt = float(debtEntry.get()) ,
                id = debtid ,
                frame=newpf
            ))
            debtUpdateButton.pack(side='right' , pady=10 , padx=180)
            debtDeleteButton = tk.Button(newpf , bg='white' , image=delPhoto , command= lambda : delete_debt(debtid))
            debtDeleteButton.place(relx=0.1 , rely=0.7)
        
        #DRAW CASHFLOW TO SCREEN
        editphoto = tk.PhotoImage(file='editpensquare.png')
        def draw_cashflow(customer_name):
            try :
                global Selectedcusid
                
                
                ###GET SELECTED CUSTOMERS ID 
                cursor.execute(f""" select customer_id from customers where customer_name = ? """ , (customer_name,))
                result = cursor.fetchone()
                Selectedcusid = result[0]
                ## get payments
                cursor.execute(f""" select * from payment where customer = ? """ , (result[0],))
                resultp = cursor.fetchall()
                ## get debts
                cursor.execute(f""" select * from debt where customer = ? """ , (result[0],))
                resultd = cursor.fetchall()
                ### DESTROY ALL THINGS IN CUSTOMER PAYMENT SCREEN 
                for widget in customer_payment_canvas.winfo_children():
                    widget.destroy()
                ## ADDING SCROLLBAR
                scrollbar = Scrollbar(customer_payment_canvas , width=int(customer_payment_canvas.cget('width')) , height=customer_payment_canvas.cget('height') , background_color='white')
                ##Payment Frame
                payment_frame = tk.Frame(scrollbar.window , width=int(customer_payment_canvas.cget('width')) / 6 * 2 , height=customer_payment_canvas.cget('height') , bg='red')
                payment_frame.grid(column=2 , row=0 , sticky='n')
                ##Debt Frame
                debt_frame = tk.Frame(scrollbar.window , width=int(customer_payment_canvas.cget('width')) / 6 * 2 , height=customer_payment_canvas.cget('height') , bg='blue')
                debt_frame.grid(column=0 , row=0 , sticky='n')
                ##CUSTOMER NAME
                #customerNameLabel = ttk.Label(scrollbar.window ,background='white' , text=customer_name , font='Calibri 15 bold')
                #customerNameLabel.grid(column=0 ,row=0 ,padx=5)
                ## PAYMENT ADD
                addPaymentButton = ttk.Button(payment_frame  , text='Ödeme Ekle' , command=lambda : add_payment_w())
                addPaymentButton.grid(column=0 , row=0)
                addDebtButton = ttk.Button(debt_frame  , text='Borç Ekle' , command=lambda : add_debt_w())
                addDebtButton.grid(column=0 , row=0)
                resultp.reverse()
                resultd.reverse()
                ## PAYMENTS
                cursor.execute("""SELECT SUM(payment) FROM payment where customer = ? """ , (Selectedcusid,))
                totalpayment = cursor.fetchone()
                print(totalpayment)
            except Exception as e : 
                print("CASHFLOW FRAME HATASI" , e)    
               
            try :         
                for i in enumerate(resultp):
                    paymentid = i[1][0]
                    print(paymentid)
                    msg=  i[1][2]
                    date = i[1][3]
                    payment = i[1][4]

                    background_color = 'black'
                    foreground_color = 'white'
                    onepaymentcanvas = tk.Canvas(payment_frame , bg=background_color , width=180 , height=50)
                    onepaymentcanvas.grid(column=i[0] if 1+i[0] <2 else i[0] % 2 , row=1 +int(i[0] / 2) , pady=3 , padx=2)
                    onepaymentframe = tk.LabelFrame(onepaymentcanvas, bg=background_color)
                    onepaymentframe.place(relheight=1 , relwidth=1)
                    onepaymentframe.grid_propagate(False)
                    
                    #ttk.Label(onepaymentframe , background=background_color , foreground=foreground_color , text='Mesaj : ' +msg , font='Verdana 10').pack(pady=1, padx=5 ,side='top' , anchor='w')
                    tk.Button(onepaymentframe , image=editphoto , bg='white' , height=15 ,width=15 , command= lambda x = paymentid: edit_payment(x)).pack(side='right' , anchor='n')
                    ttk.Label(onepaymentframe , background=background_color , foreground=foreground_color ,width=60,text='Odeme : ' +str(payment) , font='Verdana 10 bold').pack(pady=1 , padx=5, side='top' , anchor='w')
                    ttk.Label(onepaymentframe , background=background_color , foreground=foreground_color ,text='Tarih : ' + date ,font='Verdana 10 bold').pack(pady=3, padx=5, side='top' , anchor='w')

                ##DEBTS
                cursor.execute("""SELECT SUM(debt) FROM debt where customer = ?""" , (Selectedcusid , ))
                totaldebt = cursor.fetchone()
                print(totaldebt)
            except Exception as e : 
                print('ODEME YAZDIRMA KISMINDA HATA' , e)    
            try :     
                for i in enumerate(resultd):
                    debtid = i[1][0]
                    msg=  i[1][2]
                    date = i[1][3]
                    debt = i[1][4]

                    background_color = 'white' if debt >= 0 else 'black'
                    foreground_color = 'black' if background_color == 'white' else 'white'
                    onedebtcanvas = tk.Canvas(debt_frame , bg=background_color , width=180 , height=50)
                    onedebtcanvas.grid(column=i[0] if 1+i[0] <2 else i[0] % 2 , row=1 +int(i[0] / 2) , pady=3 , padx=2)
                    onedebtframe = tk.LabelFrame(onedebtcanvas, bg=background_color)
                    onedebtframe.place(relheight=1 , relwidth=1)
                    onedebtframe.grid_propagate(False)
                    
                    #ttk.Label(onedebtframe , background=background_color , foreground=foreground_color , text='Mesaj : ' +msg , font='Verdana 10').pack(pady=1, padx=5 ,side='top' , anchor='w')
                    tk.Button(onedebtframe , image=editphoto , bg='white' , height=15 ,width=15 , command= lambda x= debtid: edit_debt(x)).pack(side='right' , anchor='n')
                    ttk.Label(onedebtframe , background=background_color , foreground=foreground_color , width=60,text='Odeme : ' +str(debt) , font='Verdana 10 bold').pack(pady=1 , padx=5, side='top' , anchor='w')
                    ttk.Label(onedebtframe , background=background_color , foreground=foreground_color ,text='Tarih : ' + date ,font='Verdana 10 bold').pack(pady=3, padx=5, side='top' , anchor='w')
            except Exception as e : 
                print('BORC YAZDIRMADA HATA' , e)
            try : 
                    
                tk.Label(payment_frame , text='Ödenen : ' +str(totalpayment[0]) , bg='red' , fg='white', font='Verdana 15').grid(column=1 , row=0)
                tk.Label(debt_frame , text='Borç : ' +str(totaldebt[0]) , bg='blue' , fg='white' ,font='Verdana 15').grid(column=1 , row=0)
                tk.Label(scrollbar.window , text='Alacak : ' +str(totaldebt[0] - totalpayment[0]) , bg='white' , font='Verdana 15').grid(column=5 , row=0 , sticky='n')
            except Exception as e: 
                print("cashflow frame label hatasi" , e)        
        draw_cashflow(None)
            
        ## DRAW CUSTOMERS TO SCREEN 
        def draw_customer(listee):
            for widget in customer_canvas.winfo_children():
                widget.destroy()
            scrollbar = Scrollbar(customer_canvas , width = int(customer_canvas.cget('width')) -50 , height=int(customer_canvas.cget('height')) , background_color='white')
            customerSearchEntry = tk.Entry(scrollbar.window , font='Verdana 25' , bg='#444444')
            customerSearchEntry.pack(side='top')
            customerListBox = tk.Listbox(scrollbar.window)
            customerListBox.pack( pady=40)
                     
            customerList = []
            for x in listee:
                for i in x:
                    ttk.Button(customerListBox, text=i , width=100 , command=lambda x=i : draw_cashflow(x)).pack()
                    customerList.append(i)    
                    
            def update(data):
                
                for i in customerListBox.winfo_children():
                    i.destroy()
                for item in data :
                   ttk.Button(customerListBox, text=item , width=100 , command=lambda x=item : draw_cashflow(x)).pack()
                        
            def fillout(event):
                customerSearchEntry.delete(0 , tk.END)
                customerSearchEntry.insert(0, customerListBox.get(0 , tk.ANCHOR))

            def check(event):
                typed = customerSearchEntry.get()
                if typed == '':
                    data = customerList
                else : 
                    data = []
                    for item in customerList:
                        if typed.lower() in item.lower():
                            data.append(item)
                update(data)    
            customerSearchEntry.bind("<KeyRelease>" , check)
            customerListBox.bind("<<ListBoxSelect>>" , fillout)

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
            comment= ttk.Button(new,text="Müşteri Ekle", command=lambda: add_customer(my_text_box , new))
            #command=get_input() will wait for the key to press and displays the entered text
            comment.place(relx= 0.1 , rely=0.4 , relwidth=0.8 , relheight=0.3)
            
        
        ###create payment window     
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
                message= str(msg_text_box.get("1.0","end-1c")),
                date = paymentDateEntry.get_date().strftime("%d/%m/%Y"),
                payment=float(paymentEntry.get()),
                frame=new
            ))
            paymentSaveButton.place(relx=0.1 , rely=0.4 , relwidth=0.8 , relheight=0.3)
        
        ### create debt window 
        def add_debt_w():
            new= tk.Toplevel(master)
            new.geometry("750x250")
            new.title("Ödeme Ekleme")
            new.resizable(False,False)
            #message label and textbox
            msg_text_box=tk.Text(new , font='Verdana 10')
            msg_text_box.place(relx= 0.10 , rely=0.2 , relwidth=0.30 , relheight=0.10)
            msgStringVariable = tk.StringVar()
            msg_label = tk.Label(new ,textvariable=msgStringVariable ,font='Verdana 10 bold')
            msgStringVariable.set('Borc Mesaji')
            msg_label.place(relx=0.1 , rely=0.05)
            
            debtDateEntry=DateEntry(new,locale='tr' ,selectmode='day' , date_pattern="y/mm/dd")
            debtDateEntry.place(relx = 0.45 , rely=0.2)
            debtDateVariable = tk.StringVar()
            debtDateLabel = tk.Label(new , textvariable= debtDateVariable , font='Verdana 10 bold')
            debtDateVariable.set('Borc Tarihi')
            debtDateLabel.place(relx=0.45 , rely=0.05)

            debtVariable = tk.StringVar()
            debtEntry = tk.Entry(new , font='Verdana 10')
            debtEntry.place(relx=0.7 , rely=0.2 , relwidth=0.2 , relheight=0.1)
            debtEntryLabel = tk.Label(new , textvariable=debtVariable,font='Verdana 10 bold')
            debtVariable.set('Borc Miktari')
            debtEntryLabel.place(relx=0.7 , rely=0.05)

            print(type(debtDateEntry.get_date().strftime("%Y/%m/%d")))

            s = ttk.Style()
            s.configure('my.TButton', font=('Verdana', 36))
            debtSaveButton = ttk.Button(new , text='Borcu Kaydet' , style='my.TButton',command= lambda : add_debt(
                customerid= Selectedcusid,
                message= str(msg_text_box.get("1.0","end-1c")),
                date = debtDateEntry.get_date().strftime("%d/%m/%Y"),
                debt=float(debtEntry.get()),
                frame=new
            ))
            debtSaveButton.place(relx=0.1 , rely=0.4 , relwidth=0.8 , relheight=0.3)

        def print_debts():
            try : 
                cursor.execute(""" select customer_id , customer_name from customers""")
                customers = cursor.fetchall()
                now = datetime.now().strftime("%d-%m-%Y %H-%M-%S")
                text = f"{now} TARIHLI BORCLAR LISTESI \n\n"
                for i in customers:
                    ###get payments 
                    cursor.execute(f""" select SUM(payment) from payment where customer = {i[0]} """)
                    totalpayments = cursor.fetchone()
                    ## get debts 
                    cursor.execute(f""" select SUM(debt) from debt where customer = {i[0]} """)
                    totaldebts = cursor.fetchone()
                    print(totaldebts,totalpayments)
                    td = totaldebts[0] if not totaldebts[0] == None else 0
                    tp = totalpayments[0] if not totalpayments[0] == None else 0
                    try:
                        text += f"{i[1]} ' den ALINACAK MIKTAR {int(td) - int(tp)} \n" if not int(td) - int(tp) == 0 else '' 
                    except Exception as e:
                        print(i , e )
                with open(f'{now} borc.txt', 'w') as f:
                    f.write(text)
                messagebox.showinfo('Islem Basarili',f"Borçlarınız {now} tarihli dosyaya kaydedilmistir !")
            except Exception as e: 
                messagebox.showinfo(e)


        print_debt_button = tk.Button(navbar_frame , text="Borçları Çıkar" ,width=15 , height=5 , command=lambda : print_debts())
        print_debt_button.pack(side=tk.RIGHT , anchor='s' , padx=10 , pady=10)
        
        addCustomerButton = tk.Button(navbar_frame, text="Müşteri Ekle" , height=5 , width=15,font='Verdana 10 bold' ,command=add_customer_w)
        addCustomerButton.pack(side=tk.LEFT , anchor='s',padx=10 , pady=10)
      
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


