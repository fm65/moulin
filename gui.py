import tkinter as tk
from tkinter import Canvas, ttk
from tkinter import messagebox
import random


import damier

NB_PION = 18
field = damier.Damier()

empty_game = ["╔═══════╗",
              "║       ║",
              "║       ║",
              "║       ║",
              "║       ║",
              "║       ║",
              "║       ║",
              "║       ║",
              "╚═══════╝"]




def get_player_symbol(player):
    if player is None:
        return "◯"
    if player.get_color() == "blue":
        return "B"#"①"
    if player.get_color() == "red":
        return "R"#"②"

def print_field(field):
    to_print = empty_game
    for position in damier.Damier.position_list:
        #print("c:", c)
        player = field.get_cell(position).get_player()
        tmp_list = list(to_print[position[0]])
        tmp_list[position[1]] = get_player_symbol(player)
        to_print[position[0]] = "".join(tmp_list)
    for line in to_print:
        print(line)


class Moulin(tk.Frame):
    def __init__(self, parent, bg="white", *args, **kwargs):
        tk.Frame.__init__(self, parent, bg=bg, *args, **kwargs)
        self.parent  = parent
        
        self.width  = 1212
        self.height = 700
        
        self.gbg = "white"
        self.sbg = "white"
        self.sa_pbg = "#EFEFEF"
        
        self.start_page()
        self.parent.geometry(f'{self.width}x{self.height}')
        self.parent.resizable(0, 0)
        
        self.is_phase_one = tk.BooleanVar()
        self.is_phase_one.set(False)
        
        self.is_phase_two = tk.BooleanVar()
        self.is_phase_two.set(False)
        
        self.count_click = 0
        self.line_width = 3
        
        self.selected = None

        self.is_moulin = False
        
        self.sa = StatusArea(self, bg=self.sbg, width=self.width-200, height=self.height, sa_pbg=self.sa_pbg)
        self.ga = GameArea(  self, bg=self.gbg, width=self.width, height=self.height)
        
        self.parent.attributes('-fullscreen', False)
        self.full_screen_state = False
        
        self.parent.bind("<F2>", self.start_page)
        self.parent.bind("<F11>", self.toggle_full_screen)
        self.parent.bind("<Escape>", self.quit_full_screen)
        self.parent.bind("<Button-1>", self.on_click)
        
        self.ga_coords = list(range(self.ga.c11, self.ga.c77+1))
        self.sa_coords = list(range(self.sa.p11, self.sa.p29+1))
        self.sa_coords1 = self.sa_coords[:len(self.sa_coords)//2]
        self.sa_coords2 = self.sa_coords[len(self.sa_coords)//2:]
        
        self.dcount_pion1 = len(self.sa_coords1)
        self.dcount_pion2 = self.dcount_pion1
                
        self.list_of_pions = list(range(1, NB_PION+1))
                                  
        self.dcoords_dict = {}
        self.pcoords_dict = {}
        
        for k,v in zip(self.ga_coords, field.position_list):
            self.dcoords_dict[str(k)] = v
            
        i,j = 1,1
        for k,v in zip(self.sa_coords, self.list_of_pions):
            if v == 10: i = 2; j = 1
            self.pcoords_dict[str(k)] = "p" + str(i) + str(j)
            j +=1
        
        self.show_frame()
        
    def check_coords(self, canvas=None, coords=None, event=None):
        for i in coords:
            x0, y0, x1, y1 = canvas.coords(i)
            if x0 <= event.x <= x1 and y0 <= event.y <= y1:
                return True, i
        return False, None
        
    def on_click(self, event):
        res = self.check_coords(self.ga.canvas, self.ga_coords, event)
        self.current_color = field.get_current_player().get_color()
        
        if self.is_phase_one.get(): #=====================PHASE 1=====================#          
            if res[1]:
                print("PHASE 1 | ", self.dcoords_dict[str(res[1])])
                
                if field.is_your_turn_to_play(self.current_color) and not self.is_moulin and\
                   self.ga.canvas.itemcget(res[1], "fill") == "white":
                    
                    pcolor = "bleu" if not self.current_color == "blue" else "rouge"
                    self.sa.status_tour.set("C'est au tour de joueur " + pcolor)
                    
                    coords = self.dcoords_dict[str(res[1])]
                    cell_selected = field.get_cell(coords)
                    cell_selected.set_player(field.get_current_player())

                    if field.can_kill(cell_selected) and not self.is_moulin:
                        pcolor = "bleu" if self.current_color == "blue" else "rouge"
                        self.sa.status_tour.set("Le joueur " + pcolor + " a fait un moulin")
                        self.is_moulin = True

                    self.ga.canvas.itemconfig(res[1], fill=self.current_color, outline=self.current_color)
                    
                    if self.current_color == "blue":
                        k = self.sa_coords1[self.dcount_pion1-1]
                        self.dcount_pion1 -=1
                    else:
                        k = self.sa_coords2[self.dcount_pion2-1]
                        self.dcount_pion2 -=1
                    index = self.sa_coords[k-1]
                    self.sa.canvas.itemconfig(self.sa_coords[index-1], width=self.line_width, fill=self.sa_pbg, outline=self.sa_pbg)
                    
                    field.switch_player()
                        
                    if self.dcount_pion2 == 0 and not self.is_moulin:
                        self.is_phase_one.set(False)
                        self.is_phase_two.set(True)
                        self.sa.status_phase.set("Deuxième Phase")
                        self.sa.status_msg_rule.set(self.sa.msg_rule2)
                                                
                elif self.ga.canvas.itemcget(res[1], "fill")\
                     not in ("white", field.get_not_current_player().get_color())\
                     and self.is_moulin:
                    
                    print("CLICKEK | ", self.dcoords_dict[str(res[1])])
                    self.ga.canvas.itemconfig(res[1], fill="white", outline="black")
                    
                    pcolor = "bleu" if self.current_color == "blue" else "rouge"
                    self.sa.status_tour.set("C'est au tour de joueur " + pcolor)
                    self.is_moulin = False
                
                else: print("***WARNING2: invalid click", "#is_moulin:", self.is_moulin)
            else: print("***WARNING1: invalid click")
        
        elif self.is_phase_two.get(): #=====================PHASE 2=====================#
            if res[1]:
                print("PHASE 2 | ", self.dcoords_dict[str(res[1])])
                
                if field.is_your_turn_to_play(self.current_color) and not self.is_moulin and\
                   self.ga.canvas.itemcget(res[1], "fill") not in ("white", field.get_not_current_player().get_color()) and self.count_click == 0:
                    
                    print("CLICKEK | ", self.dcoords_dict[str(res[1])], "res:", res)
                    self.src_coord = self.dcoords_dict[str(res[1])]
                    self.src_color = self.ga.canvas.itemcget(res[1], "fill")
                    self.src_res   = res
                    self.count_click +=1
                
                elif field.is_your_turn_to_play(self.current_color) and not self.is_moulin and\
                   self.ga.canvas.itemcget(res[1], "fill") == "white" and self.count_click == 1:
                    
                    pcolor = "bleu" if not self.current_color == "blue" else "rouge"
                    self.sa.status_tour.set("C'est au tour de joueur " + pcolor)
                    
                    coords = self.dcoords_dict[str(res[1])]
                    src_coord = field.get_cell(self.src_coord)
                    cell_selected = field.get_cell(coords)
                    is_moved = field.can_move(src_coord, cell_selected)
                    
                    print("\n@can_kill:", field.can_kill(cell_selected), " | @is_moved:", is_moved, " | @is_moulin:", self.is_moulin)
                    if field.can_kill(cell_selected) and not self.is_moulin:
                        pcolor = "bleu" if self.src_color == "blue" else "rouge"
                        self.sa.status_tour.set("Le joueur " + pcolor + " a fait un moulin")
                        self.is_moulin = True
                        
                    if is_moved:
                        cell_selected.set_player(field.get_current_player())
                        self.ga.canvas.itemconfig(self.src_res[1], fill="white", outline="black")
                        self.ga.canvas.itemconfig(res[1], fill=self.src_color, outline=self.src_color)
                        print("#cur_res:", res, "          | #current_color:", self.current_color)
                        print("#src_res:", self.src_res, " | #src_color:", self.src_color)
                        field.switch_player()
                        self.count_click = 0
                    else:
                        self.count_click = 1
                
                elif self.ga.canvas.itemcget(res[1], "fill")\
                     not in ("white", field.get_not_current_player().get_color())\
                     and self.is_moulin:
                    
                    print("#MOULIN | ", self.dcoords_dict[str(res[1])])
                    self.ga.canvas.itemconfig(res[1], fill="white", outline="black")
                    
                    pcolor = "bleu" if self.current_color == "blue" else "rouge"
                    self.sa.status_tour.set("C'est au tour de joueur " + pcolor)
                    
                    self.is_moulin = False
                    self.count_click = 0
                    
                else:
                    print("***WARNING3: invalid click")
                    print("current_color:", self.current_color)
        
        else: print("***WARNING4: invalid click")
        print_field(field)
            
   
    def start_page(self, event=None):
        StartPage(self, width=self.width, height=self.height)
        
    def show_frame(self):
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        self.ga.grid(row=0, column=0, sticky="nswe")
        self.sa.grid(row=0, column=1, sticky="nswe")    
    
    def toggle_full_screen(self, event):
        self.full_screen_state = not self.full_screen_state
        self.parent.attributes("-fullscreen", self.full_screen_state)
        
    def quit_full_screen(self, event):
        self.full_screen_state = False
        self.parent.attributes("-fullscreen", self.full_screen_state)
        
    
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
                                  command=self.start_play)
        
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
        
    def start_play(self):
        self.parent.is_phase_one.set(True)
        self.destroy()
        
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

        
class GameArea(tk.Frame):
    def __init__(self, parent, bg, width, height, *args, **kwargs):
        tk.Frame.__init__(self, parent, width=width, height=height, bg=bg, *args, **kwargs)
        self.parent = parent
        self.bg = bg
        self.width  = self.winfo_reqwidth()
        self.height = self.winfo_reqheight()

        line_color = "black"
        oval_color = "white"
        line_width  = 3
        
        self.canvas = tk.Canvas(self, bg=self.bg,
                                width=self.width,
                                height=self.height,
                                highlightthickness=0)

        # rectangle creation
        self.canvas.create_rectangle(34,   34, 666, 666, width=line_width, fill=self.bg, outline=line_color) # big
        self.canvas.create_rectangle(144, 144, 556, 556, width=line_width, fill=self.bg, outline=line_color) # small
                
        # line creation
        self.canvas.create_line(34, 352, 666, 352, width=line_width, fill=line_color) # horizontal
        self.canvas.create_line(350, 34, 350, 666, width=line_width, fill=line_color) # vertical
        
        self.canvas.create_rectangle(254, 254, 446, 446, width=line_width, fill=self.bg, outline=line_color) # small
        
        self.c11 = self.canvas.create_oval(22,  22, 47,  47,  width=line_width, fill=oval_color, outline=line_color)
        self.c14 = self.canvas.create_oval(337, 22, 362, 47,  width=line_width, fill=oval_color, outline=line_color)
        self.c17 = self.canvas.create_oval(653, 22, 678, 47,  width=line_width, fill=oval_color, outline=line_color)
        
        self.c22 = self.canvas.create_oval(132, 130, 157, 155, width=line_width, fill=oval_color, outline=line_color)
        self.c24 = self.canvas.create_oval(337, 130, 362, 155, width=line_width, fill=oval_color, outline=line_color)
        self.c26 = self.canvas.create_oval(544, 130, 569, 155, width=line_width, fill=oval_color, outline=line_color)
        
        self.c33 = self.canvas.create_oval(242, 240, 267, 265, width=line_width, fill=oval_color, outline=line_color)
        self.c34 = self.canvas.create_oval(337, 240, 362, 265, width=line_width, fill=oval_color, outline=line_color)
        self.c35 = self.canvas.create_oval(434, 240, 459, 265, width=line_width, fill=oval_color, outline=line_color)
        
        self.c41 = self.canvas.create_oval(22,  337, 47,  362, width=line_width, fill=oval_color, outline=line_color)
        self.c42 = self.canvas.create_oval(132, 337, 157, 362, width=line_width, fill=oval_color, outline=line_color)
        self.c43 = self.canvas.create_oval(242, 337, 267, 362, width=line_width, fill=oval_color, outline=line_color)
        self.c45 = self.canvas.create_oval(434, 337, 459, 362, width=line_width, fill=oval_color, outline=line_color)
        self.c46 = self.canvas.create_oval(544, 337, 569, 362, width=line_width, fill=oval_color, outline=line_color)
        self.c47 = self.canvas.create_oval(653, 337, 678, 362, width=line_width, fill=oval_color, outline=line_color)
        
        self.c53 = self.canvas.create_oval(242, 434, 267, 459, width=line_width, fill=oval_color, outline=line_color)
        self.c54 = self.canvas.create_oval(337, 434, 362, 459, width=line_width, fill=oval_color, outline=line_color)
        self.c55 = self.canvas.create_oval(434, 434, 459, 459, width=line_width, fill=oval_color, outline=line_color)
        
        self.c62 = self.canvas.create_oval(132, 544, 157, 569, width=line_width, fill=oval_color, outline=line_color)
        self.c64 = self.canvas.create_oval(337, 544, 362, 569, width=line_width, fill=oval_color, outline=line_color)
        self.c66 = self.canvas.create_oval(544, 544, 569, 569, width=line_width, fill=oval_color, outline=line_color)
        
        self.c71 = self.canvas.create_oval(22,  654, 47,  679, width=line_width, fill=oval_color, outline=line_color)
        self.c74 = self.canvas.create_oval(337, 654, 362, 679, width=line_width, fill=oval_color, outline=line_color)
        self.c77 = self.canvas.create_oval(653, 654, 678, 679, width=line_width, fill=oval_color, outline=line_color)
        
        self.canvas.pack(fill="both", expand=True) # display damier
    

class StatusArea(tk.Frame):
    sa_count_pion = 0
    def __init__(self, parent, width, height, bg, sa_pbg, *args, **kwargs):
        tk.Frame.__init__(self, parent, width=width, height=height, bg=bg, *args, **kwargs)
        self.parent = parent
        
        self.msg_rule1 = "Le jeu commence avec un plateau vide. Les joueurs\n"+ \
                    "placent à tour de rôle leurs pions sur un point  \n"     + \
                    "libre du plateau. Pendant cette phase, il est    \n"     + \
                    "interdit de déplacer les pions déjà placés sur   \n"     +\
                    "le plateau.                                      \n"     + \
                    "Si un joueur forme un moulin, il retire un pion  \n"     + \
                    "(en dehors d’un moulin éventuel) à son adversaire."
                    
        self.msg_rule2 = "Une fois tous les pions placés (18 pions), chaque\n" + \
                    "joueur déplace à tour de rôle un de ses pions sur un\n"   + \
                    "point adjacent libre d’une même ligne. Le but est de\n"   + \
                    "faire des lignes de 3 pions de sa couleur pour enlever\n" + \
                    "du plateau un pion de l’adversaire qui ne fait pas\n"     +\
                    "partie d’un moulin (une ligne de 3 pions de son adversaire).\n\n" + \
                    "Phase de déplacement puis suppression : Dès qu'un\n"      +\
                    "joueur n'a plus que trois pions sur le plateau,\n"        + \
                    "il déplace librement ses pions (un par un et dès qu’il\n" + \
                    "s’agit de son tour de jeu) sur n'importe quel point\n"    + \
                    "vide du plateau."
        
        self.width = width
        self.height = height
                
        self.color1 = 'blue'
        self.color2 = 'red'
        self.sa_pbg = sa_pbg
        
        line_width  = 2
        self.bg = bg
        self.pad = 9
        
        self.bnt_width = 15
        self.bnt_height = 1
        
        self.bnt_font = 'Terminal 10 bold'

        self.spion = tk.IntVar()
        self.spion.set(1)

        self.status_msg_rule = tk.StringVar()
        self.status_msg_rule.set(self.msg_rule1)
        
        self.status_tour = tk.StringVar()
        self.status_tour.set("C'est au tour de Joueur bleu")

        self.status_phase = tk.StringVar()
        self.status_phase.set("Première Phase")

        self.status_rule = tk.StringVar()
        self.status_rule.set("Règles du jeu")
        
        height1 = 50
        height3 = 50
        height2 = height - (height1+height3)
        
        self.frame1 = tk.Frame(self, width=width, height=height1, bg=bg)
        self.frame2 = tk.Frame(self, width=width, height=height2, bg=self.sa_pbg, highlightthickness=1)
        self.frame3 = tk.Frame(self, width=width, height=height3, bg="#EFEFEF")
        
        self.height21 = 1
        self.height22 = self.height21
        self.height23 = height2 - 2*self.height21
        
        self.canvas  = tk.Canvas(self.frame2,width=width, height=self.height21, bg="#EFEFEF", highlightthickness=0)
        self.frame21 = tk.Frame(self.frame2, width=width, height=self.height23, bg=bg)
        
        self.label = tk.Label(self.frame1, textvariable=self.status_phase,
                              foreground="black", background=bg,
                              font='Terminal 12 bold')

        self.label_status = tk.Label(self.frame1, textvariable=self.status_tour,
                              foreground="#006400", background=bg,
                              font='Terminal 11 bold')

        self.label_trule = tk.Label(self.frame21, textvariable=self.status_rule,
                              foreground="black", background=bg,
                              font='Terminal 15 bold')

        self.label_rule = tk.Label(self.frame21, textvariable=self.status_msg_rule,
                              foreground="black", background=bg,
                              font='Terminal 11')
        
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
        self.label_status.pack(side=tk.RIGHT, padx=self.pad, pady=self.pad)
        
        self.btn_quit.pack(side=tk.LEFT, padx=self.pad, pady=self.pad)
        self.btn_about.pack(side=tk.LEFT, anchor='center', expand=True, padx=self.pad, pady=self.pad)
        self.btn_new.pack(side=tk.RIGHT, padx=self.pad, pady=self.pad)
        
        self.label_trule.pack(side=tk.TOP, anchor='center', padx=self.pad, pady=self.pad)
        self.label_rule.pack(side=tk.TOP, anchor='center', padx=self.pad, pady=(0, self.pad))
        
        self.p11 = self.canvas.create_oval(100,  40, 125,  65,  width=line_width, fill=self.color1, outline=self.color1)
        self.p12 = self.canvas.create_oval(145,  40, 170,  65,  width=line_width, fill=self.color1, outline=self.color1)
        self.p13 = self.canvas.create_oval(190,  40, 215,  65,  width=line_width, fill=self.color1, outline=self.color1)
        self.p14 = self.canvas.create_oval(235,  40, 260,  65,  width=line_width, fill=self.color1, outline=self.color1)
        self.p15 = self.canvas.create_oval(280,  40, 305,  65,  width=line_width, fill=self.color1, outline=self.color1)
        self.p16 = self.canvas.create_oval(325,  40, 350,  65,  width=line_width, fill=self.color1, outline=self.color1)
        self.p17 = self.canvas.create_oval(370,  40, 395,  65,  width=line_width, fill=self.color1, outline=self.color1)
        self.p18 = self.canvas.create_oval(415,  40, 440,  65,  width=line_width, fill=self.color1, outline=self.color1)
        self.p19 = self.canvas.create_oval(460,  40, 485,  65,  width=line_width, fill=self.color1, outline=self.color1)

        self.p21 = self.canvas.create_oval(100,  90, 125,  115,  width=line_width, fill=self.color2, outline=self.color2)
        self.p22 = self.canvas.create_oval(145,  90, 170,  115,  width=line_width, fill=self.color2, outline=self.color2)
        self.p23 = self.canvas.create_oval(190,  90, 215,  115,  width=line_width, fill=self.color2, outline=self.color2)
        self.p24 = self.canvas.create_oval(235,  90, 260,  115,  width=line_width, fill=self.color2, outline=self.color2)
        self.p25 = self.canvas.create_oval(280,  90, 305,  115,  width=line_width, fill=self.color2, outline=self.color2)
        self.p26 = self.canvas.create_oval(325,  90, 350,  115,  width=line_width, fill=self.color2, outline=self.color2)
        self.p27 = self.canvas.create_oval(370,  90, 395,  115,  width=line_width, fill=self.color2, outline=self.color2)
        self.p28 = self.canvas.create_oval(415,  90, 440,  115,  width=line_width, fill=self.color2, outline=self.color2)
        self.p29 = self.canvas.create_oval(460,  90, 485,  115,  width=line_width, fill=self.color2, outline=self.color2)
        
        self.canvas.create_text(50, 53, text="Jouer 1", font='Terminal 13 bold')
        self.canvas.create_text(50, 103, text="Jouer 2", font='Terminal 13 bold')
                
        self.show_frame()
    
    def show_frame(self):
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)

        self.frame1.grid(row=0, column=0, sticky="ew")
        self.frame2.grid(row=1, column=0, sticky="nsew")
        self.frame3.grid(row=2, column=0, sticky="nsew")
        
        self.canvas.pack(fill="both", side=tk.TOP, expand=True)
        self.frame21.pack(fill="both", expand=True)
        
    def about(self):
        messagebox.showinfo('À propos',
             message="Bienvenue dans le jeu du Moulin avec Tkinter.\n\n"
                     "Le jeu du moulin est un jeu de société traditionnel en Europe.\n\n"
                     "Le tablier de jeu existait déjà dans la Rome antique.\n\n"
                     "Aussi appelé jeu du charret (en Suisse), certains lui donnent le"
                     "nom médiéval de jeu de mérelles.")

def run():
    root = tk.Tk()
    root.title("Moulin")
    Moulin(root).pack(fill="both", expand=True)
    root.mainloop()
            
#---------------------------------------------            
if __name__ == '__main__': run()
