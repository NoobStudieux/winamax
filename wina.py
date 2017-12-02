#!/usr/bin/python3.6
# -*-coding:Latin-1 -*

from urllib.request import urlopen
from bs4 import BeautifulSoup
import time, pickle, sqlite3

t = time.localtime()
nom_g = "wina" + str(t.tm_year) + str(t.tm_mon) + str(t.tm_mday)
nom_basses = str(nom_g + "basses")
nom_micros = str(nom_g + "micros")

url_basses = "https://www.winamax.fr/les-challenges-winamax_cash-game_classement-basses-limites"
url_micros = "https://www.winamax.fr/les-challenges-winamax_cash-game_classement-micro-limites"

# init BDD: 
try:
    conn = sqlite3.connect("wina_data.sq3")
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS " + nom_micros + " (date DATETIME, classement INTEGER, pseudo TEXT, nb_mains INTEGER, nb_caves REAL)")
    cur.execute("CREATE TABLE IF NOT EXISTS " + nom_basses + " (date DATETIME, classement INTEGER, pseudo TEXT, nb_mains INTEGER, nb_caves REAL)")
except Exception as e:
    print(e)
try :
    html_micros = urlopen(url_micros)
    html_basses = urlopen(url_basses)
except HTTPError as e:
    print(e)
try:
    bs_m = BeautifulSoup(html_micros.read(), "html.parser")
    bs_b = BeautifulSoup(html_basses.read(), "html.parser")
    micros = bs_m("tr", recursive=True)
    basses = bs_b("tr", recursive=True)
    micros_str= "" 
    c = 0
    for l in micros :
        if not c == 0 and not 101 == c:
            if c < 21:
                mains = int(l.findAll()[4].get_text().replace(" ",""))
                caves = float(l.findAll()[6].get_text().replace(',', '.'))
                ligne = (int(l.findAll()[0].get_text()), l.findAll()[2].get_text(), mains, caves)
                cur.execute("INSERT INTO " + nom_micros + " (date, classement, pseudo, nb_mains, nb_caves) VALUES(CURRENT_TIMESTAMP, ?,?,?,?)", ligne)
            else:
                mains = int(l.findAll()[2].get_text().replace(" ",""))
                caves = float(l.findAll()[3].get_text().replace(',', '.'))
                ligne = (int(l.findAll()[0].get_text()), l.findAll()[1].get_text(), mains, caves)
                cur.execute("INSERT INTO " + nom_micros + "(date, classement, pseudo, nb_mains, nb_caves) VALUES(CURRENT_TIMESTAMP, ?,?,?,?)", ligne)
        c += 1 
    c= 0
    for a in basses:
        if not c == 0 and not 101 == c:
            if c < 21:
                mains = int(a.findAll()[4].get_text().replace(" ",""))
                caves = float(a.findAll()[6].get_text().replace(',', '.'))
                ligne = (int(a.findAll()[0].get_text()), a.findAll()[2].get_text(), mains, caves)
                cur.execute("INSERT INTO " + nom_basses +"(classement, pseudo, nb_mains, nb_caves) VALUES(?,?,?,?)", ligne)
            else:
                mains = int(a.findAll()[2].get_text().replace(" ",""))
                caves = float(a.findAll()[3].get_text().replace(',', '.'))
                ligne = (int(a.findAll()[0].get_text()), a.findAll()[1].get_text(), mains, caves)
                cur.execute("INSERT INTO " + nom_basses + "(classement, pseudo, nb_mains, nb_caves) VALUES(?,?,?,?)", ligne)
        c += 1
    conn.commit()
    cur.close()
    conn.close()
        
except AttributeError as e:
    print(e)


