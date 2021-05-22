
#importing packages
import scipy
from scipy.spatial import distance as dist
import dlib
from time import time
from imutils import face_utils
import cv2
from tkinter import *
import tkinter.messagebox
from PIL import ImageTk
import serial
import matplotlib.pyplot as plt
from drawnow import *



root = Tk()
root.geometry("1366x768+0+0")           
frame = Frame(root, relief=RIDGE, borderwidth=2)
frame.pack(fill=BOTH, expand=1)
root.title('LIE DETECTOR')
frame.config(background='blue')
filename = PhotoImage(file="media_folder/demo.png")
background_label = Label(frame, image=filename)
background_label.pack(side=TOP)



tempC = []                                                  # Empty array
pulse = []
gsr = []
arduino = serial.Serial("COM3", 9600)
plt.ion()


def makeFig():                                              # Create a function that makes our desired plot
    
    plt.ylim(550, 700)  # Set y min and max values
    plt.title('Real Time Data')  # Plot the title
    plt.grid(True)  # Turn the grid on
    plt.ylabel('GSR')  # Set ylabel
    plt.plot(gsr, 'b^-', label='GSR')  # plot the temperature
    plt.legend(loc='upper right')  # plot the legend
    plt2 = plt.twinx()  # Create a second y axis
    plt.ylim(20, 300)  # Set limits of second y axis
    plt2.plot(pulse, 'g*-', label='BPM')  # plot pressure data
    plt2.set_ylabel('BPM')  # label second y axis
    plt2.ticklabel_format(useOffset=False)
    plt2.legend(loc='upper left')

def Contri():
    tkinter.messagebox.showinfo("Contributors", "\n1. Abhishek \n2. Amey \n3. Alben\n")


def anotherWin():
    tkinter.messagebox.showinfo("About",
                                'LIE DETECTOR version v1.0')


menu = Menu(root)
root.config(menu=menu)


subm1 = Menu(menu)
menu.add_cascade(label="About", menu=subm1)
subm1.add_command(label="Lie Detector", command=anotherWin)
subm1.add_command(label="Contributors", command=Contri)


def exitt():
    plt.close()
    root.destroy()
    
    

def webdetRec():
    capture = cv2.VideoCapture(0)
    face_cascade = cv2.CascadeClassifier('lbpcascade_frontalface.xml')
    eye_glass = cv2.CascadeClassifier('haarcascade_eye_tree_eyeglasses.xml')
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    op = cv2.VideoWriter('media_folder/Sample2.avi', fourcc, 9.0, (640, 480))

    while True:
        ret, frame = capture.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray)

        for (x, y, w, h) in faces:
            font = cv2.FONT_HERSHEY_COMPLEX
            cv2.putText(frame, 'Face', (x + w, y + h), font, 1, (250, 250, 250), 2, cv2.LINE_AA)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            roi_gray = gray[y:y + h, x:x + w]
            roi_color = frame[y:y + h, x:x + w]

            eye_g = eye_glass.detectMultiScale(roi_gray)
            for (ex, ey, ew, eh) in eye_g:
                cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)
        op.write(frame)
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xff == ord('q'):
            break
    op.release()
    capture.release()
    cv2.destroyAllWindows()


def eye_aspect_ratio(eye):
    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])

    C = dist.euclidean(eye[0], eye[3])

    ear = (A + B) / (2.0 * C)

    return ear


def final_ear(shape):
    (lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
    (rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

    leftEye = shape[lStart:lEnd]
    rightEye = shape[rStart:rEnd]

    leftEAR = eye_aspect_ratio(leftEye)
    rightEAR = eye_aspect_ratio(rightEye)

    ear = (leftEAR + rightEAR) / 2.0
    return (ear, leftEye, rightEye)


def blink():
    capture = cv2.VideoCapture(0)
    face_cascade = cv2.CascadeClassifier('lbpcascade_frontalface.xml')
    eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
    blink_cascade = cv2.CascadeClassifier('CustomBlinkCascade.xml')
    detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

    predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')
    global end
    end = time() + 20            #for inital time waiting to get min max values
    global pulse_max, pulse_min, temp_max, temp_min, ear_max, ear_min, gsr_max, gsr_min,current    #holding variables for min max values
    pulse_max=0
    pulse_min=0
    temp_max=0
    temp_min=0
    ear_max=0
    ear_min=0
    gsr_max=0
    gsr_min=0
    
    global pulse_logic,eda_logic,temp_logic,ear_logic               #holding variables for true false values
    pulse_logic=0
    eda_logic=0
    temp_logic=0
    ear_logic=0
    global ear
    ear=[]
    global a_pulse,a_temp,a_ear,a_gsr,count                           #holding list for data values
    a_pulse = []
    a_temp = []
    a_ear = []
    a_gsr = []
    count = 0 
    while True:
        ret, frame = capture.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray)

        for (x, y, w, h) in faces:
            font = cv2.FONT_HERSHEY_COMPLEX
            cv2.putText(frame, 'Face', (x + w, y + h), font, 1, (250, 250, 250), 2, cv2.LINE_AA)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            roi_gray = gray[y:y + h, x:x + w]
            roi_color = frame[y:y + h, x:x + w]

            eyes = eye_cascade.detectMultiScale(roi_gray)
            for (ex, ey, ew, eh) in eyes:
                cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)

            blink = blink_cascade.detectMultiScale(roi_gray)
            for (eyx, eyy, eyw, eyh) in blink:
                cv2.rectangle(roi_color, (eyx, eyy), (eyx + eyw, eyy + eyh), (255, 255, 0), 2)

            rects = detector.detectMultiScale(gray, scaleFactor=1.1,
                                              minNeighbors=5, minSize=(30, 30),
                                              flags=cv2.CASCADE_SCALE_IMAGE)

            # for rect in rects:
            for (x, y, w, h) in rects:
                rect = dlib.rectangle(int(x), int(y), int(x + w), int(y + h))

                shape = predictor(gray, rect)
                shape = face_utils.shape_to_np(shape)
                
                eye = final_ear(shape)
                ear = eye[0]
                leftEye = eye[1]
                rightEye = eye[2]

                leftEyeHull = cv2.convexHull(leftEye)
                rightEyeHull = cv2.convexHull(rightEye)
                cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)
                cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)
                cv2.putText(frame, "EAR: {:.2f}".format(ear), (240, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
               
            while time() < end:                                         #timer loop
                
                ret, frame = capture.read()
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = face_cascade.detectMultiScale(gray)

                for (x, y, w, h) in faces:
                    font = cv2.FONT_HERSHEY_COMPLEX
                    cv2.putText(frame, 'Face', (x + w, y + h), font, 1, (250, 250, 250), 2, cv2.LINE_AA)
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                    roi_gray = gray[y:y + h, x:x + w]
                    roi_color = frame[y:y + h, x:x + w]

                    eyes = eye_cascade.detectMultiScale(roi_gray)
                    for (ex, ey, ew, eh) in eyes:
                        cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)

                    blink = blink_cascade.detectMultiScale(roi_gray)
                    for (eyx, eyy, eyw, eyh) in blink:
                        cv2.rectangle(roi_color, (eyx, eyy), (eyx + eyw, eyy + eyh), (255, 255, 0), 2)

                    rects = detector.detectMultiScale(gray, scaleFactor=1.1,
                                              minNeighbors=5, minSize=(30, 30),
                                              flags=cv2.CASCADE_SCALE_IMAGE)

                    # for rect in rects:
                    for (x, y, w, h) in rects:
                        rect = dlib.rectangle(int(x), int(y), int(x + w), int(y + h))

                        shape = predictor(gray, rect)
                        shape = face_utils.shape_to_np(shape)
                
                        eye = final_ear(shape)
                        ear = eye[0]
                
                while (arduino.inWaiting() == 0):  # Wait here until there is data
                    pass  # do nothing
                arduinoString = arduino.readline()
                dataArray = arduinoString.decode('UTF-8').split(',')  # Split it into an array
                temp = float(dataArray[0])
                bpm = float(dataArray[1])
                eda = float(dataArray[2])

                cnt = 0
                cnt1 = 0
                cnt2 = 0
                cnt3 = 0
                     
                if bpm >= 60 and bpm <= 300 :            #normalize pulse rate

                    a_pulse.append(bpm)
                    
                    pulse_max = max(a_pulse)            #store min max for pluse
                    pulse_min = min(a_pulse)
                    if cnt == 0:
                        cnt = 1
                        print(f"pma{pulse_max}")
                        print(f"pmi{pulse_min}")
                
                                       
                if temp >= 20 and temp <= 50:           #normalize temp value

                    a_temp.append(temp)
                    temp_max = max(a_temp)              #store min max for temp
                    temp_min = min(a_temp)
                    if cnt1 == 0:
                        cnt1 = 1
                        print(f"tma{temp_max}")
                        print(f"tmi{temp_min}")
                   
                if ear >= 0 and ear <= 2:             #normalize ear value

                    a_ear.append(ear)
                    ear_max = max(a_ear)
                    ear_min = min(a_ear)                #store min max for ear
                    if cnt2 == 0:
                        cnt2 = 1
                        print(f"ema{ear_max}")
                        print(f"emi{ear_min}")
                

                if eda >= 200 and eda <= 800:           #normalize gsr value

                    a_gsr.append(eda)
                    gsr_max = max(a_gsr)                #store min max for gsr
                    gsr_min = min(a_gsr)
                    if cnt3 == 0:
                        cnt3 = 1
                        print(f"gma{gsr_max}")
                        print(f"gmi{gsr_min}")
                       
            while (arduino.inWaiting() == 0):  # Wait here until there is data
                pass  # do nothing
            arduinoString = arduino.readline()
            dataArray = arduinoString.decode('UTF-8').split(',')  # Split it into an array
            temp = float(dataArray[0])
            bpm = float(dataArray[1])
            eda = float(dataArray[2])
            tempC.append(temp)
            pulse.append(bpm)
            gsr.append(eda)
            drawnow(makeFig)
            plt.pause(.000001)
            count = count + 1
            if (count > 10):# only take last 20 data if data is more it will pop first
                tempC.pop(0)
                pulse.pop(0)
                gsr.pop(0)

            #section for assigning logic values
                
            if(bpm>pulse_max or bpm<pulse_min):
                pulse_logic = False
            else:
                pulse_logic = True
                            
            if(temp>temp_max or temp<temp_min):
                temp_logic = False
            else:
                temp_logic = True

            if(ear>ear_max or ear<ear_min):
                ear_logic = False
            else:
                ear_logic = True
            
            if(eda>gsr_max or eda<gsr_min):
                gsr_logic = False
            else:
                gsr_logic = True

            print(f"pulse:{pulse_logic}")
            print(f"temp:{temp_logic}")
            print(f"ear:{ear_logic}")
            print(f"gsr:{gsr_logic}")
            

            #logic section for final decision

            
            if(pulse_logic==False and gsr_logic==False and ear_logic==False and temp_logic==False):
                cv2.putText(frame, 'FALSE', (10, 50), font, 2, (255, 0, 0), 2, cv2.LINE_AA)
            elif(pulse_logic==False and gsr_logic==False and ear_logic==False and temp_logic==True):
                cv2.putText(frame, 'FALSE', (10, 50), font, 2, (255, 0, 0), 2, cv2.LINE_AA)
            elif(pulse_logic==False and gsr_logic==False and ear_logic==True and temp_logic==False):
                cv2.putText(frame, 'FALSE', (10, 50), font, 2, (255, 0, 0), 2, cv2.LINE_AA)
            elif(pulse_logic==False and gsr_logic==False and ear_logic==True and temp_logic==True):
                cv2.putText(frame, 'FALSE', (10, 50), font, 2, (255, 0, 0), 2, cv2.LINE_AA)
            elif(pulse_logic==False and gsr_logic==True and ear_logic==False and temp_logic==False):
                cv2.putText(frame, 'FALSE', (10, 50), font, 2, (255, 0, 0), 2, cv2.LINE_AA)
            elif(pulse_logic==False and gsr_logic==True and ear_logic==False and temp_logic==True):
                cv2.putText(frame, 'FALSE', (10, 50), font, 2, (255, 0, 0), 2, cv2.LINE_AA)
            elif(pulse_logic==False and gsr_logic==True and ear_logic==True and temp_logic==False):
                cv2.putText(frame, 'TRUE', (10, 50), font, 2, (0, 255, 0), 2, cv2.LINE_AA)
            elif(pulse_logic==False and gsr_logic==True and ear_logic==True and temp_logic==True):
                cv2.putText(frame, 'TRUE', (10, 50), font, 2, (0, 255, 0), 2, cv2.LINE_AA)
            elif(pulse_logic==True and gsr_logic==False and ear_logic==False and temp_logic==False):
                cv2.putText(frame, 'FALSE', (10, 50), font, 2, (255, 0, 0), 2, cv2.LINE_AA)
            elif(pulse_logic==True and gsr_logic==False and ear_logic==False and temp_logic==True):
                cv2.putText(frame, 'FALSE', (10, 50), font, 2, (255, 0, 0), 2, cv2.LINE_AA)
            elif(pulse_logic==True and gsr_logic==False and ear_logic==True and temp_logic==False):
                cv2.putText(frame, 'TRUE', (10, 50), font, 2, (0, 255, 0), 2, cv2.LINE_AA)
            elif(pulse_logic==True and gsr_logic==False and ear_logic==True and temp_logic==True):
                cv2.putText(frame, 'TRUE', (10, 50), font, 2, (0, 255, 0), 2, cv2.LINE_AA)
            elif(pulse_logic==True and gsr_logic==True and ear_logic==False and temp_logic==False):
                cv2.putText(frame, 'TRUE', (10, 50), font, 2, (0, 255, 0), 2, cv2.LINE_AA)
            elif(pulse_logic==True and gsr_logic==True and ear_logic==False and temp_logic==True):
                cv2.putText(frame, 'TRUE', (10, 50), font, 2, (0, 255, 0), 2, cv2.LINE_AA)
            elif(pulse_logic==True and gsr_logic==True and ear_logic==True and temp_logic==False):
                cv2.putText(frame, 'TRUE', (10, 50), font, 2, (0, 255, 0), 2, cv2.LINE_AA)
            elif(pulse_logic==True and gsr_logic==True and ear_logic==True and temp_logic==True):
                cv2.putText(frame, 'TRUE', (10, 50), font, 2, (0, 255, 0), 2, cv2.LINE_AA)
            else:
                pass
            
        
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    capture.release()
    cv2.destroyAllWindows()


#tkinter section
    
start = ImageTk.PhotoImage \
        (file='media_folder/start.png')
start_button = Button(frame, image=start, relief=FLAT, activebackground="blue", borderwidth=0, background="black", cursor="hand2", command=blink)
start_button.place(x=314, y=592)

stop = ImageTk.PhotoImage \
       (file='media_folder/stop.png')
stop_button = Button(frame, image=stop, relief=FLAT, activebackground="blue", borderwidth=0, background="black", cursor="hand2", command=exitt)
stop_button.place(x=801, y=592)

root.mainloop()
