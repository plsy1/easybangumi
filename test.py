from modules.qbittorrent import QB
from core.config import conf




torrents = QB.qb.torrents_info()
for torrent in torrents:
    tags = torrent.get('tags')
    tags = tags.split(', ')
    if conf.config['qbittorrent']['tag'] not in tags: continue
    torrent_hash = torrent.get("hash")
    QB.add_tag_by_hash(tag='已整理', hash = torrent_hash)
