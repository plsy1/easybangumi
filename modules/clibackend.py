import re
from core.rss import *
def run_background_process(args):
    if args.add_single:
        print("添加单独的RSS订阅:", args.add_single)
        RSS.Add(args.add_single,Type=RSS_Type.SINGLE)
    elif args.add_gather:
        print("添加RSS订阅集合:", args.add_gather)
        RSS.Add(args.add_gather,Type=RSS_Type.GATHER)
    if args.refresh:
        print("刷新RSS订阅")
        RSS.Refresh()