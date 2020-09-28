# Author: Darryl Xian

import pyautogui
from cv2 import cv2
import win32gui, win32ui, win32con
import os
import time
import numpy as np

def im_show(img):
    cv2.imshow('', img)
    if cv2.waitKey(0) == 115:
        cv2.imwrite(input('filename: '), img)
    cv2.destroyAllWindows()

digit_templates = []
for i in range(10):
    digit_templates.append(cv2.imread(f'digits/{i}.png', 0))
def digit_ocr(img):
    distances = []
    for template in digit_templates:
        distances.append(cv2.matchTemplate(img, cv2.resize(template, (img.shape[1], img.shape[0])), cv2.TM_SQDIFF_NORMED)[0][0])
    return distances.index(min(distances))

count_templates = []
for i in [9, 11, 12]:
    count_templates.append(cv2.imread(f'counts/{i}.png'))
int2char = ['□', '♥', '?']
def count_ocr_Xian(img, pixel_size):
    ''' Xian's method: Use the template matching function (stable for every, but slow) '''
    distances = []
    for template in count_templates:
        distances.append(cv2.matchTemplate(img, cv2.resize(template, (pixel_size, pixel_size)), cv2.TM_SQDIFF_NORMED)[0][0])    
    return int2char[distances.index(min(distances))]

def count_ocr_Li(img, pixel_size):
    ''' Li's method: Some pixel's RGB features (only stable for number and mine)'''
    left_top = img[0, 1, :]
    middle = img[pixel_size // 2, pixel_size // 2 + 1, :]
    if sum(left_top) < 190 * 3:
        if 180 < middle[0] and middle[0] < 200 and 180 < middle[1] and middle[1] < 200 and 180 < middle[2] and middle[2] < 200:
            return '0'
        if 240 < middle[0] and middle[1] < 20 and middle[2] < 20:
            return '1'
        if middle[0] < 20 and 120 < middle[1] and middle[1] < 140 and middle[2] < 20:
            return '2'
        if middle[0] < 20 and middle[1] < 20 and 240 < middle[2]:
            return '3'
        if 120 < middle[0] and middle[0] < 140 and middle[1] < 20 and middle[2] < 20:
            return '4'
        if middle[0] < 20 and middle[1] < 20 and 120 < middle[2] and middle[2] < 140:
            return '5'
        if 120 < middle[0] and middle[0] < 140 and 120 < middle[1] and middle[1] < 140 and middle[2] < 20:
            return '6'
        if 60 < middle[0] and middle[0] < 80 and 60 < middle[1] and middle[1] < 80 and 60 < middle[2] and middle[2] < 80:
            return '7'
        if 120 < middle[0] and middle[0] < 140 and 120 < middle[1] and middle[1] < 140 and 120 < middle[2] and middle[2] < 140:
            return '8'
        else:
            return '■'
    return False

def count_ocr(img, pixel_size):
    if count_ocr_Li(img, pixel_size):
        return count_ocr_Li(img, pixel_size)
    return count_ocr_Xian(img, pixel_size)

class miner:
    def __init__(self):
        if not win32gui.FindWindow(None, '扫雷'):
            print('Please open your winmine!')
            exit(1)
        else:
            self.handle = win32gui.FindWindow(None, '扫雷')

        win32gui.SetForegroundWindow(self.handle)
        height_0, width_0 = self.location[3] - self.location[1], self.location[2] - self.location[0]
        pyautogui.press(['alt', 'g', 'c', 'tab', 'tab', '2', '3', 'tab', '3', '0', 'enter'])
        height_1 = self.location[3] - self.location[1]
        pyautogui.press(['alt', 'g', 'c', 'tab', 'tab', '2', '4', 'enter'])
        height_2 = self.location[3] - self.location[1]
        self.pixel_size = height_2 - height_1
        self.height = height_0 // self.pixel_size - 7
        self.width = width_0 // self.pixel_size - 1
        
        height_keys = [str(self.height // 10), str(self.height % 10)] if self.height >= 10 else [str(self.height)]
        width_keys = [str(self.width // 10), str(self.width % 10)] if self.width >= 10 else [str(self.width)]
        pyautogui.press(['alt', 'g', 'c', 'tab', 'tab'] + height_keys + ['tab'] + width_keys + ['enter'])
        self.n_of_mine = self.mine_remain

        if (self.height, self.width, self.n_of_mine) == (9, 9, 10):
            pyautogui.press(['alt', 'g', 'b'])
        elif (self.height, self.width, self.n_of_mine) == (16, 16, 40):
            pyautogui.press(['alt', 'g', 'i'])
        elif (self.height, self.width, self.n_of_mine) == (16, 30, 99):
            pyautogui.press(['alt', 'g', 'e'])
    
    def click_at(self, i, j, button='left'):
        pyautogui.click(self.location[0] + (30 + j * 20)  * self.pixel_size // 20, self.location[1] + (138 + i * 20) * self.pixel_size // 20, button=button)
    
    def build_dataset(self, i=-1, j=-1):
        if i == -1:
            i = int(input('i = '))
        if j == -1:
            j = int(input('j = '))
        im_show(self.get_pixel(i, j))
    
    def look(self):
        win32gui.SetForegroundWindow(self.handle)
        left, top, right, bottom = self.location
        pyautogui.screenshot('sight.png', region=[left, top, right - left, bottom - top])
        self.sight = cv2.imread('sight.png')

    @property
    def location(self):
        return win32gui.GetWindowRect(self.handle)
    
    @property
    def mine_remain(self):
        self.look()
        digit_1 = self.sight[78 * self.pixel_size // 20: 106 * self.pixel_size // 20, 26 * self.pixel_size // 20: 41 * self.pixel_size // 20, 2]
        digit_2 = self.sight[78 * self.pixel_size // 20: 106 * self.pixel_size // 20, 42 * self.pixel_size // 20: 57 * self.pixel_size // 20, 2]
        digit_3 = self.sight[78 * self.pixel_size // 20: 106 * self.pixel_size // 20, 59 * self.pixel_size // 20: 74 * self.pixel_size // 20, 2]
        _, th_1 = cv2.threshold(digit_1, 140, 255, cv2.THRESH_BINARY)
        _, th_2 = cv2.threshold(digit_2, 140, 255, cv2.THRESH_BINARY)
        _, th_3 = cv2.threshold(digit_3, 140, 255, cv2.THRESH_BINARY)
        return digit_ocr(th_1) * 100 + digit_ocr(th_2) * 10 + digit_ocr(th_3)
    
    def get_pixel(self, i, j):
        return self.sight[(127 + i * 20) * self.pixel_size // 20: (147 + i * 20) * self.pixel_size // 20, (19 + j * 20) * self.pixel_size // 20: (39 + j * 20) * self.pixel_size // 20, :]
    
    @property
    def player_map(self):
        self.look()
        lines = [[' '] * (self.width + 2)]
        for i in range(self.height):
            rows = [' ']
            for j in range(self.width):
                rows.append(count_ocr(self.get_pixel(i, j), self.pixel_size))
            rows.append(' ')
            lines.append(rows)
        lines.append([' '] * (self.width + 2))
        return np.matrix(lines)
    
    @property
    def win(self):
        return self.mine_remain == 0 and '□' not in self.player_map and '■' not in self.player_map
    
    @property
    def lose(self):
        return '■' in self.player_map
    
    def slower(self):
        pyautogui.PAUSE = 0.1
    
    def faster(self):
        pyautogui.PAUSE = 1e-4
    
    def press(self, keys):
        pyautogui.press(keys)

def test():
    Darryl = miner()
    while True:
        Darryl.look()
        print(count_ocr(Darryl.get_pixel(0, 0), Darryl.pixel_size))
        exit()

if __name__ == '__main__':
    # main()
    test()
