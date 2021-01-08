import multiprocessing as mp
import os
import queue
import re
import time
import pytesseract as pt
from PIL import Image


def function(data, ret):
    time.sleep(1)
    # print(data[1] + ".png")
    ret.put((data[0], data[1]+ ".png"))


def converter(data, ret):
    pt.pytesseract.tesseract_cmd = (r'C:\Program Files\Tesseract-OCR\tesseract')
    img = Image.open(data[1])
    res = pt.image_to_string(img)
    ret.put((data[0], res))
    # print(f"Finshed Convert Task for {data[0]}")



if __name__ == '__main__':
    pattern = re.compile(".+.png")
    pt.pytesseract.tesseract_cmd = (r'C:\Program Files\Tesseract-OCR\tesseract')
    path_screenshot = r'C:\Users\mille\PycharmProjects\ImageToText\Screenshots'
    fileList = os.listdir(path_screenshot)

    workQueue = queue.Queue()
    results = mp.Queue(10)
    processes = []
    orderID = 0

    start = time.perf_counter()

    for file in fileList:
        if pattern.match(file):
            filePath = path_screenshot + '\\' + file
            # img = Image.open(filePath)
            workQueue.put((orderID, filePath))
            orderID += 1

    delay = 0

    print(workQueue.qsize())

    #create and start processes
    while not workQueue.empty():
        data = workQueue.get()
        p = mp.Process(target=converter, args=(data,results))
        p.start()
        print(p)
        processes.append(p)


    #join process to main
    for p in processes:
        p.join(timeout=.5)
        print('Joining', p, p.is_alive())

    print("HERE")

    content = []

    while not results.empty():
        value = results.get()
        content.insert(value[0], value[1])

    content = ''.join(content)

    with open(r' .txt', mode='a') as file:
        file.write(content)

    fLindex = content.index('\n')

    line = content[:fLindex]

    line = line.strip()
    line = line.replace('\n', '')
    line = line.replace(':', '')

    path_project = r'C:\Users\mille\PycharmProjects\ImageToText'
    os.rename(file.name, path_project + '\\' + line + '.txt')

    # for f in fileList:
    #     os.remove(f)

    end = time.perf_counter()

    print(f"Finished in {end-start} second(s)")

    print("Done")
