autori_rijeci = []
autori = []
keywords = []
parovi = []
matches = []
past = []
lista = []


with open("C:/Users/Lenovo/Desktop/upz_mreze/autori_kljucnerijeci.txt", "r",  encoding="utf-8-sig") as f:
    for line in f:
        autori_rijeci.append(line.strip())

# clean name of authors from extra characters
# did the same to keywords
# save them to list parovi
for par in autori_rijeci:
    podjela = par.split("|")
    autor = podjela[0].lower().replace(", ",",").replace("č", "c").replace("ć", "c").replace("š", "s")\
        .replace("ž", "z").replace("đ", "d").replace("á", "a").replace("ă", "a").replace("ã", "a").split(",")
    autori.append(autor)
    keys = podjela[1].replace(",", ";").replace("; ",";").lower().split(";")
    keywords.append(keys)
    parovi.append([autor,keys])

autor_rijeci = dict()

# make a dictionary of authors and their keywords
# to every author add a list of keywords
for i in range(0,len(autori)):
    for a in range(0,len(autori[i])):
        autor = autori[i][a]
        for j in range(0, len(keywords)):
            for k in range(0, len(keywords[j])):
                rijec = keywords[j][k]
                for par in parovi:
                    if autor in par[0] and rijec in par[1]:
                        autor_rijeci.setdefault(autor, [])
                        if autor in autor_rijeci:
                            autor_rijeci[autor].append(rijec)
                        else:
                            autor_rijeci[autor] = rijec

for k,v in autor_rijeci.items():
    lista.append([k,v])

# check how much common keywords have every pair of authors
# save result in format Author1;Author2;NumberOfCommonKeywords
def checker(ime, rijeci):
    broj = 0
    for red in lista:
        ime2 = red[0]
        if ime != ime2 and ime2 not in past and ime not in past:
            kljucne = set(rijeci).intersection(red[1])
            broj = len(kljucne)

            if broj > 0:
                matches.append('"%s";"%s";%d' % (ime, ime2, broj))
    past.append(ime)
    return

for red in lista:
    checker(red[0], red[1])

# save result in file
with open('C:/Users/Lenovo/Desktop/upz_mreze/organizacija.edges', 'w') as f:
    for m in matches:
        f.write(m + "\n")
