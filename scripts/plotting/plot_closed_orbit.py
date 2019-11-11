import glob
import os
import json
import sys
import matplotlib

import xboa.common.matplotlib_wrapper as matplotlib_wrapper

from utils import utilities

def load_file(file_name):
    fin = open(file_name)
    data_out = []
    for line in fin.readlines():
        data_out.append(json.loads(line))
    return data_out

def plot_closed_orbit(data, co_axis, plot_dir):
    print("closed orbit", end=' ')
    axis_candidates = utilities.get_substitutions_axis(data)
    metres = 1e-3
    for key in axis_candidates:
        sys.stdout.flush()
        x_name = utilities.sub_to_name(key)
        x_list = axis_candidates[key]
        y_list = [item["hits"][0][co_axis] for item in data]
        y_list = [y*metres for y in y_list]
        x_name += utilities.sub_to_units(key)
        fig_index = matplotlib_wrapper.make_graph(x_list, x_name,
                                                  y_list, "Radial position [m]")
        for format in ["png"]:
            name = plot_dir+"/"+co_axis+"_closed_orbit."+format
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
            plot_closed_orbit(data, 'x', plot_dir)

if __name__ == "__main__":
    main(sys.argv[1:])
    input("Done")
