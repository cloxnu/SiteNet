from bs4 import BeautifulSoup
from urllib import request, error
import re

from info import *
info = read_info()


class site:
    def __init__(self, url):
        self.url = url
        try:
            headers = {'User-Agent': info.get('user_agent')}
            req = request.Request(url, headers=headers)
            with request.urlopen(req, timeout=info.get('timeout')) as response:
                content_type = response.headers.get_content_charset()
                html = response.read().decode(content_type) if content_type else response.read().decode()
        except KeyboardInterrupt:
            raise KeyboardInterrupt
        except error.HTTPError as err:
            print("Request HTTPError: {}".format(err))
            html = "HTTPError"
        except error.URLError as err:
            print("Request URLError: {}".format(err))
            html = "URLError"
        except TypeError as err:
            print("TypeError: {}".format(err))
            html = "TypeError"
        except:
            print("An unknown error happened")
            html = 'error'
        soup = BeautifulSoup(html, 'html.parser')
        self.name, self.links = site.get_site_info(soup)
        self.links_to = {}

    def __repr__(self):
        return self.url

    @staticmethod
    def get_site_info(soup: BeautifulSoup):
        name = soup.title.text.strip() if soup.title else "x"
        if info.get('site_settings'):
            if info.get('site_settings')['title_regex']:
                title_res = re.findall(info.get('site_settings')['title_regex'], name)
                if len(title_res) > 0:
                    name = title_res[0].strip()
        links = []
        for a in soup.find_all('a'):
            links.append(a.get('href'))
        return name, links
