from modules.database import *
from modules.bangumi import *
from core.rss import RSS, RSS_Type
DB.create_table()

#RSS.Add('https://mikanani.me/RSS/Bangumi?bangumiId=2833&subgroupid=583',RSS_Type.SINGLE)
#res = Bangumi_Helper.Get_Total_Episodes_By_SubjectID('328609')
Bangumi.Refresh_Episodes_Information()

