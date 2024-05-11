import schedule
import time
from core.config import conf
from modules import *
from core.rss import *
from core.logs import *
from utils.thirdparty.LibConnector import EpisodeReName_get_episode_name
import threading


class Scheduler:

    
    
    def run_scheduler():
        scheduler_thread = threading.Thread(target=Scheduler.Run, daemon=True)
        scheduler_thread.start()


    @staticmethod
    def Run():
        LOG_INFO('Scheduler Start Successful')
        schedule.every(15).seconds.do(Scheduler.Rename)
        schedule.every(10).minutes.do(Scheduler.Refresh)
        schedule.every(720).minutes.do(Scheduler.Update_Bangumi_Info)
        while True:
            schedule.run_pending()
            time.sleep(1)

    @staticmethod
    def Rename():
        try:
            torrents = QB.qb.torrents_info()
            for torrent in torrents:
                tags = torrent.get('tags')
                tags = tags.split(', ')
                if conf.config['qbittorrent']['tag'] not in tags: continue
                if '已整理' in tags: continue
                torrent_hash = torrent.get("hash")
                save_path = torrent.get("save_path")
                files = QB.get_torrent_file_by_hash(torrent_hash)
                for file in files:
                    old_path = file.get("name")
                    if old_path:
                        full_path = os.path.join(save_path, old_path)
                        new_path = EpisodeReName_get_episode_name(full_path)
                        if new_path:
                            QB.qb.torrents.rename_file(
                                torrent_hash=torrent_hash,
                                new_path=new_path,
                                old_path=old_path,
                            )
                        else:
                            LOG_ERROR(f"Rename failed: {old_path}")
                    else:
                        LOG_ERROR(
                            "File name not found for torrent hash: ", torrent_hash
                        )
                QB.add_tag_by_hash(tag='已整理', hash = torrent_hash)

        except Exception as e:
            LOG_ERROR("An error occurred: ", e)

    @staticmethod
    def Refresh():
        RSS.Refresh()
        RSS.Push()

    @staticmethod
    def Update_Bangumi_Info():
        LOG_INFO('Start Refresh Bangumi Episodes Information......')
        Bangumi.Refresh_Episodes_Information()