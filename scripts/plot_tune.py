import os
import glob
import json
import math
import xboa.common
import numpy

import utilities

def load_file(file_name):
    fin = open(file_name)
    data = [json.loads(line) for line in fin.readlines()]
    return data

def clean_tune_data(data, verbose=False):
    old_mean = 0
    old_std = 0
    keep_going = True
    my_data = [(0, item) for item in data if abs(item) > 1e-19]
    while keep_going:
        data_tmp = [value for delta, value in my_data]
        mean = numpy.mean(data_tmp)
        std = numpy.std(data_tmp)
        if verbose:
            print len(my_data), mean, std, abs(std - old_std)/std, abs(mean - old_mean)/std
        if verbose:
            print keep_going
        old_std = std
        old_mean = mean
        my_data = [(abs(value - mean), value) for delta, value in my_data]
        my_data = sorted(my_data)
        if verbose:
            print "   ", my_data[-3:]
        keep_going = len(my_data) > 2 and my_data[-1][0] > 2*std
        my_data = my_data[:-1]
    my_data = [item[1] for item in my_data]
    if verbose:
        print "DATA IN",  sorted(data)
        print "DATA OUT", my_data
        print "MEAN", numpy.mean(my_data)
    return my_data
        

def plot_data_1d(data, tune_axis, plot_dir, cell_conversion = 1):
    axis_candidates = utilities.get_substitutions_axis(data)
    my_axes_x = dict([(key, []) for key in axis_candidates])
    my_axes_y = dict([(key, []) for key in axis_candidates])
    x_tune, y_tune = [], []
    for item in data:
        x_dphi = clean_tune_data(item['x_dphi'])
        verbose = '__energy__' in my_axes_y.keys() and abs(item['substitutions']['__energy__']-650) < 1.
        y_dphi = clean_tune_data(item['y_dphi'], verbose)
        if verbose:
            print "X DPHI", sorted(x_dphi)
            print "Y DPHI", sorted(y_dphi)
        x_dphi = [numpy.mean(x_dphi)]
        y_dphi = [numpy.mean(y_dphi)]
        x_tune += x_dphi
        y_tune += y_dphi
        for key in my_axes_x:
            my_axes_x[key] += [item['substitutions'][key] for dphi in x_dphi]
            my_axes_y[key] += [item['substitutions'][key] for dphi in y_dphi]

    if cell_conversion != 1:
        x_tune = [nu*cell_conversion - math.floor(nu*cell_conversion) for nu in x_tune]
        y_tune = [nu*cell_conversion - math.floor(nu*cell_conversion) for nu in y_tune]
    for key in axis_candidates:
        x_ordinate = my_axes_x[key]
        y_ordinate = my_axes_y[key]
        print len(x_ordinate), len(y_ordinate), len(x_tune), len(y_tune)
        x_name = utilities.sub_to_name(key)
        canvas_name = tune_axis+' vs '+x_name
        canvas = xboa.common.make_root_canvas(canvas_name)
        hist, graph = xboa.common.make_root_graph('axes', x_ordinate+y_ordinate, x_name, x_tune+y_tune, tune_axis)
        hist.Draw()
        hist_x, graph_x = xboa.common.make_root_graph('horizontal tune', x_ordinate, x_name, x_tune, tune_axis)
        hist_y, graph_y = xboa.common.make_root_graph('vertical tune', y_ordinate, x_name, y_tune, tune_axis)
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
    for file_name in glob.glob("output/end_length/find_tune"):
        plot_dir = os.path.split(file_name)[0]
        try:
            data = load_file(file_name)
        except IndexError:
            continue
        plot_data_1d(data, 'cell tune', plot_dir, 1) # or ring tune

if __name__ == "__main__":
    main()
    raw_input("Press <CR> to end")
