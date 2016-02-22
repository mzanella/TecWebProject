#!/usr/bin/perl -w
use CGI;
use CGI::Session();
use CGI::Carp qw(fatalsToBrowser);
use strict;
use warnings;
use utf8;
binmode STDIN, ":encoding(utf8)";
binmode STDOUT, ":encoding(utf8)";
use Encode;

my $session = CGI::Session->load() or die $!;
my $SID = $session->id();
$session->close();
$session->delete();
$session->flush();

$session = CGI::Session->new();
$session->flush();
my $cookie1 = CGI::Cookie->new(-name=>'CGISESSID',-value=>$session->id);
$session->header();
print $session->header(-location=>"./index.cgi");