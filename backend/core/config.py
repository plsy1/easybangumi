import yaml
import os, sys
from core.logs import *


class ConfigManager:
    def __init__(self, config_file_path=None):
        
        self.Telegram = False
        
        if config_file_path is None:
            if getattr(sys, "frozen", False):
                binary_dir = os.path.dirname(sys.argv[0])
                config_file_path = os.path.join(binary_dir, "config.yaml")
            else:
                current_dir = os.getcwd()
                config_file_path = os.path.join(current_dir, "conf/config.yaml")
                
        self.config = self.load_config(config_file_path)
        self.check_required()
        self.check_loaded()

    def load_config(self, config_file_path):
        with open(config_file_path, "r") as f:
            config = yaml.safe_load(f)
        return config

    def check_required(self):
        missing_keys = []
        qbittorrent_config = self.config.get("qbittorrent")
        if not qbittorrent_config:
            missing_keys.append("qbittorrent")
        else:
            required_keys = ["host", "port", "username", "password", "root_folder"]
            for key in required_keys:
                if key not in qbittorrent_config:
                    missing_keys.append(f"qBittorrent - {key}")
                    
        """
        database_config = self.config.get("database")

        if not database_config:
            missing_keys.append("database")
        elif "name" not in database_config:
            missing_keys.append("database - name")
        """
        if missing_keys:
            for missing_key in missing_keys:
                LOG_ERROR(f"缺少必须配置项: {missing_key}")
            sys.exit(1)

    def check_loaded(self):
        if self.get_telegram_config() is not None:
            self.Telegram = True

    def get_telegram_config(self):
        telegram_config = self.config.get("telegram")
        if telegram_config is None:
            return None
        required_keys = ["token", "chat_id"]
        for key in required_keys:
            if key not in telegram_config:
                LOG_ERROR(f"缺少Telegram配置项: {key}")
                return None
        return telegram_config

    def get_qbittorrent_config(self):
        qbittorrent_config = self.config.get("qbittorrent", {})
        required_keys = ["host", "port", "username", "password", "root_folder"]
        for key in required_keys:
            if key not in qbittorrent_config:
                LOG_ERROR(f"缺少qBittorrent配置项: {key}")
                return None
        default_qbittorrent_config = {
            "tag": "easybangumi",
        }
        qbittorrent_config = {**default_qbittorrent_config, **qbittorrent_config}
        return qbittorrent_config

    def get_rss_config(self):
        rss_config = self.config.get("rss", {})
        required_keys = ["url"]
        for key in required_keys:
            if key not in rss_config:
                LOG_ERROR(f"缺少RSS配置项: {key}")
                return None
        if "scrape" not in rss_config:
            rss_config["scrape"] = "TMDB"
        return rss_config


    def get_bangumi_config(self):
        bangumi_config = self.config.get("bangumi", {})
        required_keys = ["token"]
        for key in required_keys:
            if key not in bangumi_config:
                LOG_ERROR(f"缺少bangumi配置项: {key}")
                return None
        return bangumi_config

conf = ConfigManager()
