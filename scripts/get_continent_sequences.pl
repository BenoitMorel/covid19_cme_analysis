#!/usr/bin/perl -w

use strict;

my $infile = "";
my $listfile = "";

my $usage = "\nPrint out sequences only from a specific continent\n\n./get_continent_sequences.pl -in <FASTA FILE> -list <LIST WITH COUNTRIES,CONT>\n\n";

if($#ARGV < 0){ die $usage; }

while(my $args = shift @ARGV){
    if($args =~ /^-in$/){ $infile = shift @ARGV; next; }
    if($args =~ /^-list$/){ $listfile = shift @ARGV; next; }
}

open(LIST, $listfile) or die "Couldn't open $listfile for input\n";

my %map = ();
while(defined(my $ln = <LIST>)){
    my @v = split(/,/, $ln);
    $map{$v[0]} = $v[1];
    print STDERR $v[0], "\n";
}

open(IN, $infile) or die "Couldn't open $infile fore reading\n";

my $flag = 0;
while( defined (my $ln = <IN>)){
    if($ln =~ /^\s*$/){ next; }
    chomp($ln);

    if($flag == 1){
	print $ln, "\n";
	$flag = 0;
	next;
    }

    if( $ln =~ /\s*>[^_]+_([^_]+)/ ){
	my $country = $1;
	my $name = $ln;
	$name =~ s/>//;
	if( defined($map{$name}) || defined( $map{$country} ) ){
	    print $ln, "\n";
	    $flag = 1;
	}

    }
}
    
