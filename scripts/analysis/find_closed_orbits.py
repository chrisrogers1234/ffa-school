"""
Script to find the closed orbit; drives xboa EllipseClosedOrbitFinder algorithm
"""
import time
import glob
import numpy
import sys
import os
import json

sys.path.insert(1, "scripts")

from opal_tracking import OpalTracking
import xboa.common as common
from xboa.hit import Hit
from xboa.algorithms.closed_orbit import EllipseClosedOrbitFinder

from utils import utilities
import matplotlib

class ClosedOrbitFinder(object):
    """
    The ClosedOrbitFinder uses an iterative process to find closed orbits. It
    tracks the beam through a number of cells. Trajectories undergo approximate 
    simple harmonic motion, so they make an ellipse in phase space. The centre
    of the ellipse is used to seed the next iteration in the closed orbit 
    finding.
    """
    def __init__(self, config):
        """
        Initialise the finder
        - config: Configuration module
        """
        self.config = config
        self.out_dir = config.run_control["output_dir"]
        self.run_dir = os.path.join(self.out_dir, "tmp/find_closed_orbits/")

    def plot_iteration(self, sub_index, i, iteration, energy):
        """
        Plot the trajectory of particles at each cell
        - sub_index: indexes element in the substitution loop (for scans)
        - i: indexes the iteration in the closed orbit loop
        - iteration: the closed orbit finder iteration object
        - energy: reference energy
        """
        fig_index = iteration.plot_ellipse_matplotlib("x", "px", "mm", "MeV/c")
        fig = matplotlib.pyplot.figure(fig_index)
        fig.suptitle('KE='+str(energy)+' iter='+str(i))
        matplotlib.pyplot.show(block=False)
        name = os.path.join(self.out_dir, "find_closed_orbits")
        name = os.path.join(name, "closed_orbit-sub-index_"+str(sub_index)+"-i_"+str(i))
        for format in ["png"]:
            fig.savefig(name+"."+format)
        matplotlib.pyplot.close(fig_index)


    def find_closed_orbit(self, sub_index, subs, seed):
        """
        Find the closed orbit
        - sub_index: indexes element in the substitution loop (for scans)
        - subs: dictionary of key value pairs for substitution into the lattice
        - seed: best guess of the closed orbit

        Returns the trajectory of the closed orbit
        """
        max_iterations = self.config.find_closed_orbits["max_iterations"]
        probe = self.config.find_closed_orbits["probe_files"]
        for key in sorted(subs.keys()):
            print(utilities.sub_to_name(key), subs[key], end=' ')
        print()
        utilities.clear_dir(self.run_dir)
        os.chdir(self.run_dir)
        print("Running in", os.getcwd())
        common.substitute(self.config.tracking["lattice_file"],
                          self.config.tracking["lattice_file_out"],
                          subs)
        energy = subs["__energy__"]
        ref_hit = utilities.reference(self.config, energy)
        tracking = utilities.setup_tracking(self.config, probe, energy)
        seed_hit = ref_hit.deepcopy()
        seed_hit["x"] = seed[0]
        seed_hit["px"] = seed[1]
        # fix momentum
        seed_hit["pz"] = (ref_hit["p"]**2-seed_hit["px"]**2)**0.5
        print("Reference kinetic energy:", ref_hit["kinetic_energy"])
        print("Seed kinetic energy:     ", seed_hit["kinetic_energy"])
        finder = EllipseClosedOrbitFinder(tracking, seed_hit)
        generator = finder.find_closed_orbit_generator(["x", "px"], 1)
        x_std_old = 1e9
        i = -1
        will_loop = True
        iteration = None
        while will_loop:
            try:
                iteration = next(generator)
            except (StopIteration, RuntimeError):
                will_loop = False
                print(sys.exc_info()[1])
            i += 1
            heading = ['station', 't', 'x', 'px', 'y', 'py', 'z', 'pz', 'r', 'pt', 'kinetic_energy']
            for key in heading:
                print(str(key).rjust(10), end=' ')
            print()
            for hit in tracking.last[0]:
                for key in heading:
                    print(str(round(hit[key], 1)).rjust(10), end=' ')
                print()
            if iteration == None:
                continue
            print(iteration.centre)
            #if iteration.centre != None: #i == 0 and 
            if i == 0:
                self.plot_iteration(sub_index, i, iteration, energy)
            if i >= max_iterations:
                break
            x_mean = numpy.mean([point[0] for point in iteration.points])
            x_std = numpy.std([point[0] for point in iteration.points])
            print("Seed:", iteration.points[0][0], "Mean:", x_mean, "Std:", x_std)
            if type(iteration.centre) != type(None) and x_std >= x_std_old: # require convergence
                break
            x_std_old = x_std
        os.chdir(self.out_dir)
        if i > 0:
            self.plot_iteration(sub_index, i, iteration, energy)
        return tracking.last[0]

    def get_seed(self, results, subs):
        """
        Get a new seed
        - results: list of previous closed orbits
        - subs: substitutions

        * If results is an empty list, then return the configuration input seed
        * If results is of length 1, then assume this is a best guess for the
          next seed
        * If results is of length >1, then attempt a linear extrapolation of
          closest previous results to guess the next seed
        """
        if len(results) == 0:
            config_seed = self.config.find_closed_orbits["seed"].pop(0)
            print("Using config seed", config_seed)
            return config_seed, len(self.config.find_closed_orbits["seed"]) > 0
        axis_candidates = utilities.get_substitutions_axis(results)
        if len(axis_candidates) == 0:
            co_hit = results[0]["hits"][0]
            seed = [co_hit["x"], co_hit["px"]]
            print("Using last co as seed", seed)
            return seed, False
        print("Doing interpolation for seed for variables", list(axis_candidates.keys()))
        # [dx, dpx]
        delta_keys_new = {}
        delta_var_new = []
        seed_var = {"x":results[-1]["hits"][0]["x"], "px":results[-1]["hits"][0]["px"]}
        print("  base", seed_var)
        for key in list(axis_candidates.keys()):
            key2 = subs[key]
            key1 = axis_candidates[key][-1]
            key0 = axis_candidates[key][-2]
            print("    key", key, "values", key0, key1, key2)
            for var in list(seed_var.keys()):
                var1 = results[-1]["hits"][0][var]
                var0 = results[-2]["hits"][0][var]
                if abs(key1-key0) < 1e-9: # div0
                    seed_var[var] = var1
                    continue
                delta = (var1-var0)/(key1-key0)*(key2-key1)
                print("      var", var, "values", var1, var0, "delta", delta)
                seed_var[var] += delta
        print("  seed", seed_var)
        seed = [seed_var["x"], seed_var["px"]]
        return seed, False

    def find_all_closed_orbits(self):
        """
        Outer loop of the closed orbit finder

        For each substitution in the config.substitution_list, attempt to find
        the closed orbit. Write the closed orbits into the output json file.
        """
        utilities.clear_dir(os.path.join(self.out_dir, "find_closed_orbits"))

        fout_name = os.path.join(self.out_dir,
                                 self.config.find_closed_orbits["output_file"])
        fout = open(fout_name+".tmp", 'w')
        subs_list = self.config.substitution_list
        results = []
        for i, sub in enumerate(subs_list):
            will_loop = True
            is_batch = i >= self.config.find_closed_orbits["root_batch"] 
            for item, key in self.config.find_closed_orbits["subs_overrides"].items():
                sub[item] = key
            hit_list = []
            while will_loop:
                try:
                    next_seed, will_loop = self.get_seed(results, sub)
                except Exception:
                    co_hit = results[0]["hits"][0]
                    next_seed = [co_hit["x"], co_hit["px"]]
                    will_loop = False
                try:
                    hit_list = self.find_closed_orbit(i, sub, next_seed)
                except IndexError as ValueError:
                    sys.excepthook(*sys.exc_info())
                except RuntimeError:
                    sys.excepthook(*sys.exc_info())
                    hit_list = []
                    print("Breaking loop due to tracking error")
                    will_loop = False
                will_loop = len(hit_list) < 20 and will_loop
            output = {"substitutions":sub,
                      "hits":[hit.dict_from_hit() for hit in hit_list]}
            results.append(output)
            print(json.dumps(output), file=fout)
            fout.flush()
        fout.close()
        time.sleep(1)
        os.rename(fout_name+".tmp", fout_name)

def main(config):
    finder = ClosedOrbitFinder(config)
    finder.find_all_closed_orbits()
    print("Done find closed orbits")
