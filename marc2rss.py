#!/usr/bin/env python3

from urllib.parse import quote
from html.parser import HTMLParser
import sys
from typing import List
from dataclasses import dataclass

@dataclass
class RSSItem:
    title: str = ""
    link: str = ""
    description: str = ""

    def render(self):
        return f"""<item>
        <title>{self.title}</title>
        <link>{self.link}</link>
        <description>{self.description}</description>
      </item>
      """
@dataclass
class RSSFeed:
    title: str
    link: str
    description: str
    items: List[RSSItem] = None
    
    def render(self):
        return f"""
<?xml version="1.0" encoding="UTF-8" ?>
  <rss version="2.0">
    <channel>
      <title>{self.title}</title>
      <link>{self.link}</link>
      <description>{self.description}</description>
      {''.join([item.render() for item in self.items])}
    </channel>
</rss>"""


class MarcParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.list_name = ""
        self.rss = None 
        self.in_item = False
        self.current_item = None

    def handle_starttag(self, tag, attrs):
        if tag == "input" and ("name", "l") in attrs:
            for attr in attrs:
                if attr[0] == "value":
                    self.list_name = attr[1]
            self.rss = RSSFeed(title=self.list_name, description=self.list_name, link=quote(f"https://marc.info?l={self.list_name}"))
        if tag == "a":
            for attr in attrs:
                if attr[0] == "href" and attr[1].startswith(f"?l={self.list_name}&r=1"):
                    self.in_item = True
                    self.current_item = RSSItem(link=quote(f"https://marc.info{attr[1]}"))

    def handle_endtag(self, tag):
        if self.in_item and tag == "a":
            if not self.rss.items:
                self.rss.items = []
            self.rss.items += [self.current_item]
            self.current_item = None
            self.in_item = False

    def handle_data(self, data):
        if self.in_item:
            self.current_item.title = data
            self.current_item.description = data

if __name__ == "__main__":
    content = sys.stdin.read()
    parser = MarcParser()
    parser.feed(content)
    print(parser.rss.render())
