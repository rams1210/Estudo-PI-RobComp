# ARITMETICA DE IMAGENS

import cv2

img1=cv2.imread('teste.png')
img2=cv2.imread('logo.avif')

# Visualizando as janelas com as imagens antes de mesclar:
# cv2.imshow("Paisagem", img1)
# cv2.imshow("Logo", img2)
# cv2.waitKey(0)
# cv2.destroyAllWindows

# Para mesclar duas imagens elas precisam ser do MESMO TAMANHO
# Verificar as dimensoes de cada imagem -> shape retorna: (altura, largura, canais):
print("Imagem 1:", img1.shape) # (534, 800, 3)
print("Imagem 2:", img2.shape) # (626, 626, 3)
altura, largura = img2.shape[:2]
# resize recebe: (largura, altura) da img2 e deixa img1 do mesmo tamanho:
img1 = cv2.resize(img1,(largura, altura),interpolation=cv2.INTER_AREA)

# Somando cores das imagens pixel a pixel
#soma = cv2.add(img1,img2)
# Visualizando a janela com o resultado:
#cv2.imshow("Soma Direta", soma)
#cv2.waitKey(0)
#cv2.destroyAllWindows()

# Somando imagens pixel a pixel definindo pesos para cada um deles
mesclagem = cv2.addWeighted(img1,0.7,img2,0.3,0) # OBS.: ultimo parametro: ajuste de brilho
# Visualizando a janela com o resultado:
cv2.imshow("Mesclagem", mesclagem)
cv2.waitKey(0)
cv2.destroyAllWindows()





