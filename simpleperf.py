import socket
from socket import *
import sys
import _thread as thread

input_lengde = len(sys.argv)

Port = 8088
Ip = '127.0.0.1'
Format = "MB"
time = 50

virker = True


#Tomme argimenter kan løses på to måter. Bruke default eller avslutte prosess


x = 0

#While løkke som går gjennom input argumentene
for i in sys.argv:


    # Finner porten fra input argumentene
    if i =="-p":
        Port = int (sys.argv[x+1])

        if Port<1024:
            print("Feil! Porten stemmer ikke. Skriv inn en port som er større eller lik 1024")
            virker = False
        elif Port > 65535:
            print("Feil! Porten stemmer ikke. Skriv inn en port som er mindre eller lik 65535")
            virker = False


    # Finner foramten fra input argumentene
    if i == "-f":
        Format = sys.argv[x+1]
        if Format != "KB" and Format != "MB" and Format != "B":
            print("Skriv inn riktig format. Enten KB, MB eller B etter -f")
            virker = False


    # Finner ip-adressen fra input argumentene
    if (i == "-b"):
        Ip = sys.argv[x+1]
        print(Ip)



    # Finner ip-adressen fra input argumentene
    if (i == "-I"):
        Ip = sys.argv[x+1]


    # Finner tiden fra input argumentene
    if (i == "-t"):
        time = int(sys.argv[x+1])
        if (time <= 0):
            print("Tid må være større en 0")


    # Finner intervallet fra input argumentene
    if (i == "-i"):
        intervall = sys.argv[x+1]


    # Finner antall paralelle klienter fra input argumentene
    if (i == "-P"):
        paraleller = sys.argv[x+1]


    # Finner antall paralelle klienter fra input argumentene
    if (i == "-n"):
        no_of_bytes = sys.argv[x+1]
        # if (no_of_bytes == ""):

    x=x+1


if virker == False:
    print("Feil i syntax. Prøv igjen")


else:
    #Server kode
    if (sys.argv[1] == "-s"):


        sock = socket(AF_INET, SOCK_STREAM)

        sock.bind((Ip, Port))
        sock.listen(5)

        # mens serveren er åpen
        while True:
            #Klart til å betjene klient
            print("[Server] Klar til å koble seg til ")





    #Klient kode
    elif (sys.argv[1] == "-c"):

        sock = socket(AF_INET, SOCK_STREAM)
        sock.connect((Ip, Port))


    else:
        print("Error: you must run either in server or client mode")