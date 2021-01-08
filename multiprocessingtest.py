import multiprocessing as mp
import queue
import time


def function(data, ret):
    # l.acquire()
    time.sleep(1)
    print(data[1] + ".png")
    ret.put((data[0], data[1]+ ".png"))
    # l.release()


if __name__ == '__main__':
    # lock = mp.Lock()
    core_count = mp.cpu_count()
    print(core_count)
    fileList = ["One", "Two", "Three", "Four", "Five"]
    workQueue = queue.Queue(10)
    results = mp.Queue()
    processes = []
    orderID = 0

    start = time.perf_counter()


    for file in fileList:
        workQueue.put((orderID, file))
        orderID += 1

    while not workQueue.empty():
        data = workQueue.get()
        p = mp.Process(target=function, args=(data,results))
        p.start()
        processes.append(p)

    for p in processes:
        p.join()

    content = []

    while not results.empty():
        value = results.get()
        content.insert(value[0], value[1])

    end = time.perf_counter()

    print(f"Finished in {end-start} second(s)")

    print("Done")
