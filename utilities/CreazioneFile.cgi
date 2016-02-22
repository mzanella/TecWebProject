#!/usr/bin/perl
print "Content-Type: text/html\n\n";
use CGI::Carp qw(fatalsToBrowser);
use Fcntl qw(O_CREAT);
require "./InserisciNelDatabase.cgi";

&creaDB;
sub creaDB {
	my $db_path=&percorsoDB;#"../database/database.xml";	
	my $db_init="<database><utenti></utenti><films></films><filmsProssimamente></filmsProssimamente><notizie></notizie><attori></attori></database>";
	sysopen(my $file, $db_path, O_CREAT) || die("file non creato");
    $mode = "6666";   chmod oct($mode), "$db_path";
    open (my $file, ">", $db_path) || die("file non aperto");
    print {$file} $db_init;
    close $file;
}
