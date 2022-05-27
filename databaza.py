from random import shuffle
import sqlite3
import hashlib
con = sqlite3.connect(':memory:')

c = con.cursor()

c.execute("""CREATE TABLE zvierata(
    meno text,
    druh_id text,
    miesto text,
    datum_nar date,
    potrava text,
    heslo text,
    frekvencia_strava integer,
    cistenie_frek integer,
    posl_cist date,
    id_prac integer
)
""")

c.execute("""CREATE TABLE pracovnici(
    id integer,
    meno text,
    priezvisko text,
    heslo text,
    admin integer

)
""")

c.execute("""CREATE TABLE druhy(
    nazov text,
    id integer
)
""")
con.commit()

zames = []
with open('mena_zam.txt','r') as f:
    for i in f:
        zames.append((i.strip(),))
        heslo = i.strip().replace("á","a").replace("ľ","l").replace("š","s").replace("č","c").replace("ť","t").replace("ž","z")
        heslo = heslo.replace("ý","y").replace("ň","n").replace("í","i").replace("é","e").replace("ď","d").replace("ŕ","r").replace("ĺ","l")
        heslo = heslo.replace("ú","u").replace("ó","o").replace("ô","o").replace("ä","a")
        zames[-1] += heslo.lower(),


with open('priezviska.txt') as f:
    shuffle(zames)
    k = 0
    for i in f:
        zames[k] += i.strip(),
        k += 1
        if k == len(zames):
            break

zames.append(('admin','admin','admin'))

#str(hashlib.md5(f"b'{heslo}'".encode('utf-8')).hexdigest())
k = 0
while zames:
    meno, heslo, priezvisko = zames.pop(0)
    c.execute("INSERT INTO pracovnici VALUES (:id, :meno, :priezvisko, :heslo, :admin)", {'id':k,'meno':meno,'priezvisko':priezvisko,'heslo':str(hashlib.md5(f"b'{heslo}'".encode('utf-8')).hexdigest()),'admin':0})
    k += 1
con.commit()

print(str(hashlib.md5(f"b'liana'".encode('utf-8')).hexdigest()))
cur = 'liana'
hes = str(hashlib.md5(f"b'{cur}'".encode('utf-8')).hexdigest())
c.execute(f"SELECT * FROM pracovnici WHERE meno='Liana' AND heslo='{hes}'")
for i in c.fetchall():
    print(i)



con.close()