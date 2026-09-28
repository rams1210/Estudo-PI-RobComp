# DOMINANDO PIXELS, RECORTES (ROI -> limpeza de imagens

import cv2

img1=cv2.imread('teste.png')

# Acessando pixel de uma imagem
# pixel=img1[100,150]
# print(f"Valor BGR do pixel: {pixel}") # Valor BGR do pixel: [239 188 124]

# Mudando cor do pixel para vermelho
# pixel=img1[100,150]=[0,0,255]
# print(f"Valor BGR do pixel: {pixel}") # Valor BGR do pixel: [0, 0, 255]

# Criando uma área maior para alteracao
# img1[100:150,150:200]=[0,0,255]

# ROI: regiao de interesse -> ignorar o resto da img e focar so no que import (economiza memoria e processamento):
roi=img1[100:300,150:350]
# janela com imagem inteira:
cv2.imshow("Paisagem", img1)
# janela com parte selecionada da imagem (recorte):
cv2.imshow("Recorte da paisagem", roi)
# Visualizando as janelas:
cv2.waitKey(0)
cv2.destroyAllWindows

