import socket       
import sys         
  
# next create a socket object 
s = socket.socket()          
print "Socket successfully created"

port = 8080                
s.bind((sys.argv[1], port))        
print "socket binded to %s" %(port) 
  
# put the socket into listening mode 
s.listen(5)      
print "socket is listening"            
  
# a forever loop until we interrupt it or  
# an error occurs 
while True: 
  
   # Establish connection with client. 
   c, addr = s.accept()      
   print 'Got connection from', addr 
  
   # send a thank you message to the client.  
   c.send('Thank you for connecting') 
  
   # Close the connection with the client 
   c.close()