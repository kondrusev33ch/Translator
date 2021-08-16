import cv2 as cv
import re
import numpy as np
import pyautogui
from time import sleep
from deep_translator import GoogleTranslator
from win32gui import GetCursorPos
from win32api import GetAsyncKeyState
from easyocr import Reader
from PIL import ImageFont, ImageDraw, Image

# Globals
SHOT_WIDTH = 400
SHOT_HEIGHT = 200
VK_END = 35
VK_XBUTTON2 = 6
CAPTURE_SCREEN_CENTER = (SHOT_WIDTH / 2, SHOT_HEIGHT / 2)
RU_FONT_PATH = 'Arial.ttf'
RU_FONT_SIZE = 22
BLACK_RGBA = (0, 0, 0, 255)
WND_SIZE = (40, 300, 3)
TEXT_LOCATION = (5, 5)


# ----------------------------------------------------------
def main():
    # Init GTranslator and EasyOCR reader
    to_rus = GoogleTranslator(source='en', target='ru')
    reader = Reader(['en'])  # pytorch for speed, I like speed

    # Main loop
    while not GetAsyncKeyState(VK_END) & 1:
        if GetAsyncKeyState(VK_XBUTTON2) & 1:
            # Find mouse position
            mouse_x, mouse_y = GetCursorPos()

            # Get screenshot of the specific region on the MAIN screen. The smaller the region, the higher the speed
            img = np.array(pyautogui.screenshot(region=(mouse_x - SHOT_WIDTH / 2, mouse_y - SHOT_HEIGHT / 2,
                                                        SHOT_WIDTH, SHOT_HEIGHT)))
            # Find all words on the screenshot
            # https://www.jaided.ai/easyocr/documentation/
            results = reader.readtext(img, width_ths=0.02, blocklist=",.:;'!?()[]{}")
            for bbox, word, _ in results:
                if re.search('[^a-zA-Z-"]', word):  # filter out not words
                    continue

                # bbox consists of [[x, y], [x, y], [x, y], [x, y]], we only need tl and br
                # If mouse inside bbox, then show window with translation
                if int(bbox[0][0]) <= CAPTURE_SCREEN_CENTER[0] <= int(bbox[2][0]) and \
                        int(bbox[0][1]) <= CAPTURE_SCREEN_CENTER[1] <= int(bbox[2][1]):
                    show_translate(word, to_rus.translate(word), mouse_x, mouse_y)
                    break  # this saves us a little time

        sleep(0.001)


# ----------------------------------------------------------
def show_translate(original: str, translated: str, x: int, y: int) -> None:
    # Show window with translation
    cv.imshow(original, get_image(translated))
    cv.setWindowProperty(original, cv.WND_PROP_TOPMOST, cv.WINDOW_AUTOSIZE)  # set window topmost
    cv.moveWindow(original, x, y)  # set window position

    # Waiting, until VK_XBUTTON2 will be pressed or window will be closed
    while not GetAsyncKeyState(VK_XBUTTON2) & 1 and cv.getWindowProperty(original, cv.WND_PROP_VISIBLE):
        cv.waitKey(1)  # a 1ms delay to not to load the system

    # Destroy window in case VK_XBUTTON2 was pressed
    cv.destroyAllWindows()
    return None


# ----------------------------------------------------------
def get_image(translated: str) -> np.array:
    # Create empty white image, technically it is a matrix
    img = np.full(WND_SIZE, 255, dtype=np.uint8)  # 255 for (255, 255, 255) = White

    # Add translated text to an image
    font = ImageFont.truetype(RU_FONT_PATH, RU_FONT_SIZE)  # we should use this technique because
    img_pil = Image.fromarray(img)                         # Russian language is not in ASCII
    draw = ImageDraw.Draw(img_pil)
    draw.text(TEXT_LOCATION, translated, font=font, fill=BLACK_RGBA)

    return np.array(img_pil)


# ----------------------------------------------------------
if __name__ == '__main__':
    main()
