import sys
import os
import math
import glob
import numpy.fft
import matplotlib
import xboa.common.matplotlib_wrapper as matplotlib_wrapper

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
            fig_index = self.plot_dump_fields("phi", "r", "bz")
        else:
            fig_index = self.plot_dump_fields("x", "y", "bz")
            matplotlib.pyplot.savefig("bz_vs_x-y.png")
            fig_index = self.plot_dump_fields("x", "y", "bx")
            matplotlib.pyplot.savefig("bx_vs_x-y.png")
            fig_index = self.plot_dump_fields("x", "y", "by")
            matplotlib.pyplot.savefig("by_vs_x-y.png")


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

    name_dict = {"phi":"#phi [degree]", "r":"r [m]",
                 "x":"x [m]", "y":"y [m]", "z":"z [m]",
                 "bx":"B$_{x}$ [T]", "by":"B$_{y}$ [T]", "bz":"B$_{z}$ [T]", 
                 "br":"B$_{r}$ [T]", "bphi":"B$_{\phi}$ [T]",
                 }

    def get_norm(self, min_z, max_z, limit=5):
        min_z = max(-limit, min_z)
        max_z = min(limit, max_z)
        divnorm = matplotlib.colors.DivergingNorm(vmin=min_z, vcenter=0, vmax=max_z)
        return divnorm

    def plot_1d(self, cuts, ax1, ax2, fig_index = None):
        self.x_list, self.y_list = [], []
        n_points = len(list(self.field_map.values())[0])
        for i in range(n_points):
            is_cut = False
            for cut_key, cut_value in cuts.items():
                if abs(self.field_map[cut_key][i] - cut_value) > 1e-3:
                    is_cut = True
            if is_cut:
                continue
            self.x_list.append(self.field_map[ax1][i])
            self.y_list.append(self.field_map[ax2][i])
        fig_index = matplotlib_wrapper.make_graph(self.x_list, ax1,
                                                  self.y_list, ax2,
                                                  fig_index = fig_index)
        return fig_index

    def plot_dump_fields(self, var_1, var_2, var_3, fig_index = None):
        min_1, max_1, n_1 = self.get_bin_list(var_1)
        min_2, max_2, n_2 = self.get_bin_list(var_2)
        min_3, max_3 = min(self.field_map[var_3]), max(self.field_map[var_3])
        norm = self.get_norm(min_3, max_3)
        fig_index = matplotlib_wrapper.get_figure_index(fig_index)
        hist = matplotlib.pyplot.hist2d(self.field_map[var_1],
                                        self.field_map[var_2],
                                        bins=[n_1, n_2],
                                        range=[[min_1, max_1], [min_2, max_2]],
                                        weights=self.field_map[var_3],
                                        norm=norm,
                                        cmap='seismic')
        bar = matplotlib.pyplot.colorbar()
        bar.set_label(self.name_dict[var_3])
        return fig_index

def main(a_dir = None):
    if a_dir == None:
        a_dir = "output/baseline/tmp/find_closed_orbits"
    is_em_field = False
    plotter = PlotDumpFields(a_dir+"/FieldMapXY.dat", is_em_field)
    plotter.load_dump_fields()
    plotter.plot()

if __name__ == "__main__":
    if len(sys.argv) < 2  or not os.path.isdir(sys.argv[1]):
        print("Usage: 'python plot_dump_fields path/to/target/directory'")
    else:
        main(sys.argv[1:])
    input("Press <CR> to end")

