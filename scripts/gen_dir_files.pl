#!perl
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

our $VERSION = '0.0.2';

use Template;
use Getopt::Long;
use Win32::TieRegistry;
use Data::Dumper;

$Data::Dumper::Terse  = 1;
$Data::Dumper::Indent = 1;
$Data::Dumper::Useqq  = 1;

use strict;
use warnings;

our $DIR_EXT = "\.DIR";
our $TPL_DIR_EXT = "${DIR_EXT}\.TPL";

our $TPL_CFG = {
		ABSOLUTE => 1, # allow absoulte pathes
		POST_CHOMP => 1, # cleanup whitespace
	       };

our $TPL = Template->new($TPL_CFG);

# Possible template variables for *.DIR files
our %TPL_VARS = (
		 DC_LOCATION => undef,
		 DC_VERSION => 0,
		 BBOS_LOCATION => $ENV{BBOSHOME},
		);

# Getting user options
GetOptions(
	   'DC_VERSION=f' => \$TPL_VARS{DC_VERSION},
	   'DC_LOCATION=s' => \$TPL_VARS{DC_LOCATION},
	   'HELP' => \&print_usage,
);

# If variable 'DC_LOCATION' is not defined by user manually it should be
# defined automatically
if (!defined $TPL_VARS{'DC_LOCATION'}) {
  # Reference on the DC key in the Windows register
  my $DC;

  # Try to get DC from the ZWorld Software
  if (!defined ($DC = $Registry->{'HKEY_CURRENT_USER'}->{'Software'}->{'ZWorld'}->{'DCW'}->{'Rabbit'})) {
    die "DC can not we detected automatically. Please, set the DC location manually.\n";
  }

  # If DC version was not set manually
  unless ($TPL_VARS{'DC_VERSION'}) {
    # The highest version will be taken
    foreach($DC->SubKeyNames) {
      $TPL_VARS{'DC_VERSION'}=eval($_) if (/^[\d\.]+$/ && eval"$_">$TPL_VARS{'DC_VERSION'});
    }
  } else {
    my %keys = map {$_ => 1} $DC->SubKeyNames;
    die "$TPL_VARS{'DC_VERSION'} does not supported.\n"
      unless defined $keys{ $TPL_VARS{'DC_VERSION'} };
  }

  print "Used DC version: $TPL_VARS{'DC_VERSION'}\n";

  if (defined (my $_ENV = $DC->{$TPL_VARS{'DC_VERSION'}}->{'Environment'})) {
    $TPL_VARS{'DC_LOCATION'} = $_ENV->{'START LOCATION'}; # "RT DIRECTION" ?
  } else {
    die "DC $TPL_VARS{'DC_VERSION'} environment can not be found.\n";
  }
}

# Check up DC location, may be it was deleted or something else
unless (-e $TPL_VARS{'DC_LOCATION'} && -d $TPL_VARS{'DC_LOCATION'}) {
  die "$TPL_VARS{'DC_LOCATION'} does not exist.\n";
}


print "Possible DIR template Variables\n";
print Dumper \%TPL_VARS;

print "Building *.DIR files\n";
{
  my @path = ($ENV{BBOSHOME});
  while (my $path = shift @path) {
    next if !-e $path;
    if (-e $path && -f $path) {
      if ($path =~ /^(.*?)$TPL_DIR_EXT$/i) {
	local *FH;
	my $dir_file = join('', $1, $DIR_EXT);
	open(FH, '>', $dir_file) || die "$dir_file cannot be created: $!\n";
	my $output = '';
	$TPL->process($path, \%TPL_VARS, $dir_file) || die $TPL->error(), "\n";
	clean_dir_file($dir_file); # remove comments and empty lines
	print " $dir_file\n";
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


exit(0);

sub print_usage {
  print <<'USAGE';
BBOS Configuration v$VERSION

  --DC_VERSION=v      Dynamic C version
  --DC_LOCATION=path  Path to Dynamic C
  --HELP              Prints this help

USAGE
    exit(0);
}

# remove comments and blocks of empty lines
sub clean_dir_file {
  my $file = shift;
  my @buf;

  open(FH, "$file") || return;
  @buf = <FH>;
  close(FH);

  open(FH, ">$file") || return;
  for (my $i=0; $i<$#buf; $i++) {
    if ($buf[$i]!~/^\s*\#(.*?)$/
	&& !(is_empty_line($buf[$i]) && is_empty_line($buf[$i+1])))
      {
	print FH $buf[$i];
      }
  }

  close(FH);
}

sub is_empty_line {
  return (shift=~/^\s+$/) ? 1 : 0;
}
