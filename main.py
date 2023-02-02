import tkinter as tk 
import sqlite3
from tkinter import ttk
from ctypes import windll
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

        #scrollbar for customer Canvas 
        scrollbar = Scrollbar(customer_canvas , width = int(customer_canvas.cget('width')) -50 , height=int(customer_canvas.cget('height')))
        db = sqlite3.connect('database.db')     
        cursor = db.cursor()   
        ##customer table
        cursor.execute('''CREATE TABLE IF NOT EXISTS customers(customer_id INTEGER PRIMARY KEY,customer_name TEXT)''')
        ##payment table 
        cursor.execute("""CREATE TABLE IF NOT EXISTS payment(customer INTEGER , message TEXT , date timestamp , payment FLOAT  , FOREIGN KEY(customer) REFERENCES customers(customer_id))""")

        ##get customers from database
        cursor.execute("select customer_name from customers")
        resultss = cursor.fetchall()
        resultss.reverse()    
        
        ## ADD CUSTOMERS ON DATABASE
        def musteri_ekle(texbox):
            value=texbox.get("1.0","end-1c")
            cursor.execute("select customer_name from customers")
            results = cursor.fetchall()
            cursor.execute(f""" INSERT or IGNORE INTO customers (customer_id , customer_name) VALUES ('{len(results)+1}', '{value}') """)
            cursor.execute("select customer_name from customers")
            results = cursor.fetchall()
            db.commit()
            musteri_yazdir(results)
        ## DRAW CUSTOMERS TO SCREEN 
        def musteri_yazdir(listee):
            for widget in customer_canvas.winfo_children():
                widget.destroy()
            scrollbar = Scrollbar(customer_canvas , width = int(customer_canvas.cget('width')) -50 , height=int(customer_canvas.cget('height')))
            listee.reverse()
            for x in listee:
                for i in x:    
                    ttk.Button(scrollbar.window, text=i , width=100).pack()
        
        ## customer adding in new window 
        def open_win():
            new= tk.Toplevel(master)
            new.geometry("750x250")
            new.title("Müşteri Ekleme")
            #Create a Label in New window
            #Creating a text box widget
            my_text_box=tk.Text(new , font='Verdana 25 bold')
            my_text_box.place(relx= 0.1 , rely=0.1 , relwidth=0.8 , relheight=0.3)

            #Create a button for Comment
            comment= tk.Button(new,text="Müşteri Ekle", command=lambda: musteri_ekle(my_text_box))

            #command=get_input() will wait for the key to press and displays the entered text
            comment.place(relx= 0.1 , rely=0.4 , relwidth=0.8 , relheight=0.3)

        tk.Button(navbar_frame, text="Müşteri Ekle" , command=open_win).pack(padx=10 , pady=10)



       
        
        

        
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


