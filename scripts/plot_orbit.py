"""
Plot a single closed orbit (once tracking has finished)
"""

import sys
import copy
import math
import numpy
import plot_dump_fields

try:
    import ROOT
except ImportError:
    print "You need to install PyROOT to run this example."

class RootObjects:
    histograms = []
    canvases = []
    graphs = []


def r_phi_track_file(data):
    data = copy.deepcopy(data)
    data["r"] = range(len(data["x"]))
    data["phi"] = range(len(data["x"]))
    for i in range(len(data["r"])):
        data["r"][i] = (data["x"][i]**2+data["y"][i]**2.)**0.5
        data["phi"][i] = math.degrees(math.atan2(data["x"][i], data["y"][i]))
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
            print "Line\n  "+line+"\nmismatched to heading\n  "+str(heading)+"\nin parse_file "+file_name
        else:
            words = [types[i](x) for i, x in enumerate(words)]
            for i, item in enumerate(heading):
                data[item].append(words[i])
        line = fin.readline()[:-1]
    print "Got data from file "+file_name
    return data

def parse_track_file(filename):
    file_name = filename
    heading = ["id", "x", "px", "y", "py", "z", "pz"]
    types = [str]+[float]*(len(heading)-1)
    data = parse_file(file_name, heading, types)
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

def plot_x_y_projection(step_list, canvas = None):
    axes = None
    if canvas == None:
        canvas = ROOT.TCanvas("x_y_projection", "x_y_projection")
        canvas.Draw()
        axes = ROOT.TH2D("x_y_projection_axes", ";x [m];y [m]",
                         1000, -25., 25.,
                         1000, -25., 25.)
        axes.SetStats(False)
        axes.Draw()
        RootObjects.histograms.append(axes)
    else:
        canvas.cd()
    graph = ROOT.TGraph(len(step_list))
    for i in range(len(step_list["x"])):
        graph.SetPoint(i, step_list["x"][i], step_list["y"][i])
    graph.Draw("l")
    canvas.Update()
    RootObjects.canvases.append(canvas)
    RootObjects.graphs.append(graph)
    return canvas, axes, graph

def plot_r_phi_projection(step_list, canvas = None):
    axes = None
    if canvas == None:
        canvas = ROOT.TCanvas("x_y_projection", "x_y_projection")
        canvas.Draw()
        axes = ROOT.TH2D("x_y_projection_axes", ";#phi [degree];r [m]",
                         1000, -180., 180.,
                         1000, 1., 4.)
        axes.SetStats(False)
        axes.Draw()
        RootObjects.histograms.append(axes)
    else:
        canvas.cd()
    graph = ROOT.TGraph(len(step_list))
    points = zip(step_list["phi"], step_list["r"])
    points = sorted(points)
    for i in range(len(step_list["r"])):
        graph.SetPoint(i, points[i][0], points[i][1])
    graph.Draw("p")
    canvas.Update()
    RootObjects.canvases.append(canvas)
    RootObjects.graphs.append(graph)
    return canvas, axes, graph

def plot_x_z_projection(step_list):
    canvas = ROOT.TCanvas("x_z_projection", "x_z_projection")
    axes = ROOT.TH2D("x_z_projection_axes", ";phi [rad];z [m]",
                     1000, -math.pi, math.pi,
                     1000, -0.20, 0.20)
    axes.SetStats(False)
    graph = ROOT.TGraph(len(step_list))
    canvas.Draw()
    axes.Draw()
    for i in range(len(step_list["x"])):
        graph.SetPoint(i, math.atan2(step_list["y"][i], step_list["x"][i]), step_list["z"][i])
    graph.Draw("l")
    canvas.Update()
    RootObjects.histograms.append(axes)
    RootObjects.canvases.append(canvas)
    RootObjects.graphs.append(graph)
    return canvas, axes, graph

def step_statistics(step_list):
    delta_r_list = []
    for i in range(len(step_list["x"])-1):
        delta_x = step_list["x"][i+1]-step_list["x"][i]
        delta_y = step_list["y"][i+1]-step_list["y"][i]
        delta_z = step_list["z"][i+1]-step_list["z"][i]
        delta_r_list.append((delta_x**2+delta_y**2+delta_z**2)**0.5)
    print "Mean step size:", numpy.mean(delta_r_list), "RMS:", numpy.std(delta_r_list)

def plot_beam_pipe(inner_radius, outer_radius, n_periods, canvas=None):
    n_steps = 361 # number of azimuthal steps

    if canvas == None:
        canvas = ROOT.TCanvas("beam_pipe", "beam_pipe")
        canvas.Draw()
        axes = ROOT.TH2D("beam_pipe_axes", ";x [mm];y [mm]",
                         1000, -25., 25.,
                         1000, -25., 25.)
        axes.Draw()
        RootObjects.histograms.append(axes)
        RootObjects.canvases.append(canvas)
    canvas.cd()
    graph_inner = ROOT.TGraph(n_steps)
    graph_outer = ROOT.TGraph(n_steps)
    for i in range(n_steps):
        graph_inner.SetPoint(i,
                             inner_radius*math.sin(i/float(n_steps-1)*2.*math.pi),
                             inner_radius*math.cos(i/float(n_steps-1)*2.*math.pi))
        graph_outer.SetPoint(i,
                             outer_radius*math.sin(i/float(n_steps-1)*2.*math.pi),
                             outer_radius*math.cos(i/float(n_steps-1)*2.*math.pi))
    for i in range(n_periods):
        graph = ROOT.TGraph(2)
        graph.SetPoint(0,
                       inner_radius*math.sin(i/float(n_periods)*2.*math.pi),
                       inner_radius*math.cos(i/float(n_periods)*2.*math.pi))
        graph.SetPoint(1,
                       outer_radius*math.sin(i/float(n_periods)*2.*math.pi),
                       outer_radius*math.cos(i/float(n_periods)*2.*math.pi))
        graph.Draw("l")
        RootObjects.graphs.append(graph)
    graph_inner.Draw("l")
    graph_outer.Draw("l")
    canvas.Update()
    RootObjects.graphs.append(graph_inner)
    RootObjects.graphs.append(graph_outer)

def plot_b_field(step_list):
    canvas = ROOT.TCanvas("bfield", "bfield")
    axes = ROOT.TH2D("bfield_axes", ";phi [rad];b [T]",
                     1000, -2.*math.pi, 2.*math.pi,
                     1000, -25., 25.)
    axes.SetStats(False)
    graph = ROOT.TGraph(len(step_list))
    canvas.Draw()
    axes.Draw()
    for i, step in enumerate(step_list):
        graph.SetPoint(i, step["x_pos"], step["y_pos"])
    graph.Draw("l")
    canvas.Update()
    RootObjects.histograms.append(axes)
    RootObjects.canvases.append(canvas)
    RootObjects.graphs.append(graph)
    return canvas, axes, graph

def scrape_vector(line):
    vector = line.split("(")[1]
    vector = vector.split(")")[0]
    vector = [float(number)/1000. for number in vector.split(",")]
    return vector

def get_elements(log_file):
    log_file = open(log_file)
    start_positions = []
    for line in log_file.readlines():
        if "Start position (" not in line:
            continue
        start_positions.append(scrape_vector(line))
    return start_positions
  
def plot_elements_xz(log_file, canvas):
    start_positions = get_elements(log_file)
    canvas.cd()
    graph = ROOT.TGraph(len(start_positions))
    for i, pos in enumerate(start_positions):
        phi = math.atan2(pos[1], pos[0])
        graph.SetPoint(i, phi, pos[2])
    RootObjects.graphs.append(graph)
    graph.SetMarkerStyle(7)
    graph.Draw("PSAME")
    canvas.Update()
    return graph

def plot_elements_xy(log_file, canvas):
    start_positions = get_elements(log_file)
    canvas.cd()
    graph = ROOT.TGraph(len(start_positions))
    for i, pos in enumerate(start_positions):
        graph.SetPoint(i, pos[0], pos[1])
    RootObjects.graphs.append(graph)
    graph.SetMarkerStyle(7)
    graph.Draw("PSAME")
    canvas.Update()
    return graph

def plot_cylindrical(output_dir, opal_run_dir, step_list):
    field_plot = plot_dump_fields.PlotDumpFields(opal_run_dir+"FieldMapRPHI.dat", True)
    field_plot.load_dump_fields()
    canvas_1d = field_plot.plot_1d({"r":4.}, "phi", "bz")
    for format in "png", "root", "eps":
        canvas_1d.Print(output_dir+"bz_1d."+format)
    
    canvas_bz_offset = field_plot.plot_dump_fields("phi", "r", "bz")
    plot_r_phi_projection(step_list, canvas_bz_offset)
    for format in "png", "root", "eps":
        canvas_bz_offset.Print(output_dir+"closed_orbit_cylindrical_bz."+format)
    canvas_br_offset = field_plot.plot_dump_fields("phi", "r", "br")
    plot_r_phi_projection(step_list, canvas_br_offset)
    for format in "png", "root", "eps":
        canvas_br_offset.Print(output_dir+"closed_orbit_cylindrical_br."+format)
    canvas_bphi_offset = field_plot.plot_dump_fields("phi", "r", "bphi")
    plot_r_phi_projection(step_list, canvas_bphi_offset)
    for format in "png", "root", "eps":
        canvas_bphi_offset.Print(output_dir+"closed_orbit_cylindrical_bphi."+format)

    canvas_bphi_offset = field_plot.plot_dump_fields("phi", "r", "bx")
    plot_r_phi_projection(step_list, canvas_bphi_offset)
    for format in "png", "root", "eps":
        canvas_bphi_offset.Print(output_dir+"closed_orbit_cylindrical_bx."+format)

    canvas_bphi_offset = field_plot.plot_dump_fields("phi", "r", "by")
    plot_r_phi_projection(step_list, canvas_bphi_offset)
    for format in "png", "root", "eps":
        canvas_bphi_offset.Print(output_dir+"closed_orbit_cylindrical_by."+format)

    canvas, axes, graph = plot_x_z_projection(step_list)
    #plot_elements_xz(opal_run_dir+"log", canvas)
    for format in "png", "root", "eps":
        canvas.Print(output_dir+"closed_orbit_elevation."+format)

def plot_zoom(output_dir, opal_run_dir, step_list):
    field_plot = plot_dump_fields.PlotDumpFields(opal_run_dir+"FieldMapXY-zoom.dat")
    field_plot.load_dump_fields()

    canvas = field_plot.plot_dump_fields("x", "y", "bz")
    canvas, axes, graph = plot_x_y_projection(step_list, canvas)
    plot_beam_pipe(2.7, 3.7, 12, canvas)
    #plot_elements_xy(opal_run_dir+"log", canvas)
    for format in "png", "root", "eps":
        canvas.Print(output_dir+"closed_orbit_plan-zoom."+format)

def plot_cartesian(output_dir, opal_run_dir, step_list):
    field_plot = plot_dump_fields.PlotDumpFields(opal_run_dir+"FieldMapXY.dat")
    field_plot.load_dump_fields()

    canvas = field_plot.plot_dump_fields("x", "y", "bz")
    canvas, axes, graph = plot_x_y_projection(step_list, canvas)
    plot_beam_pipe(2.7, 3.7, 12, canvas)
    #plot_elements_xy(opal_run_dir+"log", canvas)
    for format in "png", "root", "eps":
        canvas.Print(output_dir+"closed_orbit_plan_bz."+format)

    canvas = field_plot.plot_dump_fields("x", "y", "bx")
    canvas, axes, graph = plot_x_y_projection(step_list, canvas)
    plot_beam_pipe(2.7, 3.7, 12, canvas)
    #plot_elements_xy(opal_run_dir+"log", canvas)
    for format in "png", "root", "eps":
        canvas.Print(output_dir+"closed_orbit_cartesian_bx."+format)

    canvas = field_plot.plot_dump_fields("x", "y", "by")
    canvas, axes, graph = plot_x_y_projection(step_list, canvas)
    plot_beam_pipe(2.7, 3.7, 12, canvas)
    #plot_elements_xy(opal_run_dir+"log", canvas)
    for format in "png", "root", "eps":
        canvas.Print(output_dir+"closed_orbit_cartesian_by."+format)

    canvas = field_plot.plot_dump_fields("x", "y", "br")
    canvas, axes, graph = plot_x_y_projection(step_list, canvas)
    plot_beam_pipe(2.7, 3.7, 12, canvas)
    #plot_elements_xy(opal_run_dir+"log", canvas)
    for format in "png", "root", "eps":
        canvas.Print(output_dir+"closed_orbit_cartesian_br."+format)

    canvas = field_plot.plot_dump_fields("x", "y", "bphi")
    canvas, axes, graph = plot_x_y_projection(step_list, canvas)
    plot_beam_pipe(2.7, 3.7, 12, canvas)
    #plot_elements_xy(opal_run_dir+"log", canvas)
    for format in "png", "root", "eps":
        canvas.Print(output_dir+"closed_orbit_cartesian_bphi."+format)

def main(output_dir, run_dir, run_file):
    output_dir += "/"
    opal_run_dir = output_dir+run_dir
    step_list = parse_track_file(opal_run_dir+run_file)
    try:
        plot_cylindrical(output_dir, opal_run_dir, step_list)
    except Exception:
        sys.excepthook(*sys.exc_info())
    try:
        plot_zoom(output_dir, opal_run_dir, step_list)
    except Exception:
        sys.excepthook(*sys.exc_info())
    try:
        plot_cartesian(output_dir, opal_run_dir, step_list)
    except Exception:
        sys.excepthook(*sys.exc_info())

    step_statistics(step_list)

if __name__ == "__main__":
    output_dir = "reference/reference/"
    run_dir = "tmp/find_closed_orbits/"
    run_file = "SectorFFAGMagnet-trackOrbit.dat"
    main(output_dir, run_dir, run_file)
    raw_input()

