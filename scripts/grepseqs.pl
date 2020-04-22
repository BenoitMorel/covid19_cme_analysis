#!/usr/bin/perl -w

use strict;

my $usage = "parses only the names that we are interested in, or the opposite\n./grepseqs.pl -in <file> -p <pattern>\n\n";

if($#ARGV < 0){ die $usage; }

my $infile = "";
my $pattern = "";
my $compl = 0;
while(my $args = shift @ARGV ){
    if($args =~ /^-in$/i){ $infile = shift @ARGV; next; }
    if($args =~ /^-p$/i){ $pattern = shift @ARGV; next; }
    if($args =~ /^-v/i){ $compl = 1; next; }
    die "Argument $args is not valid.\n$usage";
}

if($infile eq "" || $pattern eq ""){
    die $usage;
}

open(IN, $infile) or die "couldn't open $infile for input\n";

my $flag = 0;
while(defined(my $ln = <IN>)){
    if($ln =~ /^\s*$/){ next; }
    chomp($ln);

    
    if($flag == 1){
	print $ln, "\n";
	$flag = 0;
	next; 
    }
    
    if($compl == 0 && $ln =~ /^\s*>/ && $ln =~ /$pattern/i){
	print $ln, "\n";
	$flag = 1;
	next; 
    }
    if($compl == 0 && $ln =~ /^\s*>/ && $ln !~ /$pattern/i){
	print $ln, "\n";
	$flag = 1;
	next; 
    }
}



