# FILTRO DE BLUR -> remover ruido de imagens
# Tecnica de convolucao e calculos da matriz de Kernel aplicarao os filtros em cada pixel
# O filtro escolhido depende do contexto de utilizacao do mesmo

import cv2
imgs=['img_ruido_cinza.png','img_ruido_colorida.png']
img=cv2.imread(imgs[0])
blur_media=cv2.blur(img,(9,9)) # recebe a img e uma matriz de kernel (quanto maior a dimensao, menor o ruido mas mais embacado)
blur_gaussiano=cv2.GaussianBlur(img,(9,9),0) # aplica o desfoque Gaussiano, preserva mais os contornos originais dos objetos
blur_mediana=cv2.medianBlur(img,9) # substitui os pixels defeituosos pela mediana, eliminando o ruído "Sal e Pimenta" sem perder a nitidez, o melhor para contornos!

cv2.imshow('Original',img)
cv2.imshow('Blur media',blur_media)
cv2.imshow('Blur Gaussiano',blur_gaussiano)
cv2.imshow('Blur Mediana',blur_mediana)

cv2.waitKey(0)
cv2.destroyAllWindows()