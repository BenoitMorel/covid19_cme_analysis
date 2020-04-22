#!/usr/bin/perl -w 
use strict;

my $usage = "\nIt parses the results of blast to detect signs of recombination\n\n./parse_results_blast.pl -in <FILE>\n\n";


my $infile = "";
my $myend = 50;
while(my $args = shift @ARGV)
{
    if( $args =~ /^-in$/){ $infile = shift @ARGV; next; }
    if( $args =~ /^-ws/i){ $myend = shift @ARGV; next; }
    die "Argument $args is invalid.$usage\n";
}

if($infile eq ""){ die $usage; }

open(IN, $infile) or die "Couldn't open $infile for input\n";

my $previous = "";
my @w = ();
my @v = ();
my @starts = ();
my @ends = ();
my @gstarts = ();
my @gends = ();
my @lninfo = ();
my $cline = "";
my $pline = "";
my @seq1 = ();
while( defined(my $ln = <IN>)){
    if($ln =~ /^\s*$/){ next; }
    chomp($ln);

    $cline = $ln;
    
    ## using the query name
    @v = split(/\s+/, $ln);
    
    #print $v[0], " $previous\n";
    
    if( $v[0] ne $previous ){
	$previous = $v[0];
    }
    elsif( $v[0] eq $previous) 
    {
	#print "HERE";
	push @starts, $v[6];
	push @ends, $v[7];
	push @gstarts, $v[8];
	push @gends, $v[9];
	push @lninfo, $ln;
	push @seq1, $v[1];
	next;
    }

    if(@starts < 1){
	push @starts, $v[6];
	push @ends, $v[7];
	push @gstarts, $v[8];
	push @gends, $v[9];
	push @lninfo, $ln;
	push @seq1, $v[1];
	next;
    }
    elsif(@starts < 2){ 
		
	@starts = ();
	@ends = ();
	@gstarts = ();
	@gends = ();
	@lninfo = ();
	@seq1 = ();
	
	push @starts, $v[6];
	push @ends, $v[7];
	push @gstarts, $v[8];
	push @gends, $v[9];
	push @seq1, $v[1];
	push @lninfo, $ln;
	
	next; 
    }
    
    my @si = sort{ $starts[$a] <=> $starts[$b] } 0..$#starts;
    
    
    for(my $ii = 0; $ii < $#si; $ii++){
	my $i = $si[$ii];
	my $ni = $si[$ii+1];
	my $absdif = abs($starts[$ni] - $ends[$i] );
	#my $absdif = $starts[$ni] - $ends[$i];
	if(  $absdif >= 0 && $absdif < 40 && $starts[$i] < 10 && $ends[$ni] > $myend - 10  && 
	     $gstarts[$i] > 1000 && $gstarts[$i] < 28500 && 
	     $gstarts[$ni] > 1000 && $gstarts[$ni] < 28500 &&
	     $ends[$i] < $myend - 10 &&
	     $seq1[$i] ne $seq1[$ni] &&
	     $starts[$i] < $ends[$i] &&
	     $starts[$ni] < $ends[$ni] &&
	     $gstarts[$i] < $gends[$i] &&
	     $gstarts[$ni] < $gends[$ni]
	    ){
	    print $lninfo[$i], "\t", $lninfo[$ni], "\n";
	    #print STDERR "---\n", $seq1[$i], "\n", $seq1[$ni], "--------\n\n";
	}
    }

    	
    @starts = ();
    @ends = ();
    @gstarts = ();
    @gends = ();
    @seq1 = ();
    @lninfo = ();
    
    push @seq1, $v[1];
    push @starts, $v[6];
    push @ends, $v[7];
    push @gstarts, $v[8];
    push @gends, $v[10];
    push @lninfo, $ln;
    
    
    $pline = $cline;


}
	
    
