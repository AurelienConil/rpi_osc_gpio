from pickle import TRUE
from OSC import OSCClient, OSCMessage
import RPi.GPIO as GPIO
import time

CHANNEL = 7
WAITFORRAISE = True
MSGADDRESS = "video/playmain"
MSGARG = 0 # has to be int
PORT = 12344
IP = "127.0.0.1"
PULLUP = GPIO.PUD_UP

###### NOTES AND DOCUMENTATION #######

#GPIO.setup(channel, GPIO.IN, pull_up_down=GPIO.PUD_UP)
  # or
#GPIO.setup(channel, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

#GPIO.wait_for_edge(channel, GPIO.RISING)
#GPIO.RISING, GPIO.FALLING or GPIO.BOTH.

#use GPIO board numbering instead of BCM
#GPIO.setmode(GPIO.BOARD) 

# PYTHON Get ARGS
#s1, s2, s3 = sys.argv[1], sys.argv[2], sys.argv[3]
#    a, b, c = float(s1), float(s2), float(s3)


def sendMessage(address, arg):
    global client_local
    oscmsg = OSCMessage()
    oscmsg.setAddress("/"+address)
    oscmsg.append(arg)
    client_local.send(oscmsg)

def main():

    print(" ===== RPI OSC GPIO ====")
    runningApp = True

    # GPIO SETUP
    GPIO.cleanup()
    GPIO.setmode(GPIO.BCM) 
    channel = CHANNEL
    GPIO.setup(channel, GPIO.IN,pull_up_down=PULLUP)

    # OSC CLIENT
    global client_local
    client_local = OSCClient()
    mip = IP
    mport = PORT
    print("Client OSC to local | ip: "+mip+"  | port: "+str(mport))
    while client_local.address() == None :
        try: 
            client_local.connect((mip, mport))
            print("connected")
        except Exception as inst:
            print("OSC Client connection error : ")
            print(inst)
        time.sleep(1)

    print(" ===== STARTING MAIN LOOP ====")
    try:  
        while True:            # this will carry on until you hit CTRL+C  
            print("wait for signal")
            while((GPIO.input(channel)==0)==WAITFORRAISE):
                time.sleep(0.3)
            try:
                sendMessage(MSGADDRESS, MSGARG)
                print("MESSAGE SENT")
            except:
                print("ERROR SEND OSC MESSAGE")
            while((GPIO.input(channel)==0)!=WAITFORRAISE):
                time.sleep(0.3)

            time.sleep(1)         # wait 0.1 seconds  
    
    finally:                   # this block will run no matter how the try block exits  
        GPIO.cleanup()         # clean up after yourself 
     

if __name__ == "__main__":
    main()