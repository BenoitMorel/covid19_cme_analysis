#!/usr/bin/perl -w

use strict;

my $usage = "\nIt creates a map between countries and continents using the table from gisaid\n\n./create_map.pl -in <SEQ FILE> -map <MAP FILE> -mode <0:same as names, 1:just a dot, 2: first letters of continent\n\n";

if($#ARGV < 0){ die $usage; }

my $infile = "";
my $seqfile = "";
my $mode = 0;
my $treefile = "";
my $greece = 0;
while(my $args = shift @ARGV){
    if($args =~ /^-map/i){ $infile = shift @ARGV; next; }
    if($args =~ /^-in/i){ $seqfile = shift @ARGV; next; }
    if($args =~ /^-mode/i){ $mode = shift @ARGV; next; }
    if($args =~ /^-tree/i){ $treefile = shift @ARGV; next; }
    if($args =~ /^-greece/i){ $greece = 1; next; }
    die "Arguemnt $args is not valid. $usage\n";
}

if($seqfile eq "" || $infile eq ""){ die $usage; }

open(IN, $infile) or die "Couldn't open $infile for reading\n";


my %map = ();
my %invmap = ();
my %initialMap = ();
my %nameMap = ();
while(defined(my $ln = <IN>)){
    if($ln =~ /^\s*$/){ next; }
    chomp($ln);

    if( $ln =~ /location/i ){ next; }
    
    my @v = split(/\t/, $ln);
    ## print $v[0], "\t", $v[2], "\n";

    my $location = $v[2];
    my @locel = split (/\//, $location);
    $locel[0] =~ s/\s+//g;
    $map{$v[0]} = $locel[0];
    $initialMap{$v[0]} = lc(substr( $locel[0], 0, 2));
    
    $invmap{$locel[0]} = $map{$v[0]};
}

my @colors = ("red", "green", "orange", "blue", "yellow", "purple", "pink", "black");
my %colormap = ();


my $i = 0;
foreach my $k (keys %invmap){
    $colormap{$k} = $colors[$i];
    $i++;
}


open(SEQ, $seqfile) or die "Couldn't open $seqfile for reading\n";

print "name\tleaf_label_color\tbranch_color\tnew_name\n";

while( defined(my $ln = <SEQ>)){
    if($ln =~ /^\s*$/){ next; }
    chomp($ln);

    if($ln =~ /\s*>.+(EPI_ISL_\d+)/){
	my $id = $1;
	my $name = $ln;
	$name =~ s/>//;

	
	
	if(!defined( $map{$id} )){
	    die "$id does not exist in map\n";
	}

	$nameMap{$name} = $initialMap{$id};

	if($ln =~ /pangolin/i || $ln =~ /bat/i){
	    print $name, "\t", "black", "\t", "black", "\t", $id, "\n";

	}

	elsif($ln !~ /Greece/i || $greece == 0){
	    if( $mode == 1){
		print $name, "\t", $colormap{ $map{$id} }, "\t", $colormap{ $map{$id} }, "\t", ".", "\n";
	    }
	    elsif( $mode == 0){
		print $name, "\t", $colormap{ $map{$id} }, "\t", $colormap{ $map{$id} }, "\t", $id, "\n";
	    }
	    elsif( $mode == 2){
		print $name, "\t", $colormap{ $map{$id} }, "\t", $colormap{ $map{$id} }, "\t", $initialMap{$id}, "\n";
		
	    }
	}
	else{
	    if( $mode == 1){
		print $name, "\t", $colormap{ $map{$id} }, "\t", $colormap{ $map{$id} }, "\t", ".", "***\n";
	    }
	    elsif( $mode == 0){
		print $name, "\t", $colormap{ $map{$id} }, "\t", $colormap{ $map{$id} }, "\t", $id, "***\n";
	    }
	    elsif( $mode == 2){
		print $name, "\t", $colormap{ $map{$id} }, "\t", $colormap{ $map{$id} }, "\t", $initialMap{$id}, "***\n";
		
	    }
	}
    }
}

close IN;
close SEQ;

if($treefile ne ""){
    open(IN, $treefile) or die "Couldn't open $treefile for input\n";
    open(OUT, ">$treefile.NAMES.newick") or die "Couldn't open outputfile\n";
    while(defined(my $ln = <IN>)){
	if($ln =~ /^\s*$/){ next; }
	chomp($ln);
	foreach my $k (keys %nameMap){
	    $ln =~ s/$k/$nameMap{$k}/;
	}
	print OUT $ln, "\n"
    }
    close IN;
    close OUT;
}

