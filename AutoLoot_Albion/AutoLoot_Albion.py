from concurrent.futures import thread
from pyautogui import *
import pyautogui
import time
import threading
import keyboard
import random
import mouse
from PIL import Image
import win32api
import win32con
import pynput.mouse as ms
import pynput.keyboard as kb

coordItem = [70,320] 
coordItemConfig = None
keyboardController = kb.Controller()
estActif  = False

pyautogui.PAUSE = 0.01

scrollPositions = [585,345]
EmptyDetectionConfig = [115,335]

multiplier = 1
timeMouseDown = 0.045
timeMouseUp = 0.01

timeDeplacementSouris1 = 0.06
timeDeplacementSouris2 = 0.06

coord_XTest = 80
coord_YTest = 300

nbColonne = 5
nbLigne = 15

nbColonneConfig = 5
nbLigneConfig = 5

delaiScroll = 0.02
DistanceScroll = 19.7

tempsTotal = ""

emptyImage = Image.open("detectItem.png")
openInventaire = Image.open("OpenInv.png")

def stopLooting():
    global estActif
    while estActif:
        if pyautogui.locateOnScreen(openInventaire, region=(1140,250,9,15), grayscale=True) == None:
            estActif = False
        time.sleep(0.1)

def checkAutolootKeyStart(key):
    global estActif
    if 'char' in dir(key):
        if key.char == "c" or key.char == "C":
            print(2)
            estActif = True

def checkAutolootKeyStop(key):
    global estActif
    if 'char' in dir(key):
        if key.char == "c" or key.char == "C":
            print(3)
            estActif = False

def startKeyboardListener():
    with kb.Listener(on_press=checkAutolootKeyStart, on_release=checkAutolootKeyStop) as listener:
        listener.join()

threading.Thread(target=startKeyboardListener).start()

def click(x,y):
    win32api.SetCursorPos((x,y))
    time.sleep(random.uniform(float(timeDeplacementSouris1), float(timeDeplacementSouris2)))
    mouse.press(button='left')
    time.sleep(float(timeCalculatedMouseDown))
    mouse.release(button='left')
    time.sleep(float(timeCalculatedMouseUp))

def getMiddleOfFrame(x,y):
    result = []
    result.append(x + random.uniform(10, 25))
    result.append(y)
    return result

def resetScrollPos():
    global scrollPositions
    scrollPositions = [585,345]

def resetAutoDetectConfig():
    global EmptyDetectionConfig
    EmptyDetectionConfig = [115,335]

def passNextItemCoordDetectConfig_X():
    global EmptyDetectionConfig
    EmptyDetectionConfig[0] = EmptyDetectionConfig[0] + 100

def passNextItemCoordConfig_X():
    global coordItemConfig
    coordItemConfig[0] = coordItemConfig[0] + 100

def passNextItemCoordConfig_Y():
    global coordItemConfig
    coordItemConfig[1] = coordItemConfig[1] + 100 

def passNextItemCoordDetectConfig_Y():
    global EmptyDetectionConfig
    EmptyDetectionConfig[1] = EmptyDetectionConfig[1] + 100

def resetCoordConfig_X():
    global coordItemConfig
    global nbColonneConfig
    coordItemConfig[0] = coordItemConfig[0] - (int(nbColonneConfig)*100)

def resetCoordDetectConfig_X():
    global EmptyDetectionConfig
    global nbColonneConfig
    EmptyDetectionConfig[0] = EmptyDetectionConfig[0] - (int(nbColonneConfig)*100)

def clickOnItem(coord,deplacementSouris1, deplacementSouris2, multiplieur, timeClickDown, timeClickUp):
    middle = getMiddleOfFrame(int(coord[0]),int(coord[1])) 
    win32api.SetCursorPos((int(middle[0]),int(middle[1])))    
    time.sleep(random.uniform((float(deplacementSouris1) * multiplieur), (float(deplacementSouris2)*multiplieur)))
    mouse.press(button='left')
    time.sleep(float(timeClickDown)*multiplieur)
    mouse.release(button='left')
    time.sleep(float(timeClickUp)*multiplieur)

def scroll(coord,distance,delai,reverse):

    win32api.SetCursorPos((int(coord[0]),int(coord[1])))
    if reverse:
        coord[1] -= float(distance)
    else:
        coord[1] += float(distance)
    mouse.press(button='left')
    time.sleep(float(delai)*multiplier)
    win32api.SetCursorPos((int(coord[0]),int(coord[1])))
    mouse.release(button='left')
    time.sleep(0.02)


def configCollectItems(coordX, coordY, nbColonne, nbLigne, timeDeplacementSouris1, timeDeplacementSouris2, timeMouseDown, timeMouseUp, scrollDelai, scrollDistance, autoDetect, reverse):

    global scrollPositions
    global tempsTotal
    global emptyImage
    global EmptyDetectionConfig
    global coordItemConfig
    global nbColonneConfig
    global nbLigneConfig

    trouve = 0

    nbColonneConfig = nbColonne
    nbLigneConfig = nbLigne

    coordItemConfig = [int(coordX), int(coordY) ]
    start = time.time()
    keyboardController.press(kb.Key.shift_l) #Appui sur shift


    for ligne in range(int(nbLigne)):

        if ligne > 0: #Si nest pas la premiere ligne
            if ligne < 5: #Si nest pas supperieur a la ligne 5
                passNextItemCoordConfig_Y()  #Saute une ligne
                if autoDetect == "on":
                    passNextItemCoordDetectConfig_Y()

            elif int(nbLigne) > 5 and ligne > 4: #Si on depasse la ligne 5 (action de scroll)
                scroll(scrollPositions,scrollDistance,scrollDelai,False)

        for colonne in range(int(nbColonne)): 

            if autoDetect == "on":
                if pyautogui.locateOnScreen(emptyImage, region=(EmptyDetectionConfig[0],EmptyDetectionConfig[1],15,15), grayscale=True, confidence=0.43) == None:
                    clickOnItem(coordItemConfig,timeDeplacementSouris1, timeDeplacementSouris2, multiplier, timeMouseDown, timeMouseUp) 
                    trouve += 1
                passNextItemCoordDetectConfig_X()
            else:
                clickOnItem(coordItemConfig,timeDeplacementSouris1, timeDeplacementSouris2, multiplier, timeMouseDown, timeMouseUp)
                
            passNextItemCoordConfig_X()  

        if autoDetect == "on":
            resetCoordDetectConfig_X()
        resetCoordConfig_X()

    if autoDetect == "on":
         resetAutoDetectConfig()
    resetScrollPos()

    keyboardController.release(kb.Key.shift_l) #On relache la touche shift

    truc = int(nbColonne)*int(nbLigne)

    print(str(trouve)+"/"+str(truc)+" trouve")
    end = time.time()
    tempsTotal = str("{0:.2f}".format(end - start))


def collectItemsAuto():
    global estActif 
    coordItem = [810,430] 
    nbColonne = 3
    nbLigne = 3
    estActif = True

    threading.Thread(target=stopLooting).start()

    keyboardController.press(kb.Key.shift_l)
    for i in range(nbLigne):
        if not estActif:
            keyboardController.release(kb.Key.shift_l)
            break
        if i > 0:
            coordItem[1] = coordItem[1] + 100

            if i > 3:
                win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL,int(coordItem[0]),int(coordItem[1]), -1, 0)
                coordItem[1] = coordItem[1] - DistanceScroll
                time.sleep(delaiScroll)

        for j in range(nbColonne):   
            if not estActif:
                keyboardController.release(kb.Key.shift_l)
                break
            middle = getMiddleOfFrame(coordItem[0],coordItem[1])
            click(int(middle[0]), int(middle[1]))
            coordItem[0] = coordItem[0] + 100           
        coordItem[0] = coordItem[0] - 300
    
    keyboardController.release(kb.Key.shift_l)
    estActif = False

def collectItems():

    global estActif 

    coordItem = [810,430] 
    nbColonne = 3
    nbLigne = 3
    threading.Thread(target=stopLooting).start()
    keyboardController.press(kb.Key.shift_l)
    for i in range(nbLigne):
        if not estActif:
            keyboardController.release(kb.Key.shift_l)
            break
        if i > 0:
            coordItem[1] = coordItem[1] + 100
        for j in range(nbColonne):   
            if not estActif:
                keyboardController.release(kb.Key.shift_l)
                break
            middle = getMiddleOfFrame(coordItem[0],coordItem[1])
            click(int(middle[0]), int(middle[1]))
            coordItem[0] = coordItem[0] + 100           
        coordItem[0] = coordItem[0] - 300
    
    keyboardController.release(kb.Key.shift_l)
    estActif = False