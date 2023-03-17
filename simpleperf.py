
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
klienter = []


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


def handle_client(conn, addr):
    print(f"New client connected: {addr}")

    # Add the client to the list of clients
    klienter.append(conn)

    # Loop to handle incoming messages from the client
    while True:
        data = conn.recv(1024)
        if not data:
            break
        message = data.decode()
        print(f"Received message from {addr}: {message}")





if virker == False:
    print("Feil i syntax. Prøv igjen")


else:
    #Server kode
    if (sys.argv[1] == "-s"):


        sock = socket(AF_INET, SOCK_STREAM)

        sock.bind((Ip, Port))
        sock.listen(5)

        print("[Server] Klar til å koble seg til ")
        # mens serveren er åpen
        print("klar til å motta")

        while True:
            conn, addr = sock.accept()
            handle_client(conn, addr)




    #Klient kode
    elif (sys.argv[1] == "-c"):

        sock = socket(AF_INET, SOCK_STREAM)
        sock.connect((Ip, Port))
        message = "Hei"
        sock.sendall(message.encode())


    else:
        print("Error: you must run either in server or client mode")