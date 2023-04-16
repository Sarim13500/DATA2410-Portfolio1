
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

    #Variable for received KB
    Total_KB = 0

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
        #Increasing the variable, so we can se how many KB is received
        Total_KB = Total_KB +1

    #Variable to see how much was received in the preferred format
    Total_sent=0

    #Finding the time it took to receive
    end_time = time.time()
    interval = end_time -start_time

    #Answer in Bytes
    if format == "B":
        Total_sent = Total_KB*1000

    #Answer in KB
    elif format == "KB":
        Total_sent = Total_KB


    #Answer in MB
    elif format == "MB":

        Total_sent = Total_KB/1000


    #Since the assignment say that bandwidth is given in "mbps" then I don´t implement anything for converting this
    #and just let it be in mbps
    bandwidth = (Total_KB*8)/1000

    #Bandwith with two decimals
    bandwidth = f"{bandwidth:.2f}"


    #Recieved bytes with two decimals
    totalBytesstr = f"{Total_sent:.2f}"
    totalBytesstr = str (totalBytesstr)



    #Adding some text to the table.

    # Adding format
    totalBytesstr = totalBytesstr + f"{format}"

    #Adding mbps to bandwidth
    bandwidth=str(bandwidth) + "mbps"

    #Interval in two decimals
    interval=f"{interval:.2f}"

    #Adding a row to the table with values
    newrow = (addr, interval, totalBytesstr, bandwidth )

    aTable.add_row(newrow)


    print(aTable)


    #Sending a message to the client
    msg = f"It was received {Total_KB} KB"
    conn.send(msg.encode())





#Client code
def client(ip, port, tid, dataSendes, interval, format_out):

    intervalstr =""
    start_time = time.time()


    #Creating a socket
    sock = socket(AF_INET, SOCK_STREAM)
    sock.connect((ip, port))



    #Finds how many Bytes will be sent to server if the -n flag is active
    if dataSendes:
        size  = list(dataSendes)

        #Checking format
        check_MB = size[-2] + size[-1]
        print(check_MB)
        sjekkb = size[-1]





        if check_MB=="KB":
            #variable to use for intervl
            extra = interval

            #Getting the formar
            format=check_MB

            # finding how much was sent
            transfer = FinnSendtBytesNum(size, sock)
            intervalstr = f"0  - {tid}"

            #Setting up interval to use in the table
            interval_start = 0
            interval_end = time.time()-start_time
            interval_end = f"{interval_end:.2f}"

            #if interval is not given
            if interval == tid:


                intervalstr= f"{interval_start} - {interval_end}"

                #Creating table
                table = results([ip,port], tid, transfer, format_out, interval, intervalstr)

                print(table)

            else:
                #If interval is given
                while time.time() > interval:
                    interval_end = time.time() - start_time
                    intervalstr = f"{interval_start} -  {interval_end}"

                    #creating a table
                    table = results([ip,port], tid, transfer, format_out, interval, intervalstr)

                    #splitting up the table to only get the intervals
                    table_str = str(table)
                    print(table_str.strip().split('\n')[1])

                    last_row_str = table_str.strip().split('\n')[-2]

                    #Getting the latest update
                    print(last_row_str)

                    #making the interval "bigger" so we can continue getting uodates
                    extra = extra+interval
                    interval_start = interval_start + interval
                    interval_end = interval_end + interval
                    print(table)


        #Same for MB and B
        elif check_MB=="MB":
            extra = interval

            format=check_MB
            #print(format)

            transfer = FinnSendtBytesNum(size, sock)
            intervalstr = f"0  - {tid}"

            interval_start = 0
            interval_end = time.time()-start_time
            interval_end = f"{interval_end:.2f}"

            if interval == tid:

                intervalstr= f"{interval_start} - {interval_end}"
                #Changing the format
                transfer = transfer / 1000
                table = results([ip,port], tid, transfer, format_out, interval, intervalstr)

                print(table)

            else:

                while time.time() > interval:
                    interval_end = time.time() - start_time
                    intervalstr = f"{interval_start} -  {interval_end}"
                    print("interval:" + intervalstr)
                    table = results([ip,port], tid, transfer, format_out, interval, intervalstr)

                    table_str = str(table)
                    print(table_str.strip().split('\n')[1])

                    last_row_str = table_str.strip().split('\n')[-2]
                    print(last_row_str)

                    extra = extra+interval
                    interval_start = interval_start + interval
                    interval_end = interval_end + interval
                    print(table)



        elif sjekkb == "B":
            extra = interval

            format=check_MB

            transfer = FinnSendtBytesNum(size, sock)
            intervalstr = f"0  - {tid}"

            interval_start = 0
            interval_end = time.time()-start_time
            interval_end = f"{interval_end:.2f}"

            if interval == tid:

                intervalstr= f"{interval_start} - {interval_end}"
                #changing the format
                transfer = transfer*1000
                table = results([ip,port], tid, transfer, format_out, interval, intervalstr)

                print(table)

            #if no format was given it will use the standard format
            else:

                while time.time() > interval:
                    interval_end = time.time() - start_time
                    intervalstr = f"{interval_start} -  {interval_end}"
                    print("interval:" + intervalstr)
                    table = results([ip,port], tid, transfer, format_out, interval, intervalstr)

                    table_str = str(table)
                    print(table_str.strip().split('\n')[1])

                    last_row_str = table_str.strip().split('\n')[-2]
                    print(last_row_str)

                    extra = extra+interval
                    interval_start = interval_start + interval
                    interval_end = interval_end + interval
                    print(table)



        #if given wrong format name
        else:
            print("Wrong format")
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
        interval_start = 0
        interval_end = interval

        #running for the time given
        while time.time() < endtime:

            #sending message
            sock.sendall(message.encode())
            transfer=transfer+1

            #printing out updates underway if it was given an interval
            #rest of the code is like above
            if time.time() - start_time == extra:

                intervalstr = f"{interval_start} -  {interval_end}"

                table = results([ip,port], tid, transfer, format_out, interval, intervalstr)

                table_str = str(table)
                print(table_str.strip().split('\n')[1])

                last_row_str = table_str.strip().split('\n')[-2]
                print(last_row_str)


                #Changing the Interval time
                extra = extra+interval
                interval_start = interval_start + interval
                interval_end = interval_end + interval


    intervalstr = f"{interval_start} -  {interval_end}"
    table = results([ip, port], tid, transfer, format_out, interval, intervalstr)
    print(table)



"""
    #Waiting for end message to close connection with client
    while True:
        after = input("To exit write BYE\n")

        if after == "BYE":
            sock.close()
            sys.exit()
"""

#Function to send and se how much data was sent
def FinnSendtBytesNum(array, sock):



    Total_data = ""
    TotalDataint = 0
    sendebytes = 0
    frmat = ""

    # senddata is 1 byte
    senddata = "A"

    # Senddata will be 1000 bytes after the loop
    while len(senddata) < 1000:
        senddata += "A"


    # finding format
    for i in array:

        #finding the amount of data that needs to be sent and finds the format
        try:
            i = int(i)
        except:
            i = str(i)

        if isinstance(i, int):
            i = str(i)
            Total_data += i

        elif isinstance(i, str):
            frmat += i



    #trying to se if the process over went correctly
    try:
        TotalDataint = int(Total_data)
    except:
        print("Give valid numbers")
        sys.exit()


    #Changing all letters to capital letters
    frmat = frmat.upper()


    if frmat:
        #Checking the format. If wrong, then we get an error message
        if frmat != "B" and frmat != "MB" and frmat != "KB":
            print("Give a valid format")
            sys.exit()


        #If format is correct then we send the correct amount of data
        elif (frmat == "B" or frmat == "MB" or frmat == "KB"):
            int(Total_data)

            #sending data in bytes
            if frmat == "B":
                while sendebytes < TotalDataint:
                    sock.sendall(senddata.encode())

                    sendebytes += 1
                return sendebytes



            #sending data in KB
            elif frmat == "KB":
                int(Total_data)

                #Converting to the right format
                Total_data = TotalDataint * 1000
                while sendebytes < Total_data:
                    sock.sendall(senddata.encode())

                    sendebytes += 1
                return sendebytes


            #Sending data in MB
            elif frmat == "MB":
                int(Total_data)

                #Converting to the right format
                Total_data = TotalDataint * (1000 * 1000)
                while sendebytes < Total_data:
                    sock.sendall(senddata.encode())

                    sendebytes += 1
                return sendebytes





#Function to create a table to print all the statistics
def results(id, tid, transfer, format_out, interval, intervalstr):

    #setting a start time
    start_time = time.time()

    kb_sent=0

    # Calculate bandwidth in kilo bits per second
    bandwidth = 8*transfer
    bandwidth = bandwidth / interval
    #Takes in KB and will convert to format_out and put this in the table

    #converts to MB
    if format_out== "MB":

        kb_sent = transfer/1000
        bandwidth = bandwidth/1000


    #Stays as KB
    elif format_out== "KB":

        kb_sent = transfer

    #Converts to B
    elif format_out == "B":

        kb_sent=transfer*1000
        bandwidth=bandwidth*1000
        #print("ut format " + str(kb_sent))

    #if format is wrong then an error message will be given
    else:
        print("Please give a valid format")
        sys.exit()


    # Create a new table with the appropriate columns
    #using prettyTable
    table = PrettyTable()
    table.field_names = ["ID", "Interval (s)", f"Transfer ({format_out})", "Bandwidth (mbps)"]

    # Add a new row to the table

    kb_sent = f"{kb_sent:.2f}"
    bandwidth = f"{bandwidth:.2f}"

    #Adding the row
    table.add_row([id, intervalstr, kb_sent, bandwidth])


    #Returns
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
        print("The IP-address is in the wrong format")
        sys.exit()



def check_time(time):
    try:
        time_value = int(time)
    except ValueError:
        raise argparse.ArgumentTypeError('expected an integer but you entered a string')
    if (time_value <= 0):
        print('Seconds must be higher than 0')
        sys.exit()






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

    #Stores the address to the clients
    joinedClients = []

    #Checks the argument given when trying to run the program
    #using argument parsing to take the arguments and check if they are correct

    parser = argparse.ArgumentParser()

    parser.add_argument('--server', '-s', action='store_true', help='server mode',)

    parser.add_argument('--client', '-c', action='store_true', help='client mode',)

    parser.add_argument('--bind', '-b', type=str, default='127.0.0.1')

    parser.add_argument('--port', '-p', type=int, default=8088)

    parser.add_argument('--format', '-f', type=str, default='MB')

    parser.add_argument('--serverip', '-I', type=str, default='127.0.0.1')

    parser.add_argument('--time', '-t', type=int, default=25)

    parser.add_argument('--interval', '-i', type=int)

    parser.add_argument('--parallel', '-P', type=int, default=1)

    parser.add_argument('--num', '-n', type=str)

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


        #checking if interval exists
        if args.interval:
            args.interval = args.interval
        else:
            args.interval = args.time


        client_ports = []

        #Gives multiple clients different ports (unique IDs)
        for i in range (0, args.parallel):
            client_ports.append(args.port + i)



        #Starts all clients, even if there are multiples
        for k in client_ports:
            thread = threading.Thread(target = client, args = (args.serverip, args.port, args.time, args.num, args.interval, args.format,))
            thread.start()



    #If no server or client tag is specified then you will get an error
    else:
        print("Error: you must run either in server or client mode")
        sys.exit()

