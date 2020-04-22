#!/usr/bin/perl -w

use strict;

my $usage = "\n\nchanges the names in order to have a database with the names that I want\n./preprocess_names.pl -in <FASTA from NCBI>\n\n";

my $infile = "";

while(my $args = shift @ARGV){
    if($args =~ /^-in$/i){ $infile = shift @ARGV; next;}
    die "ARgument $args is invalid. $usage\n";
}

open(IN, $infile) or die "Couldn't open $infile for reading\n";

while( defined(my $ln = <IN>)){
    if($ln =~ /^\s*$/){ next; }
    chomp($ln);

    if($ln =~ /\s*>([^\|\s]+)\s*\|([^\|]+)/){
	my $id=$1;
	my $des = $2;
	$des=~s/ /_/g;
	print ">$id"."_".$des."\n";
    }
    else{
	print $ln, "\n";
    }
}
