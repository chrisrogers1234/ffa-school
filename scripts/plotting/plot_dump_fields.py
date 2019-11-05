import sys
import os
import math
import glob
import numpy.fft
import ROOT

class PlotDumpFields(object):
    def __init__(self, file_name, is_em_field = False):
        if is_em_field:
            self.keys = ["r", "phi", "z", "t", "br", "bphi", "bz", "er", "ephi", "ez"]
        else:
            self.keys = ["x", "y", "z", "bx", "by", "bz"]
        self.units = {"bx":0.1, "by":0.1, "bz":0.1, "br":0.1, "bphi":0.1, "bz":0.1}
        self.n_lines = 0
        self.file_name = file_name
        self.field_map = {}
        self.field_grid = {}
        
    def plot(self):
        self.load_dump_fields()
        print(self.keys)
        if "r" in self.keys:
            canvas_xy = self.plot_dump_fields("phi", "r", "bz")
        else:
            canvas_xy = self.plot_dump_fields("x", "y", "bz")
            canvas_xy.Print("bz_vs_x-y.png")
            canvas_xy = self.plot_dump_fields("x", "y", "bx")
            canvas_xy.Print("bx_vs_x-y.png")
            canvas_xy = self.plot_dump_fields("x", "y", "by")
            canvas_xy.Print("by_vs_x-y.png")
        return canvas_xy

    def plot_1d(self, cuts, ax1, ax2):
        value1, value2 = [], []
        n_points = len(list(self.field_map.values())[0])
        for i in range(n_points):
            is_cut = False
            for cut_key, cut_value in cuts.items():
                if abs(self.field_map[cut_key][i] - cut_value) > 1e-3:
                    is_cut = True
            if is_cut:
                continue
            value1.append(self.field_map[ax1][i])
            value2.append(self.field_map[ax2][i])
        x_min, x_max = min(value1), max(value1)
        y_min, y_max = min(value2), max(value2)
        y_delta = (y_max-y_min)*0.1
        y_min -= y_delta
        y_max += y_delta
        if y_max-y_min < 1e-20 or x_max-x_min < 1e-20:
            print("x values:", value1)
            print("y values:", value2)
            print("x_min:", x_min, "x_max:", x_max, "y_min:", y_min, "y_max:", y_max)
            raise ValueError("Bad axis range")
        canvas_1d = ROOT.TCanvas(self.file_name+": "+ax1+" vs "+ax2, ax1+" vs "+ax2)
        hist = ROOT.TH2D(ax1+" vs "+ax2, ";"+ax1+";"+ax2,
                         1000, x_min, x_max,
                         1000, y_min, y_max)
        hist.SetStats(False)
        graph = ROOT.TGraph(len(value1))
        graph.SetLineWidth(2)
        for i, x in enumerate(value1):
            y = value2[i]
            graph.SetPoint(i, x, y)
        hist.Draw()
        graph.Draw("SAMEL")
        self.graph = graph
        self.canvas = canvas_1d
        self.x_list = value1
        self.y_list = value2
        canvas_1d.Update()
        self.root_objects.append(canvas_1d)
        self.root_objects.append(hist)
        self.root_objects.append(graph)
        return canvas_1d, hist, graph

    def calculate_cylindrical_fields(self):
        n_points = len(self.field_map['bx'])
        self.field_map['bphi'] = [None]*n_points
        self.field_map['br'] = [None]*n_points
        for i in range(n_points):
            x = self.field_map['x'][i]
            y = self.field_map['y'][i]
            bx = self.field_map['bx'][i]
            by = self.field_map['by'][i]
            phi = math.atan2(y, x)
            br = bx*math.cos(phi) + by*math.sin(phi)
            bphi = -bx*math.sin(phi) + by*math.cos(phi)
            self.field_map['br'][i] = br
            self.field_map['bphi'][i] = bphi

    def calculate_cartesian_fields(self):
        n_points = len(self.field_map['br'])
        self.field_map['bx'] = [None]*n_points
        self.field_map['by'] = [None]*n_points
        for i in range(n_points):
            phi = self.field_map['phi'][i]*math.pi/180.
            bphi = self.field_map['bphi'][i]
            br = self.field_map['br'][i]
            bx = br*math.cos(phi) - bphi*math.sin(phi)
            by = bphi*math.cos(phi) + br*math.sin(phi)
            self.field_map['bx'][i] = bx
            self.field_map['by'][i] = by

    def load_dump_fields(self):
        print("Loading", self.file_name)
        fin = open(self.file_name)
        header_lines = len(self.keys)+2
        for i in range(header_lines):
            fin.readline()
        for key in self.keys:
            self.field_map[key] = []
        units_ = [1. for key in self.keys]
        for i, key in enumerate(self.keys):
            if key in self.units:
                units_[i] = self.units[key]
        for self.n_lines, line in enumerate(fin.readlines()):
            try:
                data = [float(word) for word in line.split()]
                for i, key in enumerate(self.keys):
                    self.field_map[key].append(data[i]*units_[i])
            except (ValueError, IndexError):
                continue
        if 'phi' in list(self.field_map.keys()):
            self.calculate_cartesian_fields()
        if 'x' in list(self.field_map.keys()):
            self.calculate_cylindrical_fields()

    def get_bin_list(self, key):
        data = self.field_map[key]
        bin_list = [round(datum, 4) for datum in data]
        bin_list = list(set(bin_list)) # force elements to be unique
        bin_list = sorted(bin_list)
        if len(bin_list) == 0:
            raise RuntimeError("No data")
        elif len(bin_list) == 1:
            bin_min = bin_list[0] - 1
            bin_max = bin_list[0] + 1
            n_bins = 1
        else:
            bin_step = bin_list[1] - bin_list[0]
            bin_min = bin_list[0]-bin_step/2.
            bin_max = bin_list[-1]+bin_step/2.
            n_bins = len(bin_list)
        return bin_min, bin_max, n_bins

    def fft_field(self, cuts, field_component, colour=1, canvas = None):
        import xboa.common
        print("Doing fft for", field_component, "...", end=' ')
        sys.stdout.flush()
        n_points = len(list(self.field_map.values())[0])
        fft_list = []
        for i in range(n_points):
            is_cut = False
            for cut_key, cut_value in cuts.items():
                if abs(self.field_map[cut_key][i] - cut_value) > 1e-3:
                    is_cut = True
            if is_cut:
                continue
            fft_list.append(self.field_map[field_component][i])
        fft_list = sorted(fft_list)
        
        fft = numpy.fft.rfft(fft_list)
        fft_mag = [numpy.absolute(item) for item in fft]
        print(fft[:3], "...", fft[-3:])
        print(fft_mag[:3], "...", fft_mag[-3:])
        freq = [i*1./len(fft_mag)/2. for i in range(len(fft_mag))]
        hist, graph = xboa.common.make_root_graph("fft "+field_component, freq, "Frequency", fft, "FFT("+field_component+")")
        if canvas == None:
            canvas = xboa.common.make_root_canvas("fft "+field_component)
            canvas.Draw()
            hist.Draw()
        canvas.cd()
        graph.SetLineColor(colour)
        graph.Draw("SAMEL")
        canvas.Update()
        print("done")
        return canvas

    def get_field_value(self, pos_1, pos_2):
        min_1, max_1, n_1 = self.get_bin_list(var_1)
        min_2, max_2, n_2 = self.get_bin_list(var_2)
        bin_size_1 = (max_1 - min_1)/(n_1+1)
        bin_size_2 = (max_2 - min_2)/(n_2+1)
        bin_1 = int((self.field_map[var_1][i] - min_1)/bin_size_1)
        bin_2 = int((self.field_map[var_2][i] - min_2)/bin_size_2)
        b1 = self.field_grids["br"][bin_1][bin_2]
        b2 = self.field_grids["bphi"][bin_1][bin_2]
        b3 = self.field_grids["bz"][bin_1][bin_2]
        return b1, b2, b3

    def build_field_grids(self):
        if "r" in self.keys:
            self.field_grids = {"br":None, "bz":None, "bphi":None}
            grid_1 = "r"
            grid_2 = "phi"
        else:
            self.field_grids = {"bx":None, "by":None, "bz":None}
            grid_1 = "x"
            grid_2 = "y"
        for field_key in list(self.field_grids.keys()):
            self.field_grids[field_key] = self.build_2d_field_grid(grid_1, grid_2, field_key)

    def build_2d_field_grid(self, var_1, var_2, var_3):
        min_1, max_1, n_1 = self.get_bin_list(var_1)
        min_2, max_2, n_2 = self.get_bin_list(var_2)
        bin_size_1 = (max_1 - min_1)/(n_1+1)
        bin_size_2 = (max_2 - min_2)/(n_2+1)

        field = [[None]*n_2 for i in range(n_1)]
        for i in range(self.n_lines):
            bin_1 = int((self.field_map[var_1][i] - min_1)/bin_size_1)
            bin_2 = int((self.field_map[var_2][i] - min_2)/bin_size_2)
            field[bin_1][bin_2] = self.field_map[var_3][i]
        return field

    def plot_dump_fields(self, var_1, var_2, var_3):
        min_1, max_1, n_1 = self.get_bin_list(var_1)
        min_2, max_2, n_2 = self.get_bin_list(var_2)
        min_3, max_3 = min(self.field_map[var_3]), max(self.field_map[var_3])
        unique_id = str(len(self.root_objects))
        name = var_3+" vs "+var_1+" and "+var_2+" "+unique_id
        self.set_z_axis(min_3, max_3)
        canvas = ROOT.TCanvas(name)
        name_dict = self.name_dict
        hist = ROOT.TH2D(name, var_3+";"+name_dict[var_1]+";"+name_dict[var_2], n_1, min_1, max_1, n_2, min_2, max_2)
        hist.SetStats(False)
        for i in range(self.n_lines):
            hist.Fill(self.field_map[var_1][i], self.field_map[var_2][i], self.field_map[var_3][i])
        hist.Draw("COLZ")
        canvas.Update()
        self.root_objects.append(canvas)
        self.root_objects.append(hist)
        return canvas

    root_objects = []
    name_dict = {"phi":"#phi [degree]", "r":"r [m]", "x":"x [m]", "y":"y [m]", "z":"z [m]"}

    def sine_fit(self):
        voltage = max(self.y_list)
        frequency = 1e-3
        crossings = []
        for i, y in enumerate(self.y_list[1:]):
            if y > 0. and self.y_list[i] < 0: 
                crossings.append(i)
        if len(crossings) > 0:
            t0 = self.x_list[crossings[0]]
        print(crossings)#[1], crossings[0]
        #print "FIT CROSSINGS", self.x_list[crossings[1]], self.x_list[crossings[0]]
        if len(crossings) > 1:
            frequency = 1./(self.x_list[crossings[1]]-self.x_list[crossings[0]])
        frequency *= 2.*math.pi
        print("Seeding sine fit with", t0, frequency, voltage)
        fitter = ROOT.TF1("sin "+str(len(self.root_objects)), "[0]*sin([1]*(x-[2]))")
        fitter.SetParameter(0, voltage)
        fitter.SetParameter(1, frequency)
        fitter.SetParameter(2, t0)
        fitter.SetRange(min(self.x_list), max(self.x_list))
        #fitter.Draw("SAME")
        self.graph.Fit(fitter)
        self.canvas.Update()
        self.root_objects.append(fitter)
        rf_parameters = {
            "voltage":fitter.GetParameter(0),
            "frequency":fitter.GetParameter(1)/2./math.pi,
            "t0":fitter.GetParameter(2)
        }
        return rf_parameters

    def set_z_axis(self, min_z, max_z):
          r0, g0, b0 = 0.2082, 0.1664, 0.8293
          r1, g1, b1 = 1.0, 0.5293, 0.1664
          stops = [0.0000,1.0]
          red   = [r0, r1]
          green = [g0, g1/2.]
          blue  = [b0, b1]
          if min_z < 0 and max_z > 0:
              delta_z = max_z - min_z
              stops = [0.0000, -min_z/delta_z-0.01, -min_z/delta_z, -min_z/delta_z+0.01, 1.0]
              red   = [r0, 0.2, 1.0, 0.9, r1]
              green = [g0, 1.0, 1.0, 0.93, g1]
              blue  = [b0, 0.2, 1.0, 0.6, b1]

          s = numpy.array(stops)
          r = numpy.array(red)
          g = numpy.array(green)
          b = numpy.array(blue)

          ncontours = 255
          npoints = len(s)
          ROOT.TColor.CreateGradientColorTable(npoints, s, r, g, b, ncontours)
          ROOT.gStyle.SetNumberContours(ncontours)


def main_rf(a_dir = None):
    if a_dir == None:
        a_dir = "output/baseline/tmp/find_closed_orbits"
    is_em_field = True
    #plotter = PlotDumpFields(a_dir+"/FieldMapRPHI.dat", is_em_field)
    #canvas_xy = plotter.plot()
    #canvas_1d, hist, graph = plotter.plot_1d({"r":4.}, "phi", "bz")
    #for fmt in "png", "eps", "root":
    #    canvas_1d.Print(a_dir+"/field_1d."+fmt)
    #    canvas_xy.Print(a_dir+"/field_2d."+fmt)
    rf_list = []
    time, frequency = [], []
    plotter = PlotDumpFields(a_dir+"/FieldMapAzimuthal.dat", is_em_field)
    plotter.load_dump_fields()
    canvas_1d, hist, graph = plotter.plot_1d({"r":4.}, "phi", "ephi")
    for file_name in glob.glob(a_dir+"/FieldMapRf?.dat"):
        plotter = PlotDumpFields(file_name, is_em_field)
        plotter.load_dump_fields()
        canvas_1d, hist, graph = plotter.plot_1d({"r":4.}, "t", "ephi")
        rf_list.append(plotter.sine_fit())
    for item in rf_list:
        print(item)
    return rf_list


def main(a_dir = None):
    if a_dir == None:
        a_dir = "output/baseline/tmp/find_closed_orbits"
    is_em_field = False
    #plotter = PlotDumpFields(a_dir+"/FieldMapRPHI.dat", is_em_field)
    #canvas_xy = plotter.plot()
    #canvas_1d, hist, graph = plotter.plot_1d({"r":4.}, "phi", "bz")
    #for fmt in "png", "eps", "root":
    #    canvas_1d.Print(a_dir+"/field_1d."+fmt)
    #    canvas_xy.Print(a_dir+"/field_2d."+fmt)
    rf_list = []
    time, frequency = [], []
    plotter = PlotDumpFields(a_dir+"/FieldMapXY.dat", is_em_field)
    plotter.load_dump_fields()
    canvas_xy = plotter.plot()
    canvas_xy.Print("field_map_xy.png")
    for item in rf_list:
        print(item)
    return rf_list

if __name__ == "__main__":
    if len(sys.argv) < 2  or not os.path.isdir(sys.argv[1]):
        print("Usage: 'python plot_dump_fields path/to/target/directory'")
    else:
        main(sys.argv[1:])
    input("Press <CR> to end")

