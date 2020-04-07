#Libraries
import time
import RPi.GPIO as GPIO
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008
import pymongo
from pymongo import MongoClient
 
#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)
 
#set GPIO Pins for Ultrasonic sensors
GPIO_TRIGGER1 = 6
GPIO_ECHO1 = 12

GPIO_TRIGGER2 = 19
GPIO_ECHO2 = 16

GPIO_TRIGGER3 = 26
GPIO_ECHO3 = 20

#Mappings for infared sensor
CLK = 11
MISO = 9
MOSI = 10
CS = 8
 
#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER1, GPIO.OUT)
GPIO.setup(GPIO_ECHO1, GPIO.IN)

GPIO.setup(GPIO_TRIGGER2, GPIO.OUT)
GPIO.setup(GPIO_ECHO2, GPIO.IN)

GPIO.setup(GPIO_TRIGGER3, GPIO.OUT)
GPIO.setup(GPIO_ECHO3, GPIO.IN)

def distance_ultrasonic(trigger, echo):
    # set Trigger to HIGH
    GPIO.output(trigger, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(trigger, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    # save StartTime
    while GPIO.input(echo) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(echo) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2
 
    return distance
 
if __name__ == '__main__':
    try:
        #Connecting MongoDB
        client = pymongo.MongoClient("mongodb+srv://<user>:<pass>@<server endpoint>.mongodb.net/test?retryWrites=true&w=majority")
		#Gets the collection in that DB
        database = client.ParkingLots
        collection = database.maps
        
		#Variables to detect change in parking spots
		#Program doesn't send data if a parking spot doesn't change states (open/taken)
        spot1Old = 0
        spot1New = 0
        
        spot2Old = 0
        spot2New = 0
        
        spot3Old = 0
        spot3New = 0
        
        spot4Old = 0
        spot4New = 0
        
		#Object for infared sensor
        mcp = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)
        
        while True:

			#Distance for infared sensor
            v = (mcp.read_adc(0) / 1023.0) * 3.3
            distIR1 = 16.2537 * v**4 - 129.893 * v**3 + 382.268 * v**2 - 512.611 * v + 301.439
            print("Measured Distance IR1 = {:.2f}".format(distIR1))
            
			#See if a spot is taken or free
            if distIR1 < 50:
                spot1New = 1
            else:
                spot1New = 0
            
            #resultFind = collection.find({"spotId" : "1"})
            #print(resultFind)
            
			#See if a spot has a different state than last reading
			#If it does have a different state, update the database
            if spot1New != spot1Old: 
                spot1Old = spot1New
                myquery1 = { "spotId" : "1"}
                newVal1 = { "$set" : { "status" : str(spot1New) } }
                resultUpdate = collection.update_one(myquery1, newVal1)
                #resultReplace = collection.replace_one(
                #    { "slotId" : "1" },
                #    {"slotId" : "1" , "status" : str(spot1New) }
                #    )
                #print(resultReplace)
                #print(resultUpdate)

            time.sleep(2)
            
			#Distance for ultrasonic sensor
            distUS1 = distance_ultrasonic(GPIO_TRIGGER1, GPIO_ECHO1)
            print ("Measured Distance US1 = %.1f cm" % distUS1)
            
			#See if a spot is taken or free
            if distUS1 < 25:
                spot2New = 1
            else:
                spot2New = 0
            
			#See if a spot has a different state than last reading
			#If it does have a different state, update the database
            if spot2New != spot2Old:
                spot2Old = spot2New
                myquery2 = { "spotId" : "2"}
                newVal2 = { "$set" : { "status" : str(spot2New) } } 
                collection.update_one(myquery2, newVal2)
                
            time.sleep(2)
            
			#Distance for ultrasonic sensor
            distUS2 = distance_ultrasonic(GPIO_TRIGGER2, GPIO_ECHO2)
            print ("Measured Distance US2 = %.1f cm" % distUS2)
            
			#See if a spot is taken or free
            if distUS2 < 25:
                spot3New = 1
            else:
                spot3New = 0
            
			#See if a spot has a different state than last reading
			#If it does have a different state, update the database
            if spot3New != spot3Old:
                spot3Old = spot3New
                myquery3 = { "spotId" : "3"}
                newVal3 = { "$set" : { "status" : str(spot3New) } } 
                collection.update_one(myquery3, newVal3)
            
            time.sleep(2)
            
			#Distance for ultrasonic sensor
            distUS3 = distance_ultrasonic(GPIO_TRIGGER3, GPIO_ECHO3)
            print ("Measured Distance US3 = %.1f cm" % distUS3)
            time.sleep(2)
            
			#See if a spot is taken or free
            if distUS3 < 25: 
                spot4New = 1
            else:
                spot4New = 0
            
			#See if a spot has a different state than last reading
			#If it does have a different state, update the database
            if spot4New != spot4Old:
                spot4Old = spot4New
                myquery4 = { "spotId" : "4"}
                newVal4 = { "$set" : { "status" : str(spot4New) } } 
                collection.update_one(myquery4, newVal4)
            
            print("")
 
        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()