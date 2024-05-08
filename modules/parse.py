import requests
import xml.etree.ElementTree as ET
from core.logs import LOG_ERROR


class Parse:
    def Mikan(rss_url):
        try:
            response = requests.get(rss_url, timeout=30)
            if response.status_code == 200:
                item_data = []
                rss_content = response.content.decode("utf-8")
                xml_tree = ET.fromstring(rss_content)
                items = xml_tree.findall(".//item")
                for item in items:
                    title = item.find("title").text
                    link = item.find("link").text
                    enclosure = item.find(".//enclosure")
                    torrent_url = enclosure.get("url")
                    item_data.append(
                        {"title": title, "link": link, "torrent_url": torrent_url}
                    )
                return item_data
        except Exception as e:
            LOG_ERROR(e)
            return None
