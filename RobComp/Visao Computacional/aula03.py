# AULA 3 - CANAIS DE CORES
# RESUMO TEORICO EM: https://chatgpt.com/g/g-p-6a87256172d081919775b7adde1bc758-robcomp/c/6aabc40a-cc94-83e9-a996-2f1fb929a968

import cv2
import numpy as np

cap=cv2.VideoCapture(0) # captura video da webcam, mas poderia ser o caminho de um video baixado tambem
while True:
    ret, frame=cap.read()
    if not ret:
        break # Caso o webcam nao consiga "ler" a imagem > fechar janela

    hsv=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV) # Convertendo canal da imagem capturada (frame) em HSV > canal melhor para fazer FILTROS/MASCARAS
    vermelho_escuro=np.array([165,50,50]) # HSV
    vermelho_claro=np.array([179,255,255]) # HSV
    mascara=cv2.inRange(hsv,vermelho_escuro,vermelho_claro)
    # MASCARA:
    # o que é pra ser mostrado (dentro da faixa) -> PIXEL BRANCO
    # o que NAO é pra ser mostrado (fora da faixa) -> PIXEL PRETO
    resultado=cv2.bitwise_and(frame,frame,mask=mascara) # aplicacao da mascara

    # cv2.imshow('Camera Original',frame) # mostra uma janela com a captura original da webcam
    cv2.imshow('Camera Filtro',resultado) # mostra uma janela com a captura da webcam com a mascara aplicada

    if cv2.waitKey(1) & 0xFF==ord('q'):
        break # fecha a janela apenas quando for pressionada a tecla "q"
cap.release()
cv2.destroyAllWindows()

