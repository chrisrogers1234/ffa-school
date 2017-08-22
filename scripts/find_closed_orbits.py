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

import ROOT

import plot_orbit
import utilities

CONFIG = None
OUT_DIR = None
RUN_DIR = None

def reference(energy):
    """
    Generate a reference particle
    """
    hit_dict = {}
    hit_dict["pid"] = CONFIG.find_closed_orbits["pdg_pid"]
    hit_dict["mass"] = common.pdg_pid_to_mass[abs(hit_dict["pid"])]
    hit_dict["charge"] = 1
    hit_dict["x"] = 0.
    hit_dict["kinetic_energy"] = energy
    return Hit.new_from_dict(hit_dict, "pz")

def plot_iteration(sub_index, i, iteration, energy):
    """
    Plot the closed orbit ellipse and the ellipse fit
    """
    canvas, hist, graph, fit = iteration.plot_ellipse("x", "px", "mm", "MeV/c")
    hist.SetTitle('KE='+str(energy)+' iter='+str(i))
    canvas.Update()
    name = os.path.join(OUT_DIR, "closed_orbit-sub-index_"+str(sub_index)+"-i_"+str(i))
    for format in "eps", "root", "png":
        canvas.Print(name+"."+format)

def find_closed_orbit(sub_index, subs, seed):
    """
    Find the closed orbit; algorithm is to track turn by turn; fit an ellipse to
    the tracking; find the centre of the ellipse; repeat until no improvement or
    10 iterations.
    - energy: (float) kinetic energy at which the co is calculated
    - step: (float) step size in tracking
    - poly_order: (int) order of the polynomial fit to the field map (not used)
    - smooth_oder: (int) order of smoothing the polynomial fit to the field map
                   (not used)
    - seed: (list of 2 floats) [x, px] value to be used as the seed for the next 
            iteration; px value is ignored, sorry about that.
    """
    for key in sorted(subs.keys()):
        print utilities.sub_to_name(key), subs[key],
    print
    out_dir = OUT_DIR
    run_dir = RUN_DIR
    tmp_dir = "./"
    try:
        os.makedirs(run_dir)
    except OSError: # maybe the dir already exists
        pass
    os.chdir(run_dir)
    print "Running in", os.getcwd()
    common.substitute(CONFIG.tracking["lattice_file"], tmp_dir+'SectorFFAGMagnet.tmp', subs)
    energy = subs["__energy__"]
    ref_hit = reference(energy)
    opal_exe = os.path.expandvars("${OPAL_EXE_PATH}/opal")
    tracking = OpalTracking(tmp_dir+'/SectorFFAGMagnet.tmp', tmp_dir+'/disttest.dat', ref_hit, 'PROBE*.loss', opal_exe, tmp_dir+"/log")
    seed_hit = ref_hit.deepcopy()
    seed_hit["x"] = seed[0]
    seed_hit["px"] = seed[1]
    finder = EllipseClosedOrbitFinder(tracking, seed_hit)
    generator = finder.find_closed_orbit_generator(["x", "px"], 1)
    x_std_old = 1e9
    i = -1
    for i, iteration in enumerate(generator):
        #for point in iteration.points:
        heading = ['station', 't', 'x', 'px', 'y', 'py', 'z', 'pz', 'r', 'pt']
        for key in heading:
            print str(key).rjust(10),
        print
        for hit in tracking.last[0]:
            for key in heading:
                print str(round(hit[key], 1)).rjust(10),
            print
        print iteration.centre
        #if iteration.centre != None: #i == 0 and 
        if i == 0:
            plot_iteration(sub_index, i, iteration, energy)
        if i >= 10:
            break
        x_mean = numpy.mean([point[0] for point in iteration.points])
        x_std = numpy.std([point[0] for point in iteration.points])
        print "Seed:", iteration.points[0][0], "Mean:", x_mean, "Std:", x_std
        if iteration.centre != None and x_std >= x_std_old: # require convergence
            break
        x_std_old = x_std
    os.chdir(out_dir)
    if i > -1:
        plot_iteration(sub_index, i, iteration, energy)
    return tracking.last[0]

def main(config):
    global CONFIG, OUT_DIR, RUN_DIR
    CONFIG = config
    OUT_DIR = CONFIG.run_control["output_dir"]
    RUN_DIR = os.path.join(OUT_DIR, "tmp/find_closed_orbits/")
    next_seed = config.find_closed_orbits["seed"]
    fout_name = os.path.join(OUT_DIR, config.find_closed_orbits["output_file"])
    fout = open(fout_name+".tmp", 'w')
    subs_list = config.substitution_list
    for i, sub in enumerate(subs_list):
        is_batch = i >= config.find_closed_orbits["root_batch"] 
        for item, key in config.find_closed_orbits["subs_overrides"].iteritems():
            sub[item] = key
        ROOT.gROOT.SetBatch(is_batch)
        hit_list = find_closed_orbit(i, sub, next_seed)
        next_seed = [hit_list[0]["x"], hit_list[0]["px"]]
        output = {"substitutions":sub, "hits":[hit.dict_from_hit() for hit in hit_list]}
        print >> fout, json.dumps(output)
        fout.flush()
    fout.close()
    time.sleep(1)
    os.rename(fout_name+".tmp", fout_name+".out")
    ROOT.gROOT.SetBatch(False)
    #disabled because I need to hack around file names (thats all)
    #if len(energy_list) < 5:
    #    plot_orbit.main()
    #    print "Finished closed orbits"

