import multiprocessing

counter = multiprocessing.Value('i', 0)


def increment(cnt):
    for _ in range(10_000):
        with cnt.get_lock():
            cnt.value += 1
    print(f'Value counter: {cnt.value:_}')


if __name__ == '__main__':
    for i in range(5):
        processes = []
        p = multiprocessing.Process(target=increment, args=(counter,))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()

    print(f'Value counter from finish: {counter.value:_}')
