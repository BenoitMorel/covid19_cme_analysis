#!/usr/bin/perl -w
use strict;
my $usage = "\n\nIt estimates the diversity and divergence from fasta sequences\n\n./divergence_diversity.pl -in <FASTA>\n\n";

if($#ARGV < 0){ die $usage; }

my $infile = "";
my $outgroup = "";
my $k = -1;
my $windowsize = 100;
while(my $args = shift @ARGV){
    if($args =~ /^-in$/i){ $infile = shift @ARGV; next; }
    if($args =~ /^-outgroup$/i){ $outgroup = shift @ARGV; next; }
    if($args =~ /^-k$/i){ $k = shift @ARGV; next; }
    if($args =~ /^-window$/i){ $windowsize = shift @ARGV; next; }
    die "Argument $args is invalid. $usage\n";
}

open(IN, $infile) or die "Couldn't open input file:\"$infile\" for reading\n";


my @outgroupSequence = ();
my @ingroupSequences = ();
while( defined(my $ln = <IN>) ){
    if($ln =~ /^\s*$/){ next; }
    chomp($ln);
    
    if($ln =~ /\s*>$outgroup/){
	my $outgroupseq = "";
	if(defined($ln = <IN>)){
	    chomp($ln);
	    if($ln =~ /^\s*$/){ die "Error in sequence reading\n"; }
	    $outgroupseq = $ln;
	}
	
	if( $outgroupseq ne "" ){
	    @outgroupSequence = split(//, $outgroupseq);
	}else{
	    die "Error reading sequence file\n";
	}
    }
    elsif($ln =~ /\s*>/){
	my $ingroupseq = "";
	if(defined($ln = <IN>)){
	    chomp($ln);
	    if($ln =~ /^\s*$/){ die "Error in sequence reading\n"; }
	    $ingroupseq = $ln;
	}
	
	if( $ingroupseq ne "" ){
	    my @ingroupSequence = split(//, $ingroupseq);
	    push @ingroupSequences, [@ingroupSequence];
	}else{
	    die "Error reading sequence file\n";
	}
    }
}


## divergence
my $cnt = 0;
my $diffs = 0;
my $lastDiffs = 0;
my @positions = ();
my @divergence = ();
my @diversity = ();
my @cnts = ();
my $compIngroupSeqIndex = 0;
if( $k == -1 ){ # choose one randome from the ingroup
    $compIngroupSeqIndex = int(rand( @ingroupSequences ));
    print STDERR "Random Sequence: $compIngroupSeqIndex\n";
    for( my $i = 0; $i < @outgroupSequence; ++$i){
	if( ($outgroupSequence[$i] ne '-') && ($ingroupSequences[$compIngroupSeqIndex][$i] ne '-')){
	    $cnt++;

	    if( uc($outgroupSequence[$i]) ne uc($ingroupSequences[$compIngroupSeqIndex][$i]) ){
		$diffs++;
	    }
	}
	if($i >= $windowsize ){
	    my $validLast = ( ($outgroupSequence[$i-$windowsize] ne '-') && ($ingroupSequences[$compIngroupSeqIndex][$i-$windowsize] ne '-') ) ? 1 : 0;

	    my $backdif = uc($outgroupSequence[$i-$windowsize]) ne uc($ingroupSequences[$compIngroupSeqIndex][$i-$windowsize]) ? 1 : 0;
	    
	    if( $validLast == 0 ){ $backdif = 0; }
	    $cnt = $cnt - $validLast;
	    if($cnt == 0){ next; }	    
	    $diffs = $diffs - $backdif;
	    push @positions, $i+1;
	    push @divergence, $diffs/$cnt;
	    push @cnts, $cnt;
	}
	    
    }
}

$cnt = 0;
$diffs = 0;
my @validSites = ();
my @validDifs = ();
my @divPositions = ();
for(my $i = 0; $i < @outgroupSequence; ++$i){
    push @validDifs, 0;
    if($outgroupSequence[$i] ne '-'){
	push @validSites, 1;
    }else{
	push @validSites, 0;
    }
}

my %validStates = ("A" => 1, "C" => 1, "G" => 1, "T" => 1);


for( my $i = 0; $i < @outgroupSequence; ++$i){

    if( $outgroupSequence[$i] ne '-')
	{
	    my $prevState = uc($ingroupSequences[0][$i]);
	    my $j = 0; 
	    while(!defined($validStates{$prevState})){
		$prevState = uc($ingroupSequences[$j][$i]);
		$j++;
	    }
	    my $validSequences = 0;
	    for( my $j = 0; $j < @ingroupSequences; ++$j){
		if( uc($ingroupSequences[$j][$i]) eq 'N' ){
		    $ingroupSequences[$j][$i] = '-';
		}
		if( defined($validStates{uc($ingroupSequences[$j][$i])})  && (uc($ingroupSequences[$j][$i]) ne uc($prevState ) ) )
		{
		    $validDifs[$i] = 1;
		    $diffs++;
		    $validSequences++;
		    print $i, "\t", $prevState, "\t", $ingroupSequences[$j][$i], "\n";
		    last;
		}
		elsif( !defined($validStates{uc($ingroupSequences[$j][$i])}) ){
		    next; 
		    # $cnt--;
		    # $validSites[$i] = 0;
		    # last;
		}
		elsif( defined($validStates{uc($ingroupSequences[$j][$i])})  && (uc($ingroupSequences[$j][$i]) eq uc($prevState )) ){
		    $validSequences++;
		}
	    }
	    if($validSequences > 1){
		$cnt++;
	    }
	    else{
		$validSites[$i] = 0;
	    }
	}
	
    #print $cnt, "\t", $diffs, "\n";
	
	
	if($i >= $windowsize )
	{
	    my $validLast = $validSites[$i-$windowsize] == 1 ? 1 : 0;
	    my $backdif = $validDifs[$i-$windowsize] == 1 ? 1 : 0;
	    
	    if( $validLast == 0 ){ $backdif = 0; }
	    $cnt = $cnt - $validLast;
	    if($cnt == 0){ next; }	    
	    push @divPositions, $i+1;
	    $diffs = $diffs - $backdif;
	    push @diversity, $diffs/$cnt;
	    #print $diffs, "\t", $cnt, "\n";
	}
    
}
	
open(DIVERSITY, ">diversity.txt") or die "Cant' open diversity.txt for writing\n";
open(DIVERGENCE, ">divergence.txt") or die "Cant' open divergence.txt for writing\n";

for(my $i = 0; $i < @divergence; ++$i){
    print DIVERGENCE $positions[$i], "\t", $divergence[$i], "\n";
}

for(my $i = 0; $i < @diversity; ++$i){
    print DIVERSITY $divPositions[$i], "\t", $diversity[$i], "\n";
}
close DIVERSITY;
close DIVERGENCE;

    
