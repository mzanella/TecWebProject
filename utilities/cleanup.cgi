#!/usr/bin/perl -w
use CGI;
use CGI::Session();
use CGI::Carp qw(fatalsToBrowser);
my $session = CGI::Session->load() or die $!;
my $SID = $session->id();
$session->close();
$session->delete();
$session->flush();
print  $session->header(-location=>"./");

