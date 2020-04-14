#!/usr/bin/perl -w

use strict;

my $usage = "\nIt uses a mapping file to modify the leaf names of the output phylogenetic tree. ./change_name_tree.pl -in <PHYLO TREE> -map <MAP FILE>\n\n";

if($@ARGV < 0){
    die "$usage";
}


my $infile = "";
my $mapfile = "":
while( my $args = shift @ARGV){
    if($args =~ /^-in$/i){ $infile = shift @ARGV; next; }
    if($args =~ /^-map$/i){ $mapfile = shift @ARGV; next; }
    die "Argument $args is not valid. $usage\n"; 
}

open(
