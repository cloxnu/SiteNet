from net import *
from info import *
info = read_info()


def run():
    start_url = info.get('url')
    print("search will start at {}".format(start_url))
    n = net(start_url)
    n.search(info.get('search_num'))
    n.draw()


if __name__ == '__main__':
    run()
