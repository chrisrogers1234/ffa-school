import glob
import os
import json
import sys

import xboa.common as common

import utilities

def load_file(file_name):
    fin = open(file_name)
    data_out = []
    for line in fin.readlines():
        data_out.append(json.loads(line))
    return data_out

def plot_closed_orbit(data, co_axis, plot_dir):
    print "\nclosed orbit",
    axis_candidates = utilities.get_substitutions_axis(data)
    for key in axis_candidates:
        sys.stdout.flush()
        x_name = utilities.sub_to_name(key)
        x_list = axis_candidates[key]
        y_list = [item["hits"][0][co_axis] for item in data]
        canvas = common.make_root_canvas("closed orbit")
        hist, graph = common.make_root_graph("closed orbit", x_list, x_name, y_list, "Radial position [mm]")
        hist.Draw()
        graph.SetMarkerStyle(4)
        graph.Draw("psame")
        canvas.Update()
        for format in "eps", "png", "root":
            canvas.Print(plot_dir+"/"+co_axis+"_closed_orbit."+format)

def main():
    for file_name in glob.glob("iteration_1/2017-08-16_output_bkp/*/find_closed*"):
        plot_dir = os.path.split(file_name)[0]
        print file_name
        data = load_file(file_name)
        if len(data) == 0:
            continue
        plot_closed_orbit(data, 'x', plot_dir) # or ring tune
    

if __name__ == "__main__":
    main()
    raw_input("Done")
