from random import shuffle
zames = []
with open('mena_zam.txt','r') as f:
    for i in f:
        zames.append((i.strip(),))
        heslo = i.strip().replace("á","a").replace("ľ","l").replace("š","s").replace("č","c").replace("ť","t").replace("ž","z")
        heslo = heslo.replace("ý","y").replace("ň","n").replace("í","i").replace("é","e").replace("ď","d").replace("ŕ","r").replace("ĺ","l")
        heslo = heslo.replace("ú","u").replace("ó","o").replace("ô","o").replace("ä","a")
        zames[-1] += heslo.lower(),


with open('priezviska.txt') as f, open('zamestnanci.txt', 'w') as z:
    shuffle(zames)
    k = 0
    for i in f:
        zames[k] += i.strip(),
        print(zames[k][0], i.strip(), zames[k][1], file=z)
        k += 1
        if k == len(zames):
            break

    print('admin admin admin', file=z)