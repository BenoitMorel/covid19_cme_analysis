#!/usr/bin/perl -w

use strict;

my $usage = "\nIt maps sequences to continents\n\n./map_sequences_continents.pl -in <FILE with sequences>  -map <FILE>\n\n";

if($#ARGV < 0){
    die $usage, "\n";
}

my $infile = "";
my $mapfile = "";

while(my $args = shift @ARGV){
    if($args =~ /^\-in$/i){ $infile = shift @ARGV; next;}
    if($args =~ /^-map/i){ $mapfile = shift @ARGV; next;}
    die "Argument $args is not valid\n$usage\n";
}




open(IN, $infile) or die "Couldn't open $infile for input\n";

my $country = "";
my %countries = ();
while( defined(my $ln = <IN>)){
    if($ln =~ /^\s*$/){ next; }
    chomp($ln);
    if($ln =~ /^\s*>([^_]+)_([^_]+)_([^_]+)/){
	$country = $2;
	$countries{$country} = 1;
    }
}

foreach my $k (keys %countries){
    print $k, "\n";
}
my $hashsize = keys %countries;
print $hashsize, "\n";


