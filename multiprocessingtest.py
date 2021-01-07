import multiprocessing as mp
import queue

def function(l, fileName):
    l.acquire()
    print(fileName + ".png")
    l.release()


if __name__ == '__main__':
    lock = mp.Lock()
    core_count = mp.cpu_count()
    print(core_count)
    fileList = ["One", "Two", "Three", "Four", "Five"]
    workQueue = queue.Queue(10)
    processes = []
    values = []

    for file in fileList:
        workQueue.put(file)

    while not workQueue.empty():
        data = workQueue.get()
        p = mp.Process(target=function, args=(lock, data))
        p.start()
        processes.append(p)

    for p in processes:
        p.join()

    for v in values:
        print(v.value)

    print("Done")
