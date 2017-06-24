import argparse
import datetime
import imutils
import time
import cv2
from move_laser import move_laser
from move_laser import convert_to_stepper_coordinates
from send_angle import send_angle
from math import atan

def centralizarlaser(minimum_area,frame_size,step_size,serial_port):
#criando o programa e a recepcao de argumentos
#se nao recebe video, vamo usar a webcam
    camera = cv2.VideoCapture(1)
    #time.sleep(0.25)
    firstFrame = None
    initialTime = time.time()
    (grabbed,frame) = camera.read()
    frame = imutils.resize(frame,width=frame_size)
    height, width, channels = frame.shape

    #repete o seguinte loop para cada frame do video

    while True:
        #pega o frame atual e inicializa
        (grabbed,frame) = camera.read() #camera.read retorna uma tupla2 , o primeiro valro
        #indica se o frame foi lido com sucesso do buffer, o segundo valor eh o proprio frame

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
            send_angle((180 - 93), 0, serial_port)
            continue


    #ja foi detectada o fundo estatico, sera feita a deteccao de movimento e tracking

        frameDelta = cv2.absdiff(gray,firstFrame) #model fundo - frame atual
        thresh = cv2.threshold(frameDelta,40,255,cv2.THRESH_BINARY)[1] #essa linha descarta os pixels onde a diferenca com o fundo inicial seja muito pequena(menor do que 25)

    #dilata o limite da imagem pra tampar buracos e dps acha os contornos

        thresh = cv2.dilate(thresh,None,iterations=2)
        (_,cnts,_) = cv2.findContours(thresh.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE) #aqui temos cada contorno

    #Loop para os contornos,  procura o maior retangulo que ta mexendo e "seleciona" ele
        maiorArea = 0
        for c in cnts:
            if cv2.contourArea(c) > 0:
                if cv2.contourArea(c) > maiorArea:
                    maiorArea = cv2.contourArea(c)
       # vai fazer um retangulo em volta do maior objeto se mexendo
        for c in cnts:
     #       if cv2.contourArea(c) > minimum_area:
             if cv2.contourArea(c) == maiorArea :

                (x,y,w,h) = cv2.boundingRect(c) #recebe as informacoes do retangulo a ser desenhado
                cv2.rectangle(frame,(x,y),(x + w , y + h),(0,255,0),2) #desenha o retangulo no frame
                cv2.circle(frame,(x + w/2 ,y + h/2),2,(0,0,255),2) #desenha uma circulo onde o laser esta na imagem


        cv2.imshow("camera", frame) #mostra o frame com o retangulo do gato e o circulo do laser
        cv2.imshow("diferencas", thresh) #mostra a imagem de diferencas, onde ta tendo movimento na imagem

        elapsed = time.time() - initialTime
        if elapsed > 5:
            camera.release()
            cv2.destroyAllWindows()
            print("Laser centralizado.");

            return (x + w/2,y + h/2)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break