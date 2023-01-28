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
        
        main_canvas = tk.Canvas(self , width=SCREEN_WIDTH , height=SCREEN_HEIGTH , bg='black')
        main_canvas.pack()

        frame = tk.Frame(self , bg='white')
        frame.place(relheight=0.70 , relwidth=0.1 ,relx=0.005 , rely= 0.25)
        
        ##BUTTON SETTINGS
        def binder(button):
            button.bind('<Button-1>', lambda x=button: print(button))
            button.bind('<Enter>', lambda x=button : button.config(bg='#696969', fg='white'))
            button.bind('<Leave>', lambda x=button : button.config(bg='#C5C5C5', fg='black'))
        But = tk.Label(frame, text='Hi',bg='#C5C5C5' ,  relief='groove')
        But.pack(padx=10 , pady=10 , side='top')
        binder(But)
        But2 = tk.Label(frame, text='Hi',bg='#C5C5C5' ,  relief='groove')
        But2.pack(padx=10 , pady=10 , side='top', )
        binder(But2)

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