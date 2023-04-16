# DATA2410-Portfolio1
Eksamen portefølje 1 i DATA2410-Datanettverk

This portfolio is done by Sarim Asher Saeed s362123

This project is an easier implementation of the Iperf-program, called 
simpleperf. This has been implemented i Python using sockets. The Argument
parsing method was used to take inputs from the user and do perform their
actions. 

To run simpleperf, the terminal must be used. You can either test simpleperf
between a few server and client on your own machine, or you can create a fake
networ usig e.g. mininet and run the program in there to get a more "real" 
experiance. 

To run Simpleperf, start with writing "python3 simpleperf" and then you need 
either a "-s" or a "-c" tag for starting simpleperf in either server mode
or client mode. After that you need to use the different flags to run it as 
you preferred.

looking at line 580 through 600, you can see all different flags, and their function. 
That is how to run the program. 

Some important flags are: 

-t = time the client will run for

-b = Binding the server to an IP-address

-I = Binding ther client to an IP-address