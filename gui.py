import tkinter as tk
from tkinter import Canvas, ttk
from tkinter import messagebox
import random

class Moulin(tk.Frame):
    def __init__(self, parent, bg="white", *args, **kwargs):
        tk.Frame.__init__(self, parent, bg=bg, *args, **kwargs)
        self.parent  = parent

        self.init_tag = "FREE_CASE"
        
        self.width  = 1687 #self.parent.winfo_screenwidth()  // 4
        self.height = 812  #self.parent.winfo_screenheight() // 6
        
        self.start_page()
        self.parent.geometry(f'{self.width}x{self.height}')
        self.parent.resizable(1, 0)
        
        self.mbg = "#474747"
        self.gbg = 'ivory'
        self.sbg = "white"
        
        self.status_area = StatusArea(self, bg=self.sbg, width=self.width//2, height=self.height)
        self.game_area = GameArea(self, bg=self.gbg,  width=self.width//2, height=self.height)
        
        self.parent.attributes('-fullscreen', False)
        self.full_screen_state = False
        
        self.parent.bind("<F2>", self.start_page)
        self.parent.bind("<F11>", self.toggle_full_screen)
        self.parent.bind("<Escape>", self.quit_full_screen)

        self.show_frame()
   
    def start_page(self, event=None):
        StartPage(self, width=self.width, height=self.height)
        
    def show_frame(self):
        self.rowconfigure(0, weight=1, minsize=812)
        self.columnconfigure(0, weight=1, minsize=866)
        self.columnconfigure(1, weight=1)

        self.game_area.grid(row=0, column=0, sticky="nswe")
        self.status_area.grid(row=0, column=1, sticky="nswe")    
    
    def toggle_full_screen(self, event):
        self.full_screen_state = not self.full_screen_state
        self.parent.attributes("-fullscreen", self.full_screen_state)
        
    def quit_full_screen(self, event):
        self.full_screen_state = False
        self.parent.attributes("-fullscreen", self.full_screen_state)

def run_moulin():
    root = tk.Tk()
    root.title("Moulin")
    Moulin(root).pack(fill="both", expand=True)
    root.mainloop()
    
class StartPage(tk.Toplevel):
    def __init__(self, parent, width=100, height=50,  bg='white', bd=5, *args, **kwargs):
        tk.Toplevel.__init__(self, parent, width=width, height=height, bg=bg, *args, **kwargs)
        self.parent = parent
        
        self.bg = bg
        
        width  = width  // 3
        height = height // 4
        
        self.resizable(0, 0)
        self.overrideredirect(True) # remove title bar
        
        self.vlist = ['Vitesse - Lente', 'Vitesse - Normale', 'Vitesse - Rapide']
        
        self.pad = 10
        
        self.bnt_width = 8
        self.bnt_height = 1
        self.bnt_font = 'Terminal 12 bold'
        
        height1 = 50
        height3 = 50
        height2 = height - (height1+height3)
        
        self.is_human1 = tk.IntVar(value=1)
        self.is_human2 = tk.IntVar()
        
        self.is_computer1 = tk.IntVar()
        self.is_computer2 = tk.IntVar(value=1)
        
        self.frame1 = tk.Frame(self, width=width, height=height1, bg=bg)
        self.frame2 = tk.Frame(self, width=width, height=height2, bg=bg, bd=2, highlightthickness=1)
        self.frame3 = tk.Frame(self, width=width, height=height3, bg='#EFEFEF')
        
        self.frame21 = tk.Frame(self.frame2, width=width//2, height=height2, bg=bg)
        self.frame22 = tk.Frame(self.frame2, width=width//2, height=height2, bg=bg)
        
        self.label = tk.Label(self.frame1, text='Nouvelle Partie',
                              foreground="black", background=bg,
                              font='Terminal 16 bold')
        
        self.btn_play = tk.Button(self.frame3, text ='Jouer',
                                  width=self.bnt_width,
                                  height=self.bnt_height,
                                  bg='#0280FF', fg='white',
                                  font=self.bnt_font,
                                  relief=tk.FLAT,
                                  activeforeground='white',
                                  activebackground='#3D99F4',
                                  command=self.play)
        
        self.btn_quit = tk.Button(self.frame3, text ='Quitter',
                                  width=self.bnt_width,
                                  height=self.bnt_height,
                                  bg='#EFEFEF', fg='black',
                                  font=self.bnt_font,
                                  relief=tk.FLAT,
                                  activeforeground='black',
                                  activebackground='red',
                                  command=self.close)
        
        style= ttk.Style()
        style.theme_use('clam')
        style.configure("TCombobox", fieldbackground="white", background="white")
        
        self.option_add('*TCombobox*Listbox*selectBackground', '#0280FF')
        self.option_add('*TCombobox*Listbox*selectBackground', '#0280FF')
        self.option_add('*TCombobox*Listbox*Foreground', "#5E5E5E")
        self.option_add('*TCombobox*Listbox*selectForeground', "#5E5E5E")
        self.option_add('*TCombobox*Listbox*selectBackground', '#0280FF')
        
        self.combobox = ttk.Combobox(self.frame1, values=self.vlist,
                                     width=20, font="Verdana 10")
        self.combobox.current(0)
        
        self.label.pack(side=tk.LEFT,     anchor="w", padx=self.pad, pady=self.pad)
        self.combobox.pack(side=tk.RIGHT, anchor="e", padx=self.pad, pady=self.pad+40)
        
        self.set_player()
        
        self.btn_quit.pack(side=tk.LEFT,  anchor="w", padx=self.pad, pady=self.pad)
        self.btn_play.pack(side=tk.RIGHT, anchor="e", padx=self.pad, pady=self.pad)
        
        self.show_frame()
        
        self.state1 = (self.is_human1.get(), self.is_computer1.get())
        self.state2 = (self.is_human2.get(), self.is_computer2.get())
                
        self.bind("<Button-1>", self.on_checkbutton)
        
    def play(self):
        self.destroy()
        #messagebox.showinfo("Moulin", "Welcome to Moulin Game!")
        
    def show_frame(self):
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)

        self.frame1.grid(row=0, column=0, sticky="ew")
        self.frame2.grid(row=1, column=0, sticky="nsew")
        self.frame3.grid(row=2, column=0, sticky="ew")
        
        self.frame21.pack(side=tk.LEFT,  anchor="nw")
        self.frame22.pack(side=tk.RIGHT, anchor="ne")
        
    def set_player(self):        
        #===========================Player 1============================#
        self.label1 = tk.Label(self.frame21, text='Joueur 1 - Blue',
                 foreground="black", background=self.bg,
                 font='Terminal 14 bold', anchor="w")
        
        cbh1 = tk.Checkbutton(self.frame21, text="Humain", variable=self.is_human1,
                              onvalue=1, offvalue=0, height=2, width=10,
                              foreground="black", background=self.bg,
                              font='Terminal 10',activebackground=self.bg,
                              highlightthickness=0,bd=0, anchor="w")
        cbo1 = tk.Checkbutton(self.frame21, text="Ordinateur", variable=self.is_computer1,
                              onvalue=1, offvalue=0, height=2, width=10,
                              foreground="black", background=self.bg,
                              font='Terminal 10',activebackground=self.bg,
                              highlightthickness=0,bd=0, anchor="w")
        
        #===========================Player 2============================#
        self.label2 = tk.Label(self.frame22, text='Joueur 2 - Rouge',
                 foreground="black", background=self.bg,
                 font='Terminal 14 bold', anchor="e")
        
        cbh2 = tk.Checkbutton(self.frame22, text='Humain', variable=self.is_human2,
                              onvalue=1, offvalue=0, height=2, width=10,
                              foreground='black', background=self.bg,
                              font='Terminal 10',activebackground=self.bg,
                              highlightthickness=0,bd=0, anchor="w")
        cbo2 = tk.Checkbutton(self.frame22, text='Ordinateur', variable=self.is_computer2,
                              onvalue=1, offvalue=0, height=2, width=10,
                              foreground='black', background=self.bg,
                              font='Terminal 10',activebackground=self.bg,
                              highlightthickness=0,bd=0, anchor="w")
        
        
        #==========================Player 1 and 2==========================#
        self.label1.pack(padx=(self.pad+40, self.pad+40), pady=(self.pad+10, 0))
        self.label2.pack(padx=(self.pad, self.pad+40), pady=(self.pad+10, 0))
        
        cbh1.pack(padx=(self.pad+40, self.pad+40), anchor="w")
        cbo1.pack(padx=(self.pad+40, self.pad+40), pady=(self.pad, self.pad+10), anchor="w")
        
        cbh2.pack(anchor="w")
        cbo2.pack(pady=(self.pad, self.pad+10), anchor="w")
        
    def on_checkbutton(self, event=None):
        #==========Player 1============#
        if self.state1[0] != self.is_human1.get() and\
           self.state1[1] == self.is_computer1.get():
            self.is_human1.set(1)
            self.is_computer1.set(0)
            
        if self.state1[0] == self.is_human1.get() and\
           self.state1[1] != self.is_computer1.get():
            self.is_human1.set(0)
            self.is_computer1.set(1)
        
        #==========Player 2============#    
        if self.state2[0] != self.is_human2.get() and\
           self.state2[1] == self.is_computer2.get():
            self.is_human2.set(1)
            self.is_computer2.set(0)
        
        if self.state2[0] == self.is_human2.get() and\
           self.state2[1] != self.is_computer2.get():
            self.is_human2.set(0)
            self.is_computer2.set(1)
            
        self.state1 = (self.is_human1.get(), self.is_computer1.get())
        self.state2 = (self.is_human2.get(), self.is_computer2.get())
    
    def close(self):
        self.destroy()
        self.parent.quit()

class Menu(tk.Frame):
    def __init__(self, parent, bg, height, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        
        s = 6*" " 
        tk.Label(self,
              text=f'[F1] À propos {s} [F2] Nouvelle partie {s} [F11] Full screen {s} [ESC] Quitter',
              foreground="white", background=bg, height=height,
              relief="raised", font='Terminal 12 bold').pack(anchor=tk.N, fill=tk.X)
    
    def about(self, event):
        messagebox.showinfo('À propos',
             message="Bienvenue dans le jeu du Moulin avec Tkinter.\n\n"
                     "Le jeu du moulin est un jeu de société traditionnel en Europe.\n\n"
                     "Le tablier de jeu existait déjà dans la Rome antique.\n\n"
                     "Aussi appelé jeu du charret (en Suisse), certains lui donnent le nom médiéval de jeu de mérelles.")

class GameArea(tk.Frame):
    #count_on_resize = 0
    def __init__(self, parent, bg, width, height, *args, **kwargs):
        tk.Frame.__init__(self, parent, width=width, height=height, bg=bg, *args, **kwargs)
        self.parent = parent
        self.bg = bg

        #self.bind("<Configure>", self.on_resize)
        
        self.width  = self.winfo_reqwidth()
        self.height = self.winfo_reqheight()

        self.init_color = "#595959"
        self.init_tag = self.parent.init_tag

        self.move_in_plate = tk.BooleanVar()
        self.move_in_plate.set(False)

        self.selected_pion = tk.StringVar()
        self.selected_pion.set("")

        self.sselected_pion = tk.StringVar()
        self.sselected_pion.set("")

        self.count_select = 0
        
        self.x0 = 60
        self.y0 = 60
        
        self.offset1 = 100
        self.offset2 = 2*self.offset1
                
        self.d = 10
        self.csize = 25
        self.psize = 14

        self.canvas = tk.Canvas(self, bg=bg,
                               width=self.width,
                               height=self.height, 
                               highlightthickness=0)
        
        self.canvas.addtag_all("all")

        self.canvas.pack(fill="both", expand=True)

        self.draw_cross(self.x0, self.y0, self.width, self.height, self.offset1)
                
        self.draw_square(self.x0, self.y0, self.width, self.height)               #square 1
        
        self.draw_square(self.x0, self.y0, self.width, self.height, self.offset1) #square 2
        
        self.draw_square(self.x0, self.y0, self.width, self.height, self.offset2, fill=bg) #square 3
        
        self.draw_case(self.x0, self.y0, self.width, self.height, self.d, self.offset1, fill=self.init_color)

        self.cases = [self.canvas11, self.canvas14, self.canvas17,
                      self.canvas22, self.canvas24, self.canvas26,
                      self.canvas33, self.canvas34, self.canvas35,
                      self.canvas41, self.canvas42, self.canvas43,
                      self.canvas45, self.canvas46, self.canvas47,
                      self.canvas53, self.canvas54, self.canvas55,
                      self.canvas62, self.canvas64, self.canvas66,
                      self.canvas71, self.canvas74, self.canvas77] 
        
        for i in range(len(self.cases)):
            
            self.cases[i].tag_bind(self.init_tag, "<Enter>", lambda event, canvas=self.cases[i]: self.check_hand_enter(canvas=canvas))
            self.cases[i].tag_bind(self.init_tag, "<Leave>", lambda event, canvas=self.cases[i]: self.check_hand_leave(canvas=canvas))

            self.cases[i].tag_bind(self.parent.status_area.tag_name1, "<Enter>", lambda event, canvas=self.cases[i]: self.check_hand_enter(canvas=canvas))
            self.cases[i].tag_bind(self.parent.status_area.tag_name1, "<Leave>", lambda event, canvas=self.cases[i]: self.check_hand_leave(canvas=canvas))

            self.cases[i].tag_bind(self.parent.status_area.tag_name2, "<Enter>", lambda event, canvas=self.cases[i]: self.check_hand_enter(canvas=canvas))
            self.cases[i].tag_bind(self.parent.status_area.tag_name2, "<Leave>", lambda event, canvas=self.cases[i]: self.check_hand_leave(canvas=canvas))

            self.cases[i].bind("<Button-1>", lambda event, canvas=self.cases[i]: self.pion_click(event, canvas=canvas))
    
    def pion_click(self, event=None, canvas=None):        
        id = 1
        clicked_color = canvas.itemcget(id, "fill")
        clicked_tag   = canvas.itemcget(id, "tag").split(' ')[0]
        
        if self.check_case(clicked_tag) and self.parent.status_area.sa_selected_pion.get():
            color, tag = self.parent.status_area.sa_selected_pion.get().split(' ')
            self.move_pion(canvas, id, color, tag)

        if self.move_in_plate.get():
            clicked_pion = clicked_color + ' ' + clicked_tag + ' ' + str(self.cases.index(canvas))
            
            if self.count_select == 0:
                self.selected_pion.set(clicked_pion)
            if self.count_select == 1 :self.sselected_pion.set(clicked_pion)
            
            self.move_pion(canvas, id, clicked_color, clicked_tag)

        if self.parent.status_area.sa_start_second_part.get():
            self.move_in_plate.set(True)

        self.parent.status_area.sa_selected_pion.set("")

        self.count_select +=1
        if self.count_select == 2: self.count_select = 0
    
    def check_case(self, tag_name):
        return self.init_tag == tag_name
    
    def check_hand_enter(self, event=None, canvas=None):
        clicked_color = canvas.itemcget(1, "fill")
        if clicked_color == self.init_color:
            canvas.config(cursor="plus")
        else:canvas.config(cursor="hand1")

    def check_hand_leave(self, event=None, canvas=None):
        canvas.config(cursor="")

    def move_pion(self, case, id, color, tag):
        if self.move_in_plate.get() and self.check_case(tag) and \
          self.init_color not in self.selected_pion.get() and \
           self.init_color in self.sselected_pion.get():
            
            color, tag, idx = self.selected_pion.get().split(' ')
            
            case.itemconfig(id, fill=color)
            case.itemconfig(id, tag=tag)
            
            # clean after leaved move
            idx = int(idx)
            self.cases[idx].itemconfig(id, fill=self.init_color)
            self.cases[idx].itemconfig(id, tag=self.init_tag)

            self.selected_pion.set("")
            self.sselected_pion.set("")

        else:
            case.itemconfig(id, fill=color)
            case.itemconfig(id, tag=tag)

    def on_resize(self, event):
        print(event.width, event.height)
        wscale = float(event.width)/self.width
        hscale = float(event.height)/self.height
        self.width  = event.width
        self.height = event.height
        self.canvas.config(width=self.width, height=self.height)
        self.canvas.scale("all", 0, 0, wscale, hscale)
        
    def draw_square(self, x0, y0, x1, y1, offset=0, bd=2, fill=''):
        self.canvas.create_rectangle(x0+offset, y0+offset,
                                     x0+(x1 - 2*x0)-offset,
                                     y0+(y1 - 2*y0)-offset,
                                     width=bd,
                                     fill=fill)
    
    def draw_cross(self, x0, y0, x1, y1, offset, bd=2, fill='black'):
        
        self.canvas.create_line(x0, (y0+(y1 - 2*y0)+offset)//2-20,
                                x0+(x1 - 2*x0),(y0+(y1 - 2*y0)+offset)//2-20,
                                width=bd, fill=fill)
        
        self.canvas.create_line((x0+(x1 - 2*x0)+offset)//2-20, y0,
                                (x0+(x1 - 2*x0)+offset)//2-20, y0+(y1 - 2*y0),
                                width=bd, fill=fill)
        
    def draw_case(self, x0, y0, x1, y1, d, offset=0, fill="black"):
        cx0, cy0 = 0, 0

        w4 = (x0+(x1 - 2*x0)+offset)//2-25
        
        h1 = y0-5
        h2 = (y0+(y1 - 2*y0)+offset)//6+12
        h3 = y0+2*offset-6
        h4 = (y0+(y1 - 2*y0)+offset)//2-25
        h5 = h4+offset+45
        h6 = h4+2*offset+45
        h7 = y0+(y1 - 2*y0)-6
        
        #============================1============================#
        x11,y11  = (x0-5), h1
        self.cx11, self.cy11 = (x0-13), (y0-13)
        self.canvas11 = tk.Canvas(self.canvas, bg=self.bg,
                               width=self.csize,
                               height=self.csize, 
                               highlightthickness=0)
        #self.c11 = self.canvas.create_oval(x11, y11, x11+d, y11+d, fill=fill, outline="")
        self.c11 = self.canvas11.create_oval(cx0, cy0, self.csize, self.csize, fill=fill, outline="", tag=self.init_tag)
        self.canvas11.place(x=self.cx11, y=self.cy11)
        
        x14,y14  = w4, h1
        self.cx14, self.cy14 = ((x0+(x1 - 2*x0)+offset)//2-33), self.cy11
        self.canvas14 = tk.Canvas(self.canvas, bg=self.bg,
                               width=self.csize,
                               height=self.csize, 
                               highlightthickness=0)
        #self.c14 = self.canvas.create_oval(x14, y14, x14+d, y14+d, fill=fill, outline="")
        self.c14 = self.canvas14.create_oval(cx0, cy0, self.csize, self.csize, fill=fill, outline="", tag=self.init_tag)
        self.canvas14.place(x=self.cx14, y=self.cy14)
        
        x17,y17  = (x0+(x1 - 2*x0)-6), h1
        self.cx17, self.cy17 = (x0+(x1 - 2*x0)-12), self.cy11
        self.canvas17 = tk.Canvas(self.canvas, bg=self.bg,
                               width=self.csize,
                               height=self.csize, 
                               highlightthickness=0)
        #self.c17 = self.canvas.create_oval(x17, y17, x17+d, y17+d, fill=fill, outline="")
        self.c17 = self.canvas17.create_oval(cx0, cy0, self.csize, self.csize, fill=fill, outline="", tag=self.init_tag)
        self.canvas17.place(x=self.cx17, y=self.cy17)
        
        #============================2============================#
        x22,y22  = (x0+offset-4), h2
        self.cx22, self.cy22 = (x0+offset-13), (y0+(y1 - 2*y0)+offset)//6+5
        self.canvas22 = tk.Canvas(self.canvas, bg=self.bg,
                               width=self.csize,
                               height=self.csize, 
                               highlightthickness=0)
        #self.c22 = self.canvas.create_oval(x22, y22, x22+d, y22+d, fill=fill, outline="")
        self.c22 = self.canvas22.create_oval(cx0, cy0, self.csize, self.csize, fill=fill, outline="", tag=self.init_tag)
        self.canvas22.place(x=self.cx22, y=self.cy22)
        
        x24,y24  = w4, h2
        self.cx24, self.cy24 = self.cx14, self.cy22
        self.canvas24 = tk.Canvas(self.canvas, bg=self.bg,
                               width=self.csize,
                               height=self.csize, 
                               highlightthickness=0)
        #self.c24 = self.canvas.create_oval(x24, y24, x24+d, y24+d, fill=fill, outline="")
        self.c24 = self.canvas24.create_oval(cx0, cy0, self.csize, self.csize, fill=fill, outline="", tag=self.init_tag)
        self.canvas24.place(x=self.cx24, y=self.cy24)
        
        x26,y26  = (x0+(x1 - 2*x0)-offset-6), h2
        self.cx26, self.cy26 = (x0+(x1 - 2*x0)-offset-13), self.cy22
        self.canvas26 = tk.Canvas(self.canvas, bg=self.bg,
                               width=self.csize,
                               height=self.csize, 
                               highlightthickness=0)
        #self.c26 = self.canvas.create_oval(x26, y26, x26+d, y26+d, fill=fill, outline="")
        self.c26 = self.canvas26.create_oval(cx0, cy0, self.csize, self.csize, fill=fill, outline="", tag=self.init_tag)
        self.canvas26.place(x=self.cx26, y=self.cy26)
        
        #============================3============================#
        x33,y33  = (x0+2*offset-4), h3
        self.cx33, self.cy33 = (x0+2*offset-13), y0+2*offset-13
        self.canvas33 = tk.Canvas(self.canvas, bg=self.bg,
                               width=self.csize,
                               height=self.csize, 
                               highlightthickness=0)
        #self.c33 = self.canvas.create_oval(x33, y33, x33+d, y33+d, fill=fill, outline="")
        self.c33 = self.canvas33.create_oval(cx0, cy0, self.csize, self.csize, fill=fill, outline="", tag=self.init_tag)
        self.canvas33.place(x=self.cx33, y=self.cy33)

        x34,y34  = w4, h3
        self.cx34, self.cy34 = self.cx14, self.cy33
        self.canvas34 = tk.Canvas(self.canvas, bg=self.bg,
                               width=self.csize,
                               height=self.csize, 
                               highlightthickness=0)
        #self.c34 = self.canvas.create_oval(x34, y34, x34+d, y34+d, fill=fill, outline="")
        self.c34 = self.canvas34.create_oval(cx0, cy0, self.csize, self.csize, fill=fill, outline="", tag=self.init_tag)
        self.canvas34.place(x=self.cx34, y=self.cy34)
        
        x35,y35  = (x0+(x1 - 2*x0)-2*offset-6), h3
        self.cx35, self.cy35 = (x0+(x1 - 2*x0)-2*offset-13), self.cy33
        self.canvas35 = tk.Canvas(self.canvas, bg=self.bg,
                               width=self.csize,
                               height=self.csize, 
                               highlightthickness=0)
        #self.c35 = self.canvas.create_oval(x35, y35, x35+d, y35+d, fill=fill, outline="")
        self.c35 = self.canvas35.create_oval(cx0, cy0, self.csize, self.csize, fill=fill, outline="", tag=self.init_tag)
        self.canvas35.place(x=self.cx35, y=self.cy35)
        
        #============================4============================#
        x41,y41  = (x0-6), h4
        self.cx41, self.cy41 = self.cx11, (y0+(y1 - 2*y0)+offset)//2-33
        self.canvas41 = tk.Canvas(self.canvas, bg=self.bg,
                               width=self.csize,
                               height=self.csize, 
                               highlightthickness=0)
        #self.c41 = self.canvas.create_oval(x41, y41, x41+d, y41+d, fill=fill, outline="")
        self.c41 = self.canvas41.create_oval(cx0, cy0, self.csize, self.csize, fill=fill, outline="", tag=self.init_tag)
        self.canvas41.place(x=self.cx41, y=self.cy41)
        
        x42,y42  = (x0+(x1 - 2*x0)//8+5), h4
        self.cx42, self.cy42 = (x0+(x1 - 2*x0)//8-3), self.cy41
        self.canvas42 = tk.Canvas(self.canvas, bg=self.bg,
                               width=self.csize,
                               height=self.csize, 
                               highlightthickness=0)
        #self.c42 = self.canvas.create_oval(x42, y42, x42+d, y42+d, fill=fill, outline="")
        self.c42 = self.canvas42.create_oval(cx0, cy0, self.csize, self.csize, fill=fill, outline="", tag=self.init_tag)
        self.canvas42.place(x=self.cx42, y=self.cy42)
        
        x43,y43  = (x0+(x1 - 2*x0)//4+15), h4
        self.cx43, self.cy43 = (x0+(x1 - 2*x0)//4+8), self.cy41
        self.canvas43 = tk.Canvas(self.canvas, bg=self.bg,
                               width=self.csize,
                               height=self.csize, 
                               highlightthickness=0)
        #self.c43 = self.canvas.create_oval(x43, y43, x43+d, y43+d, fill=fill, outline="")
        self.c43 = self.canvas43.create_oval(cx0, cy0, self.csize, self.csize, fill=fill, outline="", tag=self.init_tag)
        self.canvas43.place(x=self.cx43, y=self.cy43)
        
        x45,y45  = (x0+(x1 - 2*x0)-(x0+(x1 - 2*x0)//5+2)), h4
        self.cx45, self.cy45 = (x0+(x1 - 2*x0)-(x0+(x1 - 2*x0)//5+9)), self.cy41
        self.canvas45 = tk.Canvas(self.canvas, bg=self.bg,
                               width=self.csize,
                               height=self.csize, 
                               highlightthickness=0)
        #self.c45 = self.canvas.create_oval(x45, y45, x45+d, y45+d, fill=fill, outline="")
        self.c45 = self.canvas45.create_oval(cx0, cy0, self.csize, self.csize, fill=fill, outline="", tag=self.init_tag)
        self.canvas45.place(x=self.cx45, y=self.cy45)
        
        x46,y46  = (x0+(x1 - 2*x0)-5-(x0+(x1 - 2*x0)//16-5)), h4
        self.cx46, self.cy46 = (x0+(x1 - 2*x0)-5-(x0+(x1 - 2*x0)//16+3)), self.cy41
        self.canvas46 = tk.Canvas(self.canvas, bg=self.bg,
                               width=self.csize,
                               height=self.csize, 
                               highlightthickness=0)
        #self.c46 = self.canvas.create_oval(x46, y46, x46+d, y46+d, fill=fill, outline="")
        self.c46 = self.canvas46.create_oval(cx0, cy0, self.csize, self.csize, fill=fill, outline="", tag=self.init_tag)
        self.canvas46.place(x=self.cx46, y=self.cy46)
        
        x47,y47  = (x0+(x1 - 2*x0)-5), h4
        self.cx47, self.cy47 = (x0+(x1 - 2*x0)-13), self.cy41
        self.canvas47 = tk.Canvas(self.canvas, bg=self.bg,
                               width=self.csize,
                               height=self.csize, 
                               highlightthickness=0)
        #self.c47 = self.canvas.create_oval(x47, y47, x47+d, y47+d, fill=fill, outline="")
        self.c47 = self.canvas47.create_oval(cx0, cy0, self.csize, self.csize, fill=fill, outline="", tag=self.init_tag)
        self.canvas47.place(x=self.cx47, y=self.cy47)
        
        #============================5============================#
        x53,y53  = (x0+2*offset-4), h5
        self.cx53, self.cy53 = self.cy33, self.cy41+offset+45
        self.canvas53 = tk.Canvas(self.canvas, bg=self.bg,
                               width=self.csize,
                               height=self.csize, 
                               highlightthickness=0)
        #self.c53 = self.canvas.create_oval(x53, y53, x53+d, y53+d, fill=fill, outline="")
        self.c53 = self.canvas53.create_oval(cx0, cy0, self.csize, self.csize, fill=fill, outline="", tag=self.init_tag)
        self.canvas53.place(x=self.cx53, y=self.cy53)
        
        x54,y54  = w4, h5
        self.cx54, self.cy54 = self.cx14, self.cy53
        self.canvas54 = tk.Canvas(self.canvas, bg=self.bg,
                               width=self.csize,
                               height=self.csize, 
                               highlightthickness=0)
        #self.c54 = self.canvas.create_oval(x54, y54, x54+d, y54+d, fill=fill, outline="")
        self.c54 = self.canvas54.create_oval(cx0, cy0, self.csize, self.csize, fill=fill, outline="", tag=self.init_tag)
        self.canvas54.place(x=self.cx54, y=self.cy54)
        
        x55,y55  = (x0+(x1 - 2*x0)-2*offset-6), h5
        self.cx55, self.cy55 = self.cx35, self.cy53
        self.canvas55 = tk.Canvas(self.canvas, bg=self.bg,
                               width=self.csize,
                               height=self.csize, 
                               highlightthickness=0)
        #self.c55 = self.canvas.create_oval(x55, y55, x55+d, y55+d, fill=fill, outline="")
        self.c55 = self.canvas55.create_oval(cx0, cy0, self.csize, self.csize, fill=fill, outline="", tag=self.init_tag)
        self.canvas55.place(x=self.cx55, y=self.cy55)
        
        #============================6============================#
        x62,y62  = (x0+offset-4), h6
        self.cx62, self.cy62 = self.cx22, self.cy41+2*offset+45
        self.canvas62 = tk.Canvas(self.canvas, bg=self.bg,
                               width=self.csize,
                               height=self.csize, 
                               highlightthickness=0)
        #self.c62 = self.canvas.create_oval(x62, y62, x62+d, y62+d, fill=fill, outline="")
        self.c62 = self.canvas62.create_oval(cx0, cy0, self.csize, self.csize, fill=fill, outline="", tag=self.init_tag)
        self.canvas62.place(x=self.cx62, y=self.cy62)
        
        x64,y64  = w4, h6
        self.cx64, self.cy64 = self.cx14, self.cy62
        self.canvas64 = tk.Canvas(self.canvas, bg=self.bg,
                               width=self.csize,
                               height=self.csize, 
                               highlightthickness=0)
        #self.c64 = self.canvas.create_oval(x64, y64, x64+d, y64+d, fill=fill, outline="")
        self.c64 = self.canvas64.create_oval(cx0, cy0, self.csize, self.csize, fill=fill, outline="", tag=self.init_tag)
        self.canvas64.place(x=self.cx64, y=self.cy64)
        
        x66,y66  = (x0+(x1 - 2*x0)-offset-6), h6
        self.cx66, self.cy66 = self.cx26, self.cy62
        self.canvas66 = tk.Canvas(self.canvas, bg=self.bg,
                               width=self.csize,
                               height=self.csize, 
                               highlightthickness=0)
        #self.c66 = self.canvas.create_oval(x66, y66, x66+d, y66+d, fill=fill, outline="")
        self.c66 = self.canvas66.create_oval(cx0, cy0, self.csize, self.csize, fill=fill, outline="", tag=self.init_tag)
        self.canvas66.place(x=self.cx66, y=self.cy66)
        
        #============================7============================#
        x71,y71  = (x0-6), h7
        self.cx71, self.cy71 = self.cx41, y0+(y1 - 2*y0)-13
        self.canvas71 = tk.Canvas(self.canvas, bg=self.bg,
                               width=self.csize,
                               height=self.csize, 
                               highlightthickness=0)
        #self.c71 = self.canvas.create_oval(x71, y71, x71+d, y71+d, fill=fill, outline="")
        self.c71 = self.canvas71.create_oval(cx0, cy0, self.csize, self.csize, fill=fill, outline="", tag=self.init_tag)
        self.canvas71.place(x=self.cx71, y=self.cy71)
        
        x74,y74  = w4, h7
        self.cx74, self.cy74 = self.cx14, self.cy71
        self.canvas74 = tk.Canvas(self.canvas, bg=self.bg,
                               width=self.csize,
                               height=self.csize, 
                               highlightthickness=0)
        #self.c74 = self.canvas.create_oval(x74, y74, x74+d, y74+d, fill=fill, outline="")
        self.c74 = self.canvas74.create_oval(cx0, cy0, self.csize, self.csize, fill=fill, outline="", tag=self.init_tag)
        self.canvas74.place(x=self.cx74, y=self.cy74)
        
        x77,y77  = (x0+(x1 - 2*x0)-6), h7
        self.cx77, self.cy77 = self.cx17, self.cy71
        self.canvas77 = tk.Canvas(self.canvas, bg=self.bg,
                               width=self.csize,
                               height=self.csize, 
                               highlightthickness=0)
        #self.c77 = self.canvas.create_oval(x77, y77, x77+d, y77+d, fill=fill, outline="")
        self.c77 = self.canvas77.create_oval(cx0, cy0, self.csize, self.csize, fill=fill, outline="", tag=self.init_tag)
        self.canvas77.place(x=self.cx77, y=self.cy77)


class StatusArea(tk.Frame):
    sa_count_pion = 0
    def __init__(self, parent, width, height, bg, *args, **kwargs):
        tk.Frame.__init__(self, parent, width=width, height=height, bg=bg, *args, **kwargs)
        self.parent = parent
        
        self.rule = "Le jeu commence avec un plateau vide. Les joueurs\n" + \
                    "placent à tour de rôle leurs pions sur un point  \n" + \
                    "libre du plateau. Pendant cette phase, il est    \n" + \
                    "interdit de déplacer les pions déjà placés sur   \n"   +\
                    "le plateau.                                      \n" + \
                    "Si un joueur forme un moulin, il retire un pion  \n" + \
                    "(en dehors d’un moulin éventuel) à son adversaire."
        
        self.width = width
        self.height = height

        self.d = 25
        self.psize = 5
        self.num_pion = 9
        self.x0, self.y0  = 0, 0
        
        self.color1 = '#1401A3'
        self.color2 = '#C10105'

        self.bg = bg
        self.pad = 9
        
        self.bnt_width = 15
        self.bnt_height = 1
        
        self.bnt_font = 'Terminal 10 bold'

        self.spion = tk.IntVar()
        self.spion.set(1)

        self.status = tk.StringVar()
        self.status.set("C'est au tour de Joueur 1")

        self.phase_status = tk.StringVar()
        self.phase_status.set("Première Phase")

        self.rule_status = tk.StringVar()
        self.rule_status.set("Règles du jeu")

        self.rule_msg_status = tk.StringVar()
        self.rule_msg_status.set(self.rule)

        self.sa_selected_pion = tk.StringVar ()
        self.sa_selected_pion.set("")

        self.sa_start_second_part = tk.BooleanVar()
        self.sa_start_second_part.set(False)
        
        height1 = 50
        height3 = 50
        height2 = height - (height1+height3)
        
        self.frame1 = tk.Frame(self, width=width, height=height1, bg=bg)
        self.frame2 = tk.Frame(self, width=width, height=height2, bg='#B5B5B5', highlightthickness=1)
        self.frame3 = tk.Frame(self, width=width, height=height3, bg='#EFEFEF')
        
        self.height21 = 1
        self.height22 = self.height21
        self.height23 = height2 - 2*self.height21
        
        self.frame21 = tk.Frame(self.frame2, width=width, height=self.height21, bg='#B5B5B5')
        self.frame22 = tk.Frame(self.frame2, width=width, height=self.height22, bg='#B5B5B5')
        self.frame23 = tk.Frame(self.frame2, width=width, height=self.height23, bg=bg)
        
        self.label = tk.Label(self.frame1, textvariable=self.phase_status,
                              foreground="black", background=bg,
                              font='Terminal 13 bold')

        self.label_status = tk.Label(self.frame1, textvariable=self.status,
                              foreground=self.color1, background=bg,
                              font='Terminal 10 bold')

        self.label_trule = tk.Label(self.frame23, textvariable=self.rule_status,
                              foreground="black", background=bg,
                              font='Terminal 12 bold')

        self.label_rule = tk.Label(self.frame23, textvariable=self.rule_msg_status,
                              foreground="black", background=bg,
                              font='Terminal 10')

        #===========================Player 1============================#
        self.label1 = tk.Label(self.frame21, text='Joueur 1',
                 foreground="white", background=self.color1,
                 font='Terminal 12 bold')

        #===========================Player 2============================#
        self.label2 = tk.Label(self.frame22, text='Joueur 2',
                 foreground="white", background=self.color2,
                 font='Terminal 12 bold')
        
        self.btn_quit = tk.Button(self.frame3, text ='Quitter',
                                  width=8,
                                  height=self.bnt_height,
                                  bg='#EFEFEF', fg='black',
                                  font=self.bnt_font,
                                  relief=tk.FLAT,
                                  activeforeground='black',
                                  activebackground='red',
                                  command=self.quit)
         
        self.btn_about = tk.Button(self.frame3, text ='À propos',
                                  width=8,
                                  height=self.bnt_height,
                                  bg='#727272', fg='white',
                                  font=self.bnt_font,
                                  relief=tk.FLAT,
                                  activeforeground='white',
                                  activebackground='#969696',
                                  command=self.about)
        
        self.btn_new = tk.Button(self.frame3, text ='Nouvelle Partie',
                                  width=self.bnt_width,
                                  height=self.bnt_height,
                                  bg='#0280FF', fg='white',
                                  font=self.bnt_font,
                                  relief=tk.FLAT,
                                  activeforeground='white',
                                  activebackground='#3D99F4',
                                  command=self.parent.start_page)
        
        self.label.pack(side=tk.LEFT, padx=self.pad, pady=self.pad)
        
        self.label1.pack(side=tk.LEFT, padx=self.pad, pady=1)
        self.label_status.pack(side=tk.RIGHT, padx=self.pad, pady=self.pad)
        self.label2.pack(side=tk.LEFT, padx=self.pad, pady=1)              
        
        self.btn_quit.pack(side=tk.LEFT, padx=self.pad, pady=self.pad)
        self.btn_about.pack(side=tk.LEFT, anchor='center', expand=True, padx=self.pad, pady=self.pad)
        self.btn_new.pack(side=tk.RIGHT, padx=self.pad, pady=self.pad)
        
        self.label_trule.pack(side=tk.TOP, anchor='center', padx=self.pad, pady=self.pad)
        self.label_rule.pack(side=tk.TOP, anchor='center', padx=self.pad, pady=(0, self.pad))
        
        self.show_frame()
        
        self.canvas1 = [tk.Canvas(self.frame21, bg='#B5B5B5',
                            width=self.x0+self.d,
                            height=self.height21, 
                            highlightthickness=0) for _ in range(self.num_pion)]

        self.canvas2 = [tk.Canvas(self.frame22, bg='#B5B5B5',
                            width=self.x0+self.d,
                            height=self.height21, 
                            highlightthickness=0) for _ in range(self.num_pion)]
        
        self.tag_name1 = "pion1"
        self.tag_name2 = "pion2"
        for i in range(self.num_pion):
            self.canvas1[i].create_oval(self.x0, self.y0, self.d, self.d, outline="", fill=self.color1, tag=self.tag_name1)
            self.canvas2[i].create_oval(self.x0, self.y0, self.d, self.d, outline="", fill=self.color2, tag=self.tag_name2)
            
            self.canvas1[i].tag_bind(self.tag_name1, "<Enter>", lambda event, canvas=self.canvas1[i]: self.check_hand_enter(canvas=canvas))
            self.canvas1[i].tag_bind(self.tag_name1, "<Leave>", lambda event, canvas=self.canvas1[i]: self.check_hand_leave(canvas=canvas))

            self.canvas2[i].tag_bind(self.tag_name2, "<Enter>", lambda event, canvas=self.canvas2[i]: self.check_hand_enter(canvas=canvas))
            self.canvas2[i].tag_bind(self.tag_name2, "<Leave>", lambda event, canvas=self.canvas2[i]: self.check_hand_leave(canvas=canvas))

            self.canvas1[i].bind("<Button-1>", lambda event, canvas=self.canvas1[i]: self.pion_click(event, canvas=canvas))
            self.canvas2[i].bind("<Button-1>", lambda event, canvas=self.canvas2[i]: self.pion_click(event, canvas=canvas))
            
            self.canvas1[i].pack(side=tk.LEFT, fill="both", expand=True, padx=(0, 9))
            self.canvas2[i].pack(side=tk.LEFT, fill="both", expand=True, padx=(0, 9))

    def pion_click(self, event=None, canvas=None):
        x, y = event.x, event.y
        ids = canvas.find_overlapping(x, y, x, y)
        clicked_color = ", ".join(canvas.itemcget(id, "fill") for id in ids)
        clicked_tag   = ", ".join(canvas.itemcget(id, "tag") for id in ids)
        
        clicked_color = clicked_color[:len(self.color1)]
        clicked_tag   = clicked_tag[:len(self.tag_name1)]
        
        clicked_pion = clicked_color + ' ' + clicked_tag
 
        self.sa_selected_pion.set(clicked_pion)

        if self.spion.get() == 1:
            self.status.set("C'est au tour de Joueur 1")
        elif self.spion.get() == 2:
            self.status.set("C'est au tour de Joueur 2")

        canvas.destroy()

        StatusArea.sa_count_pion +=1

        if StatusArea.sa_count_pion == 2*self.num_pion:
            self.sa_start_second_part.set(True)

    def check_hand_enter(self, event=None, canvas=None):
        canvas.config(cursor="hand1")

    def check_hand_leave(self, event=None, canvas=None):
        canvas.config(cursor="")
    
    def play(self):
        #messagebox.showinfo("Moulin", "Welcome to Moulin Game!")
        pass
    
    def show_frame(self):
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)

        self.frame1.grid(row=0, column=0, sticky="ew")
        self.frame2.grid(row=1, column=0, sticky="nsew")
        self.frame3.grid(row=2, column=0, sticky="nsew")
        
        self.frame21.pack(side=tk.TOP, expand=True)
        self.frame22.pack(side=tk.TOP, expand=True)
        self.frame23.pack(fill="both", expand=True)
        
    def about(self):
        messagebox.showinfo('À propos',
             message="Bienvenue dans le jeu du Moulin avec Tkinter.\n\n"
                     "Le jeu du moulin est un jeu de société traditionnel en Europe.\n\n"
                     "Le tablier de jeu existait déjà dans la Rome antique.\n\n"
                     "Aussi appelé jeu du charret (en Suisse), certains lui donnent le"
                     "nom médiéval de jeu de mérelles.")


class GraphicPion:
    def __init__(self, name=None):
        self.name = name

        #self.bind("<Button-1>", self.mouse_click)

    def draw(self, canvas, x0, y0, d, fill="", tag="pion", outline=""):
        self.canvas = canvas
        self.fill = fill
        self.tag = tag
        self.outline = outline
        self.x0, self.y0, self.d = x0, y0, d
        self.oval = self.canvas.create_oval(self.x0, self.y0,
                                            self.x0+self.d, 
                                            self.y0+self.d,
                                            fill=self.fill, 
                                            outline=self.outline)
        #self.canvas.tag_bind(self.oval, self.tag, self.mouse_click)
        #self.canvas.tag_bind(self.tag, "<Enter>", lambda event, canvas=self.canvas: self.check_hand_enter(canvas=canvas))
        #self.canvas.tag_bind(self.tag, "<Leave>", lambda event, canvas=self.canvas: self.check_hand_leave(canvas=canvas))

    def mouse_click(self, event=None, x=None, y=None):
        print(f"I got a mouse click on {self.name}")

    def check_hand_enter(self, event=None, canvas=None):
        print('*****check_hand_enter*****')
        canvas.config(cursor="hand1")

    def check_hand_leave(self, event=None, canvas=None):
        canvas.config(cursor="")

#-----------------------------------------------
class Pion:
    def __init__(self, pos=(0, 0), color=None):
        self._pos     = pos
        self._color   = color
        self.is_moved = False

    def move(self, npos):
        ret = True if  self.pos != npos else False
        self.pos = npos
        self.is_moved = ret 
        return ret
    
    @property
    def pos(self):
        return self._pos
    
    @pos.setter
    def pos(self, value):
        self._pos = value
    
    @property
    def color(self):
        return self._color
    
    @color.setter
    def color(self, value):
        self._color = value
        
    def __mul__(self, other):
        return Pion()
    
    def __rmul__(self, other):
        return Pion()
        
        
class Case:
    pos = ((1,1), (1,4), (1,7),
           (2,2), (2,4), (2,6),
           (3,3), (3,4), (3,5),
           (4,1), (4,2), (4,3),
           (4,5), (4,6), (4,7),
           (5,3), (5,4), (5,5),
           (6,2), (6,4), (6,6),
           (7,1), (7,4), (7,7))
    bpos = [x//x* False for x in range(1, len(pos)+1)]
    def __init__(self):
        
        self._pion = None
    
    def check_pos(self, pos):
        idx = Case.pos.index(pos)
        if self.bpos[idx]:
            return False
        else:
            Case.bpos[idx] = True
            return True
    
    @property
    def pion(self):
        return self._pion
    
    @pion.setter
    def pion(self, value):
        if not isinstance(value, (type(None), Pion)):
            raise TypeError('item is not of type')
        if not None and value.pos not in Case.pos:
            raise ValueError('Pion had invalid posion')
        if not None and not self.check_pos(value.pos):
            raise ValueError('Position has already pion')
        self._pion = value
        
    def __str__(self):
        pcolor = self.pion.color if self.pion else None
        cpos   = self.pion.pos
        return f'Case position is {cpos} and pion color is {pcolor}'
       
    def __mul__(self, other):
        return Case()
    
    def __rmul__(self, other):
        return Case()

class Plateau:
    def __init__(self):
        self.tl_color = 'red'
        self.tr_color = 'blue'
        
        self.field = [x//x * Case() for x in range(1, 19)]
        
        self.add2field()
    
    def add2field(self):
        temp = list(Case().pos)
        for i,v in enumerate(self.field):
            color = self.tl_color if i < 8 else self.tr_color
            p,c = random.choice(temp), color
            v.pion = Pion(p, c)
            del temp[temp.index(p)]
            
            
if __name__ == '__main__': run_moulin()