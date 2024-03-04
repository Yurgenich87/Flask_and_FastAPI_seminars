import time


def slow_function():
    print('Start f')
    time.sleep(5)
    print('End f')


print('Start p')
slow_function()
print('End p')
