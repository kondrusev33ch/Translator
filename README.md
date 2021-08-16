# Translator
This is my working prototype of word translator EN->RU using EasyOCR 
![example](https://user-images.githubusercontent.com/85990934/129613964-912f7c16-2f82-48b9-817a-2159f6d0568c.png)


## What for?
Main purpose - make translation process easier. Whith this script you will only need to press one button to get translated word.  
I personally use it while reading books, but you can use it everywhere, where you can see an english text. 

## Modules 
```sh
pip install opencv-python
pip install numpy
pip install pyautogui
pip install deep-translator
pip install pywin32
pip install easyocr
pip install pil
```

## How to use
* Wait a few seconds after start
* Move mouse cursor on the word you want to translate and press VK_XBUTTON2(left side, closest to the wire) 
* After that a translation window will appear (if not try again). 
* Close the window by pressing X or VK_XBUTTON2
* To exit press END
* Translator not tested with games, but it should work if game in a window mode
