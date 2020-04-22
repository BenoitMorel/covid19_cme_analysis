#!/usr/bin/perl -w 

use strict;

my $usage = "\n\nsplits all sequences in unique parts of n nucleotides\n./split_dataset.pl -in <FILE> -n <INT>\n\n";


if($#ARGV < 0){
    die "NO ARGS\n$usage\n";
}


my $infile = "";
my $n = 50;

while(my $args = shift @ARGV){
    if($args =~ /^-in$/){ $infile = shift @ARGV; next; }
    if($args =~ /^-n$/){ $n = shift @ARGV; next; }
}

open(IN, $infile) or die "Couldnt' open $infile for reading\n";

my $name = "";
my $start = 0;
my $end = 0;
my $substring = "";
my %allsubstrs = ();
my %allsubstrsCounter = ();
my $counter = 0;
while( defined(my $ln = <IN>) ){
    if($ln =~ /^\s*$/){ next; }
    chomp($ln);
    
    if($ln =~ /\s*>(.*)/){
	$name = $1; 
 

	if(defined(my $ln = <IN>) ){
	    chomp($ln);
	    if($ln =~ /^\s*$/){ die "Error in sequence reading\n"; }
	    my $seqLen = length($ln);
	    $start = 0;
	    $end = $start + $n - 1 ;
	    while($end < $seqLen){
		$substring = substr $ln, $start, $n;
		$start = $start + 1;
		$end = $start + $n - 1;
		if(!defined($allsubstrs{$substring})){
		    $allsubstrs{$substring} = $name."_".$start."_".$end;
		    $counter = $counter + 1;
		    $allsubstrsCounter{$substring} = 1;
		    if($counter % 10000 == 0){
			print $counter, "\n";
		    }
		}else{
		    $allsubstrsCounter{$substring}+=1;
		}
	    }
	
	}else{
	    die "Error in sequences reading\n";
	}
    }
}

close IN;

open(SPLOUT1, ">$infile.split.statistics") or die "Couldn't open file for output\n";

foreach my $k (keys %allsubstrsCounter){
    if($k !~ /N/){
	print SPLOUT1 $allsubstrs{$k}, "\t", $k, "\t", $allsubstrsCounter{$k}, "\n";
    }
}
close(SPLOUT1);

open(SPLOUT2, ">$infile.split.fasta") or die "Couldn't open file for output\n";
foreach my $k (keys %allsubstrs){
    if($k !~ /N/){
	print SPLOUT2 ">$allsubstrs{$k}\n";
	print SPLOUT2 $k, "\n";
    }
}
close(SPLOUT2);

open(IN, $infile) or die "Couldnt' open $infile for reading\n";
 
open(SPLOUT3, ">$infile.split.along") or die "Couldn't open file for output\n";

while( defined(my $ln = <IN>) ){
    if($ln =~ /^\s*$/){ next; }
    chomp($ln);
    
    if($ln =~ /\s*>(.*)/){
	$name = $1; 
    
	if(defined(my $ln = <IN>) ){
	    chomp($ln);
	    if($ln =~ /^\s*$/){ die "Error in sequence reading\n"; }
	    my $seqLen = length($ln);
	    $start = 0;
	    $end = $start + $n - 1 ;
	    while($end < $seqLen){
		$substring = substr $ln, $start, $n;
		$start = $start + 1;
		$end = $start + $n - 1;
		print SPLOUT3 $allsubstrsCounter{$substring}, " ";
	    }
	}
    }
    print SPLOUT3 "\n";
}



close IN;
close SPLOUT3;
