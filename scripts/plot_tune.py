import os
import glob
import json
import math
import xboa.common

import utilities

def load_file(file_name):
    fin = open(file_name)
    data = [json.loads(line) for line in fin.readlines()]
    print data[0].keys()
    return data

def plot_data_1d(data, tune_axis, plot_dir, cell_conversion = 1):
    axis_candidates = utilities.get_substitutions_axis(data)
    x_tune = [item['x_tune'] for item in data]
    y_tune = [item['y_tune'] for item in data]
    if cell_conversion != 1:
        x_tune = [nu*cell_conversion - math.floor(nu*cell_conversion) for nu in x_tune]
        y_tune = [nu*cell_conversion - math.floor(nu*cell_conversion) for nu in y_tune]
    for key in axis_candidates:
        x_data = axis_candidates[key]
        x_name = utilities.sub_to_name(key)
        canvas_name = tune_axis+' vs '+x_name
        canvas = xboa.common.make_root_canvas(canvas_name)
        hist, graph = xboa.common.make_root_graph('axes', x_data*2, x_name, x_tune+y_tune, tune_axis)
        hist.Draw()
        hist_x, graph_x = xboa.common.make_root_graph('horizontal tune', x_data, x_name, x_tune, tune_axis)
        hist_y, graph_y = xboa.common.make_root_graph('vertical tune', x_data, x_name, y_tune, tune_axis)
        graph_x.SetMarkerStyle(24)
        graph_x.SetMarkerColor(2)
        graph_y.SetMarkerStyle(26)
        graph_y.SetMarkerColor(4)
        graph_x.Draw("PSAME")
        graph_y.Draw("PSAME")
        legend = xboa.common.make_root_legend(canvas, [graph_x, graph_y])
        legend.Draw()
        canvas.Update()
        canvas_name = canvas_name.replace(" ", "_")
        for format in "eps", "png", "root":
            canvas.Print(plot_dir+"/"+canvas_name+"."+format)
    return

def plot_data_2d(data, tune_axis, plot_dir):
    x_tune = [item['x_tune'] for item in data]
    y_tune = [item['y_tune'] for item in data]
    x_name = "Varying "
    axis_candidates = utilities.get_substitutions_axis(data)
    for key in axis_candidates:
        min_val = str(min(axis_candidates[key]))
        max_val = str(max(axis_candidates[key]))
        x_name += utilities.sub_to_name(key)+" from "+min_val+" to "+max_val
    axis_candidates = utilities.get_substitutions_axis(data)
    canvas = xboa.common.make_root_canvas('tune x vs y')
    hist, graph = xboa.common.make_root_graph('tune x vs y', x_tune, "horizontal tune", y_tune, "vertical tune", xmin=0., xmax=1., ymin=0., ymax=1.)
    hist.SetTitle(x_name)
    hist.Draw()
    #utilities.tune_lines(canvas)
    graph.SetMarkerStyle(24)
    graph.Draw("PSAME")
    canvas.Update()
    for format in "eps", "png", "root":
        canvas.Print(plot_dir+"/tune_x_vs_y."+format)

def main():
    base_fname = "output/baseline/find_tune"
    for file_name in glob.glob("output/*/find_tune"):
        plot_dir = os.path.split(file_name)[0]
        data = load_file(file_name)
        if file_name != base_fname:
            data += load_file("output/baseline/find_tune")
        plot_data_1d(data, 'cell tune', plot_dir, 1) # or ring tune
        plot_data_1d(data, 'ring tune', plot_dir, 24) # or ring tune
        #plot_data_2d(data, 'cell tune', plot_dir) # or ring tune

if __name__ == "__main__":
    main()
    raw_input("Press <CR> to end")
