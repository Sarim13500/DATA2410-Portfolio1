
import argparse
import threading
from socket import *
import sys
import ipaddress
import time
from prettytable import *
import _thread as thread







def sendmld(format,array,sock):



    antalldata = ""
    antalldataint = 0
    sendebytes = 0
    #print(data)
    frmat = ""

    # senddata is 1 byte
    senddata = "A"

    # Senddate will be 1000 bytes after the loop
    while len(senddata) < 1000:
        senddata += "A"


    # finner format
    for i in array:
        try:
            i = int(i)
        except:
            i = str(i)

        if isinstance(i, int):
            i = str(i)
            antalldata += i
            print("antall data:" + antalldata)

        elif isinstance(i, str):
            frmat += i
            print("frmt:" + frmat)

    try:
        antalldataint = int(antalldata)
    except:
        print("gi gyldige tall")
        sys.exit()

    frmat = frmat.upper()

    if frmat:
        # finner format
        if frmat != "B" and frmat != "MB" and frmat != "KB":
            print("Give a valid format")
            sys.exit()
        elif (frmat == "B" or frmat == "MB" or frmat == "KB"):
            int(antalldata)

            if frmat == "B":
                while sendebytes < antalldataint:
                    sock.sendall(senddata.encode())

                    sendebytes += 1
                return sendebytes


            elif frmat == "KB":
                int(antalldata)

                antalldata = antalldataint * 1000
                while sendebytes < antalldata:
                    sock.sendall(senddata.encode())

                    sendebytes += 1
                return sendebytes


            elif frmat == "MB":
                int(antalldata)


                antalldata = antalldataint * (1000 * 1000)
                while sendebytes < antalldata:
                    sock.sendall(senddata.encode())

                    sendebytes += 1
                return sendebytes
    print("format er dette: " + frmat)


def server(ip, port, format):
    # Server kode
    sock = socket(AF_INET, SOCK_STREAM)

    #check_parallel(args.parallel)
    format = "B"
    sock.bind((ip, port))
    sock.listen(5)

    print("[Server] Klar til å koble seg til ")
    # mens serveren er åpen
    print("klar til å motta")

    while True:
        conn, addr = sock.accept()
        #handle_client(conn, addr, format)
        server_thread= threading.Thread(target=handle_client, args=(conn, addr, format,))
        server_thread.start()


def handle_client(conn, addr, format):
    print(f"New client connected: {addr}")
    antallkb = 0
    # Add the client to the list of clients

    entabell = PrettyTable()
    entabell.field_names = ["ID", "Interval", "Transfer", "Bandwidth"]


    klienter.append(conn)


    # Loop to handle incoming messages from the client
    start_time = time.time()
    while True:
        data = conn.recv(1024)
        if not data:
            break
        message = data.decode()
        antallkb = antallkb +1




    end_time = time.time()
    interval = end_time -start_time

    kbstr = str (antallkb)
    kbstr = kbstr + "KB"
    mbps=str(antallkb/interval) + "mbps"
    newrow = (addr, interval, kbstr, mbps )

    entabell.add_row(newrow)
    print(entabell)


    msg = f"Det ble motatt {antallkb} KB"
    conn.send(msg.encode())





def klient(ip, port, tid, data, interval):
    sock = socket(AF_INET, SOCK_STREAM)
    sock.connect((ip, port))




    #kode for format
    if data:
        size  = list(data)

        sjekkkmb = size[-2] + size[-1]
        print(sjekkkmb)
        sjekkb = size[-1]



        if (sjekkkmb=="KB" or sjekkkmb=="MB"):

            format=sjekkkmb
            print(format)

            transfer = sendmld(format,size,sock)
            results([ip,port],interval,transfer)

        elif sjekkb == "B":

            result = ""
            for i in range(len(size) - 1):
                result += size[i]


            try:
                prov = int(result)

            except:
                print("fungerer ikke")
                sys.exit()


            if not isinstance(prov, int):
                print(result)
                print("det går ikke")
                sys.exit()

            format=sjekkb
            print(format)
            transfer = sendmld(format, size,sock)

            results([ip,port], interval, transfer)


        else:
            print("Feil")
            sys.exit()


    else:
        endtime = time.time() + tid

        while time.time() < endtime:

            senddata = "A"

            while len(senddata) < 1000:
                senddata += "A"

            message = senddata
            sock.sendall(message.encode())




def results(id, interval, transfer):
    # Calculate bandwidth in bits per second
    bandwidth = transfer / interval

    # Create a new table with the appropriate columns
    table = PrettyTable()
    table.field_names = ["ID", "Interval (s)", "Transfer (kb)", "Bandwidth (mbps)"]

    # Add a new row to the table
    table.add_row([id, interval, transfer, bandwidth])

    # Print the table
    print(table)





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

    parser.add_argument('--time', '-t', type=int, default=1)

    parser.add_argument('--interval', '-i', type=int)

    parser.add_argument('--parallel', '-P', type=int, default=1)

    parser.add_argument('--num', '-n', type=str) #, required=True trenger vi denne?

    args = parser.parse_args()



    #Ny
    if(args.server == True and args.client == True):
        print('Can´t have both server and client command')
        sys.exit()




    #server
    elif (args.server == True ):

        ip_check(args.bind)
        check_port(args.port)

        if args.format:
            check_format(args.format)


        server(args.bind, args.port, args.format)









    #Klient kode
    elif (args.client == True):
        i = 0

        ip_check(args.serverip)
        check_port(args.port)
        check_time(args.time)
        check_parallel(args.parallel)

        if args.interval:
            check_interval(args.interval)
        else:
            args.interval =1


        client_ports = []


        for i in range (0, args.parallel):
            client_ports.append(args.port + i)

        #implementer en greie for konvertering av num
        #while i < args.parallel:
        #klient(args.serverip, args.port, args.time, args.num, args.interval)

        for k in client_ports:
            thread = threading.Thread(target = klient, args = (args.serverip, args.port, args.time, args.num, args.interval,))
            thread.start()


        #i = i+1




    else:
        print("Error: you must run either in server or client mode")