import multiprocessing
import time


def worker(num):
    print(f'Start working thread {num}')
    time.sleep(3)
    print(f'End working thread {num}')


if __name__ == '__main__':
    processes = []
    for i in range(5):
        p = multiprocessing.Process(target=worker, args=(i,))
        processes.append(p)

    for p in processes:
        p.start()
        p.join()

    print('All threads finish work')