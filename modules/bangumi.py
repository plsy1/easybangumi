import requests
import json
import os, time
from core.logs import LOG_INFO, LOG_ERROR
from core.config import conf

from enum import Enum
from utils.rename import *
from urllib.parse import quote
from modules.database import DB

class CollectionType(Enum):
    WISH = 1
    WATCHED = 2
    WATCHING = 3
    SHELVED = 4
    ABANDONED = 5
    
class EpisodeCollectionType(Enum):
    NOTCOLLECTED = 0
    WISH = 1
    WATCHED = 2
    ABANDONED = 3



class Bangumi_Helper:
    
    token, enable = None, False
    bangumi_config = conf.get_bangumi_config()
    if bangumi_config:
        token = bangumi_config['token']
    if token is not None:
        enable = True
        
    baseurl = 'https://api.bgm.tv/'
    headers = {
        'accept': 'application/json',
        'User-Agent': 'plsy1/easybangumi (https://github.com/plsy1/easybangumi)'
    }

    @staticmethod
    def Get_SubjectID_By_Name(name):
        try:
            name = name.replace(' ', '') 
            encoded_name = quote(name)
            link = Bangumi_Helper.baseurl + f'search/subject/{encoded_name}?type=2&responseGroup=small'
            response = requests.get(link, headers=Bangumi_Helper.headers,timeout=30)
            if response.status_code == 200:
                data = response.json()
                if data.get('list'):
                    first_result = data['list'][0]
                    subject_id = first_result.get('id')
                    return subject_id
            return None
        except Exception as e:
            return None
        
    @staticmethod
    def Get_Total_Episodes_By_SubjectID(subject_id):
        try:
            url = f'{Bangumi_Helper.baseurl}v0/subjects/{subject_id}'
            response = requests.get(url, headers=Bangumi_Helper.headers,timeout=30)
            if response.status_code == 200:
                json_data = response.json()
                total = json_data['eps']
                return total
            else:
                return None
        except Exception as e:
            return None
        
    @staticmethod
    def Get_Subject_Image_Url_By_SubjectID(subject_id):
        try:
            url = f'{Bangumi_Helper.baseurl}v0/subjects/{subject_id}'
            response = requests.get(url, headers=Bangumi_Helper.headers,timeout=30)
            if response.status_code == 200:
                json_data = response.json()
                img_url = json_data['images']['large']
                return img_url
            else:
                return None
        except Exception as e:
            return None
                
    @staticmethod
    def Get_Episodes_By_SubjectID(subject_id):
        try:
            url = f'{Bangumi_Helper.baseurl}v0/episodes?subject_id={subject_id}&limit=100&offset=0'
            response = requests.get(url, headers=Bangumi_Helper.headers,timeout=30)
            if response.status_code == 200:
                data = response.json()
                episodes_dict = {}
                for episode in data['data']:
                    if episode['name']:
                        episodes_dict[episode['sort']] = episode['id']
                return episodes_dict
            else:
                return None
        except Exception as e:
            return None
        
        
        
    @staticmethod
    def Set_Episode_Status_By_Id(episode_id,type: EpisodeCollectionType):
        url = f"https://api.bgm.tv/v0/users/-/collections/-/episodes/{episode_id}"
        headers = {
            "accept": "*/*",
            'User-Agent': 'plsy1/easybangumi (https://github.com/plsy1/easybangumi)',
            "Authorization": f"Bearer {Bangumi_Helper.token}",
            "Content-Type": "application/json"
        }
        data = {
            "type": type.value
        }

        try:
            response = requests.put(url, headers=headers, json=data,timeout=30)
            response.raise_for_status()
            return True
        except requests.exceptions.RequestException as e:
            LOG_ERROR(f"Request failed: {e}")

        
        
    @staticmethod
    def Set_Bangumi_Status(bangumi_id, type: CollectionType):
        url = f"https://api.bgm.tv/v0/users/-/collections/{bangumi_id}"
        headers = {
            "accept": "*/*",
            'User-Agent': 'plsy1/easybangumi (https://github.com/plsy1/easybangumi)',
            "Authorization": f"Bearer {Bangumi_Helper.token}",
            "Content-Type": "application/json"
        }
        data = {
            "type": type.value
        }

        try:
            response = requests.post(url, headers=headers, json=data,timeout=30)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            LOG_ERROR(f"Request failed: {e}")

    @staticmethod
    def download_image(url: str, subject_id: int, save_directory: str = "img"):
        if not os.path.exists(save_directory):
            os.makedirs(save_directory)
        
        response = requests.get(url, stream=True)
        
        if response.status_code == 200:
            content_type = response.headers.get('Content-Type', '')
            file_extension = content_type.split('/')[1] if '/' in content_type else 'jpg'
            
            file_name = f"{subject_id}.{file_extension}"
            file_path = os.path.join(save_directory, file_name)
            
            with open(file_path, 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)
            
            print(f"Image saved as {file_name}")
        else:
            print("Failed to download image")
        

class Bangumi:

    @staticmethod
    def Init_Episodes_Information_By_Bangumi_Title(title):
        try:
            subject_id = Bangumi_Helper.Get_SubjectID_By_Name(title)
            episodes = Bangumi_Helper.Get_Episodes_By_SubjectID(subject_id)
            total_episodes = Bangumi_Helper.Get_Total_Episodes_By_SubjectID(subject_id)
            episodes_str = json.dumps(episodes)
            DB.bangumi_update({"subject_name": title, "subject_id": subject_id, "episodes": episodes_str,"total_episodes": total_episodes})
            
            ## 下载封面图片到本地
            url = Bangumi_Helper.Get_Subject_Image_Url_By_SubjectID(subject_id)
            Bangumi_Helper.download_image(url,title)
            
        except Exception as e:
            LOG_ERROR("Init Episodes Information failed:",e)
            
    @staticmethod
    def Refresh_Episodes_Information_By_Bangumi_Title(bangumi_title):
        try:
            subject_id = Bangumi_Helper.Get_SubjectID_By_Name(bangumi_title)
            episodes = Bangumi_Helper.Get_Episodes_By_SubjectID(subject_id)
            total_episodes = Bangumi_Helper.Get_Total_Episodes_By_SubjectID(subject_id)
            LOG_INFO('Total Episodes:',total_episodes)
            episodes_str = json.dumps(episodes)
            LOG_INFO('Episode ID:',episodes)
            DB.bangumi_update({"subject_name": bangumi_title, "subject_id": subject_id, "episodes": episodes_str,"total_episodes": total_episodes})
            
            url = Bangumi_Helper.Get_Subject_Image_Url_By_SubjectID(subject_id)
            Bangumi_Helper.download_image(url,bangumi_title)
        except Exception as e:
            LOG_ERROR("Refresh Episodes Information failed:",e)   
        
                   
    @staticmethod
    def Refresh_Episodes_Information():
        try:
            items = DB.rss_single_get_all()
            titles = []
            for item in items:
                titles.append(item[4])
            for title in titles:
                time.sleep(3)
                LOG_INFO('Start Refresh Bangumi Data:', title)
                subject_id = Bangumi_Helper.Get_SubjectID_By_Name(title)
                LOG_INFO('Bangumi ID:', subject_id)
                if subject_id:
                    episodes = Bangumi_Helper.Get_Episodes_By_SubjectID(subject_id)
                    total_episodes = Bangumi_Helper.Get_Total_Episodes_By_SubjectID(subject_id)
                    LOG_INFO('Total Episodes:',total_episodes)
                    episodes_str = json.dumps(episodes)
                    LOG_INFO('Episode ID:',episodes)
                    DB.bangumi_update({"subject_name": title, "subject_id": subject_id, "episodes": episodes_str,"total_episodes": total_episodes})
                    
                    url = Bangumi_Helper.Get_Subject_Image_Url_By_SubjectID(subject_id)
                    Bangumi_Helper.download_image(url,title)
        except Exception as e:
            LOG_ERROR("Refresh Episodes Information failed:",e)   
                    
            
        
    @staticmethod
    def Set_Episode_Watched(data):
        try:
            path = data["Item"]["Path"]
            episode = str(data['Item']['IndexNumber'])
            if path:
                directories = path.split(os.sep)
                tit = directories[-3]
                title = str(remove_year(tit))
                season = directories[-2]
                bangumi_title = DB.rss_single_get_by_title_and_season(title,season)
            else:
                LOG_ERROR("Can Not Find Bangumi Path.")
            
            if bangumi_title:
                info = DB.bangumi_get_subject_info_by_subject_name(bangumi_title)
                subject_id = info[0]
                episodes_info = info[1]
                total_episodes = info[2]                
                if int(episode) == 1:
                    Bangumi_Helper.Set_Bangumi_Status(subject_id,type=CollectionType.WATCHING)
                elif int(total_episodes) == int(episode):
                    Bangumi_Helper.Set_Bangumi_Status(subject_id,type=CollectionType.WATCHED)
                episodes_info = json.loads(episodes_info)
                episode_number = episodes_info.get(episode)
                if Bangumi_Helper.Set_Episode_Status_By_Id(episode_number,EpisodeCollectionType.WATCHED):
                    LOG_INFO(f"{bangumi_title} E{episode} Set Watched Success.")
            else:
                LOG_ERROR("Can Not Find Bangumi Title In Database.")
                LOG_INFO("Trying To Get From Bangumi......")
                season = get_season_number(season)
                if season != 1:
                    season = number_to_chinese(season)
                    season =f'第{season}季'
                    bangumi_title = f'{title} {season}'
                else:
                    bangumi_title = title
                    
                print(bangumi_title)
                    
                
                subject_id = Bangumi_Helper.Get_SubjectID_By_Name(bangumi_title)
                episodes_info = Bangumi_Helper.Get_Episodes_By_SubjectID(subject_id)
                print(episodes_info)
                total_episodes = Bangumi_Helper.Get_Total_Episodes_By_SubjectID(subject_id)
                
                if int(total_episodes) == int(episode):
                    Bangumi_Helper.Set_Bangumi_Status(subject_id,type=CollectionType.WATCHED)
                #if int(episode) == 1:
                Bangumi_Helper.Set_Bangumi_Status(subject_id,type=CollectionType.WATCHING)
                episode_number = episodes_info[int(episode)]
                if Bangumi_Helper.Set_Episode_Status_By_Id(episode_number,EpisodeCollectionType.WATCHED):
                    LOG_INFO(f"{bangumi_title} E{episode} Set Watched Success.")
                
                
        except Exception as e:
            LOG_ERROR("Set Episode Watched failed:",e)
            
    
    @staticmethod
    def Set_Episode_Unwatched(data):
        try:
            path = data["Item"]["Path"]
            episode = str(data['Item']['IndexNumber'])

            directories = path.split(os.sep)
            tit = directories[-3]
            title = str(remove_year(tit))
            season = directories[-2]
            bangumi_title = DB.rss_single_get_by_title_and_season(title,season)
            
            if bangumi_title:
                info = DB.bangumi_get_subject_info_by_subject_name(bangumi_title)
                subject_id = info[0]
                episodes_info = info[1]
                total_episodes = info[2]
                if int(total_episodes) == int(episode):
                    Bangumi_Helper.Set_Bangumi_Status(subject_id,type=CollectionType.WATCHING)
                episodes_info = json.loads(episodes_info)
                episode_number = episodes_info.get(episode)
                if Bangumi_Helper.Set_Episode_Status_By_Id(episode_number, EpisodeCollectionType.NOTCOLLECTED):
                    LOG_INFO(f"{bangumi_title} E{episode} Set Unwatched Success.")
                
            else:
                LOG_ERROR("Can Not Find Bangumi Title In Database.")
                LOG_INFO("Trying To Get From Bangumi......")
                season = get_season_number(season)
                if season != 1:
                    season = number_to_chinese(season)
                    season =f'第{season}季'
                    bangumi_title = f'{title} {season}'
                else:
                    bangumi_title = title
                    
                print(bangumi_title)
                    
                
                subject_id = Bangumi_Helper.Get_SubjectID_By_Name(bangumi_title)
                episodes_info = Bangumi_Helper.Get_Episodes_By_SubjectID(subject_id)
                print(episodes_info)
                total_episodes = Bangumi_Helper.Get_Total_Episodes_By_SubjectID(subject_id)
                
                if int(total_episodes) == int(episode):
                    Bangumi_Helper.Set_Bangumi_Status(subject_id,type=CollectionType.WATCHING)
                episode_number = episodes_info[int(episode)]
                if Bangumi_Helper.Set_Episode_Status_By_Id(episode_number,EpisodeCollectionType.NOTCOLLECTED):
                    LOG_INFO(f"{bangumi_title} E{episode} Set Unwatched Success.")
        except Exception as e:
            LOG_ERROR("Set Episode Unwatched Failed:",e)         


                