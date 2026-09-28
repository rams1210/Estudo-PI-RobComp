import cv2
import numpy as np

class ProcessImage:

    def run_image(self, image):
        self.bgr = image
        self.hsv = cv2.cvtColor(self.bgr, cv2.COLOR_BGR2HSV)

        # verde
        low_green = np.array([35, 50, 50])
        high_green = np.array([85, 255, 255])
        self.mask_green = cv2.inRange(self.hsv,low_green,high_green)

        # azul
        low_blue = np.array([90, 50, 50])
        high_blue = np.array([130, 255, 255])
        self.mask_blue = cv2.inRange(self.hsv,low_blue,high_blue)

        # vermelho
        low_red1 = np.array([0, 50, 50])
        high_red1 = np.array([10, 255, 255])
        low_red2 = np.array([170, 50, 50])
        high_red2 = np.array([180, 255, 255])
        mask_red1 = cv2.inRange(self.hsv,low_red1,high_red1)
        mask_red2 = cv2.inRange(self.hsv,low_red2,high_red2)
        self.mask_red = mask_red1 + mask_red2

        # soma das três máscaras
        self.mask = self.mask_green + self.mask_blue + self.mask_red

    def show_image(self):
        cv2.imshow("imagem original", self.bgr)
        cv2.imshow("imagem com a mascara", self.mask)

def main():
    webcam = cv2.VideoCapture(0)
    process_image = ProcessImage()
    while True:
        val, image = webcam.read()
        if val:
            process_image.run_image(image)
            process_image.show_image()
        if cv2.waitKey(1) == 27:
            break
    cv2.destroyAllWindows()
    webcam.release()

if __name__ == "__main__":
    main()