import argparse
import datetime
import imutils
import time
import cv2
from move_laser import move_laser
from move_laser import convert_to_stepper_coordinates
from math import atan,sin,cos,sqrt,radians
from send_angle import send_angle
from centralizarlaser import centralizarlaser

from abertura import abertura

def track_cat2(minimum_area,frame_size,step_size,serial_port):
#criando o programa e a recepcao de argumentos
#se nao recebe video, vamo usar a webcam
    (offset_X,offset_Y) = centralizarlaser(minimum_area,frame_size,step_size,serial_port)

    camera = cv2.VideoCapture(1)
    #time.sleep(0.25)
    firstFrame = None

    (grabbed,frame) = camera.read()
    frame = imutils.resize(frame,width=frame_size)
    height, width, channels = frame.shape
    rotational_speed = 10
    current_position_X = width/2 #laser comeca no centro
    current_position_Y = height/2 #laser comeca no centro
    #repete o seguinte loop para cada frame do video
    a = 0

    while True:
        #pega o frame atual e inicializa
        (grabbed,frame) = camera.read() #camera.read retorna uma tupla2 , o primeiro valro
        #indica se o frame foi lido com sucesso do buffer, o segundo valor eh o proprio frame
        a+=1
        if not grabbed:
            print("deu ruim na recepcao da imagem")
            break #se nao leu o frame direito, acabou o video
        #as proximas tres linhas sao para mudar o tamanho do frame para o desejado,nao precisamos da imagem inteira
        #uma imagem de resolucao menor eh suficiente
        #fazer com que a imagem fique apenas preto e branco para facilitar a analise
        #a terceira operacao eh fazer com que a imagem fique mais borrada, para deixala mais suave
        #para que pequenas variacoes no quadro sejam diminuidas
        frame = imutils.resize(frame,width=frame_size)
        #cv2.imshow("camera", frame)
        gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray,(21,21),0)  #por que aplicar um borrao gaussiano tira o ruido de alta frequencia?
        #cv2.imshow("camera", gray)
        #o primeiro frame sera usado para definir o fundo

        if firstFrame is None:
            firstFrame = gray
            continue


    #ja foi detectada o fundo estatico, sera feita a deteccao de movimento e tracking

        frameDelta = cv2.absdiff(gray,firstFrame) #model fundo - frame atual
        thresh = cv2.threshold(frameDelta,40,255,cv2.THRESH_BINARY)[1] #essa linha descarta os pixels onde a diferenca com o fundo inicial seja muito pequena(menor do que 25)

    #dilata o limite da imagem pra tampar buracos e dps acha os contornos

        thresh = cv2.dilate(thresh,None,iterations=2)
        (_,cnts,_) = cv2.findContours(thresh.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE) #aqui temos cada contorno

    #Loop para os contornos
        vazio = True

        maiorArea = 0
        for c in cnts:
            if cv2.contourArea(c) > minimum_area:
                if cv2.contourArea(c) > maiorArea:
                    maiorArea = cv2.contourArea(c)
        for i in range(1):
            for c in cnts:
                if cv2.contourArea(c) > minimum_area:
                    if cv2.contourArea(c) == maiorArea :
                        vazio = False

                        (x,y,w,h) = cv2.boundingRect(c)
                        cv2.rectangle(frame,(x,y),(x + w , y + h),(0,255,0),2)
                        target_position_X = x + w/2 + (0.7*(sqrt(w*w + h*h)))*cos(radians(rotational_speed*a))
                        target_position_Y = y + h/2 + (0.7*(sqrt(w*w + h*h)))*sin(radians(rotational_speed*a))
                    #    print "angulo:",rotational_speed*a
                    #    (aux,current_position_X,current_position_Y) = move_laser(current_position_X,current_position_Y,target_position_X,target_position_Y,1)
                    #    (stepper_X,stepper_Y) = convert_to_stepper_coordinates(current_position_X,current_position_Y,width,height,atan(8.3/20))
                        (stepper_X,stepper_Y) = convert_to_stepper_coordinates(target_position_X,target_position_Y,width,height,abertura,offset_X,offset_Y)
                        send_angle(stepper_X, stepper_Y, serial_port)
                    #    cv2.circle(frame,(current_position_X ,current_position_Y),2,(0,0,255),2)
                        cv2.circle(frame,(int(target_position_X) ,int(target_position_Y)),2,(0,0,255),2)
                        #print(current_position_X,current_position_Y)

        
        # Tenta atrair o gato movimentando o laser em torno de um ponto caso nao detecte nada na cena
        if vazio:
            raio = 20
            target_position_X = width/2  + (0.7*(sqrt(2 * raio*raio)))*cos(radians(rotational_speed*a))
            target_position_Y = height/2 + (0.7*(sqrt(2 * raio*raio)))*sin(radians(rotational_speed*a))
            (stepper_X,stepper_Y) = convert_to_stepper_coordinates(target_position_X,target_position_Y,width,height,abertura,offset_X,offset_Y)
            send_angle(stepper_X, stepper_Y, serial_port)
            cv2.circle(frame,(int(target_position_X) ,int(target_position_Y)),2,(0,0,255),2)

            cv2.imshow("camera", frame)
            cv2.imshow("diferencas", thresh)


        key = cv2.waitKey(1) & 0xFF # por que se nao tiver essa linha o programa nao funciona?????????
        if key == ord("q"):
            break

    send_angle((181 - 93), 0, serial_port)
    camera.release()
    cv2.destroyAllWindows()
