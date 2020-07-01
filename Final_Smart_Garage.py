import RPi.GPIO as a
import time
a.setmode(a.BCM)
a.setwarnings(False)
ControlPin=[4,17,27,22]
for pin in ControlPin:
        a.setup(pin,a.OUT)
        a.output(pin,False)
step_seq_num=0
rot_spd=0.001
rotate=4096
rotate_dir=1

seq=[ [1,0,0,0],
      [1,1,0,0],
      [0,1,0,0],
      [0,1,1,0],
      [0,0,1,0],
      [0,0,1,1],
      [0,0,0,1],
      [1,0,0,1],
    ]
TRIG=2
ECHO=3
a.setup(TRIG,a.OUT)
a.setup(ECHO,a.IN) #ultrasonic i/p
a.setup(5,a.OUT) #buzzer
a.setup(20,a.IN) #IR1 i/p inner
a.setup(21,a.OUT) #IR1 o/p
a.setup(23,a.IN) #gas i/p
a.setup(24,a.OUT) #gas o/p
a.setup(7,a.IN) #IR2 i/p outer
a.setup(8,a.OUT) #IR2 o/p
print("Smart Garage")
while(1):
    x=a.input(20) #input from IR1
    z=a.input(7)
    
    y=a.input(23) #input from Gassense
    print(x)
    if(z==1 and x==0):
    
        print(" Vacant Space!")
                    #motorcode
        rotateF=1 #no. of rotations
        rotate_dir=1
        rot_spd=0.001
        rotate=int(rotateF*4096)
        if rotate<1:rotate=4096
        rotate_dir=int(rotate_dir)
        if (rotate_dir !=1 and rotate_dir !=-1) :rotate_dir=1
        rot_spd=float(rot_spd)
        if (rot_spd > 1 or rot_spd<0.001):rot_spd=0.001
                    #print(rotate,rotate_dir,rot_spd)

        for i in range(0,(rotate+1)):
            for pin in range(0,4):
                Pattern_Pin=ControlPin[pin]
                if (seq[step_seq_num][pin]==1):
                    a.output(Pattern_Pin,True)
                else:
                    a.output(Pattern_Pin,False)
                    step_seq_num+=rotate_dir
                    if(step_seq_num >=8):
                        step_seq_num=0
                    elif(step_seq_num <0):
                        step_seq_num=7
                    time.sleep(rot_spd)
                    #ultrasonic
        while(True) :
            a.output(TRIG,True)
            time.sleep(0.00001)
            a.output(TRIG,False) #input from Ultrasonis
            while a.input(ECHO) == False:
                start = time.time()
            while a.input(ECHO) == True:
                end = time.time()
            sig_time = end - start
                    #speed of sound 343m/s
            distance = sig_time *17150
                    #print("Distance: {} centimeters".format(distance))

            if (distance > 10):
                a.output(5,a.LOW) #Buzer for Ultrasonic o/p
                print("At Safe Distance!")
            else:
                a.output(5,a.HIGH)
                print("Keep  Distance")
            time.sleep(1)
    else:
        print("NO Vacant PArking")
    # else:
    #     print("No Vacant Parking")
                
    #if(y==1):
        """print("Fire Alert !")
        #a.output(15,a.HIGH) #LED if Fire
        time.sleep(0.0001)
        #a.output(15,a.LOW)
                                        
    else:
        #a.output(15,a.LOW)"""
a.cleanup()





