from socket import *
import sys
import _thread as thread

input_lengde = len(sys.argv)
Port = 8088
Ip = '127.0.0.1'
Format = "MB"
time = 50

i =1
#While løkke som går gjennom input argumentene
while( i < input_lengde):

    # Finner porten fra input argumentene
    if (sys.argv[i] == "-p"):
        Port = int (sys.argv[i+1])
        if(Port<1024):
            print("Feil! Porten stemmer ikke. Skriv inn en port som er større eller lik 1024")
        elif(Port > 65535):
            print("Feil! Porten stemmer ikke. Skriv inn en port som er mindre eller lik 65535")

    # Finner foramten fra input argumentene
    if (sys.argv[i] == "-f"):
        Format = sys.argv[i+1]
    ++i


#Server kode
if (sys.argv[1] == "-s"):

    i=0
    while (i < input_lengde):
        # Finner ip-adressen fra input argumentene
        if (sys.argv[i] == "-b"):
            Ip = sys.argv[i+1]


        
    sock = socket(AF_INET, SOCK_STREAM)

    sock.bind((Ip, Port))
    sock.listen(1)


#Klient kode
elif (sys.argv[1] == "-c"):

    i=0
    while (i < input_lengde):
        # Finner ip-adressen fra input argumentene
        if (sys.argv[i] == "-I"):
            Ip = sys.argv[i+1]

        # Finner tiden fra input argumentene
        if (sys.argv[i] == "-t"):
            time = int (sys.argv[i+1])
            if(time <=0):
                print("Tid må være større en 0")

        # Finner intervallet fra input argumentene
        if (sys.argv[i] == "-i"):
            intervall = sys.argv[i+1]

        # Finner antall paralelle klienter fra input argumentene
        if (sys.argv[i] == "-P"):
            paraleller= sys.argv[i + 1]

        # Finner antall paralelle klienter fra input argumentene
        if (sys.argv[i] == "-n"):
            no_of_bytes= sys.argv[i + 1]
            #if (no_of_bytes == ""):




    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((Ip, Port))


else:
    print("Error: you must run either in server or client mode")