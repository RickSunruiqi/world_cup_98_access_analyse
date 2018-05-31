#!/usr/bin/env python
__author__ = 'ricksunruiqi'

import os
import random
import datetime
from pyecharts import Line


logs_dir = "worldcup98/wc_txt/"
results_dir = "worldcup98/wc_analyse_results/"
result_file_per_sec = "wc_access_per_sec.log"
result_file_per_min = "wc_access_per_min.log"
result_file_per_10_min = "wc_access_per_10_min.log"
result_file_per_10_min_normalize = "wc_access_per_10_min_normalize.log"
result_file_per_10_min_normalize_random = "wc_access_per_10_min_normalize_random.log"
result_file_per_10_min_normalize_revised2 = "wc_access_per_10_min_normalize_revised2.log"
chart_file = "wc_access_per_10_min_normalize_revised2.html"


def wc_access_statistics_basic():
    result_file_handler = open(results_dir + result_file_per_sec, 'w')
    log_file_list = os.listdir(logs_dir)
    for log_file in sorted(log_file_list):
        # print log_file
        logs = open(logs_dir + log_file, 'r')
        last_time_str = ""
        access_per_sec = 0
        for line in logs:   # 3484 - - [12/Jun/1998:19:11:24 +0000] "GET /english/index.html HTTP/1.0" 200 892
            time_str = line.split('[')[1].split(']')[0]
            if time_str == last_time_str:
                access_per_sec += 1
            if time_str != last_time_str:
                if access_per_sec != 0:
                    result_file_handler.write(log_file + ',' + last_time_str + ',' + str(access_per_sec) + "\n")
                    print log_file + ',' + last_time_str + ',' + str(access_per_sec)
                last_time_str = time_str
                access_per_sec = 1
        result_file_handler.write(log_file + ',' + last_time_str + ',' + str(access_per_sec) + "\n")
        print log_file + ',' + last_time_str + ',' + str(access_per_sec)
    result_file_handler.close()


def wc_access_per_min():
    wc_access_per_min_handler = open(results_dir + result_file_per_min, 'w')
    with open(results_dir + result_file_per_sec, 'r') as logs:
        last_time_str = ""
        access_per_min = 0
        for line_per_sec in logs:  # wc_day60_1.out,23/Jun/1998:22:00:01 +0000,144
            time_str = line_per_sec.split(',')[1].split(' ')[0][:-3]
            if time_str == last_time_str:
                access_per_min += int(line_per_sec.split(',')[2])
            if time_str != last_time_str:
                if access_per_min != 0:
                    wc_access_per_min_handler.write(line_per_sec.split(',')[0] + ','
                                                    + last_time_str + ','
                                                    + str(access_per_min) + "\n")
                    print line_per_sec.split(',')[0] + ',' + last_time_str + ',' + str(access_per_min)
                last_time_str = time_str
                access_per_min = int(line_per_sec.split(',')[2])
        wc_access_per_min_handler.write(line_per_sec.split(',')[0] + ','
                                        + last_time_str + ','
                                        + str(access_per_min) + "\n")
        print line_per_sec.split(',')[0] + ',' + last_time_str + ',' + str(access_per_min)


def wc_access_per_10_min():
    wc_access_per_min_handler = open(results_dir + result_file_per_10_min, 'w')
    with open(results_dir + result_file_per_sec, 'r') as logs:
        last_time_str = ""
        access_per_min = 0
        for line_per_sec in logs:  # wc_day60_1.out,23/Jun/1998:22:00:01 +0000,144
            time_str = line_per_sec.split(',')[1].split(' ')[0][:-4]
            if time_str == last_time_str:
                access_per_min += int(line_per_sec.split(',')[2])
            if time_str != last_time_str:
                if access_per_min != 0:
                    wc_access_per_min_handler.write(line_per_sec.split(',')[0] + ','
                                                    + last_time_str + '0,'
                                                    + str(access_per_min) + "\n")
                    print line_per_sec.split(',')[0] + ',' + last_time_str + '0,' + str(access_per_min)
                last_time_str = time_str
                access_per_min = int(line_per_sec.split(',')[2])
        wc_access_per_min_handler.write(line_per_sec.split(',')[0] + ','
                                        + last_time_str + '0,'
                                        + str(access_per_min) + "\n")
        print line_per_sec.split(',')[0] + ',' + last_time_str + '0,' + str(access_per_min)


def wc_access_normalize_based_10_min():
    wc_access_normalize_based_10_min_handler = open(results_dir + result_file_per_10_min_normalize, 'w')
    max_access = 0
    with open(results_dir + result_file_per_10_min, 'r') as logs:
        for line_ in logs:  # wc_day60_1.out,23/Jun/1998:22:00,321665
            current_access = int(line_.split(',')[2])
            if max_access < current_access:
                max_access = current_access
    with open(results_dir + result_file_per_10_min, 'r') as logs:
        for line__ in logs:
            normalize_access = round(float(line__.split(',')[2]) / max_access, 4)
            wc_access_normalize_based_10_min_handler.write(line__.split(',')[0] + ','
                                                           + line__.split(',')[1] + ','
                                                           + normalize_access.__str__() + '\n')


def wc_access_normalize_based_10_min_random():
    wc_access_normalize_based_10_min_random_handler = open(results_dir + result_file_per_10_min_normalize_random, 'w')
    with open(results_dir + result_file_per_10_min_normalize, 'r') as logs:
        for line__ in logs:     # wc_day60_1.out,23/Jun/1998:22:00,0.26
            normalize_access = float(line__.split(',')[2])
            random_int = random.randint(-5, 5)
            b = round(normalize_access * (1 + random_int / 100.0), 4)
            wc_access_normalize_based_10_min_random_handler.write(line__.split(',')[0] + ','
                                                                  + line__.split(',')[1] + ','
                                                                  + b.__str__() + '\n')


def wc_access_visible():
    start_time = datetime.datetime.strptime("1998-06-20 22:00:00", '%Y-%m-%d %H:%M:%S')
    end_time = datetime.datetime.strptime("1998-06-25 22:00:00", '%Y-%m-%d %H:%M:%S')

    attr = []
    v1 = []
    logs = open(results_dir + result_file_per_10_min_normalize_revised2, 'r')
    for line_ in logs:  # wc_day49_2.log,13/Jun/1998:14:39:52 +0000,415
        # time_str = line.split(',')[1].split(' ')[0]
        # time_line = datetime.datetime.strptime(time_str, '%d/%b/%Y:%H:%M:%S')
        time_str = line_.split(',')[1]  # wc_day60_1.out,23/Jun/1998:22:10,0.2395
        time_line = datetime.datetime.strptime(time_str, '%d/%b/%Y:%H:%M')
        if start_time < time_line < end_time:
            attr.append(time_str)
            v1.append(float(line_.split(',')[2]))

    line = Line("WC Access per 10 Minute (Normalized) with Random", width=1600)
    # line = Line("WC Access per 10 Minute", width=1600)
    # line.add("A100", attr, v1, mark_point=["average"])
    line.add("users", attr, v1, is_smooth=True, mark_line=["min", "max", "average"])
    line.show_config()
    line.render(results_dir + chart_file)


if __name__ == "__main__":
    # wc_access_per_10_min()
    # wc_access_normalize_based_10_min()
    # wc_access_normalize_based_10_min_random()
    wc_access_visible()
