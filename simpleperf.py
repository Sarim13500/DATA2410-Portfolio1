
import argparse
import threading
from socket import *
import sys
import ipaddress
import time
from prettytable import *
#import _thread as thread




#Server code
def server(ip, port, format):

    #Creating a server
    sock = socket(AF_INET, SOCK_STREAM)
    sock.bind((ip, port))
    #server can have connections with 5 clients at the same time
    sock.listen(5)

    print(f"A simpleperf server is listening on port {port}")


    #Accepting connections from clients
    while True:
        conn, addr = sock.accept()
        server_thread= threading.Thread(target=handle_client, args=(conn, addr, format, ip , port,))
        server_thread.start()


def handle_client(conn, addr, format, server_ip, server_port):
    #Sending a message that a client has joined
    print(f"A simpleperf client with {addr} is connected with {server_ip}:{server_port}")

    #Variable for recieved KB
    antallkb = 0

    #Creating a table from the module prettytable so that the table looks better
    aTable = PrettyTable()
    aTable.field_names = ["ID", "Interval", "Transfer", "Bandwidth"]

    #adding client to a list
    joinedClients.append(conn)


    # Loop to handle incoming messages from the client
    start_time = time.time()

    #recieving data from client
    while True:
        data = conn.recv(1024)
        if not data:
            break
        message = data.decode()
        #Increasing the variable, so we can se how many KB is recieved
        antallkb = antallkb +1

    #Variable to see how much was recieved in the preferred format
    totalsent=0

    #Finding the time it took to recieve
    end_time = time.time()
    interval = end_time -start_time

    #Answer in Bytes
    if format == "B":
        totalsent = antallkb*1000

    #Answer in KB
    elif format == "KB":
        totalsent = antallkb


    #Answer in MB
    elif format == "MB":

        totalsent = antallkb/1000


    #Since the assignment say that bandwith is given in "mbps" then I don´t implement anything for converting this
    #and just let it be in mbps
    bandwith = (antallkb*8)/1000

    #Bandwith with two decimals
    bandwith = f"{bandwith:.2f}"


    #Recieved bytes with two decimals
    totalBytesstr = f"{totalsent:.2f}"
    totalBytesstr = str (totalBytesstr)



    #Adding some text to the table.

    # Adding format
    totalBytesstr = totalBytesstr + f"{format}"

    #Adding mbps to bandwith
    bandwith=str(bandwith) + "mbps"

    #Interval in two decimals
    interval=f"{interval:.2f}"

    #Adding a row to the table with values
    newrow = (addr, interval, totalBytesstr, bandwith )

    aTable.add_row(newrow)


    print(aTable)


    #Sending a message to the client
    msg = f"Det ble motatt {antallkb} KB"
    conn.send(msg.encode())





#Client code
def klient(ip, port, tid, dataSendes, interval, formatut):
    start_time = time.time()


    #Creating a socket
    sock = socket(AF_INET, SOCK_STREAM)
    sock.connect((ip, port))



    #Finds how many Bytes will be sent to server if the -n flag is active
    if dataSendes:
        size  = list(dataSendes)

        #Checking format
        sjekkkmb = size[-2] + size[-1]
        print(sjekkkmb)
        sjekkb = size[-1]





        if sjekkkmb=="KB":
            #variable to use for intervl
            extra = interval

            #Getting the formar
            format=sjekkkmb

            # finding how much was sent
            transfer = FinnSendtBytesNum(size, sock)
            intervalstr = f"0  - {tid}"

            #Setting up interval to use in the table
            intervalstart = 0
            intervalslutt = time.time()-start_time
            intervalslutt = f"{intervalslutt:.2f}"

            #if interval is not given
            if interval == tid:


                intervalstr= f"{intervalstart} - {intervalslutt}"

                #Creating table
                table = results([ip,port], tid, transfer, formatut, interval,intervalstr)

                print(table)

            else:
                #If interval is given
                while time.time() > interval:
                    intervalslutt = time.time() - start_time
                    intervalstr = f"{intervalstart} -  {intervalslutt}"

                    #creating a table
                    table = results([ip,port], tid, transfer, formatut, interval,intervalstr)

                    #splitting up the table to only get the intervals
                    table_str = str(table)
                    print(table_str.strip().split('\n')[1])

                    last_row_str = table_str.strip().split('\n')[-2]

                    #Getting the latest update
                    print(last_row_str)

                    #making the interval "bigger" so we can continue getting uodates
                    extra = extra+interval
                    intervalstart = intervalstart + interval
                    intervalslutt = intervalslutt + interval
                    print(table)


        #Same for MB and B
        elif sjekkkmb=="MB":
            extra = interval

            format=sjekkkmb
            #print(format)

            transfer = FinnSendtBytesNum(size, sock)
            intervalstr = f"0  - {tid}"

            intervalstart = 0
            intervalslutt = time.time()-start_time
            intervalslutt = f"{intervalslutt:.2f}"

            if interval == tid:

                intervalstr= f"{intervalstart} - {intervalslutt}"
                #Changing the format
                transfer = transfer / 1000
                table = results([ip,port], tid, transfer, formatut, interval,intervalstr)

                print(table)

            else:

                while time.time() > interval:
                    intervalslutt = time.time() - start_time
                    intervalstr = f"{intervalstart} -  {intervalslutt}"
                    print("interval:" + intervalstr)
                    table = results([ip,port], tid, transfer, formatut, interval,intervalstr)

                    table_str = str(table)
                    print(table_str.strip().split('\n')[1])

                    last_row_str = table_str.strip().split('\n')[-2]
                    print(last_row_str)

                    extra = extra+interval
                    intervalstart = intervalstart + interval
                    intervalslutt = intervalslutt + interval
                    print(table)



        elif sjekkb == "B":
            extra = interval

            format=sjekkkmb
            print(format)

            transfer = FinnSendtBytesNum(size, sock)
            intervalstr = f"0  - {tid}"

            intervalstart = 0
            intervalslutt = time.time()-start_time
            intervalslutt = f"{intervalslutt:.2f}"

            if interval == tid:

                intervalstr= f"{intervalstart} - {intervalslutt}"
                #changing the format
                transfer = transfer*1000
                table = results([ip,port], tid, transfer, formatut, interval,intervalstr)

                print(table)

            #if no format was given the it will use the standard format
            else:

                while time.time() > interval:
                    intervalslutt = time.time() - start_time
                    intervalstr = f"{intervalstart} -  {intervalslutt}"
                    print("interval:" + intervalstr)
                    table = results([ip,port], tid, transfer, formatut, interval,intervalstr)

                    table_str = str(table)
                    print(table_str.strip().split('\n')[1])

                    last_row_str = table_str.strip().split('\n')[-2]
                    print(last_row_str)

                    extra = extra+interval
                    intervalstart = intervalstart + interval
                    intervalslutt = intervalslutt + interval
                    print(table)



        #if given wrong format name
        else:
            print("Feil")
            sys.exit()

    #If time was specified and not format
    else:
        #creating a time variable of how long it should run
        endtime = time.time() + tid
        senddata = "A"

        #Message to be sent
        while len(senddata) < 1000:
            senddata += "A"

        #variables to use later
        extra = interval
        message = senddata
        transfer =0
        intervalstart = 0
        intervalslutt = interval

        #running for the time given
        while time.time() < endtime:

            #sending message
            sock.sendall(message.encode())
            transfer=transfer+1

            #printing out uodates underway if it was given an interval
            #rest of the code is like above
            if time.time() - start_time == extra:

                intervalstr = f"{intervalstart} -  {intervalslutt}"

                table = results([ip,port], tid, transfer, formatut, interval,intervalstr)

                table_str = str(table)
                print(table_str.strip().split('\n')[1])

                last_row_str = table_str.strip().split('\n')[-2]
                print(last_row_str)

                extra = extra+interval
                intervalstart = intervalstart + interval
                intervalslutt = intervalslutt + interval

        table = results([ip,port], tid, transfer, formatut, interval,intervalstr)
        print(table)



    #Waiting for end message to close connection with client
    while True:
        after = input("To exit write BYE\n")

        if after == "BYE":
            sock.close()
            sys.exit()


def FinnSendtBytesNum(array, sock):



    antalldata = ""
    antalldataint = 0
    sendebytes = 0
    frmat = ""

    # senddata is 1 byte
    senddata = "A"

    # Senddata will be 1000 bytes after the loop
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
            #print("antall data:" + antalldata)

        elif isinstance(i, str):
            frmat += i
            #print("frmt:" + frmat)



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
    #print("format er dette: " + frmat)









def results(id, tid, transfer, formatut, interval, intervalstr):

    start_time = time.time()

    kbsent=0

    # Calculate bandwidth in kilo bits per second
    bandwidth = (8*transfer) / interval

    #Får inn KB skal gi ut formatut

    if formatut=="MB":

        kbsent = transfer/1000
        bandwidth = bandwidth/1000

        #print("transfer" + str(transfer))
        #print("ut format " + str(kbsent))

    elif formatut=="KB":

        kbsent = transfer
        #print("ut format " + str(kbsent))

    elif formatut =="B":

        kbsent=transfer*1000
        bandwidth=bandwidth*1000
        #print("ut format " + str(kbsent))

    else:
        print("Gi gyldig format")
        sys.exit()


    # Create a new table with the appropriate columns
    table = PrettyTable()
    table.field_names = ["ID", "Interval (s)", f"Transfer ({formatut})", "Bandwidth (mbps)"]

    # Add a new row to the table

    kbsent = f"{kbsent:.2f}"
    bandwidth = f"{bandwidth:.2f}"
    #print(table)

    table.add_row([id, intervalstr, kbsent, bandwidth])


    # Print the table
    #print(table)
    return table








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

    joinedClients = []

    #Checks the argument given when trying to run the program

    parser = argparse.ArgumentParser()

    parser.add_argument('--server', '-s', action='store_true', help='server mode',)

    parser.add_argument('--client', '-c', action='store_true', help='client mode',)

    parser.add_argument('--bind', '-b', type=str, default='127.0.0.1')

    parser.add_argument('--port', '-p', type=int, default=8088)

    parser.add_argument('--format', '-f', type=str, default='MB')

    parser.add_argument('--serverip', '-I', type=str, default='127.0.0.1')

    parser.add_argument('--time', '-t', type=int, default=50)

    parser.add_argument('--interval', '-i', type=int)

    parser.add_argument('--parallel', '-P', type=int, default=1)

    parser.add_argument('--num', '-n', type=str) #, required=True trenger vi denne?

    args = parser.parse_args()



    #Will give an error when client and server both are asked to be active in one window
    if(args.server == True and args.client == True):
        print('Can´t have both server and client command')
        sys.exit()




    #server code
    elif (args.server == True ):

        #Checks some arguments to see if those are correct
        ip_check(args.bind)
        check_port(args.port)

        if args.format:
            check_format(args.format)

        #starts the server with the implemented server function
        server(args.bind, args.port, args.format)





    #Client kode
    elif (args.client == True):
        i = 0

        ip_check(args.serverip)


        if args.interval:
            check_interval(args.interval)
        else:
            args.interval = args.time


        client_ports = []

        #Gives multiple clients different ports (unique IDs)
        for i in range (0, args.parallel):
            client_ports.append(args.port + i)



        #Starts all clients, even if there are multiples
        for k in client_ports:
            print("args" + args.format)
            thread = threading.Thread(target = klient, args = (args.serverip, args.port, args.time, args.num, args.interval, args.format,))
            thread.start()



    #If no server or client tag is specified then you will get an error
    else:
        print("Error: you must run either in server or client mode")
        sys.exit()

