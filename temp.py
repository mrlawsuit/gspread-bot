import time


def func():
    for i in range(100):
        print(i)
        time.sleep(10)

if __name__ == '__main__':
    func()