# Multi-frame tkinter application v2.3
import tkinter as tk
import sqlite3
from tkinter import ttk
from ctypes import windll
windll.shcore.SetProcessDpiAwareness(1)


class Scrollbar():
    def __init__(self, parent):
        
        self.parent = parent
        
        
        # STEPS TO CREATE A SCROLLBAR
        # 1. Create A Main Frame in root
        self.main_frame = tk.Frame(self.parent)
        self.main_frame.pack(fill='both', expand=1)
        
        # 2. Create A Canvas in Main Frame
        self.my_canvas = tk.Canvas(self.main_frame)
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
        self.my_canvas.itemconfig('windowTag', height=((self.my_canvas.winfo_height()*2)), width=self.my_canvas.winfo_width()) #resize the frame with double height of canvaz. The internal frame need to be larger than scrollregion(=canvas size) for scrollbar to be activated.
        
        # update scrollregion to the same size as the canvas
        self.my_canvas.configure(scrollregion = self.my_canvas.bbox("all"))

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
        """Destroys current frame anda replaces it with a new one."""
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()

class Anasayfa(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        ##MAIN CANVAS
        width = self.winfo_screenwidth()
        height = self.winfo_screenheight()
        main_canvas = tk.Frame(self , width = width*0.8 , height = height*0.8)
        main_canvas.pack()
        ##NAVBAR FRAME
        navbar_frame = tk.Frame(self , bg='white' , width=1000)
        navbar_frame.place(relheight=0.2 , relwidth=0.965 , relx= 0.015 , rely=0.025)

        ##CUSTOMER FRAME
        customer_frame = tk.Canvas(self , bg='white')
        customer_frame.pack(side='bottom' , anchor='w')
        scroll = Scrollbar(customer_frame)
        
        customer_payment_frame = tk.Frame(self , bg='white')
        customer_payment_frame.place(relheight=0.70 , relwidth=0.75 ,relx=0.23 , rely=0.25 )
        ## creating database 
        db = sqlite3.connect('database.db')     
        cursor = db.cursor()   
        ##customer table
        cursor.execute('''CREATE TABLE IF NOT EXISTS customers(customer_id INTEGER PRIMARY KEY,customer_name TEXT)''')
        ##payment table 
        cursor.execute("""CREATE TABLE IF NOT EXISTS payment(customer INTEGER , message TEXT , date timestamp , payment FLOAT  , FOREIGN KEY(customer) REFERENCES customers(customer_id))""")
        ## ADD CUSTOMERS ON DATABASE
        def musteri_ekle(texbox):
            value=texbox.get("1.0","end-1c")
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
            scroll = Scrollbar(customer_frame)
            listee.reverse()
            for x in listee:
                for i in x:    
                    binder(tk.Label(scroll.window, text=i, width=16,bg='#C5C5C5' ,  relief='groove'))
            
        #BUTTON BINDER
        def binder(button):
            button.pack(padx=2, pady=2 , fill = 'y')
            button.bind('<Button-1>', lambda x=button : print(button.cget('text')))
            button.bind('<Enter>', lambda x=button : button.config(bg='#696969', fg='white'))
            button.bind('<Leave>', lambda x=button : button.config(bg='#C5C5C5', fg='black'))

        
        ##get customers
        cursor.execute("select customer_name from customers")
        resultss = cursor.fetchall()
        resultss.reverse()    
        print(resultss)
        ##create customer buttons
        for x in resultss:
                for i in x:    
                    binder(tk.Label(scroll.window, text=i, width=16,bg='#C5C5C5' ,  relief='groove'))
        ## customer adding in new window 
        def open_win():
            new= tk.Toplevel(master)
            new.geometry("750x250")
            new.title("M????teri Ekleme")
            #Create a Label in New window
            #Creating a text box widget
            my_text_box=tk.Text(new , font='Verdana 25 bold')
            my_text_box.place(relx= 0.1 , rely=0.1 , relwidth=0.8 , relheight=0.3)

            #Create a button for Comment
            comment= tk.Button(new,text="M????teri Ekle", command=lambda: musteri_ekle(my_text_box))

            #command=get_input() will wait for the key to press and displays the entered text
            comment.place(relx= 0.1 , rely=0.4 , relwidth=0.8 , relheight=0.3)

        tk.Button(navbar_frame, text="M????teri Ekle", command=open_win).pack()
        
        
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