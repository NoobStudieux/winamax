#!/usr/bin/python3.6
# -*-coding:Latin-1 -*

import sqlite3

conn = sqlite3.connect("wina_data.sq3")
cur = conn.cursor()

tables = cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
#cur.close()
chaine = "<!DOCTYPE html><html><body><h1>Resultats : </h1>"
for t in tables:
    print(t)
    cur2 = conn.cursor()
    maTable = cur2.execute("select * from %s" % t)
    chaine += "<h4>" + str(t) + "</h4>"
    chaine += "<table>"
    for m in maTable:
        chaine += "<tr><td>" + str(m[0]) + "</td><td>       <strong>" + str(m[1]) + \
        "</strong>      </td><td style='color:red'>   " + str(m[2]) + "   </td><td>   " + str(m[3]) + "   </td><td style='color:blue'>     --[+]--     " \
        + str(m[4]) + "</td></tr>"
    chaine += "</table>"
    cur2.close()
chaine += "</body></html>"

with open("resultats.html", "w") as fichier:
    fichier.write(chaine)

cur.close()
conn.close()