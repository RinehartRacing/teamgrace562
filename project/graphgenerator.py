#!/usr/bin/python3
import argparse
import sys
import matplotlib.pyplot as plt
import pandas as pd
from glob import glob
from matplotlib.figure import Figure
def array_thinnerY(big_list, NUM):
    if NUM == 0:
        return big_list
    old_length = len(big_list)
    new_length = int(old_length / NUM)
    thin_list = []
    group_sum = 0
    for i in range(old_length):
        if i % NUM == 0 and new_length != 0:
            if i != 0:
                thin_list.append(group_sum)
            group_sum = 0
        else:
            group_sum += big_list[i]
    if group_sum > 0:
        thin_list.append(group_sum)
    return thin_list

def array_thinnerX(big_list, NUM):
    if NUM == 0:
        return big_list
    old_length = len(big_list)
    new_length = int(old_length / NUM)

    thin_list = []
    for i in range(old_length):
        if i % NUM == NUM - 1:
            thin_list.append(big_list[i])
    if old_length % NUM != 0:
        thin_list.append(big_list[-1])
    return thin_list

def get_metric(metric_num):
    titles = ("Prefetches Issued", "Prefetchers in Cache", "Overall Misses", "Overall Hits",
              "Overall Accesses", "Unused Prefetches", "Overall Misses to Overall Accesses Ratio", "Overall Hits to Overall Accesses Ratio",
              "Unused Prefetches to Prefetches Issued Ratio", "Unused Prefetches to Prefetchers in Cache Ratio", "Overall Hits to Overall Misses Ratio", "Prefetchers in Cache to Prefetches Issued Ratio")
    metrics = ("pfIssued", "pfInCache", "overallMisses", "overallHits", "overallAccesses", "unusedPrefetches",
               "overallMisses overallAccesses", "overallHits overallAccesses", "unusedPrefetches pfIssued", "unusedPrefetches pfInCache", "overallHits overallMisses", "pfInCache pfIssued")
    return (titles[metric_num - 1], metrics[metric_num - 1])


def get_data(metric, workload):
   results = glob(f"./results/*{workload}*")
   x_data_set = []
   y_data_set = []
   prefetchers = []
   for result in results:
        prefetcher = result.split("/")[-1].split(".")[-2].split("-")[0]
        prefetchers.append(prefetcher)
        dataframe = pd.read_csv(result)
        x_data = dataframe["Instruction"].to_list()
        y_data = dataframe[metric].to_list()
        x_data_set.append(x_data)
        y_data_set.append(y_data)
    
   return (x_data_set, y_data_set, prefetchers)

def get_markers(index):
    markers = [".", "v", "s", "P", "X", "D", "p", "H"]
    return markers[index]

def graph(title, workload, prefetchers, x_data_set, y_data_set, x_min, x_max, NUM):
    
    fig = plt.figure(figsize = (5, 4))

    # Adding the axes to the figure
    ax = fig.add_subplot(111)
    
    marker_pos = 0
    for i in range(len(prefetchers)):
        # plotting 1st dataset to the figure
        prefetcher = prefetchers[i]
        marker = get_markers(marker_pos % 8)
        marker_pos += 1
        
        x_data = array_thinnerX(x_data_set[i], NUM)

        y_data = array_thinnerY(y_data_set[i], NUM)
        ax1 = ax.plot(x_data, y_data, marker=marker)
    ax.set_xlabel("Instruction Count")
    ax.set_ylabel(title)
    ax.set_xlim(left=x_min, right=x_max)
    
    # Adding Legend
    ax.legend(labels = prefetchers, bbox_to_anchor=(1, 1))
    ax.set_title(f"{title} vs. Instruction for {workload} Testbench")
    ax.grid()
    plt.show()
def list_divider(listA, listB):
    new_list = []
    for i in range(len(listA)):
        sub_listA = listA[i]
        sub_listB = listB[i]
        new_sub_list = []
        for j in range(len(sub_listA)):
            new_sub_list.append(sub_listA[j] / sub_listB[j])
        new_list.append(new_sub_list)
    return new_list

def parse_input(args):
    metric_num = args.metric
    workload = args.workload
    xmin = args.xmin
    xmax = args.xmax
    NUM = args.NUM
    x_label = "Instruction Count"
    metric = get_metric(metric_num)[1]
    title = get_metric(metric_num)[0]
    metric_split = metric.split()
    data_tuple = get_data(metric_split[0], workload)
    x_data = data_tuple[0]
    y_data = data_tuple[1]
    prefetchers = data_tuple[2]
    if len(metric_split) == 2:
        data_tuple = get_data(metric_split[1], workload)
        y_divisor = data_tuple[1]
        y_data = list_divider(y_data, y_divisor)

    graph(title, workload, prefetchers, x_data, y_data, xmin, xmax, NUM)



def main():
    parser = argparse.ArgumentParser(
        prog='Graph Generator')
    parser.add_argument('-metric', required=True, type=int, choices=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
                        help="statistic/metric to run-> 1:pfIssued, 2:pfInCache, 3:overallMisses, 4:overallHits, 5:overallAccesses, 6:unusedPrefetches, 7:overallMisses/overallAccesses, 8:overallHits/overallAccesses, 9:unusedPrefetches/pfIssued, 10:unusedPrefetches/pfInCache, 11:overallHits/overallMisses, 12:pfInCache/pfIssued")
    parser.add_argument('-workload', required=True, choices=[
                        "a2time01", "bitmnp01", "cacheb01", "mcf", "libquantum"], help="testbench to run")
    parser.add_argument('-xmin', required=False,
                        type=int, help="Graph minimum x")
    parser.add_argument('-xmax', required=False,
                        type=int,  help="Graph maximum x")
    parser.add_argument('-NUM', required=False,
                        type=int,  default=50, help="Thin data by dividing by this number")
    args = parser.parse_args()
    parse_input(args)


if __name__ == "__main__":
    main()
