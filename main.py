from curses import window
import sqlite3

import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar, DateEntry
from tkinter import messagebox, StringVar, IntVar
from PIL import Image  # pip install pillow
import hashlib
import datetime
con = sqlite3.connect('zoo.db')

c = con.cursor()
class FirstPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        poz = tk.PhotoImage(file = 'reg_poz.png')

        label = tk.Label(self, image=poz)
        label.image=poz
        label.place(x=0,y=0)

        
        border = tk.LabelFrame(self, text='Prihlasenie', bg='lightgreen', bd = 2, font=("Arial", 20))
        border.pack(fill="both", expand="yes", padx = 150, pady=150)
        
        L1 = tk.Label(border, text="Meno", font=("Arial Bold", 15), bg='#dda15e')
        L1.place(x=50, y=20)
        T1 = tk.Entry(border, width = 30, bd = 5)
        T1.place(x=180, y=20)
        
        L2 = tk.Label(border, text="Heslo", font=("Arial Bold", 15), bg='#dda15e')
        L2.place(x=50, y=80)
        T2 = tk.Entry(border, width = 30, show='*', bd = 5)
        T2.place(x=180, y=80)
        
        def verify():

            print(T1.get(), T2.get())
            heslo = str(hashlib.md5(f"b'{T2.get()}'".encode('utf-8')).hexdigest())
            # try:
            c.execute(f"SELECT * FROM pracovnici WHERE meno='{T1.get()}' AND heslo='{heslo}'")
            k = c.fetchall()
            if len(k) > 0:
                Application.uzivatel = T1.get()
                Application.idu = k[0][0]
                Application.admin = int(k[0][-1])
                print(Application.idu)
                controller.show_frame(SecondPage)
            else:
                messagebox.showinfo("Error", "Nespravne zadane udaje!")

         
        B1 = tk.Button(border, text="Prihlas", font=("Arial", 15), command=verify)
        B1.place(x=320, y=115)
        
        def odhlas():
            if Application.uzivatel != '':
                Application.uzivatel = ''
                T1.delete(0,'end')
                T2.delete(0, 'end')                
                messagebox.showinfo("Sucess", "Boli ste odhlaseny")
            else:
                messagebox.showinfo("Error", "Nikto nie je prihlaseny")

        B2 = tk.Button(self, text="Odhlas", bg = "dark orange", font=("Arial",15), command=odhlas)
        B2.place(x=650, y=20)
        
class SecondPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        poz = tk.PhotoImage(file = 'menu_bgss.png')

        label = tk.Label(self, image=poz)
        label.image=poz
        label.place(x=0,y=0)

        def pridaj_zv():
            if Application.admin:
                window = tk.Tk()
                window.configure(bg="#e9c46a")
                window.title("Pridaj zviera")
                l1 = tk.Label(window, text="Nazov:", font=("Arial",15), bg="#e9c46a")
                l1.place(x=10, y=10)
                t1 = tk.Entry(window, width=30, bd=5)
                t1.place(x = 200, y=10)

                c.execute("SELECT * FROM druhy")
                options = [i[1] for i in c.fetchall()]
                
                l3 = tk.Label(window, text="Druh:", font=("Arial",15), bg="#e9c46a")
                l3.place(x=10, y=60)
                druh = StringVar(window)
                t3 = tk.OptionMenu(window, druh, *options)
                t3.place(x = 200, y=60)

                l2 = tk.Label(window, text="Datum narodenia:", font=("Arial",13), bg="#e9c46a")
                l2.place(x=10, y=120)
                cal = DateEntry(window, width=12, year=2019, month=6, day=22, 
                    background='darkblue', foreground='white', borderwidth=2)
                cal.pack(padx=200, pady=120)

                            
                l4 = tk.Label(window, text="Frekvencia krmenia(hod):", font=("Arial",10), bg="#e9c46a")
                l4.place(x=10, y=180)
                t4 = tk.Entry(window, width=30, bd=5)
                t4.place(x = 200, y=180)

                l5 = tk.Label(window, text="Frekvencia cistenia(dni):", font=("Arial",10), bg="#e9c46a")
                l5.place(x=10, y=240)
                t5 = tk.Entry(window, width=30, bd=5)
                t5.place(x = 200, y=240)

                l6 = tk.Label(window, text="Potrava:", font=("Arial",15), bg="#e9c46a")
                l6.place(x=10, y=300)
                t6 = tk.Entry(window, width=30, bd=5)
                t6.place(x = 200, y=300)
                
                l7 = tk.Label(window, text="Miesto povodu:", font=("Arial",13), bg="#e9c46a")
                l7.place(x=10, y=360)
                t7 = tk.Entry(window, width=30, bd=5)
                t7.place(x = 200, y=360)
                
                c.execute("SELECT * FROM pracovnici")
                options = [i[1]+' '+i[2] for i in c.fetchall()]
                
                l8 = tk.Label(window, text="Pracovnik:", font=("Arial",15), bg="#e9c46a")
                l8.place(x=10, y=420)
                pracovnik = StringVar(window)
                t8 = tk.OptionMenu(window, pracovnik, *options)
                t8.place(x = 200, y=420)

                def check():
                    if t1.get()!="" or cal.get()!="" or druh.get()!="" or t3.get()!="" or t4.get()!="" or t5.get()!="" or t6.get()!="" or druh.get()!="" or pracovnik.get()!='':
                        c.execute(f"SELECT * FROM druhy WHERE nazov='{druh.get()}'")
                        id_druh = c.fetchall()[0][0]
                        meno, priezvisko = pracovnik.get().split()
                        c.execute(f"SELECT * FROM pracovnici WHERE meno='{meno}' AND priezvisko='{priezvisko}'")
                        id_prac = c.fetchall()[0][0]
                        # print(id_prac)
                        teraz = datetime.datetime.now()
                        # print(f"INSERT INTO zvierata ('meno', 'druh_id', 'miesto', 'datum_nar', 'potrava', 'frekvencia_strava_hod', 'cistenie_frek_den', 'posl_krm', 'posl_cist', 'id_prac') VALUES ('{t1.get()}', '{id_druh}', '{t7.get()}',  '{cal.get_date()}',  '{t6.get()}',  '{t4.get()}',  '{t5.get()}',  '{teraz}',  '{teraz}',  '{id_prac}')")
                        c.execute(f"INSERT INTO zvierata ('meno', 'druh_id', 'miesto', 'datum_nar', 'potrava', 'frekvencia_strava_hod', 'cistenie_frek_den', 'posl_krm', 'posl_cist', 'id_prac') VALUES ('{t1.get()}', '{id_druh}', '{t7.get()}',  '{cal.get_date()}',  '{t6.get()}',  '{t4.get()}',  '{t5.get()}',  '{teraz}',  '{teraz}',  '{id_prac}')")
                        con.commit()
                        # print(t1.get(),
                        # druh.get(),
                        # t4.get(),
                        # t5.get(),
                        # t6.get(),
                        # t7.get(),
                        # cal.get_date(),
                        # pracovnik.get()
                        #         )
                        messagebox.showinfo("Sucess", "Uspesne pridane do databazy")
                        window.destroy()
                    else:
                        messagebox.showinfo("Error", "Nespravne zadane udaje alebo nezvolena kategoria!")
                        
                b1 = tk.Button(window, text="Pridaj", font=("Arial",15), bg="#ffc22a", command=check)
                b1.place(x=170, y=500)
                
                window.geometry("500x550")
                window.mainloop()
            else:
                messagebox.showinfo("Error", "Na takuto operaciu potrebujes administratorske prava!")

        def pridaj_zam():
            if Application.admin:
                window = tk.Toplevel()
                window.resizable(0,0)
                window.configure(bg="deep sky blue")
                window.title("Pridaj zamestanca")
                l1 = tk.Label(window, text="Meno:", font=("Arial",15), bg="deep sky blue")
                l1.place(x=10, y=10)
                t1 = tk.Entry(window, width=30, bd=5)
                t1.place(x = 200, y=10)

                l12 = tk.Label(window, text="Priezvisko:", font=("Arial",15), bg="deep sky blue")
                l12.place(x=10, y=60)
                t12 = tk.Entry(window, width=30, bd=5)
                t12.place(x = 200, y=60)
                
                l2 = tk.Label(window, text="Heslo:", font=("Arial",15), bg="deep sky blue")
                l2.place(x=10, y=110)
                t2 = tk.Entry(window, width=30, show="*", bd=5)
                t2.place(x = 200, y=110)
                
                l3 = tk.Label(window, text="Heslo znovu:", font=("Arial",15), bg="deep sky blue")
                l3.place(x=10, y=160)
                t3 = tk.Entry(window, width=30, show="*", bd=5)
                t3.place(x = 200, y=160)
                
                c.execute("SELECT * FROM zvierata WHERE id_prac='0'")
                opaa = ['-']
                for i in c.fetchall():
                    opaa.append(i[0])
                
                l5 = tk.Label(window, text="zvieratko:", font=("Arial",15), bg="#e9c46a")
                l5.place(x=10, y=210)
                stara = StringVar(window)
                t5 = tk.OptionMenu(window, stara, *opaa)
                t5.place(x = 200, y=210)

                l4 = tk.Label(window, text="Prava admina:")
                var = IntVar()
                t4 = tk.Checkbutton(window, text="Ano", variable=var)
                t4.place(x=325, y=270)
                l4.place(x=200,y=270)
                

                def check():
                    if t1.get()!="" or t2.get()!="" or t3.get()!="":
                        if t2.get()==t3.get():
                            heslo = str(hashlib.md5(f"b'{t2.get()}'".encode('utf-8')).hexdigest())
                            c.execute(f"INSERT INTO pracovnici ('meno', 'priezvisko', 'heslo', 'admin') VALUES ('{t1.get()}', '{t12.get()}', '{heslo}', '{var.get()}')")
                            con.commit()
                            c.execute(f"select last_insert_rowid()")
                            id_us = c.fetchall()[0][0]
                            print(id_us)
                            print(stara.get())
                            c.execute(f"UPDATE zvierata SET id_prac='{id_us}' WHERE meno='{stara.get()}'")
                            con.commit()
                            messagebox.showinfo("Sucess","Zamestnanec bol uspesne pridany",parent=window)
                            window.destroy()
                        else:
                            messagebox.showinfo("Error","Hesla sa nezhoduju",parent=window)
                    else:
                        messagebox.showinfo("Error", "Nespravne vyplneny formular",parent=window)
                
                b1 = tk.Button(window, text="Pridaj", font=("Arial",15), bg="#ffc22a", command=check)
                b1.place(x=170, y=300)
                
                window.geometry("470x350")
                window.mainloop()
            else:
                messagebox.showinfo("Error", "Nemas administratorske prava!")

        x1 = 365
        y1 = 116
        delta = 43
        Button = tk.Button(self, text="Moje zvierata", font=("Arial", 8), bg='#bc6c25', command=lambda: controller.show_frame(MojeZvierata))
        Button.place(x=x1, y=y1)
        y1 += delta
        Button = tk.Button(self, text="Krmenie", font=("Arial", 8), bg='#bc6c25', command=lambda: controller.show_frame(Krmenie))
        Button.place(x=x1+15, y=y1)
        y1 += delta-5
        Button = tk.Button(self, text="Cistenie", font=("Arial", 8), bg='#bc6c25', command=lambda: controller.show_frame(Cistenie))
        Button.place(x=x1+15, y=y1)        
        y1 += delta-5
        Button = tk.Button(self, text="Zvierata", font=("Arial", 8), bg='#bc6c25', command=lambda: controller.show_frame(Zvierata))
        Button.place(x=x1+15, y=y1)
        y1 += delta-5
        x1 -= 10

        Button = tk.Button(self, text="--Pridaj zviera--", font=("Arial", 8), bg='#283618',fg='white', command=pridaj_zv)
        Button.place(x=x1, y=y1)
        y1 += delta

        Button = tk.Button(self, text="--Pridaj zamestnanca--", font=("Arial", 8),  bg='#283618', fg='white',command=pridaj_zam)
        Button.place(x=x1-15, y=y1)
        y1 += delta-5

        Button = tk.Button(self, text="--Prehlad zamestnancov--", font=("Arial", 8), bg='#283618', fg='white',command=lambda: controller.show_frame(PrehladZamestnancov))
        Button.place(x=x1-25, y=y1)        
        y1 += delta-5

        Button = tk.Button(self, text="Prihlasenie/ Odhlasenie", font=("Arial", 8), bg='red', command=lambda: controller.show_frame(FirstPage))
        Button.place(x=625, y=10)

class PrehladZamestnancov(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        self.configure(bg='#f4a261')
        Button = tk.Button(self, text="Menu", font=("Arial", 8), bg='#283618',fg='white', command=lambda: controller.show_frame(SecondPage))
        Button.place(x=700, y=10)

        l1 = tk.Label(self, text="Zamestnanec", font=("Arial",15), fg='white', bg="#f4a261")
        l1.place(x=10, y=65)
        var = StringVar()
        c.execute("SELECT * FROM pracovnici")
        options = [i[1]+' '+i[2] for i in c.fetchall()]
        t1 = ttk.Combobox(self, textvariable=var,values=options)
        t1.place(x=175, y=70)

        def hladaj():
            frame = tk.Frame(self, width=800,height=500, bg="#f4a261")
            frame.place(x=0,y=100)
            
            meno, priezvisko = var.get().split()
            k = tk.Label(self, text=f"Meno: {meno}\n Priezvisko: {priezvisko}", font=("Arial",15), fg='white', bg="#f4a261")
            k.place(x=10, y=120)

            c.execute(f"SELECT * FROM pracovnici WHERE meno='{meno}' AND priezvisko='{priezvisko}'")
            k = c.fetchall()
            if len(k) == 0:
                messagebox.showerror('Error', 'Zadany zamestnanec nie je v systeme')
            else:
                self.id_us, self.admin = k[0][0], k[0][-1]
                kzm = tk.Label(self, text=f"Admin: {self.admin}", font=("Arial",15), fg='white', bg="#f4a261")
                kzm.place(x=10, y=190)

                def zmen_adm():
                    c.execute(f"UPDATE pracovnici SET admin='{(self.admin+1)%2}' WHERE id='{self.id_us}'")
                    con.commit()
                    self.admin = (self.admin+1)%2
                    kzm = tk.Label(self, text=f"Admin: {self.admin}", font=("Arial",15), fg='white', bg="#f4a261")
                    kzm.place(x=10, y=190)
                    messagebox.showinfo('Success', 'Hodnota admina bola uspesne zmenena')

                bzm = tk.Button(self, text="Zmen", font=("Arial",10), fg='white', bg="#f4a261", command=zmen_adm)
                bzm.place(x=130, y=190)

                c.execute(f"SELECT * FROM zvierata WHERE id_prac='{self.id_us}'")

                y1 = 120
                x1 = 300
                delta = 40
                stara = {}
                premenne = ['Potrava', 'Frekvencia podavania stravy (hod)','Cistenie (dni)','Naposledy krmene', 'Naposledy cistene']
                for zviera in c.fetchall():
                    stara[zviera[0]] = {}
                    c.execute(f"SELECT * FROM druhy WHERE id='{zviera[1]}'")
                    stara[zviera[0]]['Druh'] = c.fetchall()[0][1]
                    for pop, i in enumerate(zviera[4:-1]):
                        stara[zviera[0]][premenne[pop]] = i

                def vypis_stara():
                    y1 = 160
                    x1 = 300
                    delta = 40
                    for key in stara[okoho.get()]:
                        fore = 'white'
                        if key == 'Naposledy krmene':
                            if datetime.datetime.now() > (datetime.datetime.strptime(stara[okoho.get()][key], '%Y-%m-%d %H:%M:%S'))+datetime.timedelta(hours=int(stara[okoho.get()]['Frekvencia podavania stravy (hod)'])):
                                fore = 'red'
                        if key == 'Naposledy cistene':
                            if datetime.datetime.now() > (datetime.datetime.strptime(stara[okoho.get()][key], '%Y-%m-%d %H:%M:%S'))+datetime.timedelta(days=int(stara[okoho.get()]['Cistenie (dni)'])):
                                fore = 'red'
                        kzm = tk.Label(self, text=f"{key}: {stara[okoho.get()][key]}", font=("Arial",15), fg=fore, bg="#f4a261")
                        kzm.place(x=x1, y=y1)
                        y1 += delta



                okoho = StringVar()
                self.stara_zveri = (list(stara.keys()))
                t1 = ttk.OptionMenu(self, okoho,*list(stara.keys()))
                t1.place(x=x1, y=y1)

                bzm = tk.Button(self, text="Detail", font=("Arial",10), fg='white', bg="#f4a261", command=vypis_stara)
                bzm.place(x=x1+250, y=y1)

                def vyhod():
                    print(meno)
                    for odznac in self.stara_zveri:
                        c.execute(f"UPDATE zvierata SET id_prac='0' WHERE meno='{odznac}'")  
                    c.execute(f"DELETE FROM pracovnici WHERE meno='{meno}' AND priezvisko='{priezvisko}'")
                    con.commit()
                    messagebox.showinfo('Success', 'Zamestnanca sa podarilo uspesne odstranit zo systemu')
                
                bzm = tk.Button(self, text="Vyhod", font=("Arial",10), fg='white', bg="#f4a261", command=vyhod)
                bzm.place(x=400, y=450)



        Button = tk.Button(self, text="Hladaj zamestnanca", font=("Arial", 10), command=hladaj)
        Button.place(x=400, y=65)

    def restart(self):
        self.refresh()
        self.controller.show_frame(PrehladZamestnancov)

    def refresh(self):
        self.wentry.delete(0, "end")
        self.text.delete("1.0", "end")
        # set focus to any widget except a Text widget so focus doesn't get stuck in a Text widget when page hides
        self.wentry.focus_set()
    
    


class Krmenie(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        self.configure(bg='Tomato')
        
        Label = tk.Label(self, text="Krmenie", bg = "orange", font=("Arial Bold", 25))
        Label.place(x=40, y=150)
        
        Button = tk.Button(self, text="Home", font=("Arial", 15), command=lambda: controller.show_frame(SecondPage))
        Button.place(x=650, y=450)

class Cistenie(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        self.configure(bg='Tomato')
        
        Label = tk.Label(self, text="Cistenie", bg = "orange", font=("Arial Bold", 25))
        Label.place(x=40, y=150)
        
        Button = tk.Button(self, text="Home", font=("Arial", 15), command=lambda: controller.show_frame(SecondPage))
        Button.place(x=650, y=450)

class MojeZvierata(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        self.configure(bg='Tomato')
        
        Label = tk.Label(self, text="Moje Zvierata", bg = "orange", font=("Arial Bold", 25))
        Label.place(x=40, y=150)
        
        Button = tk.Button(self, text="Home", font=("Arial", 15), command=lambda: controller.show_frame(SecondPage))
        Button.place(x=650, y=450)

class Zvierata(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        self.configure(bg='Tomato')
        
        Label = tk.Label(self, text="Zvierata", bg = "orange", font=("Arial Bold", 25))
        Label.place(x=40, y=150)
        
        Button = tk.Button(self, text="Home", font=("Arial", 15), command=lambda: controller.show_frame(SecondPage))
        Button.place(x=650, y=450)


    
class ThirdPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        self.configure(bg='Tomato')
        
        Label = tk.Label(self, text="Store some content related to your \n project or what your application made for. \n All the best!!", bg = "orange", font=("Arial Bold", 25))
        Label.place(x=40, y=150)
        
        Button = tk.Button(self, text="Home", font=("Arial", 15), command=lambda: controller.show_frame(FirstPage))
        Button.place(x=650, y=450)
        
        Button = tk.Button(self, text="Back", font=("Arial", 15), command=lambda: controller.show_frame(SecondPage))
        Button.place(x=100, y=450)
        
        
class Application(tk.Tk):
    uzivatel = ''
    idu = ''
    admin = 0
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        
        #creating a window
        window = tk.Frame(self)
        window.pack()
        
        window.grid_rowconfigure(0, minsize = 500)
        window.grid_columnconfigure(0, minsize = 800)
        
        self.frames = {}
        for F in (FirstPage, SecondPage, ThirdPage, Krmenie, Cistenie, MojeZvierata, PrehladZamestnancov):
            frame = F(window, self)
            self.frames[F] = frame
            frame.grid(row = 0, column=0, sticky="nsew")
            
        self.show_frame(FirstPage)
        
    def show_frame(self, page):
        frame = self.frames[page]
        frame.tkraise()
        self.title("Application")

    def daj():
        print(Application.uzivatel)
            
app = Application()
app.maxsize(800,500)
app.mainloop()
