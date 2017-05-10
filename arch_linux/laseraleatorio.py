import imutils
import time
import cv2
from numpy import linalg as LA
from random import randint
from move_laser import move_laser
from move_laser import convert_to_stepper_coordinates
from math import atan
from send_angle import send_angle

def random_position(frame_size,step_size, serial_port):
    
    camera = cv2.VideoCapture(1)

    ##################comeca lendo o quadro#################################

    (grabbed,frame) = camera.read()
    if not grabbed:
        print("deu ruim na recepcao da imagem")
    frame = imutils.resize(frame,width=frame_size)
    height, width, channels = frame.shape

    current_position_X = width/2 #laser comeca no centro
    current_position_Y = height/2 #laser comeca no centro

    reached = True
    ###################inicio do loop de visualizacao + sorteio ##################

    while True:

        (grabbed,frame) = camera.read()
        if not grabbed:
            print("deu ruim na recepcao da imagem")
            break

        frame = imutils.resize(frame,width=frame_size)

        if reached == True:
        #chegou na posicao desejada, sortear novo alvo
            target_position_X = randint(0,width)
            target_position_Y = randint(0,height)
            reached = False

        (reached,current_position_X,current_position_Y) = move_laser(current_position_X,current_position_Y,target_position_X,target_position_Y,step_size)



        cv2.circle(frame,(current_position_X ,current_position_Y),2,(0,0,255),2)
        cv2.circle(frame,(target_position_X ,target_position_Y),2,(0,255,0),2)
	(stepper_X,stepper_Y) = convert_to_stepper_coordinates(current_position_X,current_position_Y,frame_size,frame_size,atan(8.3/20))
    
        send_angle(stepper_X, stepper_Y, serial_port)


        cv2.imshow("camera", frame)



        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break

    camera.release()
    cv2.destroyAllWindows()


