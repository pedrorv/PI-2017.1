import argparse
import datetime
import imutils
import time
import cv2
from move_laser import move_laser
from move_laser import convert_to_stepper_coordinates
from math import atan

def track_cat(minimum_area,frame_size,step_size):
#criando o programa e a recepcao de argumentos
#se nao recebe video, vamo usar a webcam
    camera = cv2.VideoCapture(0)
    #time.sleep(0.25)
    firstFrame = None

    (grabbed,frame) = camera.read()
    frame = imutils.resize(frame,width=frame_size)
    height, width, channels = frame.shape

    current_position_X = width/2 #laser comeca no centro
    current_position_Y = height/2 #laser comeca no centro
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
            continue


    #ja foi detectada o fundo estatico, sera feita a deteccao de movimento e tracking

        frameDelta = cv2.absdiff(gray,firstFrame) #model fundo - frame atual
        thresh = cv2.threshold(frameDelta,40,255,cv2.THRESH_BINARY)[1] #essa linha descarta os pixels onde a diferenca com o fundo inicial seja muito pequena(menor do que 25)

    #dilata o limite da imagem pra tampar buracos e dps acha os contornos

        thresh = cv2.dilate(thresh,None,iterations=2)
        (cnts,_) = cv2.findContours(thresh.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE) #aqui temos cada contorno

    #Loop para os contornos,  procura o maior retangulo que ta mexendo e "seleciona" ele
        maiorArea = 0
        for c in cnts:
            if cv2.contourArea(c) > minimum_area:
                if cv2.contourArea(c) > maiorArea:
                    maiorArea = cv2.contourArea(c)
       # vai fazer um retangulo em volta do maior objeto se mexendo 
        for c in cnts:
     #       if cv2.contourArea(c) > minimum_area:
             if cv2.contourArea(c) == maiorArea :

                (x,y,w,h) = cv2.boundingRect(c) #recebe as informacoes do retangulo a ser desenhado
                cv2.rectangle(frame,(x,y),(x + w , y + h),(0,255,0),2) #desenha o retangulo no frame
                target_position_X = x + w/2 #target position é onde o laser deveria estar, variavel criada para suavizar o movimento e controlar a velocidade
                target_position_Y = y - 20
                (aux,current_position_X,current_position_Y) = move_laser(current_position_X,current_position_Y,target_position_X,target_position_Y,step_size) #faz a current_position(onde o laser realmente esta) dar um "passo em direcao ao target_position
                (stepper_X,stepper_Y) = convert_to_stepper_coordinates(current_position_X,current_position_Y,width,height,atan(8.3/20)) #converte as coordenadas em pixels na imagem para coordenadas em radianos para serem utilizadas pelo servo
                cv2.circle(frame,(current_position_X ,current_position_Y),2,(0,0,255),2) #desenha uma circulo onde o laser esta na imagem

        cv2.imshow("camera", frame) #mostra o frame com o retangulo do gato e o circulo do laser
        cv2.imshow("diferencas", thresh) #mostra a imagem de diferenças, onde ta tendo movimento na imagem


        key = cv2.waitKey(1) & 0xFF 
        if key == ord("q"):
            break

    camera.release()
    cv2.destroyAllWindows()
