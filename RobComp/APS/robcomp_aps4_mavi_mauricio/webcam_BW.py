import cv2

class ProcessImage:

    def run_image(self, image):
        self.bgr = image
        self.gray = cv2.cvtColor(self.bgr, cv2.COLOR_BGR2GRAY)
        self.gray[self.gray < 128] = 0
        self.gray[self.gray >= 128] = 255

    def show_image(self):
        cv2.imshow("webcam BW", self.gray)


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