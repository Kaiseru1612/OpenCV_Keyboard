import cv2
from cvzone.HandTrackingModule import HandDetector
from time import sleep
from pynput.keyboard import Controller
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)
finalText = ""
detector = HandDetector(detectionCon=0.8)
keyboard = Controller()

def Drawkeyboard(img, Keyimglist):
    for button in Keyimglist:
        x, y = button.pos
        w, h = button.size
        cv2.rectangle(img, button.pos, (x + w, y + h), (255, 0, 0), cv2.FILLED)
        cv2.putText(img, button.text, (x + 20, y + 75),
                cv2.FONT_HERSHEY_PLAIN, 5, (255, 255, 255), 4)
    return img

class Key():
    def __init__(self, pos, text, size=[90, 90]):
        self.pos = pos
        self.size = size
        self.text = text




Keyimglist = []
Keys = [["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
        ["A", "S", "D", "F", "G", "H", "J", "K", "L", ";"],
        ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "/"]]

# create Keyboard
for i in range(len(Keys)):
    for j, key in enumerate(Keys[i]):
        Keyimglist.append(Key([100 * j + 50, 100 * i + 50], key))

while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmlist, bboxinfo = detector.findPosition(img)
    img = cv2.flip(img,1)
    img = Drawkeyboard(img, Keyimglist)
    if (keyboard.press==']'):
        finalText = ""
    if lmlist:
        for button in Keyimglist:
            x, y = button.pos
            w, h = button.size

            if (1180 - x < lmlist[8][0] < 1180 - x+w) and (y < lmlist[8][1] < y+h):
                cv2.rectangle(img, button.pos, (x + w, y + h), (0, 255, 0), cv2.FILLED)
                cv2.putText(img, button.text, (x + 20, y + 75),
                            cv2.FONT_HERSHEY_PLAIN, 5, (255, 255, 255), 4)
                l, _, _ = detector.findDistance(8,12,img,draw=False)
                print(l)
                #click
                if l < 80:
                    keyboard.press(button.text)
                    cv2.rectangle(img, button.pos, (x + w, y + h), (100, 0, 100), cv2.FILLED)
                    cv2.putText(img, button.text, (x + 20, y + 75),
                                cv2.FONT_HERSHEY_PLAIN, 5, (255, 255, 255), 4)
                    finalText += button.text
                    sleep(0.15)
    cv2.rectangle(img, (50,350), (700, 450), (175, 0, 175), cv2.FILLED)
    cv2.putText(img, finalText, (60, 425),
                cv2.FONT_HERSHEY_PLAIN, 5, (255, 255, 255), 4)


    #showifamera

    cv2.imshow("image", img)
    cv2.waitKey(1)