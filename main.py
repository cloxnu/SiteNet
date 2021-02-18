import pickle
from net import *
from info import *
info = read_info()


def run():
    n = init()
    try:
        n.search(info.get('search_num'))
        n.draw()
    finally:
        save(n)
    print('\nBye~~')


def save(n):
    file_path = 'res/{}'.format(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
    with open(file_path, 'wb') as f:
        pickle.dump(n, f)
    print('data saved at {}'.format(file_path))


def init():
    load_file = info.get('load_file')
    if not load_file:
        return net(info.get('url'))
    with open(load_file, 'rb') as f:
        return pickle.load(f)


if __name__ == '__main__':
    run()
