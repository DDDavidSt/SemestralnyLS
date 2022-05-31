#vytvorenie databazy(spustit raz)

from random import shuffle
import random
import sqlite3
import hashlib
import json
import datetime # vytvarranie datumov
con = sqlite3.connect('zoo.db')

c = con.cursor()

c.execute("""CREATE TABLE zvierata(
    meno text,
    druh_id integer,
    miesto text,
    datum_nar TIMESTAMP,
    potrava text,
    frekvencia_strava_hod integer,
    cistenie_frek_den integer,
    posl_krm TIMESTAMP,
    posl_cist TIMESTAMP,
    id_prac integer
)
""")

c.execute("""CREATE TABLE pracovnici(
    id INTEGER PRIMARY KEY,
    meno text,
    priezvisko text,
    heslo text,
    admin integer
)
""")

c.execute("""CREATE TABLE druhy(
    id INTEGER PRIMARY KEY,
    nazov text
)
""")
con.commit()

##vytvorenie tab zamestnancov
k = 0
with open('zamestnanci.txt') as f:
    for i in f:
        meno, priezvisko, heslo= i.split()
        heslo = str(hashlib.md5(f"b'{heslo}'".encode('utf-8')).hexdigest())
        c.execute(f"INSERT INTO 'pracovnici' ('meno', 'priezvisko', 'heslo', 'admin') VALUES ('{meno}','{priezvisko}','{heslo}','0')")
        k += 1

con.commit()
###KONIEC

#takto sa zistuje spravnost hesla
# cur = 'liana'
# hes = str(hashlib.md5(f"b'{cur}'".encode('utf-8')).hexdigest())

# c.execute(f"SELECT * FROM pracovnici WHERE meno='Liana' AND heslo='{hes}'")
# for i in c.fetchall():
#     print(i)

# vytvorenie databazy druhov
dic = {} #v nom si budeme pamatat id kategorie
for id,i in enumerate('bezstavovce cicavce obojzivelniky ostatne vtaky'.split()):
    c.execute("INSERT INTO druhy VALUES (:id, :nazov)", {'id':id, 'nazov':i})
    dic[i] = id

#zapamatanie si dict druhov kvoli ich id
with open('druhy.txt','w') as d:
    json.dump(dic, d, indent=2)

con.commit()

# c.execute("SELECT * FROM druhy")

# for i in c.fetchall():
#     print(i)
###################################

#vytvorenie databazy zvierat

another = {}
pot = {
    'bezstavovce':list('cukry tuky bielkoviny voda minerály vitamíny'.split()) ,
    'cicavce': list('maso byliny hmyz dazdovky semena'.split()) ,
    'obojzivelniky': list('rastlinny listy dazdovky larvy'.split()) ,
    'ostatne': list('mix3000-ultra obilniny granulky'.split()),
    'vtaky': list('larvy, ziabre, chrobaky, dazdovky'.split())
}
for i in dic:
    with open(f"{i}.txt") as f:
        for ziv in f:
            ziv =ziv.strip()
            zviera = ziv
            druh =  dic[i]

            miesto =  random.choice(('Europa','Azia', 'Afrika','Australia','Amerika','Brazilia','Slovensko'))
            
            narodenie = datetime.datetime(random.randrange(2010, 2023), random.randrange(1,6), random.randrange(1,28), random.randrange(1,24), random.randrange(1,60))

            potrava = random.choice(pot[i])
            
            frekvencia = random.randint(3,10)
            
            cistenie = random.randint(1,3)
            
            posledne_krm = datetime.datetime(2022, 5, random.randrange(24,28), random.randrange(1,24))
            
            posledne_cist = datetime.datetime(2022, 5, random.randrange(20,28), random.randrange(1,24))
            id = random.randrange(66)
            c.execute(f"INSERT INTO zvierata ('meno','druh_id','miesto','datum_nar','potrava','frekvencia_strava_hod','cistenie_frek_den','posl_krm','posl_cist','id_prac') VALUES ('{zviera}','{druh}','{miesto}','{narodenie}','{potrava}','{frekvencia}','{cistenie}','{posledne_krm}','{posledne_cist}','{id}')")

con.commit()

# c.execute("SELECT * FROM zvierata")
# for i in c.fetchall():
#     print(i)

con.close()