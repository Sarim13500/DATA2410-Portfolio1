
import argparse
from socket import *
import sys
import ipaddress
import _thread as thread


"""
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
"""

def server(ip, port, format):
    # Server kode
    sock = socket(AF_INET, SOCK_STREAM)

    #check_parallel(args.parallel)

    sock.bind((ip, port))
    sock.listen(5)

    print("[Server] Klar til å koble seg til ")
    # mens serveren er åpen
    print("klar til å motta")

    while True:
        conn, addr = sock.accept()
        ipc, portc = addr
        handle_client(conn, ipc, portc)


def klient(ip, port):
    sock = socket(AF_INET, SOCK_STREAM)
    sock.connect((ip, port))

    while True:
        message = input()
        sock.sendall(message.encode())




def handle_client(conn, ip, port):
    print(f"New client connected: {ip} : {port}")

    # Add the client to the list of clients
    klienter.append(conn)

    # Loop to handle incoming messages from the client
    while True:
        data = conn.recv(1024)
        if not data:
            break
        message = data.decode()
        print(f"Received message from {ip}:{port}:  {message}")




def check_port(val):
    try:
        value = int(val)
    except ValueError:
        raise argparse.ArgumentTypeError('expected an integer but you entered a string')
    if (value<1024 or value>65535):
        print('it is not a valid port')
        sys.exit()



def ip_check(address):
    try:
        val= ipaddress.ip_address(address)
        print("IP-adressen er nå godkjent")
    except:
        print("IP-adressen er på feil format")
        sys.exit()



def check_time(time):
    try:
        time_value = int(time)
    except ValueError:
        raise argparse.ArgumentTypeError('expected an integer but you entered a string')
    if (time_value <= 0):
        print('Seconds must be higher than 0')
        sys.exit()



def check_interval(interval):
    try:
        interval_val = int(interval)

        if interval_val < 0:
            print("Intervallet må være større enn 0")
            sys.exit()

    except ValueError:
        raise argparse.ArgumentTypeError('expected an integer but you entered a string')



def check_parallel(parallel):
    try:
        parallel_val = int(parallel)
    except ValueError:
        raise argparse.ArgumentTypeError('expected an integer but you entered a string')
    if (parallel_val < 1 or parallel_val > 5):
        print('Value is not correct, it should be between 1 and 5')
        sys.exit()


def check_format(format):
    try:
        Format = str(format)
    except ValueError:
        raise argparse.ArgumentTypeError('expected a String but you entered an Integer')
    if Format != "KB" and Format != "MB" and Format != "B":
        print('it is not valid format')
        sys.exit()




if __name__ == '__main__':

    klienter = []

    parser = argparse.ArgumentParser()

    parser.add_argument('--server', '-s', action='store_true', help='server mode',)

    parser.add_argument('--client', '-c', action='store_true', help='client mode',)

    parser.add_argument('--bind', '-b', type=str, default='127.0.0.1')

    parser.add_argument('--port', '-p', type=check_port, default=8088)

    parser.add_argument('--format', '-f', type=str, default='MB')

    parser.add_argument('--serverip', '-I', type=str, default='127.0.0.1')

    parser.add_argument('--time', '-t', type=int, default=50)

    parser.add_argument('--interval', '-i', type=int)

    parser.add_argument('--parallel', '-P', type=int, default=1)

    parser.add_argument('--num', '-n', type=str, default="MB") #, required=True trenger vi denne?

    args = parser.parse_args()



    #Ny
    if(args.server == True and args.client == True):
        print('Can´t have both server and client command')
        sys.exit()


    elif (args.server == True ):

        ip_check(args.bind)
        check_port(args.port)

        if args.format:
            check_format(args.format)


        server(args.bind, args.port, args.format)







    #Klient kode
    elif (args.client == True):

        ip_check(args.serverip)
        check_port(args.port)
        check_time(args.time)
        print(args.port)



        klient(serverip, port)




    else:
        print("Error: you must run either in server or client mode")