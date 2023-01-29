# Multi-frame tkinter application v2.3
import tkinter as tk
from settings import SCREEN_HEIGTH , SCREEN_WIDTH
import sqlite3

class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self._frame = None
        ##Main Settings 
        self.resizable(False , False)
        photo = tk.PhotoImage(file = 'money.png')
        self.wm_iconphoto(False, photo)
        self.title('Kumluca Sanayi Lokantasi Muhasebe')
        self.switch_frame(Anasayfa)
        

    def switch_frame(self, frame_class):
        """Destroys current frame and replaces it with a new one."""
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()

class Anasayfa(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        ##MAIN CANVAS
        main_canvas = tk.Canvas(self , width=SCREEN_WIDTH , height=SCREEN_HEIGTH)
        main_canvas.pack()
        ##CUSTOMER FRAME
        customer_frame = tk.Frame(self , bg='white')
        customer_frame.place(relheight=0.70 , relwidth=0.1 ,relx=0.005 , rely= 0.25)
        
        customer_payment_frame = tk.Frame(self , bg='white')
        customer_payment_frame.place(relheight=0.70 , relwidth=0.80 ,relx=0.15 , rely=0.25 )
        ## creating database 
        db = sqlite3.connect('database.db')     
        cursor = db.cursor()   
        ##customer table
        cursor.execute('''CREATE TABLE IF NOT EXISTS customers(customer_id INTEGER PRIMARY KEY,customer_name TEXT)''')
        ##payment table 
        cursor.execute("""CREATE TABLE IF NOT EXISTS payment(customer INTEGER , message TEXT , date timestamp , payment FLOAT  , FOREIGN KEY(customer) REFERENCES customers(customer_id))""")
        ## ADD CUSTOMERS ON DATABASE
        def musteri_ekle():
            value=my_text_box.get("1.0","end-1c")
            print(value)
            cursor.execute("select customer_name from customers")
            results = cursor.fetchall()
            cursor.execute(f""" INSERT or IGNORE INTO customers (customer_id , customer_name) VALUES ('{len(results)+1}', '{value}') """)
            cursor.execute("select customer_name from customers")
            results = cursor.fetchall()
            db.commit()
            musteri_yazdir(results)
        ## DRAW CUSTOMERS TO SCREEN 
        def musteri_yazdir(listee):
            for widget in customer_frame.winfo_children():
                widget.destroy()
            for i in listee:    
                binder(tk.Label(customer_frame, text=i, width=16,bg='#C5C5C5' ,  relief='groove'))
            
        #BUTTON BINDER
        def binder(button):
            button.pack(padx=1, pady=2 , side='top')
            button.bind('<Button-1>', lambda x=button : print(button.cget('text')))
            button.bind('<Enter>', lambda x=button : button.config(bg='#696969', fg='white'))
            button.bind('<Leave>', lambda x=button : button.config(bg='#C5C5C5', fg='black'))

        #Creating a text box widget
        my_text_box=tk.Text(customer_frame, height=3, width=10)
        my_text_box.pack(side='top')

        #Create a button for Comment
        comment= tk.Button(customer_frame, height=5, width=10, text="musteri ekle", command=lambda: musteri_ekle())

        #command=get_input() will wait for the key to press and displays the entered text
        comment.pack(side='top')

        ##get customers
        cursor.execute("select customer_name from customers")
        resultss = cursor.fetchall()
        liste = resultss
        
        ##BUTTON SETTINGS
        for i in liste:    
                binder(tk.Label(customer_frame, text=i, width=16,bg='#C5C5C5' ,  relief='groove'))


class PageOne(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Canvas(self , width=SCREEN_WIDTH+500 , height=SCREEN_HEIGTH).pack()
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
    app.mainloop()