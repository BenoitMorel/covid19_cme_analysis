#!/usr/bin/env python3

import argparse
import csv
import datetime
import math
import multiprocessing
from multiprocessing.pool import ThreadPool
from collections import namedtuple
import os
import random
import shutil
import string
import subprocess
import sys
import json
from json import JSONEncoder
import itertools
import copy

import ete3
import numpy
import progressbar
from Bio import SeqIO

progressbar.streams.flush()

PROGRESS_BAR = None
PROGRESS_BAR_ITER = multiprocessing.Value('i', 0)

IQTREE = "iqtree -m gtr+g4 -s {msa} -g {tree} -pre {prefix} -seed {seed} -nt 1"
model_file = "subst.model"
freqs_file = "freqs.model"

RUN_TEMPLATE = "run_{run_iter:0{leading_zeroes}}"
TOTAL_ITERS = 0

class indel_control_file:
    def __init__(self, subst_model_params, freq_params, pinv, alpha,
            ngamcat, tree, sites):
        self.subst_model_params = subst_model_params
        self.freq_params = freq_params
        self.pinv = pinv
        self.alpha = alpha
        self.ngamcat = ngamcat
        self.tree = tree
        self.sites = sites
        self.randomseed = numpy.random.randint(int(2**32-1))

    def write(self, path):
        with open(os.path.join(path, "control.txt"), 'w') as outfile:
            outfile.write(self.control_txt)

    @property
    def control_txt(self):
        return """
        [TYPE] NUCLEOTIDE 1

        [SETTINGS]
          [randomseed] {randomseed}
          [output] FASTA

        [MODEL] m1
          [submodel] GTR {subst_model_params}
          [statefreq] {freq_params}
          [rates] {pinv} {alpha} {ngamcat}

        [TREE] t1 {tree}

        [PARTITIONS] p1
          [t1 m1 {sites}]

        [EVOLVE] p1 1 simulated_sequences
        """.format(
                randomseed = self.randomseed,
                subst_model_params = self.subst_model_params,
                freq_params = self.freq_params,
                pinv = self.pinv,
                alpha = self.alpha,
                ngamcat = self.ngamcat,
                tree = self.tree,
                sites = self.sites)


class directory_guard:
    def __init__(self, path):
        self._path = path

    def __enter__(self):
        self._old_dir = os.getcwd()
        os.chdir(self._path)
        return self

    def __exit__(self, *args):
        os.chdir(self._old_dir)


class indel_param:
    def indel_repr(self):
        return ' '.join([str(f) for f in self.params])

    @property
    def params(self):
        return self._params


class single_param(indel_param):
    def __init__(self, value=None):
        if value is None:
            self._params = [numpy.random.random()]
        else:
            self._params = [value]


class subst_params(indel_param):
    def __init__(self, matrix):
        self._params = matrix

    @property
    def params(self):
        return [float(numpy.random.choice(self._params[i], 1)) for i in range(6)]


class freq_params(indel_param):
    def __init__(self, matrix):
        self._params = matrix

    @property
    def params(self):
        arr = [float(numpy.random.choice(self._params[i], 1)) for i in range(4)]
        arr /= numpy.linalg.norm(arr, 1)
        return arr

class pinvar_param(single_param):
    pass

class alpha_param(single_param):
    pass

class tree_param:
    def __init__(self, tree_name, tree=None, tree_size=None):
        self._name = tree_name
        self._tree_file = None
        if not tree is None:
            self._tree_file = tree
            with open(self._tree_file) as infile:
                self._tree = ete3.Tree(infile.read())
        elif not tree_size is None:
            t = ete3.Tree()
            t.populate(tree_size)
            for n in t.traverse():
                n.dist = numpy.random.exponential(0.1) + 0.01
            self._tree = t

    @property
    def tree_name(self):
        return self._name

    @property
    def name(self):
        return self._name

    @property
    def tree(self):
        return self._tree

    @property
    def newick(self):
        if self._tree_file is None:
            return self._tree.write(format=5)
        with open(self._tree_file) as infile:
            return infile.read()


class dataset:
    def __init__(self,
                 tree,
                 sites,
                 prefix,
                 summary_file,
                 seed = None):

        with open(summary_file) as infile:
            json_dict = json.load(infile)
        self._tree = tree
        self._sites = sites
        self._subst_params = subst_params(json_dict['subst'])
        self._freq_params = freq_params(json_dict['freqs'])
        self._pinv = pinvar_param(0.90)
        self._alpha = alpha_param(1.0)
        self._ngamcat = 0
        self._path = os.path.join(prefix, str(tree.tree_name) + "tree", str(sites) + "sites")
        os.makedirs(self._path, exist_ok=True)
        self._control_file = None
        self._results = {}

    def write_control_file(self, path):
        if not self._control_file:
            self._control_file =\
                indel_control_file(
                        self._subst_params.indel_repr(),
                        self._freq_params.indel_repr(),
                        self._pinv.indel_repr(),
                        self._alpha.indel_repr(),
                        str(self._ngamcat),
                        self._tree.newick,
                        str(self._sites))
        self._control_file.write(path)

    def run_indel(self, path):
        with directory_guard(path):
            subprocess.run("indelible", stdout = subprocess.DEVNULL)
        self._alignment_path = os.path.join(path, "simulated_sequences.fas")

    @property
    def path(self):
        return self._path

    @property
    def tree_path(self):
        return os.path.join(self._path, self._tree.tree_name + ".newick")

    def tree_path_str(self):
        return os.path.join(self._path, self._tree.tree_name + ".newick")

    @property
    def alignment(self):
        return self._alignment_path

    def make_iteration(self, path):
        self.write_control_file(path)
        self.run_indel(path)

    def make_tree(self):
        with open(self.tree_path, 'w') as outfile:
            outfile.write(self._tree.newick)

    def add_result(self, result):
        if not result.program_name() in self._results:
            self._results[result.program_name()] = []
        self._results[result.program_name()].append(result)

    def summarize_rf(self):
        summary = {}
        for prog, results in self._results.items():
            summary[prog] = numpy.mean([r.rfdist for r in results])
        return summary

    def __hash__(self):
        return hash((self._tree.name, self._sites))

    def __repr__(self):
        return "dataset(tree: {}, sites: {})".format(self._tree.name,
                self._sites)

    def __str__(self):
        self.__repr__()

    def __eq__(self, other):
        return self._tree.name == other._tree.name and\
                self._sites == other._sites

class program:
    @property
    def name(self):
        return self._name

class iqtree(program):
    def __init__(self):
        self._name = "iqtree"

    def run(self, path, alignment, seed):
        subprocess.run(["iqtree",
            "-m", "GTR+G4",
            "-s", alignment,
            "-pre", path,
            "-seed", str(seed),
            "-nt", "1"],
            stdout=subprocess.DEVNULL)

    @staticmethod
    def result(directory, true_tree):
        return iqtree_result(directory, true_tree)

class raxml_ng(program):
    def __init__(self):
        self._name = "raxml-ng"

    def run(self, path, alignment, seed):
        subprocess.run(["raxml-ng",
            "--msa", alignment,
            "--model", "gtr+g4",
            "--prefix", path,
            "--seed", str(seed),
            "--threads", "1"],
            stdout=subprocess.DEVNULL)

    @staticmethod
    def result(directory, true_tree):
        return raxml_ng_result(directory, true_tree)

class iteration:
    def __init__(self, iteration, dataset, programs):
        self._iteration = int(iteration)
        self._dataset = copy.copy(dataset)
        self._path = os.path.join(dataset.path, str(iteration) + "iter")
        self._programs = programs

    def run(self):
        os.makedirs(self._path, exist_ok=True)

        self._seed_file = os.path.join(self._path, '.seed')
        if not os.path.exists(self._seed_file):
            self._seed = numpy.random.randint(int(2**32)-1)
            with open(self._seed_file, 'w') as sf:
                sf.write(str(self._seed))
        else:
            with open(self._seed_file) as sf:
                self._seed = int(sf.read())

        self._dataset.make_iteration(self._path)

        iter_results = {self._dataset : []}
        for prog in self._programs:
            if not self.check_done(prog.name, self._path):
                run_dir = os.path.join(self._path, prog.name)
                os.makedirs(run_dir, exist_ok=True)
                run_prefix = os.path.join(run_dir, "simulation")
                prog.run(run_prefix, self._dataset.alignment, self._seed)
                self.set_done(prog.name, self._path)
            try:
                iter_results[self._dataset].append(prog.result(self._path,
                    self._dataset.tree_path))
            except:
                print("WARNING: failed to parse the result of",
                        str(self._dataset), "iteration", self._iteration,
                        "for program", prog.name)

        PROGRESS_BAR.update(PROGRESS_BAR_ITER.value)
        PROGRESS_BAR_ITER.value += 1
        return iter_results

    @staticmethod
    def set_done(program, path):
        with open(os.path.join(path, ".done"), 'a') as done_file:
            done_file.write(program + ":" +
                    datetime.datetime.now().isoformat()+"\n")

    @staticmethod
    def check_done(program, path):
        if os.path.exists(os.path.join(path, '.done')):
            with open(os.path.join(path, ".done")) as done_file:
                for line in done_file:
                    if line.find(program) != -1:
                        return True
        return False

class experiment:
    def __init__(self,
                 root_path,
                 run_iters,
                 trees,
                 aligns,
                 summary_file,
                 run_iq=True,
                 seed=None):

        self._run_path = root_path
        self._run_iq = run_iq
        self._run_iter = run_iters
        leading_zeroes = math.ceil(math.log10(TOTAL_ITERS))

        if not os.path.exists(self._run_path):
            os.mkdir(self._run_path)


        self._datasets = []

        tree_counter = 0
        for tree in trees:
            t_name = base26_encode(tree_counter, len(trees))
            try:
                base = os.path.split(tree)[1]
                t = tree_param(t_name, tree_size = int(base))
            except:
                t = tree_param(t_name, tree = tree)
            for sites in aligns:
                self._datasets.append(dataset(t, sites, self._run_path,
                    summary_file))
            tree_counter += 1

        self._dataset_map = {ds : ds for ds in self._datasets}
        self._programs = []

    def register_program(self, program):
        self._programs.append(program)

    def _prep_runs(self):
        self._iterations = []
        for ds in self._datasets:
            ds.make_tree()
            for i in range(self._run_iter):
                self._iterations.append(iteration(i, ds, self._programs))

    def run(self, procs):
        self._prep_runs()
        PROGRESS_BAR.update(0)
        with multiprocessing.Pool(procs) as mp:
            finished_iters = mp.map(iteration.run, self._iterations)
        for item in finished_iters:
            for ds, results in item.items():
                for r in results:
                    self._dataset_map[ds].add_result(r)

    def summarize_rf(self):
        summary = {}
        for ds in self._datasets:
            summary[ds] = ds.summarize_rf()
        return summary

class result:
    @property
    def time(self):
        return self._time

    @property
    def tree(self):
        return self._tree.write(format=5)

    @property
    def lh(self):
        return self._final_lh

    @property
    def taxa(self):
        return self._taxa

    @property
    def sites(self):
        return self._sites

    @property
    def rfdist(self):
        rf, max_rf, _, _, _, _, _ = self._true_tree.robinson_foulds(self._tree, unrooted_trees=True)
        return rf/max_rf

    def read_true_tree(self, true_tree_filename):
        with open(true_tree_filename) as infile:
            self._true_tree = ete3.Tree(infile.read())

    def get(self):
        return {
            'time': self.time,
            'tree': self.tree,
            'lh': self.lh,
            'rfdist': self.rfdist,
        }

    def make_row_dict(self):
        return {
            'time': self.time,
            'lh': self.lh,
            'program': self.program_name(),
            'sites': self.sites,
            'taxa': self.taxa,
            'rfdist': self.rfdist,
        }

class iqtree_result(result):
    def __init__(self, directory, true_tree_filename):
        result_path = os.path.join(directory, 'iqtree')
        with directory_guard(result_path):
            with open('simulation.treefile') as tree_file:
                self._tree = iqtree_result._read_tree(tree_file.read())
            with open('simulation.iqtree') as iqtree_file:
                for line in iqtree_file:
                    if 'Log-likelihood of the tree:' in line:
                        self._final_lh = iqtree_result._read_lh(line)
                    if 'Total wall-clock time used:' in line:
                        self._time = iqtree_result._read_time(line)
        self.read_true_tree(true_tree_filename)

    def program_name(self):
        return 'iq'

    @staticmethod
    def _read_tree(tree_string):
        return ete3.Tree(tree_string)

    @staticmethod
    def _read_lh(lh_string):
        start_index = len('Log-likelihood of the tree: ')
        end_index = lh_string.rfind('(') - 1
        return float(lh_string[start_index:end_index])

    @staticmethod
    def _read_time(time_string):
        start_index = len('Total wall-clock time used: ')
        end_index = start_index + time_string[start_index:].find(' ')
        return float(time_string[start_index:end_index])

class raxml_ng_result(result):
    def __init__(self, path, true_tree_filename):
        best_tree_file = os.path.join(path, "raxml-ng", "simulation.raxml.bestTree")
        self._tree = self._read_tree(best_tree_file)
        logfile = os.path.join(path, "raxml-ng", "simulation.raxml.log")
        self._lh = self._read_lh(logfile)
        self._time = self._read_time(logfile)
        self.read_true_tree(true_tree_filename)

    @staticmethod
    def _read_tree(tree_file):
        with open(tree_file) as infile:
            return ete3.Tree(infile.read())

    @staticmethod
    def _read_lh(logfile):
        with open(logfile) as infile:
            for line in infile:
                if 'Final LogLikelihood:' in line:
                    start_index = len('Final LogLikelihood: ')
                    return float(line[start_index:])

    def program_name(self):
        return 'raxml-ng'

    @staticmethod
    def _read_time(logfile):
         with open(logfile) as infile:
            for line in infile:
                if 'Elapsed time: ' in line:
                    start_index = len('Elapsed time: ')
                    end_index = start_index + line[start_index:].find(' ')
                    return float(line[start_index:end_index])

def base26_encode(index, maximum):
    if index == 0:
        return 'a'
    iters = math.ceil(math.log(maximum, 26))
    bases = [
        string.ascii_lowercase[(index % (26**(e + 1))) // (26**e)]
        for e in range(iters)
    ]
    bases.reverse()
    return ''.join(bases)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--path',
                        type=str,
                        help='Path to store the exp',
                        required=True)
    parser.add_argument('--msa', nargs='+', type=str, required=True)
    parser.add_argument('--trees', nargs='+', type=str, required=True)
    parser.add_argument('--iters', type=int, required=True)
    parser.add_argument('--procs', type=int, default=None)
    parser.add_argument('--run-iq-tree', dest='runiq', action='store_true')
    parser.add_argument('--no-run-iq-tree', dest='runiq', action='store_false')
    parser.add_argument('--run-raxml-ng', dest='runraxmlng', action='store_true')
    parser.add_argument('--no-run-raxml-ng', dest='runraxmlng', action='store_false')
    parser.add_argument('--summary',required=True, type=str)
    parser.set_defaults(runiq=True)
    parser.set_defaults(runraxmlng=True)
    args = parser.parse_args()

    trees = []
    for tree in args.trees:
        try:
            trees.append(int(tree))
        except ValueError:
            with open(tree) as tree_file:
                trees.extend([ete3.Tree(s) for s in tree_file])

    aligns = []
    for align in args.msa:
        try:
            aligns.append(int(align))
            """
            if not shutil.which("indelible"):
                print("Please add indelible to your path")
                sys.exit()
            """
        except ValueError:
            aligns.append(
                list(SeqIO.parse(align,
                                 os.path.splitext(align)[1].strip('.'))))

    exp_path = os.path.abspath(args.path)
    TOTAL_ITERS = args.iters * len(aligns) * len(trees)

    PROGRESS_BAR = progressbar.ProgressBar(max_value=TOTAL_ITERS)

    if not os.path.exists(exp_path):
        os.mkdir(exp_path)

    trees_corrected_paths = []
    for t in args.trees:
        try:
            trees_corrected_paths.append(os.path.join(os.getcwd(), t))
        except:
            trees_corrected_paths.append(t)


    summary_file = os.path.abspath(args.summary)

    with directory_guard(exp_path):
        exp = experiment('.', args.iters, trees_corrected_paths, args.msa,
                summary_file)
        if args.runiq:
            exp.register_program(iqtree())
        if args.runraxmlng:
            exp.register_program(raxml_ng())
        exp.run(args.procs)
        PROGRESS_BAR.finish()
        print(exp.summarize_rf())
    with open("simulation_results.log", "w") as outfile:
        outfile.write(str(exp.summarize_rf()))
