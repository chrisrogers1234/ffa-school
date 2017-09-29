#This file is a part of xboa
#
#xboa is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#xboa is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with xboa in the doc folder.  If not, see 
#<http://www.gnu.org/licenses/>.

"""
\namespace _opal_tracking
"""

import tempfile
import subprocess
import os
import glob
import math

from xboa import common
from xboa.hit import Hit

from xboa.tracking import TrackingBase 

class StoreDataInMemory(object):
    def __init__(self, config):
        self.hit_dict_of_lists = {}

    def process_hit(self, event, hit):
        if not event in self.hit_dict_of_lists:
            self.hit_dict_of_lists[event] = []
        self.hit_dict_of_lists[event].append(hit)

    def finalise(self):
        # convert from a dict of list of hits to a list of list of hits
        # one list per event
        # each list contains one hit per station
        events = sorted(self.hit_dict_of_lists.keys())
        hit_list_of_lists = [self.hit_dict_of_lists[ev] for ev in events]
        # sort by time within each event
        for i, hit_list in enumerate(hit_list_of_lists):
            hit_list_of_lists[i] = sorted(hit_list, key = lambda hit: hit['t'])        
        self.last = hit_list_of_lists
        self.hit_dict_of_lists = {}
        return hit_list_of_lists

class OpalTracking(TrackingBase):
    """
    Provides an interface to OPAL tracking routines for use by xboa.algorithms
    """
    def __init__(self, lattice_filename, beam_filename, reference_hit, output_filename, opal_path, log_filename, save_dir = None, n_cores = 1, mpi = None):
        """
        Initialise OpalTracking routines
        - lattice_filename is the Opal lattice file that OpalTracking will use
        - beam_filename is a filename that OpalTracking will overwrite when it
          runs the tracking, putting in beam data
        - reference_hit defines the centroid for the tracking; this should
          correspond to 0 0 0 0 0 0 in the beam file
        - output_filename the name of the PROBE file that OpalTracking will
          read to access output data; wildcards (*, ?) are allowed, in which
          case all files matching the wildcards will be loaded
        - opal_path path to the OPAL executable
        - allow_duplicate_station when evaluates to False, OpalTracking will
          discard duplicate stations on the same event
        - log_filename set to a string file name where OpalTracking will put the 
          terminal output from the opal command; if None, OpalTracking will make
          a temp file
        """
        self.beam_filename = beam_filename
        self.lattice_filename = lattice_filename
        self.output_name = output_filename
        self.opal_path = opal_path
        if not os.path.isfile(self.opal_path):
            raise RuntimeError(str(self.opal_path)+" does not appear to exist."+\
                  " Check that this points to the opal executable.")
        self.ref = reference_hit
        self.last = None
        self.allow_duplicate_station = False
        self.do_tracking = True
        self.log_filename = log_filename
        if self.log_filename == None:
            self.log_filename = tempfile.mkstemp()[1]
        self.save_dir = save_dir
        self.n_cores = n_cores
        self.mpi = mpi

    def save(self):
        """
        If save_dir is defined, output files will be saved here; otherwise does 
        nothing
        """
        if self.save_dir == None:
            return
        for probe_file in glob.glob(output_filename):
            target = os.path.join(self.save_dir, probe_file)
            os.rename(probe_file, target)

    def cleanup(self):
        """
        Delete output files (prior to tracking)
        """
        for probe_file in glob.glob(self.output_name):
            os.unlink(probe_file)

    def track_one(self, hit):
        """
        Track one hit through Opal

        Returns a list of hits, sorted by time.
        """
        return self.track_many([hit])[0]
        
    def track_many(self, list_of_hits, pass_through_analysis = StoreDataInMemory(None)):
        """
        Track many hits through Opal

        Returns a list of lists of hits; each list of hits corresponds to a
        track, defined by probe "id" field. Output hits are sorted by time 
        within each event.
        """
        if self.do_tracking:
            self._tracking(list_of_hits)
        if pass_through_analysis == None:
            return None
        else:
            hit_list_of_lists = self._read_probes(pass_through_analysis)
            self.save()
            return hit_list_of_lists

    def open_subprocess(self):
        command = [self.opal_path, self.lattice_filename]
        will_do_bsub = False
        if self.mpi != None:
            try:
                subprocess.check_output(["bsub", "-V"])
                will_do_bsub = True
                bsub_command = ["bsub",
                                "-n", str(self.n_cores),
                                "-q", 'scarf-ibis',
                                "-W", "24:00",
                                "-o", self.log_filename,
                                "-K", ]
                command = bsub_command+[self.mpi]+command
            except OSError:
                command = [self.mpi, "-n", str(self.n_cores)]+command
        if will_do_bsub:
            log = open("scarf.log", "w")
        else:
            log = open(self.log_filename, "w")

        proc = subprocess.Popen(command,
                                stdout=log,
                                stderr=subprocess.STDOUT)
        return proc

    def _tracking(self, list_of_hits):
        print "Using logfile ", self.log_filename
        open(self.lattice_filename).close() # check that lattice exists
        m, GeV = common.units["m"], common.units["GeV"]
        p_mass = common.pdg_pid_to_mass[2212]
        fout = open(self.beam_filename, "w")
        print >> fout, len(list_of_hits)
        for i, hit in enumerate(list_of_hits):
            if i < 1 or i == len(list_of_hits)-1:
                print 'tracking hit ...',
                for key in 'x', 'y', 'z', 'px', 'py', 'pz':
                    print key+":", hit[key],
                print
                print '         ref ...',
                for key in 'x', 'y', 'z', 'px', 'py', 'pz':
                    print self.ref[key],
                print
            if i == 1 and len(list_of_hits) > 2:
                print "<", len(list_of_hits)-2, " more hits>"
            x = (hit["x"]-self.ref["x"])/m
            y = (hit["y"]-self.ref["y"])/m
            z = (hit["z"]-self.ref["z"])/m
            px = (hit["px"]-self.ref["px"])/p_mass
            py = (hit["py"]-self.ref["py"])/p_mass
            pz = (hit["pz"]-self.ref["pz"])/p_mass
            print >> fout, x, px, z, pz, y, py
        fout.close()
        self.cleanup()
        proc = self.open_subprocess()
        proc.wait()
        # returncode 1 -> particle fell out of the accelerator
        if proc.returncode != 0 and proc.returncode != 1:
            raise RuntimeError("OPAL quit with non-zero error code "+\
                               str(proc.returncode)+". Review the log file: "+\
                               str(fname))

    def _remove_duplicate_stations(self, list_of_hit_dicts):
        if self.allow_duplicate_station:
            return list_of_hit_dicts
        dict_of_hit_dicts = {} # temp mapping of station to hit_dict
        for hit_dict in list_of_hit_dicts:
            dict_of_hit_dicts[station] = hit_dict # overwrites if a duplicate
        return dict_of_hit_dicts.values() # list of hit dicts

    def _read_probes(self, pass_through_analysis):
        # loop over files in the glob, read events and sort by event number
        file_list = glob.glob(self.output_name)
        for i, file_name in enumerate(file_list):
            fin = open(file_name)
            fin.readline()
            # go through file line by line reading hit data
            for line in fin.readlines():
                words = line.split()
                hit_dict = {}
                for key in "pid", "mass", "charge":
                    hit_dict[key] = self.ref[key]
                for i, key in enumerate(["x", "z", "y"]):
                    hit_dict[key] = float(words[i+1])
                for i, key in enumerate(["px", "pz", "py"]):
                    hit_dict[key] = float(words[i+4])*self.ref["mass"]
                event = int(words[7])
                hit_dict["event_number"] = int(words[7])
                hit_dict["station"] = int(words[8])*len(file_list)+i
                x = hit_dict["x"]
                y = hit_dict["z"]
                px = hit_dict["px"]
                py = hit_dict["pz"]
                phi = math.atan2(y, x)
                hit_dict["t"] = float(words[9])
                hit_dict["x"] = + x*math.cos(phi) + y*math.sin(phi)
                hit_dict["z"] = - x*math.sin(phi) + y*math.cos(phi)
                hit_dict["px"] = + px*math.cos(phi) + py*math.sin(phi)
                hit_dict["pz"] = - px*math.sin(phi) + py*math.cos(phi)
                hit = Hit.new_from_dict(hit_dict, "energy")
                pass_through_analysis.process_hit(event, hit)
        self.last = pass_through_analysis.finalise()
        return self.last
    
