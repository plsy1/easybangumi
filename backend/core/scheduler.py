import schedule
import time
from core.config import conf
from modules import *
from core.rss import *
from core.logs import *
import threading


class Scheduler:

    def Start():
        scheduler_thread = threading.Thread(target=Scheduler.Run, daemon=True)
        scheduler_thread.start()


    @staticmethod
    def Run():
        LOG_INFO('Scheduler Start Successful')
        schedule.every(10).minutes.do(Scheduler.Refresh)
        schedule.every(720).minutes.do(Scheduler.Update_Bangumi_Info)
        while True:
            schedule.run_pending()
            time.sleep(1)


    @staticmethod
    def Refresh():
        RSS.Refresh()
        RSS.Push()
        

    @staticmethod
    def Update_Bangumi_Info():
        if Bangumi_Helper.token is not None:
            LOG_INFO('Start Refresh Bangumi Episodes Information......')
            Bangumi.Refresh_Episodes_Information()
            