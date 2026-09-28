import cv2
imagem=cv2.imread('teste.png')  # ler imagem e transformar em matriz de pixels
cv2.imshow('Primeira imagem', imagem) # mostra janela com a imagem
cv2.waitKey(0)
cv2.destroyAllWindows() # limpar memoria
print(imagem.shape) # imprime (linhas, colunas, canais) da imagem
# No caso: (534,800,3) -> 534 pixels em linhas, 800 pixels em colunas e 3 canais de cor RGB