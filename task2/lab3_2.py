import cv2
import matplotlib.pyplot as plt


# read image from path
def read_image (path):
    image = cv2.imread(path)
    # show image
    plt.imshow(image)
    plt.title('Зображення до корекції кольору')
    plt.show()
    return image


# edit image color
def image_redactor(image):
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
    blur = cv2.GaussianBlur(gray, (3, 3), 10)
    edged = cv2.Canny(blur, 110, 250)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (16, 16))
    closed = cv2.morphologyEx(edged, cv2.MORPH_CLOSE, kernel)
    # show edited image
    plt.imshow(closed)
    plt.title('Зображення після корекції кольору')
    plt.show()
    return closed


# find contours in edited image
def image_contour(image):
    contours, hierarchy = cv2.findContours(image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    return contours


# draw all input contours
def draw_contour(image, contours):
    for countour in contours:
        cv2.drawContours(image, countour, -1, (0, 255, 0), 3)
    plt.imshow(image)
    plt.title('Зображення після виділення контурів')
    plt.show()


# draw contours with 4 corners and count them, also draw contours bigger than 1000
def image_recognition (image_entrance, image_cont):
    total = 0
    picked_contours = []
    image_all = image_entrance.copy()
    #pick contours with 4 corners
    for c in image_cont:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)
        if len(approx) == 4:
            picked_contours.append(approx)
            cv2.drawContours(image_all, [approx], -1, (0, 255, 0), 4)
    plt.imshow(image_all)
    plt.title('Зображення після виділення контурів усіх прямокутних об\'єктів')
    plt.show()
    #draw contours bigger than 1000, count them
    for contour in picked_contours:
        area = cv2.contourArea(contour)
        if area > 1000:
            cv2.drawContours(image_entrance, [contour], -1, (0, 255, 0), 3)
            total += 1
    cv2.imwrite('result.png', image_entrance)
    plt.imshow(image_entrance)
    print("Знайдено {0} сегмент(а) об'єктів".format(total))
    plt.title('Зображення після виділення контурів великих об\'єктів')
    plt.show()


# main
image = read_image('img.png')
image_edited = image_redactor(image)
contours = image_contour(image_edited)
#draw_contour(image, contours)
image_recognition(image, contours)

