import re
from modules import *
from core.logs import LOG_ERROR, LOG_INFO
from core.config import conf
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from enum import Enum
from utils.rename import *
from utils.thirdparty.LibConnector import EpisodeReName_get_episode_name

class RSS_Type(Enum):
    SINGLE = 1
    GATHER = 2
    
class RSS_INFO(Enum):
    REFRESH = 'Find New Torrents From'
    FINDRSS = 'Found New Subscription'
    FAILEDRSS = 'Subscription Addition Failure'


class RSS_Helper():
    
    @staticmethod
    def get_title_from_rss_link(link):
        try:
            response = requests.get(link, timeout=10)
            soup = BeautifulSoup(response.content, 'xml')
            title = soup.find('title').text
            title = re.sub(r'^Mikan Project - ', '', title)
            return title
        except Exception as e:
                LOG_ERROR(e)
                
    @staticmethod
    def get_subject_id_from_rss_link(link):
        try:
            response = requests.get(link, timeout=10)
            soup = BeautifulSoup(response.content, 'xml')
            title = soup.find('link').text
            return title
        except Exception as e:
                LOG_ERROR(e)
                
    @staticmethod
    def get_rss_link_from_torrent_info_page_link(link):
        try:
            response = requests.get(link, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            links_found = soup.find_all('a', href=lambda href: href and "/RSS/Bangumi?bangumiId=" in href)
            for link_found in links_found:
                    full_href = urljoin(link, link_found['href'])
                    return full_href
        except Exception as e:
                LOG_ERROR(e)    
    
    @staticmethod
    def get_title_from_torrent_info_page_link(link):
        try:
            response = requests.get(link, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                p_tag = soup.find('p', class_='bangumi-title')
                result = p_tag.get_text(strip=True)
                return result
        except Exception as e:
                LOG_ERROR(e)
                
                
    @staticmethod
    def Torrents_File_Rename():
        try:
            torrents = None
            while True:
                torrents = QB.qb.torrents_info()
                has_files = False
                for torrent in torrents:
                    torrent_hash = torrent.get("hash")
                    files = QB.get_torrent_file_by_hash(torrent_hash)
                    if files: 
                        has_files = True
                        break
                if has_files:
                    break


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
                QB.add_tag_by_hash(tag='已整理', hash=torrent_hash)

        except Exception as e:
            LOG_ERROR("An error occurred: ", e)
        

class RSS:
    
    config = conf.get_qbittorrent_config()
    rss_config = conf.get_rss_config()
    
    @staticmethod
    def Init():
        try:
            link = RSS.rss_config.get('url')
            if RSS.Add(link,Type=RSS_Type.GATHER):
                LOG_INFO("RSS init Successful")
        except Exception as e:
                LOG_ERROR(e)
    
    """添加订阅
    """   
    @staticmethod
    def Add(link,Type=RSS_Type.GATHER):
        try:
            if Type == RSS_Type.SINGLE:
                if DB.rss_single_is_link_exist(link):
                    return True
                bangumi_title = RSS_Helper.get_title_from_rss_link(link)
                season, title = split_season_title(bangumi_title)
                if not all([link,title,season,bangumi_title]):
                    LOG_ERROR(f"{RSS_INFO.FAILEDRSS.value}{link}")
                    return None
                item = (link,title,season,bangumi_title)
                DB.rss_single_insert(item)
                ## 初始化剧集信息
                Bangumi.Init_Episodes_Information_By_RSS_Link(bangumi_title,link)
                
            elif Type == RSS_Type.GATHER:
                if DB.rss_gather_is_link_exist(link):
                    return True
                DB.rss_gather_insert(link)
                
            return True
                
        except Exception as e:
                LOG_ERROR(e)
                
        """根据ID删除订阅
        """                
    def Delete(Type, id):
        if Type == RSS_Type.SINGLE:
            try:
                DB.bangumi_delete_by_rss_single_id(id)
                DB.download_status_delete_by_rss_single_id(id)
                DB.rss_single_delete_by_id(id)
                return True
            except Exception as e:
                LOG_ERROR(e)
                return False
        elif Type == RSS_Type.GATHER:
            if DB.rss_gather_delete_by_id(id):
                return True
        else:
            raise ValueError("Invalid RSS Type")
        
        """将给定订阅的内容推送到下载器
        """        
    def Collect(url):
        try:
            Items = Parse.Mikan(url)
            if Items is  None:
                return False
            for Item in Items:
                link = Item['link']
                bangumi_name = RSS_Helper.get_title_from_torrent_info_page_link(link)
                season, title = split_season_title(bangumi_name)
                if not all([link, title, season]):
                    LOG_ERROR(f"{RSS_INFO.FAILEDRSS.value} {link}")
                    return
                root_folder = RSS.config.get('root_folder')
                Path = os.path.join(root_folder, title, season)
                if RSS.Push_torrent_file_to_downloader(Item,Path) == True:
                    if conf.Telegram:
                        TGBOT.Send_Message(f"【番剧更新】\n{bangumi_name}  更新了。")   
                        
            return True
        except Exception as e:
            LOG_ERROR("RSS Collect",e)
            
        """订阅刷新
        """            
    def Refresh():
        try:
            gather_links = DB.rss_gather_get_all()
            for gather_link in gather_links:
                Items = Parse.Mikan(gather_link[1])
                if Items is None:
                    continue
                for Item in Items:
                    if DB.rss_items_is_link_exist_and_pushed(Item['link']):
                        continue;
                    link = RSS_Helper.get_rss_link_from_torrent_info_page_link(Item['link'])
                    if DB.rss_single_is_link_exist(link):
                        continue;
                    bangumi_title = RSS_Helper.get_title_from_torrent_info_page_link(Item['link'])
                    season, title = split_season_title(bangumi_title)
                    if not all([link,title,season,bangumi_title]):
                        LOG_ERROR(f"{RSS_INFO.FAILEDRSS.value} {Item['link']}")
                        continue;
                    item = (link,title,season,bangumi_title)
                    LOG_INFO(f'{RSS_INFO.FINDRSS.value} {bangumi_title}')
                    DB.rss_single_insert(item)
                    Bangumi.Init_Episodes_Information_By_RSS_Link(bangumi_title,link)
                    
            single_links = DB.rss_single_get_all()
            for single_link in single_links:
                LOG_INFO(f'{RSS_INFO.REFRESH.value} {single_link[4]}')
                link = single_link[1]
                Items = Parse.Mikan(link)
                if Items is not None:
                    Id = single_link[0]
                    for Item in Items:
                        DB.rss_items_insert(Item,Id)
        except Exception as e:
                LOG_ERROR(e)
                      
        """推送新种子到下载器
        """                    
    def Push():
        items = DB.rss_items_get_new()
        for item in items:
            Id = item['id']
            Info = DB.rss_single_get_by_rss_single_id(Id)
            bangumi_name = Info[4]
            root_folder = RSS.config.get('root_folder')
            if conf.get_rss_config().get('scrape') == 'TMDB':
                Path = os.path.join(root_folder, Info[2], Info[3])
            elif conf.get_rss_config().get('scrape') == 'Bangumi':
                Path = os.path.join(root_folder, Info[4], 'Season 1')
            if RSS.Push_torrent_file_to_downloader(item,Path) == True:
                DB.rss_items_set_pushed_to_downloader_by_title(item['title'])
                if conf.Telegram:
                    TGBOT.Send_Message(f"【番剧更新提醒】\n{bangumi_name}  更新了。")
                RSS_Helper.Torrents_File_Rename()       

        """查找新的单一订阅
        """    
    def Refresh_Get_New_Single():
        LOG_INFO(RSS_INFO.FINDRSS.value)
        gather_links = DB.rss_gather_get_all()
        for gather_link in gather_links:
            Items = Parse.Mikan(gather_link[1])
            for Item in Items:
                itemlink = Item['link']
                LOG_INFO(f'{RSS_INFO.FINDRSS.value} {itemlink}')
                link = RSS_Helper.get_rss_link_from_torrent_info_page_link(Item['link'])
                bangumi_title = RSS_Helper.get_title_from_torrent_info_page_link(Item['link'])
                season, title = split_season_title(bangumi_title)
                if not all([link,title,season,bangumi_title]):
                    LOG_ERROR(f"{RSS_INFO.FAILEDRSS.value} {Item['link']}")
                    continue;
                item = (link,title,season,bangumi_title)
                DB.rss_single_insert(item)
                
        """进行单一订阅RSS刷新
        """                
    def Refresh_From_All_Single():
        LOG_INFO(RSS_INFO.REFRESH.value)
        single_links = DB.rss_single_get_all()
        for single_link in single_links:
            LOG_INFO(f'{RSS_INFO.REFRESH.value} {single_link}')
            link = single_link[1]
            Items = Parse.Mikan(link)
            Id = single_link[0]
            for Item in Items:
                DB.rss_items_insert(Item,Id)
                
                
    def Push_torrent_file_to_downloader(item,path):
        torrent_data = QB.download_torrent_file(item["torrent_url"])
        if torrent_data:
            return QB.add_torrent_file(item['title'],torrent_data, path)
