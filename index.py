import cv2
import time
from pyfirmata import Arduino, util
# import matplotlib.pyplot as plt
import cvlib as cv
# from cvlib.object_detection import draw_bbox


def imagecapture():
    video = cv2.VideoCapture(0)
    a = 0
    while True:
        a = a + 1
        check, frame = video.read()
        cv2.imshow("Capturing", frame)
        key = cv2.waitKey(1)
        break
    showPic = cv2.imwrite(
        r"C:\Users\adity\OneDrive\Desktop\Project_HS202\captured_photos\filename.jpg", frame)
    print(showPic)
    video.release()
    cv2.destroyAllWindows


input = [2, 15,50,10]
novhcl = [0, 0, 0, 0]


def imageread(input):
    im1 = cv2.imread(
        r"C:\Users\adity\OneDrive\Desktop\Project_HS202\captured_photos\filename.jpg")
    im2 = cv2.imread(
        r"C:\Users\adity\OneDrive\Desktop\Project_HS202\captured_photos\filename.jpg")
    im3 = cv2.imread(
        r"C:\Users\adity\OneDrive\Desktop\Project_HS202\captured_photos\filename.jpg")
    im4 = cv2.imread(
        r"C:\Users\adity\OneDrive\Desktop\Project_HS202\captured_photos\filename.jpg")
    bbox1, label1, conf1 = cv.detect_common_objects(im1)
    bbox2, label2, conf2 = cv.detect_common_objects(im2)
    bbox3, label3, conf3 = cv.detect_common_objects(im3)
    bbox4, label4, conf4 = cv.detect_common_objects(im4)
    # output_image = draw_bbox(im, bbox, label, conf)
    # plt.imshow(output_image)
    # plt.show()
    noc1 = int(str(label1.count('car')))
    noc2 = int(str(label2.count('car')))
    noc3 = int(str(label3.count('car')))
    noc4 = int(str(label4.count('car')))
    print(noc1, noc2, noc3, noc4)
    input.append(noc1)
    input.append(noc2)
    input.append(noc3)
    input.append(noc4)
    return input


def strt(input):
    while input:
        input.pop()
    imagecapture()
    imageread(input)
    return input


try:
    board = Arduino('COM3')
    print("Success")
except:
    print("CONNECTION FAILURE")
    exit()
iterator = util.Iterator(board)
iterator.start()

r1 = board.get_pin('d:11:o')
r2 = board.get_pin('d:8:o')
r3 = board.get_pin('d:5:o')
r4 = board.get_pin('d:2:o')
g1 = board.get_pin('d:13:o')
g2 = board.get_pin('d:10:o')
g3 = board.get_pin('d:7:o')
g4 = board.get_pin('d:4:o')
y1 = board.get_pin('d:12:o')
y2 = board.get_pin('d:9:o')
y3 = board.get_pin('d:6:o')
y4 = board.get_pin('d:3:o')
red_led = [r1, r2, r3, r4]
yellow_led = [y1, y2, y3, y4]
green_led = [g1, g2, g3, g4]

cnumber = 1
tme = 1  # in seconds
dtme = 2
ydelay = 0.5


def low():
    for i in range(4):
        red_led[i].write(0)
        green_led[i].write(0)
        yellow_led[i].write(0)
    for i in range(4):
        red_led[i].write(1)


def signalfunction(input, i, dtme, tme, cnumber, ydelay):  # i=0
    print("Signal {0}".format(i+1))
    strt(input)
    if input == novhcl:
        print("0 Vehicles")
        low()
        red_led[0].write(0)
        green_led[0].write(1)
        strt(input)
    elif input[i] > 0:
        print("input is greater than zero")
        if input[i] < cnumber:
            print("time reduced")
            dtme = tme
        else:
            print("time not reduced")
            dtme = dtme
        print("High red LED")
        low()
        print("Low red LED")
        red_led[i].write(0)
        print("High green LED")
        green_led[i].write(1)
        print("sleep time")
        time.sleep(dtme)
        strt(input)
        if input[abs(1-i)] > 0 or input[abs(2-i)] > 0 or input[abs(3-i)] > 0:
            print("In the loop")
            print("low green LED")
            green_led[i].write(0)
            print("High yellow LED")
            yellow_led[i].write(1)
            print("Time delay")
            time.sleep(ydelay)
        else:
            flag = False
            while flag == False:
                strt(input)
                if input[abs(1-i)] > 0 or input[abs(2-i)] > 0 or input[abs(3-i)] > 0:
                    flag = True
                    green_led[i].write(0)
                    yellow_led[i].write(1)
                    time.sleep(ydelay)

                else:
                    time.sleep(5)  # 5 sec sleep


while True:
    print(input)
    signalfunction(input, 0, dtme, tme, cnumber, ydelay)
    signalfunction(input, 1, dtme, tme, cnumber, ydelay)
    signalfunction(input, 2, dtme, tme, cnumber, ydelay)
    signalfunction(input, 3, dtme, tme, cnumber, ydelay)
1