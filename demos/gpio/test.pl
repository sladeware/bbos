#!/usr/bin/perl

use strict;

my $dev = '/dev/ttyUSB0'; # device to be listen

if (open IN, '<', $dev) {
	while (<IN>) {
		print;
	}
} else {
	die "Cannot open serial connection on device $dev\n"
}

close IN;


