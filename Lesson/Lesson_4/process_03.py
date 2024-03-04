import multiprocessing

counter = 0


def increment():
    global counter
    for _ in range(10_000):
        counter += 1
    print(f'Value counter: {counter:_}')


if __name__ == '__main__':
    for i in range(4):
        processes = []
        p = multiprocessing.Process(target=increment)
        processes.append(p)
        p.start()

    for p in processes:
        p.join()

    print(f'Value counter from finish: {counter:_}')
