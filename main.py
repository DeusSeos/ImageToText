import pytesseract
from PIL import Image
import os
import time
import re



def converter(image) -> str:
    return pytesseract.image_to_string(image)


start_time = time.time()

pattern = re.compile(".+.png")

pytesseract.pytesseract.tesseract_cmd = (r'C:\Program Files\Tesseract-OCR\tesseract')

path_screenshot = r'C:\Users\mille\PycharmProjects\ImageToText\Screenshots'

files = os.listdir(path_screenshot)
result = ''
fScreenshot = []

for afile in files:
    if pattern.match(afile):
        filePath = path_screenshot +'\\' + afile
        img = Image.open(filePath)
        result += converter(img)
        fScreenshot.append(filePath)

with open(r' .txt', mode='a') as file:
    file.write(result)


fLindex = result.index('\n')

line = result[:fLindex]

line = line.strip()
line = line.replace('\n', '')
line = line.replace(':', '')


path_project = r'C:\Users\mille\PycharmProjects\ImageToText'
os.rename(file.name, path_project + '\\' + line + '.txt')

for f in fScreenshot:
    os.remove(f)

end_time = time.time()

print(f'{end_time-start_time}')


