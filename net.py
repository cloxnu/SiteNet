import os
from bs4 import BeautifulSoup
from urllib import request, error
from urllib.parse import urljoin, urldefrag, urlsplit
import networkx as nx
import time
import re
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
            print("\rsearching {} / {}, search times: {}".format(i, search_num, self.search_times), end="")
            url, current_url = self.search_queue[0]
            url = urljoin(current_url, urldefrag(url)[0])
            if self.is_url_valid(url, info.get('url_filter')):
                print(", url: {}".format(url))
                next_site = site(url)
                self.search_queue += [(one_url, url) for one_url in next_site.links]
                current_site = self.all_sites.get(current_url)
                current_site.links_to.append(next_site)
                self.add_edge(current_url, current_site.name, url, next_site.name)
                self.all_sites[url] = next_site
            i += 1
            self.search_times += 1
            self.search_queue.pop(0)

    def is_url_valid(self, url, url_filter):
        if url in self.all_sites:
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
        res_path = os.path.join(output_dir if output_dir else 'res', '{}.png'.format(time.strftime('%Y-%m-%d-%H:%M:%S', time.localtime(time.time()))))
        os.makedirs(os.path.dirname(res_path), exist_ok=True)
        plt.annotate('searched {} {} times'.format(self.root.url, self.search_times), xy=(1, 0), xycoords='axes fraction', ha='right', va='bottom', fontsize=24)
        plt.savefig(res_path)
        print('\nresult saved at {}'.format(res_path))
        plt.show()


class site:
    def __init__(self, url):
        self.url = url
        try:
            with request.urlopen(url) as response:
                html = response.read().decode(response.headers.get_content_charset())
        except KeyboardInterrupt:
            raise KeyboardInterrupt
        except:
            print("request error")
            html = "error"
        soup = BeautifulSoup(html, 'html.parser')
        self.name, self.links = site.get_site_info(soup)
        self.links_to = []

    def __repr__(self):
        return self.url

    @staticmethod
    def get_site_info(soup: BeautifulSoup):
        name = soup.title.text if soup.title else "x"
        if info.get('site_settings'):
            if info.get('site_settings')['title_regex']:
                title_res = re.findall(info.get('site_settings')['title_regex'], name)
                if len(title_res) > 0:
                    name = title_res[0]
        links = []
        for a in soup.find_all('a'):
            links.append(a.get('href'))
        return name, links
