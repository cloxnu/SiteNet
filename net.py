from bs4 import BeautifulSoup
from urllib import request, error
from urllib.parse import urljoin, urldefrag
import networkx as nx
import time
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimSun']
plt.rcParams['axes.unicode_minus'] = False

import ssl
ssl._create_default_https_context = ssl._create_unverified_context


class net:
    def __init__(self, url):
        url = urldefrag(url)[0]
        self.root = site(url)
        self.all_sites = {url: self.root}
        self.search_queue = [(one_url, url) for one_url in self.root.links]
        self.graph = nx.DiGraph()

    def search(self, search_num=100):
        i = 0
        while self.search_queue and i < search_num:
            i += 1
            print("\rsearching {} / {}".format(i, search_num), end="")
            url, current_url = self.search_queue[0]
            url = urljoin(current_url, urldefrag(url)[0])
            if url in self.all_sites:
                self.search_queue.pop(0)
                continue
            next_site = site(url)
            self.search_queue += [(one_url, url) for one_url in next_site.links]
            current_site = self.all_sites.get(current_url)
            current_site.links_to.append(next_site)
            self.add_edge(current_url, current_site.name, url, next_site.name)
            self.all_sites[url] = next_site
            self.search_queue.pop(0)

    def add_edge(self, u, u_name, v, v_name):
        self.graph.add_nodes_from([(u, {'name': u_name}), (v, {'name': v_name})])
        self.graph.add_edge(u, v)

    def draw(self):
        plt.figure(figsize=(50, 50))
        nx.draw(self.graph, node_size=500, node_color="#fff", font_color="#000", font_size=18, node_shape="s", edge_color="b", width=3, font_weight="bold", with_labels=True, labels=nx.get_node_attributes(self.graph, 'name'))
        res_path = 'res/{}.png'.format(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
        plt.savefig(res_path)
        print('result saved at {}'.format(res_path))
        plt.show()


class site:
    def __init__(self, url):
        self.url = url
        print(", url: {}".format(url))
        try:
            with request.urlopen(url) as response:
                html = response.read()
        except:
            html = "error"
        soup = BeautifulSoup(html, 'html.parser')
        self.name, self.links = site.get_site_info(soup)
        self.links_to = []

    def __repr__(self):
        return self.url

    @staticmethod
    def get_site_info(soup: BeautifulSoup):
        name = soup.title.text if soup.title else "x"
        links = []
        for a in soup.find_all('a'):
            links.append(a.get('href'))
        return name, links
