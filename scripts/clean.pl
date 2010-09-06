#!/usr/bin/perl
#
# Copyright (c) 2010 Slade Maurer, Alexander Sviridenko
#

use v5.8.1;

BEGIN
{
  require FindBin and import FindBin;
  require File::Spec;

  $ENV{BBOSHOME} = File::Spec->join($FindBin::Bin, '..')
    unless -d $ENV{BBOSHOME};
  -d $ENV{BBOSHOME} or die "\$BBOSHOME not correct.\n";
}

our $VERSION = '0.0.1';

use strict;
use warnings;

my @ext = qw(
	      .bak  .hdl  .bdl  .brk  .bdl
	      .hx1  .md1  .map  .org  .rom
	      .dbg  .upl  .hex
	      ~
	   );

# Counters
my ($count_files, $count_bytes) = (0, 0);

my %ext;
foreach(@ext) {
  $ext{$_}++;
}

{
  my @path = ($ENV{BBOSHOME});
    while (my $path = shift @path) {
      next if !-e $path;
      if (-e $path && -f $path) {
	foreach my $ext (@ext) {
	  if ($path =~ /$ext$/i) {
	    print "$path\n";

	    $count_bytes += ((stat($path))[7]);
	    unlink $path or warn "Could not unlink $path: $!";
	    $count_files += 1;
	  }
	}
      } elsif (-e $path && -d $path) {
	my $dir = File::Spec->canonpath($path);
	next unless opendir(DIR, $dir);
	my @items = grep { $_ ne '.' && $_ ne '..' } readdir DIR;

	foreach (@items) {
	  my $item = File::Spec->canonpath(File::Spec->join($dir, $_));
	  push @path, $item;
	}
	
	closedir (DIR);
      }
    }
}

print "-" x 80, "\n";
printf("%d file(s) (%d byte(s))\n", $count_files, $count_bytes);

exit(0);

__END__


