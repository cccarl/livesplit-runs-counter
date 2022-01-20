import xml.etree.ElementTree as ET
import math
from os.path import exists


# gets all the final times of runs from the xml tree in a livesplit save file
# return: tuple with lists of real and game time in a dict for easy access
def get_final_run_times(file_name):

    if not exists(file_name):
        print("THAT FILE DOESNT EXIST!!!!!!!!")
        return [], []

    # parse xml, create tree
    tree = ET.parse(file_name)

    # get root of tree
    root = tree.getroot()

    real_time_list = []
    game_time_list = []
    for attempt in root.find("AttemptHistory"):
        if attempt.text is not None:
            for data in attempt:

                if data.tag == "RealTime":
                    timelistaux = attempt[0].text.split(":")
                    timedict = {"id": attempt.attrib["id"], "hr": timelistaux[-3], "min": timelistaux[-2], "sec": timelistaux[-1]}
                    real_time_list.append(timedict)

                if data.tag == "GameTime":
                    timelistaux = attempt[1].text.split(":")
                    timedict = {"id": attempt.attrib["id"], "hr": timelistaux[-3], "min": timelistaux[-2], "sec": timelistaux[-1]}
                    game_time_list.append(timedict)

    return real_time_list, game_time_list


def get_game_data(file_name):
    data_dict = {}

    if not exists(file_name):
        print("THAT FILE DOESNT EXIST!!!!!!!!")
        return {"game": "", "category": ""}

    # parse xml, create tree
    tree = ET.parse(file_name)

    # get root of tree
    root = tree.getroot()

    data_dict["game"] = root.find("GameName").text
    data_dict["category"] = root.find("CategoryName").text

    return data_dict


# counts the amount of X time gotten in the splits (hours, minutes, seconds
# parameter: string, h: count hours, m: count minutes, s: count seconds
def count_time_barriers(times_list, barrier_type):
    barrier_count_dict = {}

    for time in times_list:
        hour = int(time["hr"])
        minute = int(time["min"])
        second = math.floor(float(time["sec"]))

        if barrier_type == "h":
            hour_str = str(hour) + "h"
            if hour_str not in barrier_count_dict.keys():
                barrier_count_dict[hour_str] = 1
            else:
                barrier_count_dict[hour_str] += 1

        elif barrier_type == "m":
            total_minutes = str(hour) + ":" + (str(minute) if minute >= 10 else "0" + str(minute))
            if total_minutes not in barrier_count_dict.keys():
                barrier_count_dict[total_minutes] = 1
            else:
                barrier_count_dict[total_minutes] += 1

        elif barrier_type == "s":
            total_seconds = str(hour) + ":" + (str(minute) if minute >= 10 else "0" + str(minute)) + ":" + (str(second) if second >= 10 else "0" + str(second))
            if total_seconds not in barrier_count_dict.keys():
                barrier_count_dict[total_seconds] = 1
            else:
                barrier_count_dict[total_seconds] += 1

        else:
            print("Wrong input, choose h, m, or s as second parameter")
            return {}

    return barrier_count_dict


def write_times_file(times_dict, max_lines=-1, ordered=True):
    sorted_keys = []
    for key in times_dict:
        sorted_keys.append(key)
    sorted_keys.sort()

    file = open("split_times.txt", "w")
    if ordered:
        i = 0
        while i <= len(sorted_keys)-1:
            file.write(sorted_keys[i] + " - " + str(times_dict[sorted_keys[i]]) + "\n")
            i += 1
            if i == max_lines:
                i = len(sorted_keys)

    else:
        i = 0
        for key in times_dict:
            if i < max_lines:
                file.write(key + " - " + str(times_dict[key]) + "\n")

            i += 1

    file.close()

    return