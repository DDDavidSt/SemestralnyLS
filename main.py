from calendar import prcal
from curses import window
import sqlite3

import tkinter as tk
from tkinter import INSERT, ttk
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
                if Application.admin:
                    controller.frames[SecondPage].zobraz_admin()
                    controller.show_frame(SecondPage)
                else:
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
        self.controller = controller
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
                t8 = ttk.Combobox(window, textvariable=pracovnik,values=options)
                t8.place(x=200, y=420)

                def check():
                    print(t1.get(), cal.get(), druh.get(),t4.get(), t5.get(), t6.get(), druh.get(), pracovnik.get())
                    if t1.get()!="" and cal.get()!="" and druh.get()!=""  and t4.get()!="" and t5.get()!="" and t6.get()!="" and druh.get()!="" and pracovnik.get()!='':
                        c.execute(f"SELECT * FROM druhy WHERE nazov='{druh.get()}'")
                        id_druh = c.fetchall()[0][0]
                        meno, priezvisko = pracovnik.get().split()
                        c.execute(f"SELECT * FROM zvierata WHERE meno='{t1.get()}' AND druh_id='{id_druh}'")
                        if len(c.fetchall()) > 1:
                                messagebox.showerror("Error", "Taketo zviera uz mame v databaze!",parent=window)
                        else:
                            c.execute(f"SELECT * FROM pracovnici WHERE meno='{meno}' AND priezvisko='{priezvisko}'")
                            id_prac = c.fetchall()[0][0]
                            # print(id_prac)
                            teraz = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
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
                            c.execute(f"SELECT * FROM pracovnici WHERE meno='{t1.get()}' AND priezvisko='{t12.get()}'")
                            if len(c.fetchall()) > 1:
                                messagebox.showerror("Error", "Zamestnanec s takymto menom a priezviskom uz existuje!",parent=window)
                            else:
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

        def prejdi_na_moje_zver(): #aby najprv vykreslilo customized plochu
            controller.frames[MojeZvierata].nacitaj()
            controller.show_frame(MojeZvierata)

        def prejdi_na_krm(): #aby najprv vykreslilo customized plochu
            controller.frames[Krmenie].nacitaj()
            controller.show_frame(Krmenie)

        def prejdi_na_cist(): #aby najprv vykreslilo customized plochu
            controller.frames[Cistenie].nacitaj()
            controller.show_frame(Cistenie)

        Button = tk.Button(self, text="Moje zvierata", font=("Arial", 8), bg='#bc6c25', command=prejdi_na_moje_zver)
        Button.place(x=x1, y=y1)
        y1 += delta
        Button = tk.Button(self, text="Krmenie", font=("Arial", 8), bg='#bc6c25', command=prejdi_na_krm)
        Button.place(x=x1+15, y=y1)
        y1 += delta-5
        Button = tk.Button(self, text="Cistenie", font=("Arial", 8), bg='#bc6c25', command=prejdi_na_cist)
        Button.place(x=x1+15, y=y1)        
        y1 += delta-5
        print(y1)
        # def zver():
        #     if Application.admin:
        #         controller.show_frame(Zvierata)
        #     else:
        #         messagebox.showerror("Error", "Na zadanu operaciu nemas prava!")
        # Button = tk.Button(self, text="--Zvierata--", font=("Arial", 8), bg='#283618',fg='white', command=zver)
        # Button.place(x=x1+5, y=y1)
        # y1 += delta-5
        # x1 -= 10

        # Button = tk.Button(self, text="--Pridaj zviera--", font=("Arial", 8), bg='#283618',fg='white', command=pridaj_zv)
        # Button.place(x=x1, y=y1)
        # y1 += delta

        # Button = tk.Button(self, text="--Pridaj zamestnanca--", font=("Arial", 8),  bg='#283618', fg='white',command=pridaj_zam)
        # Button.place(x=x1-15, y=y1)
        # y1 += delta-5

        # def prehlad():
        #     if Application.admin:
        #         controller.show_frame(PrehladZamestnancov)
        #     else:
        #         messagebox.showerror("Error", "Na zadanu operaciu nemas prava!")


        # Button = tk.Button(self, text="--Prehlad zamestnancov--", font=("Arial", 8), bg='#283618', fg='white',command=prehlad)
        # Button.place(x=x1-25, y=y1)        
        # y1 += delta-5

        Button = tk.Button(self, text="Prihlasenie/ Odhlasenie", font=("Arial", 8), bg='red', command=lambda: controller.show_frame(FirstPage))
        Button.place(x=625, y=10)
    def zobraz_admin(self):
        y1 = 235
        x1 = 365
        delta = 43
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
                t8 = ttk.Combobox(window, textvariable=pracovnik,values=options)
                t8.place(x=200, y=420)

                def check():
                    print(t1.get(), cal.get(), druh.get(),t4.get(), t5.get(), t6.get(), druh.get(), pracovnik.get())
                    if t1.get()!="" and cal.get()!="" and druh.get()!=""  and t4.get()!="" and t5.get()!="" and t6.get()!="" and druh.get()!="" and pracovnik.get()!='':
                        c.execute(f"SELECT * FROM druhy WHERE nazov='{druh.get()}'")
                        id_druh = c.fetchall()[0][0]
                        meno, priezvisko = pracovnik.get().split()
                        c.execute(f"SELECT * FROM zvierata WHERE meno='{t1.get()}' AND druh_id='{id_druh}'")
                        if len(c.fetchall()) > 1:
                                messagebox.showerror("Error", "Taketo zviera uz mame v databaze!",parent=window)
                        else:
                            c.execute(f"SELECT * FROM pracovnici WHERE meno='{meno}' AND priezvisko='{priezvisko}'")
                            id_prac = c.fetchall()[0][0]
                            # print(id_prac)
                            teraz = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
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
                            c.execute(f"SELECT * FROM pracovnici WHERE meno='{t1.get()}' AND priezvisko='{t12.get()}'")
                            if len(c.fetchall()) > 1:
                                messagebox.showerror("Error", "Zamestnanec s takymto menom a priezviskom uz existuje!",parent=window)
                            else:
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

        def zver():
            if Application.admin:
                self.controller.show_frame(Zvierata)
            else:
                messagebox.showerror("Error", "Na zadanu operaciu nemas prava!")
        Button = tk.Button(self, text="--Zvierata--", font=("Arial", 8), bg='#283618',fg='white', command=zver)
        Button.place(x=x1+5, y=y1)
        y1 += delta-5
        x1 -= 10

        Button = tk.Button(self, text="--Pridaj zviera--", font=("Arial", 8), bg='#283618',fg='white', command=pridaj_zv)
        Button.place(x=x1, y=y1)
        y1 += delta

        Button = tk.Button(self, text="--Pridaj zamestnanca--", font=("Arial", 8),  bg='#283618', fg='white',command=pridaj_zam)
        Button.place(x=x1-15, y=y1)
        y1 += delta-5

        def prehlad():
            if Application.admin:
                self.controller.show_frame(PrehladZamestnancov)
            else:
                messagebox.showerror("Error", "Na zadanu operaciu nemas prava!")


        Button = tk.Button(self, text="--Prehlad zamestnancov--", font=("Arial", 8), bg='#283618', fg='white',command=prehlad)
        Button.place(x=x1-25, y=y1)        
        y1 += delta-5

        

    

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
            print(Application.uzivatel)
            print(var.get())
            if var.get() != '':
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
                    print(self.id_us)
                    print(Application.admin)
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
                        if okoho.get() != '':
                            y1 = 160
                            x1 = 300
                            delta = 40
                            for key in stara[okoho.get()]:
                                fore = 'white'
                                if key == 'Naposledy krmene':
                                    print(stara[okoho.get()][key])
                                    if datetime.datetime.now() > (datetime.datetime.strptime(stara[okoho.get()][key], '%Y-%m-%d %H:%M:%S'))+datetime.timedelta(hours=int(stara[okoho.get()]['Frekvencia podavania stravy (hod)'])):
                                        fore = 'red'
                                    else:
                                        fore = 'green'
                                if key == 'Naposledy cistene':
                                    if datetime.datetime.now() > (datetime.datetime.strptime(stara[okoho.get()][key], '%Y-%m-%d %H:%M:%S'))+datetime.timedelta(days=int(stara[okoho.get()]['Cistenie (dni)'])):
                                        fore = 'red'
                                    else:
                                        fore = 'green'
                                kzm = tk.Label(self, text=f"{key}: {stara[okoho.get()][key]}", font=("Arial",15), fg=fore, bg="#f4a261")
                                kzm.place(x=x1, y=y1)
                                y1 += delta

                            def odober():
                                c.execute(f"UPDATE zvierata SET id_prac='0' WHERE meno='{okoho.get()}'")
                                messagebox.showinfo("Success", f"Zamestnancovi si odobral zviera {okoho.get()}")
                                hladaj()
                            Button = tk.Button(self, text="Odober zviera", font=("Arial", 8), bg='red',fg='white', command=odober)
                            Button.place(x=x1, y=y1)
                            y1 += delta
                        else:
                            messagebox.showerror("Error", "Nezvolene zviera!")

                    okoho = StringVar()
                    self.stara_zveri = (list(stara.keys()))

                    t1 = ttk.OptionMenu(self, okoho,*list(stara.keys()))
                    t1.place(x=x1, y=y1)

                    bzm = tk.Button(self, text="Detail", font=("Arial",10), fg='white', bg="#f4a261", command=vypis_stara)
                    bzm.place(x=x1+250, y=y1)

                    c.execute("SELECT * FROM zvierata WHERE id_prac='0'")
                    opaa = ['-']
                    for i in c.fetchall():
                        opaa.append(i[0])
                    
                    l5 = tk.Label(self, text="Pridaj zamestnancovi \n zvieratko:", font=("Arial",15), bg="#f4a261")
                    l5.place(x=10, y=250)
                    prid = StringVar()
                    t5 = tk.OptionMenu(self, prid, *opaa)
                    t5.place(x = 10, y=310)

                    def pridaj_zv_zm():
                        c.execute(f"UPDATE zvierata SET id_prac='{self.id_us}' WHERE meno='{prid.get()}'")
                        con.commit()
                        messagebox.showinfo("Success", f"Zamestnancovi {meno} {priezvisko} si priradil {prid.get()}")
                        hladaj()
                    pridaj = tk.Button(self, text="Pridaj", font=("Arial",10), fg='white', bg="#f4a261", command=pridaj_zv_zm)
                    pridaj.place(x=10, y=350)

                    def vyhod():
                        print(meno)
                        for odznac in self.stara_zveri:
                            c.execute(f"UPDATE zvierata SET id_prac='0' WHERE meno='{odznac}'")  
                        c.execute(f"DELETE FROM pracovnici WHERE meno='{meno}' AND priezvisko='{priezvisko}'")
                        con.commit()
                        if len(c.fetchall()) > 0: 
                            messagebox.showinfo('Success', 'Zamestnanca sa podarilo uspesne odstranit zo systemu')
                        else:
                            messagebox.showerror('Error', 'Zamestnanca sa nepodarilo odstranit zo systemu (neexistuje alebo nastal problem s databazou)')
                    bzm = tk.Button(self, text="Vyhod", font=("Arial",10), fg='white', bg="#f4a261", command=vyhod)
                    bzm.place(x=400, y=450)
            else:
                messagebox.showerror("Error", "Nezvoleny zamestnanec")


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
        self.controller = controller
        Label = tk.Label(self, text="Krmenie", bg = "orange", font=("Arial Bold", 25))
        Label.place(x=40, y=150)
        
        Button = tk.Button(self, text="Home", font=("Arial", 15), command=lambda: controller.show_frame(SecondPage))
        Button.place(x=650, y=450)

    def nakrm(self,ktore):
        c.execute(f'UPDATE zvierata SET posl_krm=\'{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\' WHERE meno=\'{ktore}\'')
        messagebox.showinfo("Success", f'Nakrmil si {ktore}')
        con.commit()
        self.nacitaj()

    def nacitaj(self):
        poz = tk.PhotoImage(file = 'sub_bgss.png')

        label = tk.Label(self, image=poz)
        label.image=poz
        label.place(x=0,y=0)

        Label = tk.Label(self, text=f" Rozpis krmenia pre {Application.uzivatel} ", bg = "#283618", bd=10,fg='#bc6c25',font=("Gulim", 25))
        
        Label.place(x=150, y=20)
        
        c.execute(f"SELECT * FROM zvierata, druhy WHERE druhy.id = zvierata.druh_id AND id_prac='{Application.idu}'")

        y1 = 100
        deltay = 30
        deltax = 100
        self.buttons = []
        poz = ['#ccd5ae','#e9edc9']
        i = 0
        for zviera in c.fetchall():
            x1 = 5
            i += 1
            if datetime.datetime.now() > (datetime.datetime.strptime(zviera[7], '%Y-%m-%d %H:%M:%S'))+datetime.timedelta(hours=int(zviera[5])):
                fore = 'red'
            elif datetime.datetime.now() > (datetime.datetime.strptime(zviera[7], '%Y-%m-%d %H:%M:%S'))+datetime.timedelta(hours=int(zviera[5])-2):
                fore = '#ffb703'
            else:
                i -= 1
                continue

            print(zviera)
            col_poz_descr = '#606c38' #farba pozadia na mena stlpcov tabulky
            text_poz_descr = '#e9c46a' #farba textu mena stlpcov
            col_poz_data = '#d4a373' # farba na jednotlive stlpce tabulky
            text_poz_data = '#faedcd' # farba textu dat
            col_zv = '#d4a373' # farba na zviera
            text_zv = '#faedcd' #farba textu zveri

            frame = tk.Frame(self, width=800,height=105, bg=poz[i%2])
            frame.place(x=0,y=y1-5)

            Label = tk.Label(self, text=f"{ zviera[0]}",width=21, bg = col_zv, font=('Gulim', 15),fg=text_zv)
            Label.place(x=x1, y=y1)
            x1 += 10
            y1 += deltay+10

            Label = tk.Label(self, text=f"DRUH",width=11, bg = col_poz_descr, font=("Arial Bold", 10), fg=text_poz_descr)
            Label.place(x=x1+2, y=y1)
            x1 += deltax+10

            Label = tk.Label(self, text=f"POTRAVA", width=11,bg = col_poz_descr, font=("Arial Bold", 10), fg=text_poz_descr)
            Label.place(x=x1+2, y=y1)
            x1 += deltax+10

            Label = tk.Label(self, text=f"krm.(hod)", width=8, bg = col_poz_descr, font=("Arial Bold", 10), fg=text_poz_descr)
            Label.place(x=x1+2, y=y1)
            x1 += deltax-20

            Label = tk.Label(self, text=f"Naposledy krm.",bg=col_poz_descr, width=24, font=("Arial Bold", 10), fg=text_poz_descr)
            Label.place(x=x1+2, y=y1)

            y1 += deltay
            x1 = 15
            Label = tk.Label(self, text=f"{zviera[-1]}",width=11, bg = col_poz_data, font=("Arial Bold", 10), fg=text_poz_data)
            Label.place(x=x1+2, y=y1)
            x1 += deltax+10

            Label = tk.Label(self, text=f"{zviera[4]}", width=11,bg = col_poz_data, font=("Arial Bold", 10), fg=text_poz_data)
            Label.place(x=x1+2, y=y1)
            x1 += deltax+10

            Label = tk.Label(self, text=f"{ zviera[5] }", width=8, bg = col_poz_data, font=("Arial Bold", 10), fg=text_poz_data)
            Label.place(x=x1+2, y=y1)
            x1 += deltax-20

            Label = tk.Label(self, text=f"{ zviera[7] }", width=18, bg = fore, font=("Arial Bold", 10),fg=text_poz_data)
            Label.place(x=x1+2, y=y1)
            x1 += deltax+75

            self.buttons.append(tk.Button(self, text="Nakrm", font=("Arial", 9), fg=text_poz_data, bd=0,padx=1,pady=1, bg='green', command=lambda i=zviera[0]: self.nakrm(i)))
            self.buttons[-1].place(x=x1-2, y=y1)
            x1 += 55
            y1 += deltay

        Button = tk.Button(self, text="Menu", font=("Arial", 15), bg='#283618', command=lambda: self.controller.show_frame(SecondPage))
        Button.place(x=650, y=450)

class Cistenie(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        self.configure(bg='Tomato')
        self.controller = controller
        Label = tk.Label(self, text="Cistenie", bg = "orange", font=("Arial Bold", 25))
        Label.place(x=40, y=150)
        
        Button = tk.Button(self, text="Home", font=("Arial", 15), command=lambda: controller.show_frame(SecondPage))
        Button.place(x=650, y=450)

    def vycisti(self,ktore):
        c.execute(f'UPDATE zvierata SET posl_cist=\'{(datetime.datetime.now()).strftime("%Y-%m-%d %H:%M:%S")}\' WHERE meno=\'{ktore}\'')
        messagebox.showinfo("Success", f'Vycistil si klietku pre {ktore}')
        con.commit()
        self.nacitaj()

    def nacitaj(self):
        poz = tk.PhotoImage(file = 'sub_bgss.png')

        label = tk.Label(self, image=poz)
        label.image=poz
        label.place(x=0,y=0)

        Label = tk.Label(self, text=f" Rozpis cistenia pre {Application.uzivatel} ", bg = "#283618", bd=10,fg='#bc6c25',font=("Gulim", 25))
        
        Label.place(x=150, y=20)
        
        c.execute(f"SELECT * FROM zvierata, druhy WHERE druhy.id = zvierata.druh_id AND id_prac='{Application.idu}'")

        y1 = 100
        deltay = 30
        deltax = 100
        self.buttons = []
        poz = ['#ccd5ae','#e9edc9']
        i = 0
        for zviera in c.fetchall():
            x1 = 5
            i += 1
            print( datetime.datetime.now(),datetime.datetime.strptime(zviera[8], '%Y-%m-%d %H:%M:%S'),(datetime.datetime.strptime(zviera[8], '%Y-%m-%d %H:%M:%S'))+datetime.timedelta(hours=int(zviera[6])))
            if datetime.datetime.now() > (datetime.datetime.strptime(zviera[8], '%Y-%m-%d %H:%M:%S'))+datetime.timedelta(hours=int(zviera[6])):
                fore = 'red'
            elif datetime.datetime.now() > (datetime.datetime.strptime(zviera[8], '%Y-%m-%d %H:%M:%S'))+datetime.timedelta(hours=int(zviera[6])-1):
                fore = '#ffb703'
            else:
                i -= 1
                continue


            print(zviera)
            col_poz_descr = '#606c38' #farba pozadia na mena stlpcov tabulky
            text_poz_descr = '#e9c46a' #farba textu mena stlpcov
            col_poz_data = '#d4a373' # farba na jednotlive stlpce tabulky
            text_poz_data = '#faedcd' # farba textu dat
            col_zv = '#d4a373' # farba na zviera
            text_zv = '#faedcd' #farba textu zveri

            frame = tk.Frame(self, width=800,height=105, bg=poz[i%2])
            frame.place(x=0,y=y1-5)

            Label = tk.Label(self, text=f"{ zviera[0]}",width=21, bg = col_zv, font=('Gulim', 15),fg=text_zv)
            Label.place(x=x1, y=y1)
            x1 += 10
            y1 += deltay+10

            Label = tk.Label(self, text=f"DRUH",width=11, bg = col_poz_descr, font=("Arial Bold", 10), fg=text_poz_descr)
            Label.place(x=x1+2, y=y1)
            x1 += deltax+10

            Label = tk.Label(self, text=f"POTRAVA", width=11,bg = col_poz_descr, font=("Arial Bold", 10), fg=text_poz_descr)
            Label.place(x=x1+2, y=y1)
            x1 += deltax+10

            Label = tk.Label(self, text=f"cist.(dni)", width=8, bg = col_poz_descr, font=("Arial Bold", 10), fg=text_poz_descr)
            Label.place(x=x1+2, y=y1)
            x1 += deltax-20

            Label = tk.Label(self, text=f"Naposledy cist.",bg=col_poz_descr, width=24, font=("Arial Bold", 10), fg=text_poz_descr)
            Label.place(x=x1+2, y=y1)

            y1 += deltay
            x1 = 15
            Label = tk.Label(self, text=f"{zviera[-1]}",width=11, bg = col_poz_data, font=("Arial Bold", 10), fg=text_poz_data)
            Label.place(x=x1+2, y=y1)
            x1 += deltax+10

            Label = tk.Label(self, text=f"{zviera[4]}", width=11,bg = col_poz_data, font=("Arial Bold", 10), fg=text_poz_data)
            Label.place(x=x1+2, y=y1)
            x1 += deltax+10

            Label = tk.Label(self, text=f"{ zviera[6] }", width=8, bg = col_poz_data, font=("Arial Bold", 10), fg=text_poz_data)
            Label.place(x=x1+2, y=y1)
            x1 += deltax-20

            Label = tk.Label(self, text=f"{ zviera[8] }", width=18, bg = fore, font=("Arial Bold", 10),fg=text_poz_data)
            Label.place(x=x1+2, y=y1)
            x1 += deltax+75

            self.buttons.append(tk.Button(self, text="Vycisti", font=("Arial", 9), fg=text_poz_data, bd=0,padx=1,pady=1, bg='green', command=lambda i=zviera[0]: self.vycisti(i)))
            self.buttons[-1].place(x=x1-2, y=y1)
            x1 += 55
            y1 += deltay

        Button = tk.Button(self, text="Menu", font=("Arial", 15), bg='#283618', command=lambda: self.controller.show_frame(SecondPage))
        Button.place(x=650, y=450)

class MojeZvierata(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        poz = tk.PhotoImage(file = 'sub_bgss.png')

        label = tk.Label(self, image=poz)
        label.image=poz
        label.place(x=0,y=0)
        self.controller = controller
        Button = tk.Button(self, text="Menu", font=("Arial", 15), command=lambda: controller.show_frame(SecondPage))
        Button.place(x=650, y=450)

    def nakrm(self,ktore):
        c.execute(f'UPDATE zvierata SET posl_krm=\'{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\' WHERE meno=\'{ktore}\'')
        messagebox.showinfo("Success", f'Nakrmil si {ktore}')
        con.commit()
        self.nacitaj()

    def vycisti(self,ktore):
        c.execute(f'UPDATE zvierata SET posl_cist=\'{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\' WHERE meno=\'{ktore}\'')
        messagebox.showinfo("Success", f'Vycistil si klietku pre {ktore}')
        con.commit()
        self.nacitaj()

    def nacitaj(self):
        poz = tk.PhotoImage(file = 'sub_bgss.png')

        label = tk.Label(self, image=poz)
        label.image=poz
        label.place(x=0,y=0)

        Label = tk.Label(self, text=f" Zvierata pouzivatela {Application.uzivatel} ", bg = "#283618", bd=10,fg='#bc6c25',font=("Gulim", 25))
        
        Label.place(x=150, y=20)
        
        c.execute(f"SELECT * FROM zvierata, druhy WHERE druhy.id = zvierata.druh_id AND id_prac='{Application.idu}'")
        x1 = 5
        y1 = 100
        deltay = 30
        deltax = 100
        self.buttons = []
        for zviera in c.fetchall():
            print(zviera)
            col_poz_descr = '#606c38' #farba pozadia na mena stlpcov tabulky
            text_poz_descr = '#e9c46a' #farba textu mena stlpcov
            col_poz_data = '#d4a373' # farba na jednotlive stlpce tabulky
            text_poz_data = '#faedcd' # farba textu dat
            col_zv = '#d4a373' # farba na zviera
            text_zv = '#faedcd' #farba textu zveri

            frame = tk.Frame(self, width=800,height=105, bg="#fefae0")
            frame.place(x=0,y=y1-5)

            Label = tk.Label(self, text=f"{ zviera[0]}",width=21, bg = col_zv, font=('Gulim', 15),fg=text_zv)
            Label.place(x=x1, y=y1)
            x1 += 10
            y1 += deltay+10

            Label = tk.Label(self, text=f"DRUH",width=11, bg = col_poz_descr, font=("Arial Bold", 10), fg=text_poz_descr)
            Label.place(x=x1+2, y=y1)
            x1 += deltax+10

            Label = tk.Label(self, text=f"POTRAVA", width=11,bg = col_poz_descr, font=("Arial Bold", 10), fg=text_poz_descr)
            Label.place(x=x1+2, y=y1)
            x1 += deltax+10

            Label = tk.Label(self, text=f"krm.(hod)", width=8, bg = col_poz_descr, font=("Arial Bold", 10), fg=text_poz_descr)
            Label.place(x=x1+2, y=y1)
            x1 += deltax-20

            Label = tk.Label(self, text=f"cist(dni)", width=8,bg = col_poz_descr, font=("Arial Bold", 10), fg=text_poz_descr)
            Label.place(x=x1+2, y=y1)
            x1 += deltax-20
    
            Label = tk.Label(self, text=f"Naposledy krm.",bg=col_poz_descr, width=24, font=("Arial Bold", 10), fg=text_poz_descr)
            Label.place(x=x1+2, y=y1)
            x1 += deltax+130

            Label = tk.Label(self, text=f"Naposledy cist.",bg=col_poz_descr, width=18, fg=text_poz_descr, font=("Arial Bold", 10))
            Label.place(x=x1+2, y=y1)
            x1 += 115
            y1 += deltay
            x1 = 15
            Label = tk.Label(self, text=f"{zviera[-1]}",width=11, bg = col_poz_data, font=("Arial Bold", 10), fg=text_poz_data)
            Label.place(x=x1+2, y=y1)
            x1 += deltax+10

            Label = tk.Label(self, text=f"{zviera[4]}", width=11,bg = col_poz_data, font=("Arial Bold", 10), fg=text_poz_data)
            Label.place(x=x1+2, y=y1)
            x1 += deltax+10

            Label = tk.Label(self, text=f"{ zviera[5] }", width=8, bg = col_poz_data, font=("Arial Bold", 10), fg=text_poz_data)
            Label.place(x=x1+2, y=y1)
            x1 += deltax-20

            Label = tk.Label(self, text=f"{ zviera[6] }", width=8,bg = col_poz_data, font=("Arial Bold", 10), fg=text_poz_data)
            Label.place(x=x1+2, y=y1)
            x1 += deltax-20
            if datetime.datetime.now() > (datetime.datetime.strptime(zviera[7], '%Y-%m-%d %H:%M:%S'))+datetime.timedelta(hours=int(zviera[5])):
                fore = 'red'
            else:
                fore = 'green'
            Label = tk.Label(self, text=f"{ zviera[7] }", width=18, bg = fore, font=("Arial Bold", 10),fg=text_poz_data)
            Label.place(x=x1+2, y=y1)
            x1 += deltax+75

            self.buttons.append(tk.Button(self, text="Nakrm", font=("Arial", 9), fg=text_poz_data, bd=0,padx=1,pady=1, bg='green', command=lambda i=zviera[0]: self.nakrm(i)))
            self.buttons[-1].place(x=x1-2, y=y1)
            x1 += 55

            if datetime.datetime.now() > (datetime.datetime.strptime(zviera[8], '%Y-%m-%d %H:%M:%S'))+datetime.timedelta(hours=int(zviera[6])):
                fore = 'red'
            else:
                fore = 'green'
            Label = tk.Label(self, text=f"{ zviera[8][:-9] }", width=11,bg = fore, fg=text_poz_data, font=("Arial Bold", 10))
            Label.place(x=x1+2, y=y1)
            x1 += 118

            self.buttons.append(tk.Button(self, text="Vycisti", font=("Arial", 9), fg=text_poz_data,bd=0,padx=1,pady=1, bg='green', command=lambda i=zviera[0]: self.vycisti(i)))
            self.buttons[-1].place(x=x1, y=y1)
            x1 = 5
            y1 += deltay+20

        Button = tk.Button(self, text="Menu", font=("Arial", 15), bg='#283618', command=lambda: self.controller.show_frame(SecondPage))
        Button.place(x=650, y=450)

class Zvierata(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        self.configure(bg='Tomato')

        poz = tk.PhotoImage(file = 'sub_bgss.png')

        label = tk.Label(self, image=poz)
        label.image=poz
        label.place(x=0,y=0)

        Label = tk.Label(self, text=f" Prehlad zvierat ", bg = "#283618", bd=10,fg='#bc6c25',font=("Gulim", 25))
        Label.place(x=150, y=20)


        col_zv = '#d4a373' # farba na zviera
        text_zv = '#faedcd' #farba textu zveri

        frame = tk.Frame(self, width=800,height=50, bg="#fefae0")
        frame.place(x=0,y=95-5)
        l1 = tk.Label(self, text=f"Zviera:",width=12, bg = col_zv, font=('Gulim', 10),fg=text_zv)
        l1.place(x=20, y=100)
        zviera = StringVar()
        c.execute("SELECT * FROM zvierata")
        options = [i[0] for i in c.fetchall()]
        t1 = ttk.Combobox(self, textvariable=zviera, values=options)
        t1.place(x=150, y=100)

        def hladaj():

            y1 = 150
            x1 = 5
            dy = 35
            print(zviera.get())
            c.execute(f"SELECT * FROM zvierata WHERE meno='{zviera.get()}'")
            inf = (c.fetchall())
            
            if len(inf)>0:
                inf = list(inf[0])
                nazvy = ['Druh', 'Povod', 'Narodene', 'Potrava', 'Frekvencia krmenia (hod)', 'Frekvencia cistenia (dni)', 'Naposledy krmene', 'Naposledy cistene', 'Stara sa on: ']
                c.execute(f"SELECT * FROM druhy WHERE id='{inf[1]}'")
                druh = c.fetchall()[0][1]
                print(druh)
                inf[1] = druh
                c.execute(f"SELECT * FROM pracovnici WHERE id='{inf[-1]}'")
                prac = c.fetchall()[0][1]
                inf[-1] = prac
                for nazov,info in enumerate(inf[1:]):
                    frame = tk.Frame(self, width=800,height=30, bg="#fefae0")
                    frame.place(x=0,y=y1-5)
                    l1 = tk.Label(self, text=f"{nazvy[nazov]}: {info}",width=50, bg = col_zv, font=('Gulim', 10),fg=text_zv)
                    l1.place(x=400, y=y1+9, anchor='center')
                    y1 += dy

                            
                def vymaz():
                    print(zviera, zviera.get())
                    c.execute(f"DELETE FROM zvierata WHERE meno='{zviera.get()}'")
                    con.commit()
                    messagebox.showinfo("Success", "Zviera bolo vymazane z databazy")

                Button = tk.Button(self, text="Vymaz", font=("Arial", 15), bg='red', command=vymaz)
                Button.place(x=350 , y=460)
            else:
                messagebox.showerror("Error", "nepodarilo sa najst")
        


        Button = tk.Button(self, text="Vyhladaj zviera", font=("Arial", 7), bg='#283618',fg=text_zv, command=hladaj)
        Button.place(x=350, y=100)

        
        Button = tk.Button(self, text="Menu", font=("Arial", 15), bg='#283618', command=lambda: controller.show_frame(SecondPage))
        Button.place(x=650, y=460)
    
        
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
        for F in (FirstPage, SecondPage, Zvierata, Krmenie, Cistenie, MojeZvierata, PrehladZamestnancov):
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
