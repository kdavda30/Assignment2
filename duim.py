#!/usr/bin/env python3

import subprocess, sys
import os
import argparse



'''
OPS435 Assignment 2 - Summer 2021
Program: duim.py 
Author: Kishen Davda
The python code in this file (duim.py) is original work written by
Kishen Davda. No code in this file is copied from any other source 
except those provided by the course instructor, including any person, 
textbook, or on-line resource. I have not shared this python script 
with anyone or anything except for submission for grading.  
I understand that the Academic Honesty Policy will be enforced and 
violators will be reported and appropriate action will be taken.


Date: July 27, 2021
'''

def parse_command_args():
    "Set up argparse here. Call this function inside main."
    parser = argparse.ArgumentParser(description="DU Improved -- See Disk Usage Report with bar charts",epilog="Copyright 2021")
    parser.add_argument("-l", "--length", type=int, default=20, help="Specify the length of the graph. Default is 20.")
    # add argument for "human-readable". USE -H, don't use -h! -h is reserved for --help which is created automatically.
    # check the docs for an argparse option to store this as a boolean.
    # add argument for "target". set number of args to 1.
    args = parser.parse_args()


def percent_to_graph(percent, total_chars):
    "returns a string: eg. '##  ' for 50 if total_chars == 4"
    graph = percent/100
    graph = graph * total_chars
    graph = round(graph)
    bar=""
    space=""
    p = 0
    i = 0
    end = total_chars - graph
    
    while p != graph:
        bar = bar + "#"
        p = p + 1
    finish = "["+ bar
    
    while i != end:
        space = space + " "
        i = i + 1
    finish = finish + space + "]"    
    
    return finish

def call_du_sub(location):
    "use subprocess to call `du -d 1 + location`, rtrn raw list"

    p = subprocess.Popen(['du -d 1 ' + location], stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output = p.communicate()
    stdout = output[0].decode('utf-8').strip()
    outputlist = list(stdout)

    return outputlist    

def create_dir_dict(raw_dat):
    "get list from du_sub, return dict {'directory': 0} where 0 is size"
    valueslist = [i.split('\t')[0] for i in raw_dat]
    valuesint = [int(i) for i in valueslist]
    keys = [i.split('\t')[1] for i in raw_dat]
    outputDict = dict(zip(keys, valuesint))
    return outputDict

def get_total_size(dir_dict_list):
    return sum(dir_dict.values())

def get_unit(n):
    factor = 1000 
    if n < factor:
        return 'B'
    elif factor <= n < factor ** 2:
        return 'KiB'
    elif factor**2 <= n < factor**3:
        return 'MiB'
    elif factor**3 <= n < factor**4:
        return 'GiB'
    else:
        return 'TiB'

def auto_scale_n(n):
    factor = 1000 
    scaled = n
    while scaled > factor:
        scaled /= factor
    return scaled

if __name__ == "__main__":
    args = sys.argv
    if len(args) == 0:
        directory = "."
    elif len(args) > 1 or not os.path.isdir(args[0]):
        print("ERROR: Invalid number of arguments or path is not valid.")
        exit(0)
    else:
        directory = args[0]     
    dir_dict = ceate_dir_dict(du_sub(directory))
    total_size = get_total_size(dir_dict)
    graph_max_size = 20
    for subdir, size in dir_dict.items():
        percentage = int(size / total_size * 100)
        graph = percent_to_graph(percentage, graph_max_size)
        print("{:>2} % [{}] {:0.1f} {:<5}\t{}".format(percentage, graph, auto_scale_n(size),get_unit(size) , subdir))
        print("Total: {:0.1f} {}\t\t\t{}".format(auto_scale_n(total_size), get_unit(total_size), directory))


