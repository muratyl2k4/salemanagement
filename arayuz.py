# Multi-frame tkinter application v2.3
import tkinter as tk
from settings import SCREEN_HEIGTH , SCREEN_WIDTH

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

        main_canvas = tk.Canvas(self , width=SCREEN_WIDTH , height=SCREEN_HEIGTH)
        main_canvas.pack()

        frame = tk.Frame(self , bg='white')
        frame.place(relheight=0.70 , relwidth=0.1 ,relx=0.005 , rely= 0.25)
        customer_frame = tk.Frame(self , bg='white')
        customer_frame.place(relheight=0.70 , relwidth=0.80 ,relx=0.15 , rely=0.25 )
        label = tk.Label(customer_frame , text='' , bg=None  , fg='black')
        label.pack(padx=10 , pady=10 , side='top')
        liste = ['musteri1' , 'musteri2']
        def binder(button):
            button.pack(padx=1, pady=2 , side='top')
           
            button.bind('<Button-1>', lambda x=button : customer_informations(button.cget('text')))
            button.bind('<Enter>', lambda x=button : button.config(bg='#696969', fg='white'))
            button.bind('<Leave>', lambda x=button : button.config(bg='#C5C5C5', fg='black'))
        def musteri_ekle(musteri):
            
            liste.append(musteri)
            for widget in frame.winfo_children():
                widget.destroy()
            for i in liste:    
                binder(tk.Label(frame, text=i, width=16,bg='#C5C5C5' ,  relief='groove'))
        
        musteri_ekle_button = tk.Button(customer_frame , text='musteri ekle' , command= lambda : musteri_ekle(musteri_ekle_button.cget('text')))
        musteri_ekle_button.pack(padx=1 , pady=1 , side='right')
        
        def customer_informations(customer):
            label.config(text=customer)
            frame.mainloop()
            frame.place(relheight=0.70 , relwidth=0.1 ,relx=0.005 , rely= 0.25)
            print(liste)

        ##BUTTON SETTINGS
        for i in liste:    
                binder(tk.Label(frame, text=i, width=16,bg='#C5C5C5' ,  relief='groove'))

        tk.Button(self, text="Return to 1",
                  command=lambda: master.switch_frame(PageOne)).pack()
        tk.Button(self, text="Return to 2",
                  command=lambda: master.switch_frame(PageTwo)).pack()

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