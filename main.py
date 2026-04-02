from mss import mss
import numpy as np
import easyocr
import cv2
from keyboard import *
import tkinter as tk
from googletrans import Translator
import asyncio


async def write_ocr_output_on_screen(ocrOutput):
    win = tk.Tk()

    win.overrideredirect(True)
    win.geometry('1920x1080')
    win.lift()
    win.wm_attributes("-topmost", True)
    win.wm_attributes("-disabled", True)
    win.config(bg='gray')
    win.attributes('-transparentcolor', 'gray')
    #win.attributes('-transparentcolor', 'white')

    # ocrOutput = [([[np.int32(566), np.int32(393)], [np.int32(1402), np.int32(393)],[np.int32(1402), np.int32(508)],
    #             [np.int32(566), np.int32(508)]], 'eran las diez de', np.float64(0.818656078641447)), ([[np.int32(749), np.int32(549)],
    #             [np.int32(1213), np.int32(549)], [np.int32(1213), np.int32(663)], [np.int32(749), np.int32(663)]], 'la noche', np.float64(0.950960837480548))]


    for element in ocrOutput:
        element[1] = await Translator().translate(element[1], src='ru', dest='en')
        label = tk.Label(text=element[1].text, font=('Times New Roman','10'), fg='black', bg='white', wraplength=100)
        label.place(x=element[0][0][0], y=element[0][0][1])




    while True:

        if is_pressed('q'):
            win.destroy()

        win.update_idletasks()
        win.update()  


def read_screen(ocrReader,mon={'top': 100, 'left': 250, 'width': 1420, 'height': 880}):
    print('Scanning...')

    with mss() as sct:

        img = np.array(sct.grab(mon))
        #cv2.imshow('test',img)

        #time.sleep(1)
        
        text = ocrReader.readtext(img,paragraph=True)
        return text




async def main():
    printLoop = 0

    print('loading Reader into memory')
    reader = easyocr.Reader(['ru'], gpu= True)


    mon = mss().monitors[1]
    while True:

        printLoop += 1
        if printLoop >= 10:
            printLoop = 0
            print('Loop entered')

        if is_pressed('a'):
            ocrOutput = read_screen(reader, mon)
            print(ocrOutput)
            await write_ocr_output_on_screen(ocrOutput)

        if (cv2.waitKey(25) & 0xFF == ord('q')) or is_pressed('q'):
            cv2.destroyAllWindows()
            break
if __name__ == '__main__':
    asyncio.run(main())