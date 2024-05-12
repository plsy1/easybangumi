import sqlite3
from core.config import conf
from core.logs import *


class DB:
    
    data_dir = '/app/data'
    #data_dir = 'data'
    file_name = conf.get_database_config().get('name')
    db_file = os.path.join(data_dir, file_name)
    @staticmethod
    def create_table():
        conn = sqlite3.connect(DB.db_file)
        c = conn.cursor()

        c.execute("PRAGMA foreign_keys = ON")

        c.execute(
            """CREATE TABLE IF NOT EXISTS rss_items
            (id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            link TEXT,
            torrent_url TEXT,
            pushed_to_downloader INTEGER,
            rss_single_id INTEGER,
            FOREIGN KEY (rss_single_id) REFERENCES rss_single(id) ON DELETE CASCADE
            )"""
        )

        c.execute(
            """CREATE TABLE IF NOT EXISTS rss_single
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                link TEXT,
                title TEXT,
                season INTEGER,
                bangumi_title TEXT
                )"""
        )


        c.execute(
            """CREATE TABLE IF NOT EXISTS rss_gather
                        (id INTEGER PRIMARY KEY AUTOINCREMENT,
                        link TEXT)"""
        )
        
        c.execute('''CREATE TABLE IF NOT EXISTS bangumi (
                subject_name TEXT UNIQUE,
                subject_id TEXT,
                episodes TEXT,
                total_episodes INTEGER
             )''')

        conn.commit()
        conn.close()

    
    @staticmethod
    def bangumi_get_subject_info_by_subject_name(subject_name):
        conn = sqlite3.connect(DB.db_file)
        c = conn.cursor()
        
        c.execute("SELECT subject_id, episodes,total_episodes FROM bangumi WHERE subject_name = ?", (subject_name,))
        result = c.fetchone()
        return result
        
        
    @staticmethod
    def bangumi_update(item):
        conn = sqlite3.connect(DB.db_file)
        c = conn.cursor()
        c.execute('''INSERT OR REPLACE INTO bangumi (subject_name, subject_id, episodes, total_episodes) 
                 VALUES (?, ?, ?, ?)''',
              (item["subject_name"], item["subject_id"], item["episodes"],item['total_episodes']))
        conn.commit()
        conn.close()
        
    @staticmethod
    def rss_single_get_by_title_and_season(title, season):
        conn = sqlite3.connect(DB.db_file)
        c = conn.cursor()
        
        # 执行查询并返回匹配的条目
        c.execute("SELECT * FROM rss_single WHERE title = ? AND season = ?", (title, season))
        result = c.fetchone()
        
        conn.close()
        return result[4] if result else None
    
    
    @staticmethod
    def old_rss_items_insert(item):
        conn = sqlite3.connect(DB.db_file)
        c = conn.cursor()
        c.execute("SELECT * FROM rss_items WHERE title=?", (item["title"],))
        existing_item = c.fetchone()
        if not existing_item:
            c.execute(
                "INSERT INTO rss_items (title, link, torrent_url, pushed_to_downloader) VALUES (?, ?, ?, 0)",
                (item["title"], item["link"], item["torrent_url"]),
            )
            conn.commit()
        conn.close()

    @staticmethod
    def rss_items_insert(item, rss_single_id):
        try:
            conn = sqlite3.connect(DB.db_file)
            c = conn.cursor()
            c.execute("SELECT * FROM rss_items WHERE title=?", (item["title"],))
            existing_item = c.fetchone()
            if not existing_item:
                c.execute(
                    "INSERT INTO rss_items (title, link, torrent_url, pushed_to_downloader, rss_single_id) VALUES (?, ?, ?, ?, ?)",
                    (
                        item["title"],
                        item["link"],
                        item["torrent_url"],
                        0,
                        rss_single_id,
                    ),
                )
                conn.commit()
        except Exception as e:
            print("Error:", e)
        finally:
            conn.close()

    @staticmethod
    def rss_items_get_all():
        conn = sqlite3.connect(DB.db_file)
        c = conn.cursor()
        c.execute("SELECT * FROM rss_items")
        items = c.fetchall()
        conn.close()
        items_dicts = [
            {
                "title": item[1],
                "link": item[2],
                "torrent_url": item[3],
                "pushed_to_downloader": item[4],
                "id": item[5],
            }
            for item in items
        ]
        return items_dicts

    @staticmethod
    def rss_items_get_new():
        try:
            conn = sqlite3.connect(DB.db_file)
            c = conn.cursor()
            c.execute("SELECT * FROM rss_items WHERE pushed_to_downloader=0")
            items = c.fetchall()
            conn.close()
            items_dicts = [
                {
                    "title": item[1],
                    "link": item[2],
                    "torrent_url": item[3],
                    "pushed_to_downloader": item[4],
                    "id": item[5],
                }
                for item in items
            ]
            return items_dicts
        except Exception as e:
            LOG_ERROR("An error occurred while querying the database:", e)
            return None

    @staticmethod
    def rss_items_set_pushed_to_downloader_by_title(title):
        try:
            conn = sqlite3.connect(DB.db_file)
            c = conn.cursor()
            c.execute("UPDATE rss_items SET pushed_to_downloader=1 WHERE title=?", (title,))
            conn.commit()
            conn.close()
        except Exception as e:
            LOG_ERROR("An error occurred while querying the database:", e)
            return None

    @staticmethod
    def rss_items_set_pushed_to_downloader(title):
        conn = sqlite3.connect(DB.db_file)
        c = conn.cursor()
        c.execute("UPDATE rss_items SET pushed_to_downloader=1 WHERE title=?", (title,))
        conn.commit()
        conn.close()

    @staticmethod
    def rss_items_is_link_exist_and_pushed(link):
        try:
            conn = sqlite3.connect(DB.db_file)
            c = conn.cursor()
            c.execute(
                "SELECT * FROM rss_items WHERE link=? AND pushed_to_downloader=1",
                (link,),
            )
            found_item = c.fetchone()
            return found_item is not None
        except Exception as e:
            print("Error:", e)
        finally:
            conn.close()

    @staticmethod
    def rss_single_insert(item):
        try:
            conn = sqlite3.connect(DB.db_file)
            c = conn.cursor()
            c.execute(
                "SELECT * FROM rss_single WHERE link=?", (item[0],)
            )  # item[0] 是链接部分
            existing_link = c.fetchone()
            if not existing_link:
                c.execute(
                    "INSERT INTO rss_single (link, title, season, bangumi_title) VALUES (?, ?, ?, ?)",
                    item,
                )
                conn.commit()
        except Exception as e:
            LOG_ERROR(e)
        finally:
            conn.close()

    @staticmethod
    def rss_single_get_all():
        conn = sqlite3.connect(DB.db_file)
        c = conn.cursor()
        c.execute("SELECT * FROM rss_single")
        items = c.fetchall()
        conn.close()
        return items

    @staticmethod
    def rss_single_is_link_exist(link):
        conn = sqlite3.connect(DB.db_file)
        c = conn.cursor()
        c.execute("SELECT * FROM rss_single WHERE link=?", (link,))
        result = c.fetchone()
        conn.close()
        return result is not None
    
    @staticmethod
    def rss_single_delete_by_id(id):
        conn = sqlite3.connect(DB.db_file)
        c = conn.cursor()
        c.execute("DELETE FROM rss_single WHERE id=?", (id,))
        conn.commit()
        conn.close()
        return True

    @staticmethod
    def rss_single_get_by_rss_single_id(Id):
        try:
            conn = sqlite3.connect(DB.db_file)
            c = conn.cursor()
            c.execute("SELECT * FROM rss_single WHERE id=?", (Id,))
            rss_single = c.fetchone()
            return rss_single
        except Exception as e:
            print("Error:", e)
        finally:
            conn.close()

    @staticmethod
    def rss_gather_insert(item):
        conn = sqlite3.connect(DB.db_file)
        c = conn.cursor()
        c.execute("SELECT * FROM rss_gather WHERE link=?", (item,))
        existing_link = c.fetchone()
        if not existing_link:
            c.execute("INSERT INTO rss_gather (link) VALUES (?)", (item,))
            conn.commit()
        conn.close()

    @staticmethod
    def rss_gather_get_all():
        conn = sqlite3.connect(DB.db_file)
        c = conn.cursor()
        c.execute("SELECT * FROM rss_gather")
        items = c.fetchall()
        conn.close()
        return items

    @staticmethod
    def rss_gather_is_link_exist(link):
        conn = sqlite3.connect(DB.db_file)
        c = conn.cursor()
        c.execute("SELECT * FROM rss_gather WHERE link=?", (link,))
        result = c.fetchone()
        conn.close()
        return result is not None
    
    @staticmethod
    def rss_gather_delete_by_id(id):
        conn = sqlite3.connect(DB.db_file)
        c = conn.cursor()
        c.execute("DELETE FROM rss_gather WHERE id=?", (id,))
        conn.commit()
        conn.close()
        return True
