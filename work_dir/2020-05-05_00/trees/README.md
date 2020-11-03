The following trees are copied from the other result directories:

 - fmsan.MRE_consensus_tree.newick
 - fmsao.MRE_consensus_tree.newick
 - smsan.MRE_consensus_tree.newick
 - smsan.rootdigger.1.newick
 - smsan.rootdigger.2.newick
 - smsao.MRE_consensus_tree.newick

In addition, we created these trees:

 - smsan.rootdigger.2.contracted-dendroscope.newick
 - smsan.rootdigger.2.nonzero-all.newick
 - smsan.rootdigger.2.nonzero-no-leaves.newick

These are versions of smsan.rootdigger.2.newick where branches of length zero were collapsed into multifurcations.
This is because those branches were resolved randomly in the first place, so these branches are non meaninful splits.
In the visualizations as cladograms (which ignore branch lengths), these however show up as artificial splits,
which we hence removed here again, for visualization purposes only. The first one uses dendroscope 
("Select Short branches" followed by "Collapse Branches"); the second is a custom genesis app that collapses all
zero lenghts branches, even if those lead to a leaf (which messes up the visualiztion, but we keep it here for
reference), and the third one is the same genesis app, but does not collapse branches that lead to leaf nodes.
