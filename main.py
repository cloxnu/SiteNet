import pickle
import os
from net import *
from info import *
info = read_info()


def run():
    n = init()
    try:
        n.search(info.get('search_num'))
        n.output(info.get('output_dir'))
        if info.get('is_output_image'):
            n.draw(info.get('output_dir'), info.get('output_image_size'))
    except KeyboardInterrupt:
        print("Interrupt")
    save(n)
    print('\nBye~~')


def save(n):
    output_dir = info.get('output_dir')
    file_path = os.path.join(output_dir if output_dir else 'res', time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time.time())))
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'wb') as f:
        pickle.dump(n, f)
    print('\ndata saved at {}'.format(file_path))


def init():
    load_path = info.get('load_path')
    output_dir = info.get('output_dir')
    os.makedirs(os.path.dirname(os.path.join(output_dir, '')), exist_ok=True)
    if not load_path:
        return net(info.get('url'))
    with open(load_path, 'rb') as f:
        return pickle.load(f)


if __name__ == '__main__':
    run()
