import glob
import os
import json
import sys
import matplotlib
import numpy

import xboa.common.matplotlib_wrapper as matplotlib_wrapper

from utils import utilities

def load_file(file_name):
    fin = open(file_name)
    data_out = []
    for line in fin.readlines():
        data_out.append(json.loads(line))
    return data_out

def filtered_dphi(dphi_list):
    n_in = len(dphi_list)
    while True:
        print(len(dphi_list), end=' ')
        sys.stdout.flush()
        mean_dphi = numpy.mean(dphi_list)
        dphi_err = [(abs((dphi-mean_dphi)/mean_dphi), dphi) for dphi in dphi_list]
        dphi_err = sorted(dphi_err)
        if dphi_err[-1][0] > 0.5:
            dphi_list = [dphi[1] for dphi in dphi_err[:-1]]
        else:
            break
    mean_dphi = numpy.mean(dphi_list)
    print(mean_dphi)
    return mean_dphi

def plot_tune(data, tune_axis, plot_dir):
    print("Plotting tune")
    axis_candidates = utilities.get_substitutions_axis(data)
    metres = 1e-3
    for key in axis_candidates:
        sys.stdout.flush()
        x_name = utilities.sub_to_name(key)
        x_list = axis_candidates[key]
        y_list = [filtered_dphi(item[tune_axis]) for item in data]
        x_name += utilities.sub_to_units(key)
        fig_index = matplotlib_wrapper.make_graph(x_list, x_name,
                                                  y_list, tune_axis)
        for format in ["png"]:
            name = plot_dir+"/"+tune_axis+"."+format
            fig = matplotlib.pyplot.figure(fig_index)
            fig.savefig(name)

def main(glob_list):
    for glob_name in glob_list:
        for file_name in glob.glob(glob_name):
            plot_dir = os.path.split(file_name)[0]
            print(file_name)
            data = load_file(file_name)
            if len(data) == 0:
                continue
            plot_tune(data, 'x_dphi', plot_dir)
            plot_tune(data, 'y_dphi', plot_dir)

if __name__ == "__main__":
    main(sys.argv[1:])
    matplotlib.pyplot.show(block=False)
    input("Done - press Enter to finish")
