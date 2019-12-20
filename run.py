#!/usr/bin/env python3

import keyboard
import pyautogui
import pytesseract
import os
import PIL
import time
import pdfminer
import sys
import io
import pdfminer.pdfinterp
import pdfminer.pdfpage
import pdfminer.converter
import pdfminer.layout

# Create dictionary of unit

# Janky!
def pdf_to_text():
    rsrcmgr = pdfminer.pdfinterp.PDFResourceManager()
    retstr = io.StringIO()
    codec = "utf-8"
    laparams = pdfminer.layout.LAParams()
    device = pdfminer.converter.TextConverter(rsrcmgr, retstr, laparams=laparams)
    interpreter = pdfminer.pdfinterp.PDFPageInterpreter(rsrcmgr, device)
    with open("input.pdf", 'rb') as f:
        for page in pdfminer.pdfpage.PDFPage.get_pages(f):
            interpreter.process_page(page)
            data = retstr.getvalue()
    return data

def format_text(text):
    print(text)
    # Remove first three lines
    text = text.split("\n")[3:]
    # Remove empty lines
    text = [line for line in text if line.strip() != ""]
    # Find "English"
    for index, line in enumerate(text):
        if line.strip() == "English":
            pad_lang = index
    print(pad_lang)
    # Remove "English"
    text = [line for line in text if line.strip() != "English"]
    # Convert to german,english syntax
    newtext = []
    i = 0
    while i < len(text) / 2:
        newtext.append(text[i].strip() + "," + text[i + pad_lang].strip() + "\n")
        i += 1
    return newtext

def get_maps(maps):
    maps = [x.strip().split(",") for x in maps]
    maps.pop(0)
    maps = [[x[0].split(";", 1)[0], x[1].split(";", 1)[0]] for x in maps]
    maps.sort(key = lambda s: len(s[0]))
    return maps

def get_text():
    # Get screenshot of EP screen
    try:
        os.remove("word.png")
    except FileNotFoundError:
        pass
    pyautogui.screenshot("word.png")

    # Extract text from it
    # German
    return pytesseract.image_to_string(PIL.Image.open("word.png"), lang="deu").lower()

def get_matches(maps, word_text):
    matches = []
    for option in maps:
        if option[0].lower() in word_text:
            matches.append(option[1])
    return matches

def act(matches):
    if matches == []:
        print("Unable to find word.")
        pyautogui.typewrite("?")
        pyautogui.press('enter')
        pyautogui.press('enter')
    else:
        print("Found " + matches[-1] + " as match.")
        pyautogui.typewrite(matches[-1])
        pyautogui.press('enter')
        pyautogui.press('enter')

def main():
    maps = get_maps(format_text(pdf_to_text()))
    input("Press enter when ready: ")
    while True:
        time.sleep(1)
        act(get_matches(maps, get_text()))

if __name__ == "__main__":
    main()
