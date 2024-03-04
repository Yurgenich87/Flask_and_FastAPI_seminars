import threading
import time


def worker(num):
    print(f'Start working thread {num}')
    time.sleep(3)
    print(f'End working thread {num}')


threads = []
for i in range(5):
    t = threading.Thread(target=worker, args=(i,))
    threads.append(t)

for t in threads:
    t.start()
    t.join()

print('All threads finish work')
