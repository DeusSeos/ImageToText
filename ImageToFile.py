
from PIL import Image
import queue
import threading
import pytesseract
import os
import time
import re

exitFlag = 0

class myThread(threading.Thread):

    def __init__(self, threadID, name, q):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.q = q

    def run(self):
        print("Starting " + self.name)
        process_data(self.name, self.q)
        print("Exiting " + self.name)


def process_data(threadName, q):
    while not exitFlag:
        queueLock.acquire()
        if not workQueue.empty():
            data = q.get()
            converter(data)
            print(f"{threadName} processing {data}")
            queueLock.release()
            return
        else:
            queueLock.release()
        time.sleep(1)


def converter(fileName):
    img = Image.open(fileName)
    pytesseract.pytesseract.image_to_string(img)


start_time = time.time()

pattern = re.compile(".+.png")
pytesseract.pytesseract.tesseract_cmd = (r'C:\Program Files\Tesseract-OCR\tesseract')
path_screenshot = r'C:\Users\mille\PycharmProjects\ImageToText\Screenshots'
files = os.listdir(path_screenshot)
result = ''


threadList = ['Thread-1', 'Thread-2', 'Thread-3', 'Thread-4'] #TODO adjust thread activation dynamically based on number of screenshots
fileList = []
queueLock = threading.Lock()
workQueue = queue.Queue(10)
threads = []
threadID = 1

for afile in files:
    if pattern.match(afile):
        # if correct file type then send into queue
        fileList.append(path_screenshot +'\\' + afile)

for tName in threadList:
    thread = myThread(threadID, tName, workQueue)
    thread.start()
    threads.append(thread)
    threadID += 1

# Fill the queue
queueLock.acquire()
for fileName in fileList:
    workQueue.put(fileName)
queueLock.release()

# Wait for queue to empty
while not workQueue.empty():
    pass

# Notify threads it's time to exit
exitFlag = 1

# Wait for all threads to complete
for t in threads:
    t.join()

print("Exiting Main Thread")
#
#
# with open(r' .txt', mode='a') as file:
#     file.write(result)
#
#
# fLindex = result.index('\n')
#
# line = result[:fLindex]
#
# line = line.strip()
# line = line.replace('\n', '')
# line = line.replace(':', '')
#
#
# path_project = r'C:\Users\mille\PycharmProjects\ImageToText'
# os.rename(file.name, path_project + '\\' + line + '.txt')
#
end_time = time.time()

print(f'{end_time-start_time}')