#!/usr/bin/env python3

import os
import sys

sys.path.insert(0, 'scripts')
import common
import root_digger_launcher
import ete3
import numpy
import csv


def compute_entropy(tree):
    acc = 0.0
    for node in tree.traverse("postorder"):
        lwr = 0.0
        # some nodes do not have LWR set and ete3
        # does not allow to check that a feature is set
        try:
            lwr = float(node.LWR)
        except:
            continue
        if (lwr == 0.0):
            continue
        acc -= lwr * numpy.log2(lwr)
    return acc


paths = common.Paths(sys.argv)

alignment = paths.alignment
csv_outfile = paths.root_digger_output_csv
runs_dir = paths.root_digger_runs_dir
credible_trees_file = paths.raxml_credible_ml_trees
all_trees_file = paths.raxml_all_ml_trees_ll
cores = str(common.available_cores)
model = common.subst_model

# read the file with the tree lhs
with open(all_trees_file) as infile:
    lh_map = {}
    for line in infile:
        lh, tree = line.split(' ')
        lh_map[tree] = lh

#use those lhs to find the best credible trees
with open(credible_trees_file) as infile:
    trees = [(lh_map[tree], tree) for tree in infile if tree in lh_map]

sorted_trees = sorted(trees, key=lambda tree: tree[0])
sample_trees_len = (len(sorted_trees) // 10) + 1

#run analysis

os.makedirs(runs_dir, exist_ok=True)

index = 0
print("running", sample_trees_len, "iterations")
for lh, tree in sorted_trees[:sample_trees_len]:
    file_prefix = os.path.join(runs_dir, '{}'.format(index))
    logfile = file_prefix + '.log'
    tmp_tree_file = os.path.join(runs_dir, "{}.in.tree".format(index))
    with open(tmp_tree_file, 'w') as tree_file:
        tree_file.write(tree)
    root_digger_launcher.launch_root_digger(tmp_tree_file, alignment, model,
                                            file_prefix, logfile, cores)
    index += 1

results = []

#compute entropy of each tree, export to a csv

for root, dirs, files in os.walk(runs_dir):
    for f in files:
        if (not f.endswith(".lwr.tree") or "in" in f):
            continue
        with open(os.path.join(root, f)) as infile:
            tree = ete3.Tree(infile.read())
        index = int(os.path.splitext(os.path.basename(f))[0])
        results.append({
            'lh': sorted_trees[index][0],
            'index': index,
            'entropy': compute_entropy(tree)
        })

with open(csv_outfile, "w") as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=results[0].keys())
    writer.writeheader()
    for r in results:
        writer.writerow(r)
