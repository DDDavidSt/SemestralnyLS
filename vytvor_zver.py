import json
from datetime import date, datetime
import random

dic = {} #v nom si budeme pamatat id kategorie
for id,i in enumerate('bezstavovce cicavce obojzivelniky ostatne vtaky'.split()):
    dic[i] = id

another = {}
pot = {
    'bezstavovce':list('cukry tuky bielkoviny voda minerálny vitamíny'.split()) ,
    'cicavce': list('maso byliny hmyz dazdovky semena'.split()) ,
    'obojzivelniky': list('rastlinny listy dazdovky larvy'.split()) ,
    'ostatne': list('mix3000-ultra obilniny granulky'.split()),
    'vtaky': list('larvy, ziabre, chrobaky, dazdovky')
}
for i in dic:
    with open(f"{i}.txt") as f:
        for ziv in f:
            ziv =ziv.strip()
            another[ziv] = {}
            zviera = ziv
            druh =  dic[i]
            another[ziv]['druh'] = druh
            
            miesto =  random.choice(('Europa','Azia', 'Afrika','Australia','Amerika','Brazilia','Slovensko'))
            another[ziv]['miesto_nar'] = miesto
            
            narodenie = datetime(random.randrange(2010, 2023), random.randrange(1,6), random.randrange(1,28), random.randrange(1,24), random.randrange(1,60))
            another[ziv]['narodeny'] = narodenie 
            
            potrava = random.choice(pot[i])
            another[ziv]['potrava'] = potrava
            
            frekvencia = random.randint(3,10)
            another[ziv]['frekvencia_potr'] = frekvencia
            
            cistenie = random.randint(1,3)
            another[ziv]['cistenie'] = cistenie
            
            posledne_krm = datetime(2022, 5, random.randrange(24,28), random.randrange(1,24))
            another[ziv]['posl_krm'] = posledne_krm
            
            posledne_cist = datetime(2022, 5, random.randrange(20,28), random.randrange(1,24))
            another[ziv]['posl_cist'] = posledne_cist

def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError ("Type %s not serializable" % type(obj))

with open('zvierata.txt','w') as zv:
    json.dump(another, zv, indent=2,default=json_serial)

print(another)