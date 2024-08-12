import requests

from qbittorrentapi import Client
from core.config import conf
from core.logs import LOG_ERROR
from io import BytesIO


class QB:

    qb = Client(
        host=conf.config["qbittorrent"]["host"],
        port=conf.config["qbittorrent"]["port"],
        username=conf.config["qbittorrent"]["username"],
        password=conf.config["qbittorrent"]["password"],
    )

    @staticmethod
    def add_torrent_url(download_link, save_path, tags=conf.config['qbittorrent']['tag']):
        try:
            torrent_options = {
                "urls": download_link,
                "tags": tags,
                "save_path": save_path,
            }
            return QB.qb.torrents_add(**torrent_options) == "Ok."
        except Exception as e:
            LOG_ERROR(f"Error adding torrent: {e}")
            return False

    @staticmethod
    def add_torrent_file(torrent_name, torrent_data, save_path, tags=conf.config['qbittorrent']['tag']):
        try:
            torrent_bytes = torrent_data.getvalue()
            torrent_options = {
                "torrent_files": torrent_bytes,
                "tags": tags,
                "save_path": save_path,
                "rename": torrent_name,
            }
            return QB.qb.torrents_add(**torrent_options) == "Ok."

        except Exception as e:
            LOG_ERROR(f"Error adding torrent: {e}")
            return False

    @staticmethod
    def download_torrent_file(torrent_url):
        try:
            response = requests.get(torrent_url, timeout=10)
            torrent_data = BytesIO(response.content)
            return torrent_data
        except Exception as e:
            LOG_ERROR(f"Error downloading torrent: {e}")
            return None

    @staticmethod
    def get_torrent_file_by_hash(hash):
        return QB.qb.torrents.files(hash)
    
    
    def create_tags(tags):
        QB.qb.torrent_tags.create_tags(tags=tags)
        
        
    def add_tag_by_hash(tag,hash):
        QB.qb.torrent_tags.add_tags(tag,hash)
