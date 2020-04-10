#!/usr/bin/perl -w

use strict;

my $usage = "keep only sequences with length greater than a threshold. Default value is 29000.\n ./getFullSeq.pl -in <FILE> -length <INT>\n";

if($#ARGV < 0){
    die $usage;
}

my $infile = "";
my $minlength = 29000;

while(my $args = shift @ARGV){
    if($args =~ /^-in$/i){
	$infile = shift @ARGV;
	next;
    }
    if($args =~ /^-length$/i){
	$minlength = shift @ARGV;
	next;
    }
    die "Argument $args is invalid.\n$usage\n";
}

##print $infile, "\t", $minlength, "\n";


open(IN, $infile) or die "Couldn't open $infile for reading\n";


my $index = 1;
while(defined(my $ln = <IN>)){
    if($ln =~ /^\s*$/){ next; }
    chomp($ln);

    $ln =~ s/\r//g;
    
    my $newName = ">XXX";
    if($ln =~ /^\s*>([^\/]+)\/([^\/]+)\/.+\|(EPI_ISL_\d+)\|([^\/\|]+)$/){
	my $id = $1;
	my $loc = $2;
	my $uniqID = $3;
	my $dat = $4;
    
	$id =~ s/ //g;
	$loc =~ s/ //g;
	$dat =~ s/ //g;
	$dat =~ s/-//g;
	$newName = ">$id"."_".$loc."_".$dat."_".$uniqID;
	$index++;
	##print $newName, "\n";
	
	my $seqLine = "";
	if(defined(my $ln = <IN>)){
	    $ln =~ s/\r//g;
	    chomp($ln);
	    if($ln =~ /^\s*$/){ die "Error 1 read sequence\n"; }
	    $seqLine = $ln;
	}
	else{
	    die "Error cannot read next sequence\n";
	}
	
	if( length($seqLine) > $minlength ){
	    print uc($newName), "\n", uc($seqLine), "\n";
	}
    }

    
    
    
}
