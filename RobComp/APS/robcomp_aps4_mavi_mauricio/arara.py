import cv2
import numpy as np

class ProcessImage:
    def run_image(self, image):
        self.bgr = image
        height, width, _ = self.bgr.shape
        saida = np.zeros_like(self.bgr)
        metade_height = int(height / 2)
        terco_width = int(width / 3)
        dois_tercos_width = int(2 * width / 3)

        # regiao superior esquerda
        saida[:metade_height, :terco_width] = self.bgr[:metade_height, :terco_width]
        # regiao superior direita
        saida[:metade_height, dois_tercos_width:] = self.bgr[:metade_height, dois_tercos_width:]
        # regiao inferior centro
        saida[metade_height:, terco_width:dois_tercos_width] = self.bgr[
            metade_height:, terco_width:dois_tercos_width
        ]
        self.bgr = saida

    def show_image(self):
        cv2.imshow("Arara process", self.bgr)
        cv2.waitKey()
        cv2.destroyAllWindows()


def main():
    process_image = ProcessImage()
    arara = cv2.imread("arara.jpg")
    process_image.run_image(arara)
    process_image.show_image()

if __name__ == "__main__":
    main()