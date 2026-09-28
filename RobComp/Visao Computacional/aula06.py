import cv2

# Comecar convertendo as imagens em tons de cinza antes da limerizacao
# Binarização que Ignora Sombra e Brilhos Excessivos

imagens=['texto_a.png', 'texto_b.png']
img=cv2.imread(imagens[1],0) # lendo imagem e ja convertendo-a em uma matriz em tons de cinza

# THRESH PADRÃO: aplica a limerizacao, o segundo parametro é um valor limiar ("intensidade"), o terceiro parametro é um valor máximo para o tom claro. Ambos variam de varia de 0 a 255. O quarto parametro é o tipo de thresh binary (nesse caso, selecionamos os binário invertido)
# ret, thresh_binario_inv = cv2.threshold(img,127,255,cv2.THRESH_BINARY_INV)

# THRESH ADAPTATIVO: melhor para situacoes de sombra excessiva
# Pode transformar sombras em ruidos e depois retirar ruido com outro recurso (aula05.py)
thresh_adaptativo = cv2.adaptiveThreshold(
    img,
    255, # tonalidade max desejada
    cv2.ADAPTIVE_THRESH_GAUSSIAN_C, # tipo do adaptative thresh
    cv2.THRESH_BINARY, # tipo de thresh binary
    11, # tamanho do bloco quadrado em px (impar)
    10 # constante de ajuste
)

cv2.imshow('Original',img)
cv2.imshow('Limiar Adaptativo',thresh_adaptativo)
cv2.waitKey(0)
cv2.destroyAllWindows()