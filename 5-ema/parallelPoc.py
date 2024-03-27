import threading
import queue as Queue

def main():
    c1 = Queue.Queue(maxsize=0)
    c2 = Queue.Queue(maxsize=0)
    quit = Queue.Queue(maxsize=0)

    def func1():
        for i in range(10):
            c1.put(i)
        quit.put(0)

    threading.Thread(target=func1).start()

    def func2():
        for i in range(2):
            c2.put(i)

    threading.Thread(target=func2).start()

    combined = Queue.Queue(maxsize=0)

    def listen_and_forward(queue):
        while True:
            combined.put((queue, queue.get()))

    t1 = threading.Thread(target=listen_and_forward, args=(c1,))
    t1.daemon = True

    t2 = threading.Thread(target=listen_and_forward, args=(c2,))
    t2.daemon = True
    # t3 = threading.Thread(target=listen_and_forward, args=(quit,))
    # t3.daemon = True
    t2.start()
    t1.start()
    t2.join()
    t1.join()
    # t3.start()

    while True:
        which, message = combined.get()
        if which is c1:
            print ('Received value from c1')
        elif which is c2:
            print ('Received value from c2')
        elif which is quit:
            print ('Received value from quit')
            return
main()