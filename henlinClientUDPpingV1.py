from socket import *
from array import *
import time
from builtins import str
from _ast import Str
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt

serverName = '192.168.2.80' 
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_DGRAM) 
clientSocket.settimeout(2.0);   #setting timeout of socket
message = input('Input lowercase sentence:')   #getting user input for the message
message = message.encode('utf-8')
#making all the variables for the program
count = 0; min = 0; max = 0; startTime = 0; sum = 0; avg = 0; lostPackets = 0; meanDifference = 0;

RTTimes = list() #declaration of a list to store data collected

#sending 10 ping messages
while (count < 20):  #REMEMBER TO CHANGE THIS NUMBER TO 200
    clientSocket.sendto(message,(serverName, serverPort))   #sending of the message
    
    startTime = time.time()
    try:
        modifiedMessage, serverAddress = clientSocket.recvfrom(2048) #listening for the server response
    except timeout:
        print("Request timed out")
        lostPackets = lostPackets + 1  
        continue
        
    elapsedTime = time.time() - startTime
    elapsedTime = elapsedTime / 1000 
    RTTimes.append(elapsedTime) #adding each value to array for std dev calculation
       
    if(count == 1):       #determines the minimum
        min = elapsedTime
    elif(elapsedTime < min):
        min = elapsedTime 
            
    if(elapsedTime > max): #determines the maximum
        max = elapsedTime  
          
    sum = sum + elapsedTime  #THE SUM IS BEING CALCULATED 
    count = count + 1
    
    
avg = sum / 20 #calculating the average

stdDev = np.std(RTTimes)

packetLoss = (lostPackets/20) * 100
    
print("Minimum: " + str(min) + "Maximum: " + str(max) + "Average: " + str(avg) + "Packets loss rate: " + str(packetLoss) + "%")
print("Standard Deviation:" + str(stdDev))
           
plt.hist(RTTimes, normed=True, bins='auto')
plt.ylabel('Pings');
plt.xlabel("RTT (ms)")
plt.show()
 
clientSocket.close()