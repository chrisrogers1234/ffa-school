import sys
import copy
import math
import glob
import os
import json
import numpy
import scipy.spatial
import matplotlib

import xboa.common as common
import xboa.common.matplotlib_wrapper as matplotlib_wrapper
from xboa.hit import Hit
from xboa.algorithms.tune import DPhiTuneFinder

from utils import utilities

def load_data(file_name):
    fin = open(file_name)
    data = []
    for line in fin.readlines():
        try:
            data.append(json.loads(line))
        except:
            continue
    print("Loaded", len(data), "lines")
    return data

def polar(point):
    polar = [math.atan2(point[1], point[0]),
             (point[0]**2+point[1]**2)**0.5]
    return polar


def centre(points_cartesian):
    mean = [
        numpy.mean([point[0] for point in points_cartesian]),
        numpy.mean([point[1] for point in points_cartesian])
    ]
    points_cartesian -= mean
    return points_cartesian

def calculate_da(row_data, da_key, n_points):
    axis1, axis2 = {"x_da":("x", "x'"), "y_da":("y", "y'")}[da_key]
    points = []
    mass = common.pdg_pid_to_mass[2212]
    hit_list = []
    for i, tmp_list in enumerate(row_data[da_key]):
        print(len(tmp_list), tmp_list[0])
        # hit_list[0] is the x/y offset in mm; hit_list[1] is the corresponding
        # set of probe hits
        if len(tmp_list[1]) < n_points:
            break
        hit_list = tmp_list
    hit_list = [Hit.new_from_dict(hit_dict) for hit_dict in hit_list[1]]
    points = numpy.array([[hit[axis1], hit[axis2]] for hit in hit_list])
    x_list = [hit[axis1] for hit in hit_list]
    print(min(x_list), max(x_list))
    y_list = [hit[axis2] for hit in hit_list]
    print(min(y_list), max(y_list))
    pz = hit_list[0]['pz']
    print(math.pi*(max(x_list)-min(x_list))*(max(y_list)-min(y_list))/4.*mass/pz)
    if len(points):
        geometric_acceptance = get_area(points)/math.pi
        # beta gamma * geometric emittance
        normalised_acceptance = geometric_acceptance*pz/mass
        return normalised_acceptance
    else:
        return 0.

def get_area(points_cartesian):
    points_cartesian = centre(points_cartesian)
    points_polar = [polar(point) for point in points_cartesian]
    points_polar = numpy.array(sorted(points_polar))
    area = 0.
    for i, point_1 in enumerate(points_polar[1:]):
        point_0 = points_polar[i]
        # triangle with base length r0 and height r1 sin phi
        phi = point_1[0] - point_0[0]
        h = point_1[1]*math.sin(phi)
        delta_area = 0.5*point_0[1]*h
        area += delta_area
    phi_first = 2.*math.pi+points_polar[0, 0]-points_polar[-1, 0]
    delta_area = 0.5*points_polar[0, 1]*math.sin(phi_first)*points_polar[-1, 1]
    area += delta_area
    return area

def plot_da(data, max_n_points, plot_dir, acceptance):
    variables = utilities.get_substitutions_axis(data)
    plot_dir = os.path.join(plot_dir, "find_da")
    utilities.clear_dir(plot_dir)
    for index, item in enumerate(data):
        for key in variables:
            variables[key] = item['substitutions'][key]
        for da_key in 'y_da', 'x_da': 
            if da_key not in list(item.keys()):
                print("Did not find", da_key, "in keys", list(item.keys()), "... skipping")
                continue
            for axis1, axis2 in ('x', "x'"), ('y', "y'"):
                fig_index = plot_one_da(item, da_key, axis1, axis2, max_n_points, variables, acceptance)
                plot_name = "da_"+str(index)+"_"+da_key+"_"+axis1+"_"+axis2
                for format in ["png"]:
                    matplotlib.pyplot.savefig(plot_dir+"/"+plot_name+"."+format)
                if axis1[0] not in da_key:
                    continue

def get_da_row(hit_data, max_n_points):
    hit_lengths = [len(hit_list[1]) for hit_list in hit_data]
    da_row = len(hit_lengths)-1
    for i, length in enumerate(hit_lengths):
        if length < max_n_points:
            da_row = i-1
            break
    if da_row < 0:
        da_row = 0
    return da_row

def get_title(variables):
    title = ""
    for key in variables:
        title += utilities.sub_to_name(key)+": "+str(variables[key])
    return title

def get_color(row, da_row):
    if row == da_row:
        return 'black'
    elif row < da_row:
        return 'lime'
    else:
        return 'lightgrey'

def plot_one_da(row_data, da_key, axis1, axis2, max_n_points, variables, acceptance):
    hit_data = row_data[da_key]
    name = da_key+"_"+axis1+" vs "+axis2
    title = get_title(variables)
    name += " "+title
    canvas = None
    da_row = get_da_row(hit_data, max_n_points)
    graph_list = []
    acceptance_graph = None
    units = {'x':'mm', 'y':'mm', 'px':'MeV/c', 'py':'MeV/c', "x'":'rad', "y'":'rad'}
    fig_index = None
    for i, hit_list in enumerate(hit_data):
        hit_list = [Hit.new_from_dict(hit_dict) for hit_dict in hit_list[1]]
        x_data = [hit[axis1] for hit in hit_list]
        y_data = [hit[axis2] for hit in hit_list]
        axis1_label = axis1+" ["+units[axis1]+"]"
        axis2_label = axis2+" ["+units[axis2]+"]"
        fig_index = matplotlib_wrapper.make_scatter(x_data, axis1_label,
                                                y_data, axis2_label,
                                                fig_index=fig_index,
                                                kwds={"color":get_color(i, da_row)})
        if i == da_row:
            matplotlib.pyplot.autoscale(enable=True)
            matplotlib.pyplot.autoscale(enable=False)
    return canvas

def main(file_name_list):
    for file_name_glob in file_name_list:
        for file_name in glob.glob(file_name_glob):
            data = load_data(file_name)
            plot_dir = os.path.split(file_name)[0]
            # acceptance should be normalised mm mrad
            plot_da(data, 50, plot_dir, 2.7*1e-3*math.pi)

if __name__ == "__main__":
    main(sys.argv[1:])
    print("Finished - press <CR> to close")
    input()

