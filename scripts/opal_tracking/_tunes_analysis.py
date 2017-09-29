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

import math
import numpy


class TunesAnalysis(object):
    def __init__(self, config):
        self.beam_centre = None
        self.beam_ellipse = None
        self.coordinates = ['x', 'px', 'y', 'py']
        self.points = {}
        self.x_tunes = {}
        self.x_actions = {}
        self.y_tunes = {}
        self.y_actions = {}
        self.fourd_actions = {}

    def process_hit(self, event, hit):
        if event != 3:
            return
        if not event in self.points:
            self.points[event] = [None, None]
            self.x_tunes[event] = []
            self.y_tunes[event] = []
            self.x_actions[event] = []
            self.y_actions[event] = []
            return
        print "    process", hit['y'], hit['py'],
        hits = self.points[event]
        hits[0] = hits[1]
        hit = self._cholesky_conversion(hit)
        print "...", hit[2], hit[3]
        hits[1] = hit
        self.x_actions[event].append(self.get_action(hit, 0))
        self.y_actions[event].append(self.get_action(hit, 2))
        if type(hits[0]) != type(None):
            self.get_tunes(event, hits[0], hits[1])

    def get_action(self, hit, ax):
        action = numpy.dot(numpy.transpose(hit[ax:ax+2]), self.cholesky_inv[ax:ax+2, ax:ax+2])
        action = numpy.dot(action, hit[ax:ax+2])
        return action

    def get_tunes(self, event, hit0, hit1):
        delta = hit1 - hit0
        dphi_x = math.pi/2.-math.atan2(delta[1], delta[0])
        dphi_y = math.pi/2.-math.atan2(delta[3], delta[2])
        self.x_tunes[event].append(dphi_x/math.pi/2.)
        self.y_tunes[event].append(dphi_y/math.pi/2.)

    def _cholesky_conversion(self, hit):
        hit_array = numpy.array([hit[var] for var in self.coordinates])
        hit_array -= self.beam_centre
        hit_array = numpy.dot(self.cholesky_inv, hit_array)
        return hit_array

    def set_match(self, mean, ellipse):
        self.beam_ellipse = ellipse
        self.beam_centre = mean
        cholesky = numpy.linalg.cholesky(self.beam_ellipse)
        cholesky /= numpy.linalg.det(cholesky)**(1./len(self.coordinates))
        self.cholesky_inv = numpy.linalg.inv(cholesky)
        self.cholesky_x = numpy.linalg.inv(cholesky[0:2, 0:2])
        self.cholesky_y = numpy.linalg.inv(cholesky[2:4, 2:4])
        print self.cholesky_inv

    def finalise(self):
        for event, data in self.x_tunes.iteritems():
            print "event", event, "with", len(data), "planes"
            for key, thing in ["x_tune", self.x_tunes], ["y_tune", self.y_tunes], ["x_action", self.x_actions], ["y_action", self.y_actions]:
                data = thing[event]
                print "   ", key, numpy.mean(data), "+/-", numpy.std(data), data
        return self.x_tunes, self.y_tunes

    def plot_tunes(self):
        pass
