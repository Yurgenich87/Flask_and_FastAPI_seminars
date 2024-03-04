import threading

counter = 0


def increment():
    global counter
    for _ in range(250_000):
        counter += 1
    print(f'Value counter: {counter:_}')


threads = []
for i in range(4):
    t = threading.Thread(target=increment)
    threads.append(t)
    t.start()

for t in threads:
    t.join()

print(f'Value counter from finish: {counter:_}')
