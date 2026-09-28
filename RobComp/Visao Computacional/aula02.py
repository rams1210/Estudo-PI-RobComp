# video -> sequencia/loop de imagens/frames

import cv2

cap=cv2.VideoCapture(0) # seleciona video da webcam
largura=int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)) # armazena largura do video que esta sendo capturado
altura=int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)) # armazena altura do video que esta sendo capturado
codec=cv2.VideoWriter_fourcc(*'XVID')
gravador=cv2.VideoWriter('meu_video1.avi',codec,20,(largura,altura)) # o video que sera gravado sera salvo nessa pasta

while True:
    ret,frame=cap.read() # ret retorna booleano e frame a captura
    frame_cinza=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY) # converte frame colorido em escala de cinza
    gravador.write(frame) # grava video colorido
    if not ret:
        print('Erro na captura')
        break

    # VISUALIZACAO
    # cv2.imshow('Captura do video',frame) # em RGB/colorido
    cv2.imshow('Captura do video',frame_cinza) # em escala de cinza
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
gravador.release()
cv2.destroyAllWindows


