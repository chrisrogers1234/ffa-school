"""
Plot a single closed orbit (once tracking has finished)
"""

import os
import sys
import copy
import math
import numpy
import matplotlib
import xboa.common.matplotlib_wrapper as matplotlib_wrapper

from utils import utilities
import plotting.plot_dump_fields as plot_dump_fields

MASS = 938.2720813

class Colors:
    ref_colours = numpy.array(["red", "orange", "darkkhaki", 
                          "green", "darkcyan", "blue", "darkviolet", "magenta"])
    colours = copy.deepcopy(ref_colours)

    @classmethod
    def next(cls):
        a_colour = cls.colours[0]
        cls.colours = numpy.roll(cls.colours, 1)
        return a_colour
    
    @classmethod
    def reset(cls):
        cls.colours = copy.deepcopy(cls.ref_colours)

def r_phi_track_file(data):
    data = copy.deepcopy(data)
    data["r"] = list(range(len(data["x"])))
    data["phi"] = list(range(len(data["x"])))
    data["pr"] = list(range(len(data["x"])))
    data["pphi"] = list(range(len(data["x"])))
    for i in range(len(data["r"])):
        data["r"][i] = (data["x"][i]**2+data["y"][i]**2.)**0.5
        phi = math.atan2(data["y"][i], data["x"][i])
        data["phi"][i] = math.degrees(phi)
        p = (data["px"][i]**2+data["py"][i]**2)**0.5
        data["pr"][i] = p*math.sin(phi)
        data["pphi"][i] = p*math.cos(phi)
    return data

def parse_file(file_name, heading, types):
    if len(heading) != len(types):
        raise KeyError("Heading mismatched to types in parse_file "+file_name)
    fin = open(file_name)
    line = fin.readline()
    data = {}
    for item in heading:
        data[item] = []
    line = fin.readline()[:-1]
    while line != "":
        words = line.split()
        if len(words) != len(heading):
            print("Line\n  "+line+"\nmismatched to heading\n  "+str(heading)+"\nin parse_file "+file_name)
        else:
            words = [types[i](x) for i, x in enumerate(words)]
            for i, item in enumerate(heading):
                data[item].append(words[i])
        line = fin.readline()[:-1]
    print("Got data from file "+file_name)
    return data

def parse_track_file(filename):
    file_name = filename
    heading = ["id", "x", "px", "y", "py", "z", "pz"]#, "bx", "by", "bz", "ex", "ey", "ez"]
    types = [str]+[float]*(len(heading)-1)
    data = parse_file(file_name, heading, types)
    data["px"] = [px*MASS for px in data["px"]]
    data["py"] = [py*MASS for py in data["py"]]
        
    data = r_phi_track_file(data)
    return data

def load_track_orbit(file_name):
    fin = open(file_name)
    step_list = []
    for i, line in enumerate(fin.readlines()):
        if i < 2:
          continue
        words = line.split()
        step = {}
        step["particle_index"] = int(words[0][2:])
        step["x_pos"] = float(words[1])
        step["beta_x_gamma"] = float(words[2])
        step["y_pos"] = float(words[3])
        step["beta_y_gamma"] = float(words[4])
        step["z_pos"] = float(words[5])
        step["beta_z_gamma"] = float(words[6])
        step_list.append(step)
    return step_list

def plot_x_y_projection(step_list, fig_index = None):
    axes = None
    fig_index = matplotlib_wrapper.make_graph(step_list["x"], "x [mm]",
                                              step_list["y"], "y [mm]",
                                              sort=False, fig_index=fig_index)
    return fig_index

def plot_r_phi_projection(step_list, fig_index = None):
    points = list(zip(step_list["phi"], step_list["r"]))
    points = sorted(points)
    phi_points = [p[0] for p in points]
    r_points = [p[1] for p in points]
    fig_index = matplotlib_wrapper.make_graph(phi_points, "$\phi$ [$^{\circ}$]",
                                              r_points, "r [mm]",
                                              sort=False, fig_index=fig_index,
                                              kwds={"color":next(Colors)})
    return fig_index

def plot_x_z_projection(step_list, fig_index = None):
    points = list(zip(step_list["phi"], step_list["z"]))
    points = sorted(points)
    phi_points = [p[0] for p in points]
    r_points = [p[1] for p in points]
    fig_index = matplotlib_wrapper.make_graph(phi_points, "$\phi$ [$^{\circ}$]",
                                              r_points, "z [mm]",
                                              sort=False, fig_index=fig_index,
                                              kwds={"color":next(Colors)})
    return fig_index

def plot_beam_pipe(inner_radius, outer_radius, n_periods, fig_index=None):
    n_steps = 361 # number of azimuthal steps
    dt = 2.*math.pi/float(n_steps-1)
    x_inner = [inner_radius*math.sin(i*dt) for i in range(n_steps)]
    y_inner = [inner_radius*math.cos(i*dt) for i in range(n_steps)]
    options = {
        "linewidth":0.5,
        "color":"grey"
    }
    fig_index = matplotlib_wrapper.make_graph(x_inner, "",
                                              y_inner, "",
                                              sort=False, fig_index=fig_index,
                                              kwds=options)

    x_outer = [outer_radius*math.sin(i*dt) for i in range(n_steps)]
    y_outer = [outer_radius*math.cos(i*dt) for i in range(n_steps)]
    fig_index = matplotlib_wrapper.make_graph(x_outer, "",
                                              y_outer, "",
                                              sort=False, fig_index=fig_index,
                                              kwds=options)

    dt = 2.*math.pi/float(n_periods)
    for i in range(n_periods):
        x_list = [inner_radius*math.sin(i*dt), outer_radius*math.sin(i*dt)]
        y_list = [inner_radius*math.cos(i*dt), outer_radius*math.cos(i*dt)]
        fig_index = matplotlib_wrapper.make_graph(x_list, "",
                                                  y_list, "",
                                                  sort=False,
                                                  fig_index=fig_index,
                                                  kwds=options)
    return fig_index

def plot_cylindrical(output_dir, opal_run_dir, step_list_of_lists):
    field_plot = plot_dump_fields.PlotDumpFields(opal_run_dir+"FieldMapRPHI.dat", True)
    field_plot.load_dump_fields()
    try:
        canvas_1d , hist, graph = field_plot.plot_1d({"r":4.}, "phi", "bz")
        for format in ["png"]:
            canvas_1d.Print(output_dir+"bz_1d."+format)
        Colors.reset()
    except Exception:
        sys.excepthook(*sys.exc_info())
    
    canvas_bz_offset = field_plot.plot_dump_fields("phi", "r", "bz")
    for step_list in step_list_of_lists:
        plot_r_phi_projection(step_list, canvas_bz_offset)
    for format in ["png"]:
        canvas_bz_offset.Print(output_dir+"closed_orbit_cylindrical_bz."+format)
    Colors.reset()

    canvas_br_offset = field_plot.plot_dump_fields("phi", "r", "br")
    for step_list in step_list_of_lists:
        plot_r_phi_projection(step_list, canvas_br_offset)
    for format in ["png"]:
        canvas_br_offset.Print(output_dir+"closed_orbit_cylindrical_br."+format)
    Colors.reset()

    canvas_bphi_offset = field_plot.plot_dump_fields("phi", "r", "bphi")
    for step_list in step_list_of_lists:
        plot_r_phi_projection(step_list, canvas_bphi_offset)
    for format in ["png"]:
        canvas_bphi_offset.Print(output_dir+"closed_orbit_cylindrical_bphi."+format)
    Colors.reset()

    canvas_bphi_offset = field_plot.plot_dump_fields("phi", "r", "bx")
    for step_list in step_list_of_lists:
        plot_r_phi_projection(step_list, canvas_bphi_offset)
    for format in ["png"]:
        canvas_bphi_offset.Print(output_dir+"closed_orbit_cylindrical_bx."+format)
    Colors.reset()

    canvas_bphi_offset = field_plot.plot_dump_fields("phi", "r", "by")
    for step_list in step_list_of_lists:
        plot_r_phi_projection(step_list, canvas_bphi_offset)
    for format in ["png"]:
        canvas_bphi_offset.Print(output_dir+"closed_orbit_cylindrical_by."+format)
    Colors.reset()

    for step_list in step_list_of_lists:
        canvas, axes, graph = plot_x_z_projection(step_list)
    for format in ["png"]:
        canvas.Print(output_dir+"closed_orbit_elevation."+format)
    Colors.reset()

def plot_zoom(output_dir, opal_run_dir, step_list_of_lists):
    field_plot = plot_dump_fields.PlotDumpFields(opal_run_dir+"FieldMapXY-zoom.dat")
    field_plot.load_dump_fields()

    canvas = field_plot.plot_dump_fields("x", "y", "bz")
    for step_list in step_list_of_lists:
        canvas, axes, graph = plot_x_y_projection(step_list, canvas)
    plot_beam_pipe(2.7, 3.7, 12, canvas)
    for format in ["png"]:
        canvas.Print(output_dir+"closed_orbit_plan-zoom."+format)

def plot_cartesian(output_dir, opal_run_dir, step_list):
    field_plot = plot_dump_fields.PlotDumpFields(opal_run_dir+"FieldMapXY.dat")
    field_plot.load_dump_fields()
    inner_radius, outer_radius, ncells = 3., 5., 60

    fig_index = field_plot.plot_dump_fields("x", "y", "bz")
    fig_index = plot_beam_pipe(inner_radius, outer_radius, ncells, fig_index)
    fig_index = plot_x_y_projection(step_list, fig_index)
    for format in ["png"]:
        matplotlib.pyplot.savefig(output_dir+"closed_orbit_plan_bz."+format)
    return
    canvas = field_plot.plot_dump_fields("x", "y", "bx")
    canvas, axes, graph = plot_x_y_projection(step_list, canvas)
    plot_beam_pipe(inner_radius, outer_radius, ncells, canvas)
    for format in ["png"]:
        canvas.Print(output_dir+"closed_orbit_cartesian_bx."+format)

    canvas = field_plot.plot_dump_fields("x", "y", "by")
    canvas, axes, graph = plot_x_y_projection(step_list, canvas)
    plot_beam_pipe(inner_radius, outer_radius, ncells, canvas)
    for format in ["png"]:
        canvas.Print(output_dir+"closed_orbit_cartesian_by."+format)

    canvas = field_plot.plot_dump_fields("x", "y", "br")
    canvas, axes, graph = plot_x_y_projection(step_list, canvas)
    plot_beam_pipe(inner_radius, outer_radius, ncells, canvas)
    for format in ["png"]:
        canvas.Print(output_dir+"closed_orbit_cartesian_br."+format)

    canvas = field_plot.plot_dump_fields("x", "y", "bphi")
    canvas, axes, graph = plot_x_y_projection(step_list, canvas)
    plot_beam_pipe(inner_radius, outer_radius, ncells, canvas)
    for format in ["png"]:
        canvas.Print(output_dir+"closed_orbit_cartesian_bphi."+format)

def print_track(tgt_phi, step_list_of_lists):
    for step_list in step_list_of_lists:
        for i, phi in enumerate(step_list['phi']):
            if phi > tgt_phi:
                break
        print("step list item", i)
        for key in sorted(step_list):
            print("    ", key, step_list[key][i])
        print(step_list['pr'][i]**2+step_list['pphi'][i]**2)
        print(step_list['px'][i]**2+step_list['py'][i]**2)
        print()

def main(output_dir, run_dir, run_file_list):
    output_dir += "/"
    opal_run_dir = output_dir+run_dir
    step_list_of_lists = []
    for run_file in run_file_list:
        step_list_of_lists.append(parse_track_file(opal_run_dir+run_file))
    #plot_cylindrical(output_dir, opal_run_dir, step_list_of_lists)
    #print_track(0.1*360./15, step_list_of_lists)
    #try:
    #    plot_zoom(output_dir, opal_run_dir, step_list)
    #except Exception:
    #    sys.excepthook(*sys.exc_info())
    try:
        plot_cartesian(output_dir, opal_run_dir, step_list_of_lists[0])
    except Exception:
        sys.excepthook(*sys.exc_info())

if __name__ == "__main__":
    output_dir = os.path.split(sys.argv[1])[0]
    run_dir = ""
    run_file_list = [os.path.split(arg)[1] for arg in sys.argv[1:]]
    main(output_dir, run_dir, run_file_list)

