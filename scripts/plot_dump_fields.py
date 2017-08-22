import ROOT

class PlotDumpFields(object):
    def __init__(self, file_name):
        self.keys = ["x", "y", "z", "bx", "by", "bz"]
        self.n_lines = 0
        self.file_name = file_name
        self.field_map = {}

    def plot(self):
        self.load_dump_fields()
        canvas_xy = self.plot_dump_fields("x", "y", "bz")
        #self.plot_dump_fields("x", "z", "by")
        return canvas_xy

    def load_dump_fields(self):
        print "Loading", self.file_name
        fin = open(self.file_name)
        for i in range(8):
            fin.readline()
        for key in self.keys:
            self.field_map[key] = []
        for self.n_lines, line in enumerate(fin.readlines()):
            data = [float(word) for word in line.split()]
            for i, key in enumerate(self.keys):
                #if i > 2 and abs(data[i]) > 1e-9:
                #    print "FIELD"
                self.field_map[key].append(data[i])

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


    def plot_dump_fields(self, var_1, var_2, var_3):
        min_1, max_1, n_1 = self.get_bin_list(var_1)
        min_2, max_2, n_2 = self.get_bin_list(var_2)
        unique_id = str(len(self.root_objects))
        canvas = ROOT.TCanvas(var_3+" vs "+var_1+" and "+var_2+" "+unique_id)
        hist = ROOT.TH2D(unique_id, var_3+";"+var_1+";"+var_2, n_1, min_1, max_1, n_2, min_2, max_2)
        hist.SetStats(False)
        for i in range(self.n_lines):
            hist.Fill(self.field_map[var_1][i], self.field_map[var_2][i], self.field_map[var_3][i])
        hist.Draw("COLZ")
        canvas.Update()
        self.root_objects.append(canvas)
        self.root_objects.append(hist)
        return canvas

    root_objects = []

def main():
    plotter = PlotDumpFields("tmp/FieldMapXY.dat")
    canvas_xy = plotter.plot()
    #plotter = PlotDumpFields("tmp/FieldMapXZ.dat")
    #plotter.plot()

if __name__ == "__main__":
    main()
    raw_input("Press <CR> to end")

