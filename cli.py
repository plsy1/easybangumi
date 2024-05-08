# cli.py
import argparse
from modules.clibackend import run_background_process
from utils.tools import *

def main():
    parser = argparse.ArgumentParser(description='命令行工具')

    parser.add_argument('-ag', '--add_gather', dest='add_gather', metavar='URL', help='添加RSS订阅集合')
    parser.add_argument('-as', '--add_single', dest='add_single', metavar='URL', help='添加单独的RSS订阅')
    parser.add_argument('-de', '--delete', dest='delete', metavar='URL', help='删除RSS订阅')
    parser.add_argument('-re', '--refresh', dest='refresh', nargs='?', const=True, help='刷新RSS订阅')
    
    
    args = parser.parse_args()
    
    if args.add_gather and not is_valid_url(args.add_gather):
        print("错误：无效的URL:", args.add_gather)
        return
    if args.add_single and not is_valid_url(args.add_single):
        print("错误：无效的URL:", args.add_single)
        return
    run_background_process(args)

if __name__ == "__main__":
    main()