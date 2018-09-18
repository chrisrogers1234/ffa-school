import glob
import os
import json
import ROOT
import xboa.common as common
import utilities
from xboa.hit import Hit

def load_data(file_name):
    fin = open(file_name)
    data = []
    for line in fin.readlines():
        try:
            data.append(json.loads(line))
        except:
            continue
    return data

def plot_da(data, max_n_points, plot_dir):
    variables = utilities.get_substitutions_axis(data)
    for index, item in enumerate(data):
        print item.keys()
        for key in variables:
            variables[key] = item['substitutions'][key]
        for da_key in 'x_da', 'y_da':
            if da_key not in item.keys():
                continue
            for axis1, axis2 in ('x', 'px'), ('y', 'py'), ('x', "x'"), ('y', "y'"):
                canvas = plot_one_da(item, da_key, axis1, axis2, max_n_points, variables)
                plot_name = "da_"+str(index)+"_"+da_key+"_"+axis1+"_"+axis2
                for format in ["eps", "png", "root"]:
                    canvas.Print(plot_dir+"/"+plot_name+"."+format)

def get_da_row(hit_data, max_n_points):
    hit_lengths = [len(hit_list[1]) for hit_list in hit_data]
    da_row = len(hit_lengths)-1
    for i, length in enumerate(hit_lengths):
        if length < max_n_points:
            da_row = i-1
            break
    if da_row < 0:
        da_row = 0
    print hit_lengths, da_row
    return da_row

def get_title(variables):
    title = ""
    for key in variables:
        title += utilities.sub_to_name(key)+": "+str(variables[key])
    return title

def plot_one_da(row_data, da_key, axis1, axis2, max_n_points, variables):
    hit_data = row_data[da_key]
    name = da_key+"_"+axis1+" vs "+axis2
    title = get_title(variables)
    name += " "+title
    canvas = None
    da_row = get_da_row(hit_data, max_n_points)
    graph_list = []
    units = {'x':'mm', 'y':'mm', 'px':'MeV/c', 'py':'MeV/c', "x'":'rad', "y'":'rad'}
    for i, hit_list in enumerate(hit_data):
        hit_list = [Hit.new_from_dict(hit_dict) for hit_dict in hit_list[1]]
        x_data = [hit[axis1] for hit in hit_list]
        y_data = [hit[axis2] for hit in hit_list]
        axis1_label = axis1+" ["+units[axis1]+"]"
        axis2_label = axis2+" ["+units[axis2]+"]"
        hist, graph = common.make_root_graph(name+" "+str(i), x_data, axis1_label, y_data, axis2_label)
        graph.SetMarkerStyle(7)
        if i == da_row:
            canvas = common.make_root_canvas(name)
            hist.SetTitle(title)
            hist.Draw()
            print x_data, y_data
        elif i < da_row:
            graph.SetMarkerColor(ROOT.kGreen)
        else:
            graph.SetMarkerColor(ROOT.kGray)
        graph_list.append(graph)
    for graph in graph_list:
        graph.Draw("SAMEP")
    canvas.Update()
    return canvas

def main():
    base_dir = "output/"
    #base_fname = base_dir+"/baseline/get_da.tmp"
    for file_name in glob.glob(base_dir+"*/get_da.tmp"):
        data = load_data(file_name)
        #if file_name != base_fname:
        #    data += load_data(base_fname)
        plot_dir = os.path.split(file_name)[0]
        plot_da(data, 100, plot_dir)

if __name__ == "__main__":
    main()
    print "Finished - press <CR> to close"
    raw_input()

