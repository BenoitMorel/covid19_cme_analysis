#!/usr/bin/perl  -w
use strict;

my $usage = "\n\nIt filters sequences based on N's. Also it can print sequences only within a range\n\n./filterSequences.pl -in <FILE> -start <int> -end <int> -pstart <int> -pend <int>\n\n";

if($#ARGV < 0){
    die $usage, "\n";
}

my $infile = "";
my $start = 0;
my $end = 0;
my $pstart = 0; 
my $pend = 0;
my $excludeList = "";

my $lessthanN = 10;

while(my $args = shift @ARGV){
    if($args =~ /^-in$/i){ $infile = shift @ARGV; next; }
    if($args =~ /^-start$/i){ $start = shift @ARGV; next; }
    if($args =~ /^-end$/i){ $end = shift @ARGV; next; }
    if($args =~ /^-pstart/i){ $pstart = shift @ARGV; next; }
    if($args =~ /^-pend/i){ $pend = shift @ARGV; next; }
    if($args =~ /^-exclude/i){ $excludeList = shift @ARGV; next; }
    die "Argument $args is invalid\n$usage\n\n"; 
}

open(IN, $infile) or die "Couldn't open $infile for reading\n";

my @names = ();
my @percentages = ();
my @good = ();
my @sequences = ();
my @starts = ();
my @ends = ();


while(defined(my $ln = <IN>)){
    if($ln =~ /^\s*$/){ next; }
    chomp($ln);
    
    if($ln =~ /^>/){
	push @names, $ln; 
	if(defined(my $ln = <IN>)){
	    if($ln =~ /^\s*$/){ next; }
	    chomp($ln);
	    push @sequences, $ln;
	    # if( $start == 0 && $end == 0){
	    # 	$start = 0;
	    # 	$end = length($ln);
	    # }
	    # if( $pstart == 0 && $pend == 0){
	    # 	$pstart = 0;
	    # 	$pend = length($ln);
	    push @starts, $pstart;
	    push @ends, $pend;
	    
	    my $subln = substr($ln, $start, length($ln) - $start - $end);
	    $subln =~ s/^N+//i;
	    $subln =~ s/N+$//i;
	    my $ns = () = $subln =~ /n/ig;
	    	    
	    push @percentages, $ns; 
	    
	}
	else{ die "couldn't read line correctly\n"; }
    }
}

my $cnt = 0;
for(my $i = 0; $i < @sequences; ++$i){
    if( $percentages[$i] < $lessthanN  && ($excludeList eq "" || $names[$i] !~ /$excludeList/i)  ){
	print "$names[$i]\n$sequences[$i]\n";
	print STDERR $names[$i], "\t", $percentages[$i], " ***\n";
	$cnt++;
    }
    else{
	print STDERR $names[$i], "\t", $percentages[$i], "\n";
    }
}

print STDERR "Totally $cnt sequences pass the filter of less than $lessthanN Ns\n"

