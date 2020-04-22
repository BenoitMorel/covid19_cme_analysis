#!/usr/bin/perl -w

use strict;

my $usage = "\n\nIt removes mutations of class k (e.g. 1 for singletons)\n\n./removekclass.pl -in <ALIGNMENT FILE> -k <CLASS TO REMOVE>\n";

if($#ARGV < 0){ die $usage;}

my $infile = "";
my $k = -1;

while(my $args = shift @ARGV){
    if($args =~ /^-in$/i){ $infile = shift @ARGV; next; }
    if($args =~ /^-k$/i){ $k = shift @ARGV; next; }
    die "Argument $args is invalid\n"; 
}


open(IN, $infile) or die "Couldn't open $infile for reading\n";

my @classv = ();
my @names = ();
my @seqs = ();
my $seq = "";
while(defined(my $ln = <IN>)){
    if($ln =~ /^\s*$/){ next; }
    chomp($ln);

    if($ln =~ /^\s*>/){ 
	push @names, $ln;
	if( @names > 1){
	    push @seqs, $seq;
	}
	$seq = "";
	next; 
    }
    $seq .= $ln;
}

print STDERR scalar @seqs, "\t", scalar @names, "\n";
if(@seqs == @names - 1){
    push @seqs, $seq;
}
else{ die "Something is wrong with reading the last sequence\n"; }


my @dataset = ();
my $l = 0;
for(my $i = 0; $i < @seqs; ++$i){
    my @s = split(//, $seqs[$i]);
    if($l != 0 && scalar(@s) != $l){
	die "Something is wrong with the length of the sequences, $l\n";
    }
    $l = scalar(@s);
    push @dataset, [@s];
}

my %states = ();


for(my $i = 0; $i < $l; ++$i){
    my $minState = 99999999;
    $classv[$i] = 0;
    %states = ();
    for(my $j = 0; $j < @dataset; ++$j){
	if( defined( $states{ $dataset[$j][$i] } ) ){ $states{ $dataset[$j][$i] }++; }
	else{ $states{ $dataset[$j][$i] } = 1; }
    }
    
    foreach my $key (keys %states){
	#print STDERR $key, "\t", $states{$key}, "\n";
	if($states{$key} < $minState){ 
	    $minState = $states{$key}; 
	}
    }
    
    $classv[$i] = $minState;
}

my $cnt = 0;
for(my $i = 0; $i < @names; ++$i){
    print $names[$i], "\n";
    $cnt = 0;
    for(my $j = 0; $j < $l; ++$j){
	if($classv[$j] != $k){
	    $cnt++;
	    print $dataset[$i][$j];
	}
    }
    #print STDERR "Old length was ", $l, " now it is $cnt\n";
    print "\n";
}
