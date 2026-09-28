import cv2

class ProcessImage:

    def load_image(self, image_path):
        self.bgr = cv2.imread(image_path)

    def show_image(self):
        cv2.imshow("Imagem", self.bgr)
        cv2.waitKey()
        cv2.destroyAllWindows()

    def show_channels(self):
        self.bgr_b, self.bgr_g, self.bgr_r = cv2.split(self.bgr)
        cv2.imshow("Azul (B)", self.bgr_b)
        cv2.imshow("Verde (G)", self.bgr_g)
        cv2.imshow("Vermelho (R)", self.bgr_r)

        cv2.waitKey()
        cv2.destroyAllWindows()

def main():
    process_image = ProcessImage()
    process_image.load_image("arara.jpg")
    process_image.show_channels()

if __name__ == "__main__":
    main()