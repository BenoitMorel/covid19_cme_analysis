#!/usr/bin/perl -w
use strict;

my $usage = "It trims the ends of the alignment\n\n./trimalignment.pl -in <FILE> -l <INT>\n\n";

if($#ARGV < 0){ die $usage; }

my $infile = "";
my $trimlength = 0;
while(my $args = shift @ARGV ){
    if($args =~ /^-in$/i){ $infile = shift @ARGV; next; }
    if($args =~ /^-l$/i){ $trimlength = shift @ARGV; next; }
    die "Argument $args is invalid.$usage\n";
}


open(IN, $infile) or die "Coudln;t open $infile for reading\n";
my $name = "";
while(defined(my $ln=<IN>)){
    if($ln =~ /^\s*$/){ next; }
    chomp($ln);

    if($ln =~ /^\s*\>/){
	$name = $ln;
	print $ln, "\n";
	next;
    }

    my $seqLength = length($ln);
    my $subseq = substr($ln, $trimlength, -$trimlength);

    print $subseq, "\n";

    print STDERR "Seq: $name.. old length $seqLength... new length is ", length($subseq), "\n";

    
}
