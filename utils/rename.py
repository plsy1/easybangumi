import re


def split_season_title(title):
    pattern = r"(.*)(第\w+季)"
    match = re.match(pattern, title)
    if match:
        matched_part = match.group(2)
        rest_part = match.group(1).strip()
        return f"Season {chinese_to_number(matched_part)}", rest_part
    else:
        return "Season 1", title


def chinese_to_number(season_str):
    chinese_to_number = {
        "一": 1,
        "二": 2,
        "三": 3,
        "四": 4,
        "五": 5,
        "六": 6,
        "七": 7,
        "八": 8,
        "九": 9,
        "十": 10,
    }
    if (
        season_str.startswith("第")
        and season_str.endswith("季")
        and len(season_str) >= 3
    ):
        chinese_number_str = season_str[1:-1]
        if all(char in chinese_to_number for char in chinese_number_str):
            number = 0
            for char in chinese_number_str:
                number += chinese_to_number[char]
            return number
        else:
            return None
    else:
        return None


def get_episode_number(text):

    pattern = r".*\[第*(\d{2}\.*\d*)v*\d*话*集*\]|.* - (\d{2}\.*\d*) [\(|\[]"
    match = re.search(pattern, text)
    if match:
        return match.group(1) or match.group(2)
    return None


def get_season_number(text):
    pattern = r".*/*Season (\d+)"
    match = re.search(pattern, text)
    if match:
        return int(match.group(1))
    return None

def number_to_chinese(number):
    number_to_chinese = {
        1: "一",
        2: "二",
        3: "三",
        4: "四",
        5: "五",
        6: "六",
        7: "七",
        8: "八",
        9: "九",
        10: "十",
    }
    return number_to_chinese.get(number)


def remove_year(text):
    # 使用正则表达式去除括号及其中的数字部分
    return re.sub(r'\s*\(\d+\)\s*', '', text)