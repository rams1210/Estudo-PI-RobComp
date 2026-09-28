import cv2
import numpy as np

tam = 5
tam2=9
tamanhoBlur=9
imagens=['teste.png']

img=cv2.imread(imagens[0],0)
kernel=np.ones((tam,tam),np.uint8)
kernel2=np.ones((tam2,tam2),np.uint8)

blur_mediana=cv2.medianBlur(img,tamanhoBlur)

# Juntando com o blur: trocar img por blur_mediana
erosao=cv2.erode(blur_mediana,kernel,iterations=1)
dilatacao=cv2.dilate(blur_mediana,kernel2,iterations=1)
abertura=cv2.morphologyEx(img,cv2.MORPH_OPEN,kernel) #erosao avancada
fechamento=cv2.morphologyEx(img,cv2.MORPH_CLOSE,kernel) #dilatacao avancada

cv2.imshow('Original',img)
cv2.imshow('Erosao',erosao)
cv2.imshow('Dilatacao',dilatacao)
cv2.imshow('Abertura',abertura)
cv2.imshow('Fechamento',fechamento)

cv2.waitKey(0)
cv2.destroyAllWindows()