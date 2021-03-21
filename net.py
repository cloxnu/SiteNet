import os
from urllib.parse import urljoin, urldefrag, urlsplit
import networkx as nx
import time
from sites import *
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimSun']
plt.rcParams['axes.unicode_minus'] = False
from info import *
info = read_info()

import ssl
ssl._create_default_https_context = ssl._create_unverified_context


class net:
    def __init__(self, url):
        url = urldefrag(url)[0]
        self.root = site(url)
        self.all_sites = {url: self.root}
        self.search_times = 0
        self.search_queue = [(one_url, url) for one_url in self.root.links]
        self.graph = nx.DiGraph()

    def search(self, search_num=100):
        i = 1
        while self.search_queue and i <= search_num:
            print("searching {} / {}, search times: {}".format(i, search_num, self.search_times))
            url, current_url = self.search_queue[0]
            url = urljoin(current_url, urldefrag(url)[0])
            current_site = self.all_sites.get(current_url)
            if self.is_url_valid(current_site, url, info.get('url_filter')):
                print("url: {}".format(url))
                if url in self.all_sites:
                    next_site = self.all_sites[url]
                else:
                    next_site = site(url)
                    self.search_queue += [(one_url, url) for one_url in next_site.links]
                current_site.links_to[url] = next_site
                self.add_edge(current_url, current_site.name, url, next_site.name)
                self.all_sites[url] = next_site
            i += 1
            self.search_times += 1
            self.search_queue.pop(0)

    @staticmethod
    def is_url_valid(current_site, url, url_filter):
        if url in current_site.links_to:
            return False
        if url_filter:
            if url_filter['url_regex'] and not re.search(url_filter['url_regex'], url):
                return False
            if url_filter['netloc_regex'] and not re.search(url_filter['netloc_regex'], urlsplit(url)[1]):
                return False
            if url_filter['path_regex'] and not re.search(url_filter['path_regex'], urlsplit(url)[2]):
                return False

        return True

    def add_edge(self, u, u_name, v, v_name):
        self.graph.add_nodes_from([(u, {'name': u_name}), (v, {'name': v_name})])
        self.graph.add_edge(u, v)

    def draw(self, output_dir, output_image_size):
        plt.figure(figsize=(output_image_size, output_image_size))
        nx.draw(self.graph, node_size=500, node_color="#fff", font_color="#000", font_size=18, node_shape="s", edge_color="b", width=3, font_weight="bold", with_labels=True, labels=nx.get_node_attributes(self.graph, 'name'))
        res_path = os.path.join(output_dir if output_dir else 'res', '{}.png'.format(time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time.time()))))
        os.makedirs(os.path.dirname(res_path), exist_ok=True)
        plt.annotate('searched {} {} times'.format(self.root.url, self.search_times), xy=(1, 0), xycoords='axes fraction', ha='right', va='bottom', fontsize=24)
        plt.savefig(res_path)
        print('\nresult saved at {}'.format(res_path))
        plt.show()

    def output(self, output_dir):
        def recur(current_site: site, depth: int):
            nonlocal res, visited
            if current_site.url in visited:
                return
            for i in range(depth):
                res += "  "
            res += "- {} || {}\n".format(current_site.name, current_site.url)
            visited.add(current_site.url)
            for next_site in current_site.links_to.values():
                recur(next_site, depth + 1)

        res_path = os.path.join(output_dir if output_dir else 'res', '{}.md'.format(time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time.time()))))
        os.makedirs(os.path.dirname(res_path), exist_ok=True)
        res, visited = "", set()
        recur(self.root, 0)
        print(res)

        with open(res_path, 'w') as f:
            f.write(res)

