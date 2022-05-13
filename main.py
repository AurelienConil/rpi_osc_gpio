from OSC import OSCClient, OSCMessage
import RPi.GPIO as GPIO
import time

CHANNEL = 13
WAITFORRAISE = False
MSGADDRESS = "playmain"
MSGARG = 0 # has to be int
PORT = 12345
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
    GPIO.setmode(GPIO.BOARD) 
    channel = CHANNEL #Use BOARD numbering
    GPIO.setup(channel, GPIO.IN,pull_up_down=PULLUP)

    # OSC CLIENT
    global client_local
    client_local = OSCClient()
    mip = IP
    mport = PORT
    print("Client OSC to local | ip: "+mip+"  | port: "+str(mport))
    client_local.connect((mip, mport))

    print(" ===== STARTING MAIN LOOP ====")
    while runningApp:

        
        print("Waiting for GPIO event")
        if(WAITFORRAISE):
            GPIO.wait_for_edge(channel, GPIO.RISING)
        else :
            GPIO.wait_for_edge(channel, GPIO.FALLING)
            try:
                sendMessage(MSGADDRESS, MSGARG)
            except:
                print("ERROR SEND OSC MESSAGE")
            print("OSC MESSAGE SENT :"+MSGADDRESS+" : "+str(MSGARG))
            # if(WAITFORRAISE):
            #     GPIO.wait_for_edge(channel, GPIO.GPIO.FALLING)
            # else:
            #     GPIO.wait_for_edge(channel, GPIO.RISING)
            
            time.sleep(1)
        

    print("Main loop is quit. Closing software")
    GPIO.cleanup()


if __name__ == "__main__":
    main()